#!/usr/bin/python

import os
import time
from sys import stdout
from color import Color

from threading import Thread

#Set the filename and open the file
filename = 'test.log'

def open_file(filename):
   file = open(filename,'r')
   file_stats = os.stat(filename)
   file_size = file_stats[6]
   file.seek(file_size)
   return file

TYPE_ERROR = 0
TYPE_INFO = 1
TYPE_WARN = 2

tag = 'VsanVcCluster'
ERROR_TOKEN = 'ERROR'
INFO_TOKEN = 'INFO'
WARN_TOKEN = 'WARN'
DEBUG_TOKEN = 'DEBUG'

FLAG = True

def get_line_color(line):
   if line.count(ERROR_TOKEN):
      return Color.RED
   elif line.count(INFO_TOKEN):
      return Color.WHITE
   elif line.count(WARN_TOKEN):
      return Color.YELLOW
   elif line.count(DEBUG_TOKEN):
      return Color.PURPLE
   else:
      return Color.WHITE

def println(line, color=Color.WHITE):
   stdout.write("%s%s%s" % (color, line, Color.RESET))

def print_file(file):
   global FLAG
   while FLAG:
      where = file.tell()
      line = file.readline()

      if not line:
         time.sleep(1)
         file.seek(where)
      else:
         if line.count(tag): 
            color = get_line_color(line)
            println(line, color) # already has newline

def get_command():
   global FLAG
   while FLAG:
      line = raw_input()
      if line == 'exit':
         FLAG = False
         signal.

if __name__ == '__main__':
   print 'this is a test main'

   file = open_file(filename)
   t1 = Thread(target=print_file, args=(file,))
   t1.start()

   t2 = Thread(target=get_command)
   t2.start()

   signal.pause()

   t1.join()
   t2.join()

