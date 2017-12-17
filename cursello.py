#!/usr/bin/env python2.7
import curses
from curses.textpad import rectangle
import time

class List:
  def __init__(self, name):
    self.name = name
    self.size = 0
    self.items = []
    self.archived = []

  def add(self, item):
    self.items.append(item)
    self.size += 1

  def archive(self, n):
    self.archived.append(self.items[n])
    del self.items[n]
    self.size -= 1

stdscr = curses.initscr()
curses.noecho()
curses.start_color()
stdscr.refresh()

def refresh_lists(stdscr, data, ilist, itemw):
  at = 1
  for i, items in enumerate(data):
    width = max(max(map(len, items.items) + [0]), len(items.name)) + 1
    rectangle(stdscr, 0, at - 1, items.size + 2, at + width)
    if i == ilist:
      stdscr.addstr(1, at, items.name, curses.A_UNDERLINE)
      for j, item in enumerate(items.items):
        if j == itemw:
          stdscr.addstr(j + 2, at, item, curses.A_BOLD)
        else:
          stdscr.addstr(j + 2, at, item)
    else:
      y = 1
      stdscr.addstr(y, at, items.name)
      for j, item in enumerate(items.items):
        y += 1
        stdscr.addstr(y, at, item)
    at += width + 2

def new_item(stdscr, data, ilist):
  stdscr.addstr(curses.LINES - 1, 0, "Enter item description, then press enter:", curses.A_BOLD)
  i = stdscr.getch()
  stdscr.addstr(curses.LINES - 1, 0, "                                         ", curses.A_BOLD)
  st = chr(i)
  while i != 10:
    debug(stdscr, str(st), style=curses.A_UNDERLINE)
    stdscr.refresh()
    i = stdscr.getch()
    if i < 256:
      st += chr(i)
  stdscr.addstr(curses.LINES - 1, 0, "                                         ", curses.A_BOLD)
  data[ilist].add(st)
  
def init(stdscr):
  stdscr.addstr(curses.LINES - 1, 0, "(q) to quit. (o) to add an item to a list.  vim style movement.", curses.A_DIM)

def debug(stdscr, msg, style=curses.A_DIM):
  stdscr.addstr(curses.LINES - 1, 0, msg, style)

def main(stdscr):
  ilist = 0
  item = 0
  data = [List("To Do"), List("Done")]
  while True:
    refresh_lists(stdscr, data, ilist, item)
    stdscr.refresh()
    c = stdscr.getch()
    if c == ord('j'):
      item = min(item + 1, data[ilist].size - 1)
    elif c == ord('k'):
      item = max(item - 1, 0)
    elif c == ord('l'):
      ilist = min(ilist + 1, len(data) - 1)
      item = min(item, data[ilist].size - 1)
    elif c == ord('h'):
      ilist = max(ilist - 1, 0)
      item = min(item, data[ilist].size - 1)
    elif c == ord('o'):
      new_item(stdscr, data, ilist)
    elif c == ord('q'):
      break
    else:
      pass

curses.wrapper(main)
