'''
cursello_io.py

IO/handling module for cursello. Centers around curses-style inputs.

Douglas J. Smith
12/28/17
'''
import curses

'''
debug - take a string and a screen and display the string at the base of the
  window, useful for alerts or certain I/O display.

INPUT:
stdscr:Window[curses] - screen object.
msg:String - message to be displayed.
style:Integer - curses macro code for styling input.
'''
def debug(stdscr, msg, style=curses.A_DIM):
  stdscr.addstr(curses.LINES - 1, 0, msg, style)


'''
StringInput - take a string entered by the user in a command bar, return the
properly-processed result.

INPUT:
screen:Window[curses] - window object that bar will be displayed within
prompt:String - string that is used to request input. Prompt is flashed before
  input and disappears when the user starts typing. Must be included, otherwise
  a confusingly blank box is flashed.

OUTPUT:
result:String - processed version of user's input
'''
def BarInput(screen, prompt):
  screen.addstr(curses.LINES - 1, 0, prompt, curses.A_BOLD)
  i = screen.getch()
  screen.addstr(curses.LINES - 1, 0, " "*len(prompt), curses.A_BOLD)
  st = chr(i)
  while i != 10:
    debug(screen, str(st), style=curses.A_UNDERLINE)
    screen.refresh()
    i = screen.getch()
    if i < 256:
      st += chr(i)
  screen.addstr(curses.LINES - 1, 0, " "*len(prompt), curses.A_BOLD)
  
  return st.strip()
