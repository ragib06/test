##library download:
##  http://sourceforge.net/projects/pywin32/files/pywin32/Build%20217/pywin32-217.win32-py2.7.exe/download

##reference links:
##  http://timgolden.me.uk/python/win32_how_do_i/catch_system_wide_hotkeys.html
##  http://www.hep.wisc.edu/~rgavin/mg2/cuts/scratch/mercurial/lib/python2.6/site-packages/IPython/lib/clipboard.py
##  http://docs.activestate.com/activepython/2.4/pywin32/win32clipboard.html
##  http://docs.activestate.com/activepython/2.4/pywin32/win32gui.html
##  http://stackoverflow.com/questions/7596502/send-key-event-to-a-child-window
##  http://www.gossamer-threads.com/lists/python/python/654440
##  http://sourcetumble.appspot.com/dictionary-full-windows-keys/
##  http://stackoverflow.com/questions/3827511/copying-and-pasting-from-to-clipboard-with-python-win32

import os
import sys
import ctypes
from ctypes import wintypes
import win32con
import win32api
import win32gui
import win32com.client
import win32clipboard

byref = ctypes.byref
user32 = ctypes.windll.user32

flag = False
APPEND_WITH = '\n'


keys = {
    "shift": win32con.MOD_SHIFT
    , "control": win32con.MOD_CONTROL
    , "ctrl": win32con.MOD_CONTROL
    , "alt": win32con.MOD_ALT
    , "win": win32con.MOD_WIN
    , "up": win32con.VK_UP
    , "down": win32con.VK_DOWN
    , "left": win32con.VK_LEFT
    , "right": win32con.VK_RIGHT
    , "pgup": win32con.VK_PRIOR
    , "pgdown": win32con.VK_NEXT
    , "home": win32con.VK_HOME
    , "end": win32con.VK_END
    , "insert": win32con.VK_INSERT
    , "enter": win32con.VK_RETURN
    , "tab": win32con.VK_TAB
    , "space": win32con.VK_SPACE
    , "backspace": win32con.VK_BACK
    , "delete": win32con.VK_DELETE
    , "del": win32con.VK_DELETE
    , "apps": win32con.VK_APPS
    , "popup": win32con.VK_APPS
    , "escape": win32con.VK_ESCAPE
    , "npmul": win32con.VK_MULTIPLY
    , "npadd": win32con.VK_ADD
    , "npsep": win32con.VK_SEPARATOR
    , "npsub": win32con.VK_SUBTRACT
    , "npdec": win32con.VK_DECIMAL
    , "npdiv": win32con.VK_DIVIDE
    , "np0": win32con.VK_NUMPAD0
    , "numpad0": win32con.VK_NUMPAD0
    , "np1": win32con.VK_NUMPAD1
    , "numpad1": win32con.VK_NUMPAD1
    , "np2": win32con.VK_NUMPAD2
    , "numpad2": win32con.VK_NUMPAD2
    , "np3": win32con.VK_NUMPAD3
    , "numpad3": win32con.VK_NUMPAD3
    , "np4": win32con.VK_NUMPAD4
    , "numpad4": win32con.VK_NUMPAD4
    , "np5": win32con.VK_NUMPAD5
    , "numpad5": win32con.VK_NUMPAD5
    , "np6": win32con.VK_NUMPAD6
    , "numpad6": win32con.VK_NUMPAD6
    , "np7": win32con.VK_NUMPAD7
    , "numpad7": win32con.VK_NUMPAD7
    , "np8": win32con.VK_NUMPAD8
    , "numpad8": win32con.VK_NUMPAD8
    , "np9": win32con.VK_NUMPAD9
    , "numpad9": win32con.VK_NUMPAD9
    , "f1": win32con.VK_F1
    , "f2": win32con.VK_F2
    , "f3": win32con.VK_F3
    , "f4": win32con.VK_F4
    , "f5": win32con.VK_F5
    , "f6": win32con.VK_F6
    , "f7": win32con.VK_F7
    , "f8": win32con.VK_F8
    , "f9": win32con.VK_F9
    , "f10": win32con.VK_F10
    , "f11": win32con.VK_F11
    , "f12": win32con.VK_F12
    , "f13": win32con.VK_F13
    , "f14": win32con.VK_F14
    , "f15": win32con.VK_F15
    , "f16": win32con.VK_F16
    , "f17": win32con.VK_F17
    , "f18": win32con.VK_F18
    , "f19": win32con.VK_F19
    , "f20": win32con.VK_F20
    , "f21": win32con.VK_F21
    , "f22": win32con.VK_F22
    , "f23": win32con.VK_F23
    , "f24": win32con.VK_F24
}


def send_ctrl_c(hwnd):
  shell = win32com.client.Dispatch("WScript.Shell")
  shell.SendKeys("^c")
  win32api.Sleep(100)


def handle_win_f3 ():
  global flag
  
  text = ''

  if(flag):
    win32clipboard.OpenClipboard() 
    text = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
    win32clipboard.CloseClipboard()  
  else:
    flag = True;

  handler = win32gui.GetForegroundWindow()
  send_ctrl_c(handler)

  win32clipboard.OpenClipboard()

  if(flag and text):
    text = text + APPEND_WITH

  text = text + win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)

  win32clipboard.EmptyClipboard()
  win32clipboard.SetClipboardText(text)

  win32clipboard.CloseClipboard()
  
  print text + '\n********'



def handle_win_f4 ():
  user32.PostQuitMessage (0)



HOTKEYS = {
  1 : (keys['f3'], keys['win']),
  2 : (keys['f4'], keys['win'])
}

HOTKEY_ACTIONS = {
  1 : handle_win_f3,
  2 : handle_win_f4
}




#
# RegisterHotKey takes:
#  Window handle for WM_HOTKEY messages (None = this thread)
#  arbitrary id unique within the thread
#  modifiers (MOD_SHIFT, MOD_ALT, MOD_CONTROL, MOD_WIN)
#  VK code (either ord ('x') or one of win32con.VK_*)
#
for id, (vk, modifiers) in HOTKEYS.items ():
  print "Registering id", id, "for key", vk
  if not user32.RegisterHotKey (None, id, modifiers, vk):
    print "Unable to register id", id

#
# Home-grown Windows message loop: does
#  just enough to handle the WM_HOTKEY
#  messages and pass everything else along.
#
try:
  msg = wintypes.MSG ()
  while user32.GetMessageA (byref (msg), None, 0, 0) != 0:
    if msg.message == win32con.WM_HOTKEY:
      action_to_take = HOTKEY_ACTIONS.get (msg.wParam)
      if action_to_take:
        action_to_take ()

    user32.TranslateMessage (byref (msg))
    user32.DispatchMessageA (byref (msg))

finally:
  for id in HOTKEYS.keys ():
    user32.UnregisterHotKey (None, id)
