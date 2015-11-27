#!/usr/bin/python

import os
import sys
import time
from sys import stdout
from color import Color
from config import Configuration

def open_file(filename):
   f = open(filename,'r')
   file_stats = os.stat(filename)
   file_size = file_stats[6]
   f.seek(file_size)
   return f

class LogProcessor(object):

   def __init__(self, config):
      self.last_color = None
      self.filter_list = config.filter_list
      self.ignore_list = config.ignore_list
      self.new_log_entry_regex = config.new_log_entry_regex
      self.color_map = config.color_map.copy()
      self.default_color = config.default_color

   def get_line_color(self, line):
      result = None
      for entry, color in self.color_map.iteritems():
         if entry in line:
            result = color
            break
      else:
         result = self.default_color

      return result

   def is_new_log_entry(self, line):
      return line.startswith(self.new_log_entry_regex)

   def println(self, line):
      if self.is_new_log_entry(line):
         if self.ignore_list and self.contains(line, self.ignore_list):
            self.last_color = None
         elif self.filter_list and self.contains(line, self.filter_list) \
              or not self.filter_list:
            color = self.get_line_color(line)
            if color:
               self.last_color = color
               self.print_with_color(line, color)
            else:
               print line
         else:
            self.last_color = None
      elif self.last_color:
         self.print_with_color(line, self.last_color)

   @staticmethod
   def contains(line, tokens):
      result = False
      for token in tokens:
         if token in line:
            result = True
            break

      return result

   @staticmethod
   def print_with_color(line, color):
      stdout.write("%s%s%s" % (color, line, Color.RESET))

def is_new_line(value):
   return value == '' or value == '\r' or value == '\n' or value == '\r\n'

def print_file(f, log_processor, start_from=None):
   if start_from:
      f.seek(start_from)

   while True:
      where = f.tell()
      line = f.readline()

      if not line:
         time.sleep(1)
         f.seek(where)
      else:
         log_processor.println(line)

def mode_print(config):
   print 80*'-'
   f = open_file(config.filename)
   log_processor = LogProcessor(config)
   print_file(f, log_processor)

def mode_command(config):
   print
   print 80*'-'
   while True:
      stdout.write('[command]: ')
      command = raw_input()
      if command == 'exit':
         sys.exit(0)
      elif command == 'resume':
         return MODE_PRINT
      elif command == 'config':
         print config.filename
         print config.filter
         print config.new_log_entry_regex
      elif command.startswith('filename='):
         config.filename = command.replace('filename=', '', 1)
      elif command.startswith('filter='):
         config.filter = command.replace('filter=', '', 1)
      elif is_new_line(command):
         continue
      else:
         print "\tUnknown command: %s" % command

   return None

MODE_PRINT = mode_print
MODE_COMMAND = mode_command

conf = Configuration()
conf.filename = '/var/log/vmware/vsan-health/vmware-vsan-health-service.log'
conf.new_log_entry_regex = '2015'
conf.filter = 'VsanVcClusterConfigSystemImpl'

if __name__ == '__main__':
   print 'Hello!'
   print 'This is loggy :)'
   print "You are following: %s" % conf.filename

   mode = MODE_PRINT
   while True:
      try:
         mode = mode(conf)
      except KeyboardInterrupt, ki:
         if mode == MODE_COMMAND:
            print
            print 80*'-'
            print 'Bye, bye! :)'
            sys.exit(0)
         else:
            mode = MODE_COMMAND
      except Exception, ex:
         print 'Something has gone wrong...'
         print ex
