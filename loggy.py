#!/usr/bin/python

import os
import sys
import time
from sys import stdout
from color import Color

#Set the filename and open the file
FILENAME = '/var/log/vmware/vsan-health/vmware-vsan-health-service.log'

def open_file(filename):
   f = open(filename,'r')
   file_stats = os.stat(filename)
   file_size = file_stats[6]
   f.seek(file_size)
   return f

TYPE_ERROR = 0
TYPE_INFO = 1
TYPE_WARN = 2

tag = 'VsanVcClusterConfigSystemImpl'
ERROR_TOKEN = 'ERROR'
INFO_TOKEN = 'INFO'
WARN_TOKEN = 'WARN'
DEBUG_TOKEN = 'DEBUG'
CRITICAL_TOKEN = 'CRITICAL'

FLAG = True

def is_new_line(value):
   return value == '' or value == '\r' or value == '\n' or value == '\r\n'

def is_new_log_entry(line):
   return line.startswith('2015')

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

def print_file(f):
   LAST_COLOR = None
   while True:
      where = f.tell()
      line = f.readline()

      if not line:
         time.sleep(1)
         f.seek(where)
      else:
         if is_new_log_entry(line):
            if line.count(tag):
               color = get_line_color(line)
               LAST_COLOR = color
               println(line, color)
            else:
               LAST_COLOR = None
         elif LAST_COLOR:
            println(line, LAST_COLOR)

def mode_print():
   print
   print '=================================='
   print ' You have entered print mode'
   print '=================================='
   f = open_file(FILENAME)
   print_file(f)

def mode_command():
   print
   print '=================================='
   print ' You have entered command mode'
   print '=================================='
   while True:
      stdout.write('[command]: ')
      command = raw_input()
      if command == 'exit':
         sys.exit(0)
      elif command == 'resume':
         return MODE_PRINT
      elif is_new_line(command):
         continue
      else:
         print "\tUnknown command: %s" % command

   return None

MODE_PRINT = mode_print
MODE_COMMAND = mode_command

if __name__ == '__main__':
   print 'Hello!'
   print 'This is loggy :)'
   print "You are following: %s" % FILENAME

   global_stop = False
   mode = MODE_PRINT
   while not global_stop:
      try:
         mode = mode()
      except KeyboardInterrupt, kb:
         if mode == MODE_COMMAND:
            print
            sys.exit(0)
         else:
            mode = MODE_COMMAND
      except Exception, ex:
         print 'Something has gone wrong...'
