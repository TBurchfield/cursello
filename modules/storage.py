'''
storage.py

Module that handles storing of cursello list state.

Douglas J. Smith
01/02/18
'''

import os
import yaml

STORAGE_DIR = "~/.config/cursello/"
STORAGE_FILE = "items.yaml"

'''
check_store - Verifies that storage files can be accessed/created.

OUTPUT:
Error:string|NoneType - Error message. None if no error occurs.
'''
def check_store():
  fname = os.path.expanduser(os.path.join(STORAGE_DIR, STORAGE_FILE))
  if not os.path.isfile(fname):
    if not os.path.isdir(os.path.expanduser(STORAGE_DIR)):
      os.mkdir(os.path.expanduser(STORAGE_DIR))
    open(fname, 'w').close()
    return "Created new directory"

  # Try and create directory if it doesn't exist.
  if not os.access(fname, os.F_OK ^ os.R_OK ^ os.W_OK):
    return "ERROR: {} is not a valid storage file.".format(fname)

  return None

'''
load_store - loads any sotred yaml data.

OUTPUT
items:[]List - All the todo lists stored in the YAML
'''
def load_store():
  fname = os.path.expanduser(os.path.join(STORAGE_DIR, STORAGE_FILE))
  f = open(fname, 'r')
  d = yaml.load(f)

  f.close()
  return d

'''
write_store - writes provided data to a YAML dict.

INPUT:
data:[]List - All todo lists to be stored.
'''
def write_store(data):
  fname = os.path.expanduser(os.path.join(STORAGE_DIR, STORAGE_FILE))
  f = open(fname, 'w')

  f.write(yaml.dump(data))

  f.close()
