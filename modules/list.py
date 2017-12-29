'''
list.py

List class module for cursello's item-containing data structure. Stores
sequences items, each displays in a trello-style rectangle.

12/28/17
Douglas J. Smith (@dsmith47)
'''
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

