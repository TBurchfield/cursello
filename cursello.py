#!/usr/bin/env python2.7

import curses
from curses.textpad import rectangle
import time
import sys

from modules import storage
from modules.list import List
from modules.cursello_io import BarInput
from modules.cursello_io import debug


class Cursello:

  def __init__(self):
    self.win = curses.initscr()

    yx = self.win.getmaxyx()
    self.stdscr = curses.newpad(1000, 1000)
    self.stdscr.keypad(1)

    curses.noecho()
    curses.start_color()
    curses.curs_set(0)
    self.stdscr.refresh(0,0,0,0,yx[0]-1, yx[1]-1)

    self.pad_pos_x = 0
    self.pad_pos_y = 0
    self.data = {}
    self.ilist = 0
    self.item = 0

    self.changes_made = False

    if len(sys.argv) == 2:
      # User has given board name
      board_name = sys.argv[1]
      if '.yaml' not in board_name:
        board_name += '.yaml'

      storage.STORAGE_FILE = board_name

  def refresh_lists(self):
    self.stdscr.clear()
    at = 1
    for i, items in enumerate(self.data):
      width = max(map(len, items.items) + [len(items.name)]) + 1
      #rectangle(stdscr, 0, at - 1, items.size + 2, at + width)
      rectangle(self.stdscr, 0, at - 1, items.size + 2, at + width)

      text_type = 0
      if i == self.ilist: text_type = curses.A_UNDERLINE
      self.stdscr.addstr(1, at, items.name, text_type)

      for j, itemw in enumerate(items.items):
        text_type = 0
        if j == self.item and i == self.ilist: text_type = curses.A_BOLD
        #stdscr.addstr(j + 2, at, item, text_type)
        self.stdscr.addstr(j + 2, at, itemw, text_type)
      at += width + 2


  def new_item(self):
    self.changes_made = True
    item_string = BarInput(self, "Enter the item description, then press enter: ")
    self.data[self.ilist].add(item_string)


  def new_list(self):
    self.changes_made = True
    item_string = BarInput(self, "Enter the name of the new list, then press enter: ")
    self.data.append(List(item_string))
    self.ilist = len(self.data) - 1


  def delete_item(self):
    self.changes_made = True
    if self.ilist >= len(self.data) or self.ilist < 0 or self.item >= self.data[self.ilist].size or self.item < 0:
      return
    answer = BarInput(self, "Are you sure you wish to delete this item? (y/n): ")
    if answer == 'y':
      self.data[self.ilist].archive(self.item)

    self.item = min(self.item, self.data[self.ilist].size - 1)


  def delete_list(self):
    self.changes_made = True
    if self.ilist >= len(self.data) or self.ilist < 0:
      return
    answer = BarInput(self, "Are you sure you wish to delete this entire list? (y/n): ")
    if answer == 'y':
      del self.data[self.ilist]

    self.ilist = min(self.ilist, len(self.data) - 1)
    self.item = min(self.item, self.data[self.ilist].size - 1)


  def save_board(self):
    board_name = BarInput(self, 'What name do you want to save this board as? Leave blank to save as "' + storage.STORAGE_FILE.strip('.yaml') + '": ')

    if not board_name == '':
      if '.yaml' not in board_name:
        board_name += '.yaml'

      storage.STORAGE_FILE = board_name

    storage.write_store(self.data)

    self.changes_made = False


  def switch_board(self):

    if self.changes_made:
      # User has unsaved changes, prompt to see if they wish to save
      answer = BarInput(self, 'You have unsaved changes in the current board, do you wish to save them? (y/n): ')
      if answer == 'y':
        save_board(self.stdscr, self.data)

    self.changes_made = False

    board_name = BarInput(self.stdscr, 'Which board do you wish to switch to: ')

    if '.yaml' not in board_name:
      board_name += '.yaml'

    storage.STORAGE_FILE = board_name

    storage_file_present = storage.check_store()
    self.data = storage.load_store()
    if self.data is None or len(self.data) == 0:
      self.data = [List("To Do"), List("Done")]

    return self.data


  def init(self):
    self.stdscr.addstr(curses.LINES - 1, 0, "(q) to quit. (o) to add an item to a list. Vim style movement.", curses.A_BOLD)

  def handle_shutdown(self):
    storage.write_store(self.data)

  def main(self, screen):
    # Load/prepare storage.
    storage_file_present = storage.check_store()
    self.data = storage.load_store()
    if self.data is None or len(self.data) == 0:
      self.data = [List("To Do"), List("Done")]

    yx = self.win.getmaxyx()
    self.stdscr.refresh(0,0,0,0,yx[0]-1, yx[1]-1)

    while True:
      self.refresh_lists()
      self.stdscr.refresh(self.pad_pos_y,self.pad_pos_x,0,0,yx[0]-1, yx[1]-1)
      c = self.stdscr.getch()
      l = open('log', 'w+')
      l.write(str(c))
      l.flush()
      l.close()
      # Move down within list
      if c == ord('j'):
        self.item = min(self.item + 1, self.data[self.ilist].size - 1)
      # Move up within list
      elif c == ord('k'):
        self.item = max(self.item - 1, 0)
      # Move right to next list
      elif c == ord('l'):
        self.ilist = min(self.ilist + 1, len(self.data) - 1)
        self.item = min(self.item, self.data[self.ilist].size - 1)
      # Move left to next list
      elif c == ord('h'):
        self.ilist = max(self.ilist - 1, 0)
        self.item = min(self.item, self.data[self.ilist].size - 1)
      # Create new item in list
      elif c == ord('o'):
        self.new_item()
      # Create new list
      elif c == ord('a'):
        self.new_list()
      # Delete Item
      elif c == ord('d'):
        self.delete_item()
      # Delete List
      elif c == ord('D'):
        self.delete_list()
      # Save board
      elif c == ord('w'):
        self.save_board()
      # Switch boards
      elif c == ord('m'):
        self.data = self.switch_board()
        self.ilist = 0
        self.item = 0
      # Quit
      elif c == ord('q'):
        break
      elif c == curses.KEY_RIGHT and self.pad_pos_x < yx[1] - 1:
        self.pad_pos_x += 1
      elif c == curses.KEY_LEFT and self.pad_pos_x > 0:
        self.pad_pos_x -= 1
      elif c == curses.KEY_UP and self.pad_pos_y > 0:
        self.pad_pos_y -= 1
      elif c == curses.KEY_DOWN and self.pad_pos_y < yx[0] - 1:
        self.pad_pos_y += 1
      else:
        pass

    self.handle_shutdown()

cursello = Cursello()
curses.wrapper(cursello.main)
