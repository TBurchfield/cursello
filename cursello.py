#!/usr/bin/env python2.7

import curses
from curses.textpad import rectangle
import time

from modules import storage
from modules.list import List
from modules.cursello_io import BarInput
from modules.cursello_io import debug

stdscr = curses.initscr()
curses.noecho()
curses.start_color()
stdscr.refresh()

def refresh_lists(stdscr, data, ilist, itemw):
  stdscr.clear()
  at = 1
  for i, items in enumerate(data):
    width = max(map(len, items.items) + [len(items.name)]) + 1
    #rectangle(stdscr, 0, at - 1, items.size + 2, at + width)
    rectangle(stdscr, 0, at - 1, items.size + 2, at + width)

    text_type = 0
    if i == ilist: text_type = curses.A_UNDERLINE
    stdscr.addstr(1, at, items.name, text_type)

    for j, item in enumerate(items.items):
      text_type = 0
      if j == itemw and i == ilist: text_type = curses.A_BOLD
      #stdscr.addstr(j + 2, at, item, text_type)
      stdscr.addstr(j + 2, at, item, text_type)
    at += width + 2


def new_item(stdscr, data, ilist):
  item_string = BarInput(stdscr, "Enter the item description, then press enter: ")
  data[ilist].add(item_string)


def new_list(stdscr, data, ilist):
  item_string = BarInput(stdscr, "Enter the name of the new list, then press enter: ")
  data.append(List(item_string))
  ilist = len(data) - 1


def delete_item(stdscr, data, ilist, item):
  answer = BarInput(stdscr, "Are you sure you wish to delete this item? (y/n): ")
  if answer == 'y':
    data[ilist].archive(item)


def delete_list(stdscr, data, ilist):
  answer = BarInput(stdscr, "Are you sure you wish to delete this entire list? (y/n): ")
  if answer == 'y':
    del data[ilist]


def init(stdscr):
  stdscr.addstr(curses.LINES - 1, 0, "(q) to quit. (o) to add an item to a list. Vim style movement.", curses.A_BOLD)

def handle_shutdown(data):
  storage.write_store(data)

def main(stdscr):
  # Load/prepare storage.
  storage_file_present = storage.check_store()
  data = storage.load_store()
  if data is None or len(data) == 0:
    data = [List("To Do"), List("Done")]

  ilist = 0
  item = 0
  while True:
    refresh_lists(stdscr, data, ilist, item)
    stdscr.refresh()
    c = stdscr.getch()
    # Move down within list
    if c == ord('j'):
      item = min(item + 1, data[ilist].size - 1)
    # Move up within list
    elif c == ord('k'):
      item = max(item - 1, 0)
    # Move right to next list
    elif c == ord('l'):
      ilist = min(ilist + 1, len(data) - 1)
      item = min(item, data[ilist].size - 1)
    # Move left to next list
    elif c == ord('h'):
      ilist = max(ilist - 1, 0)
      item = min(item, data[ilist].size - 1)
    # Create new item in list
    elif c == ord('o'):
      new_item(stdscr, data, ilist)
    # Create new list
    elif c == ord('a'):
      new_list(stdscr, data, ilist)
    # Delete Item
    elif c == ord('d'):
      delete_item(stdscr, data, ilist, item)
    # Delete List
    elif c == ord('D'):
      delete_list(stdscr, data, ilist)
    # Quit
    elif c == ord('q'):
      break
    else:
      pass

  handle_shutdown(data)

curses.wrapper(main)
