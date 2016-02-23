#!/usr/bin/python

import time
from sys import stdout

from core.color import Color
from core.config import ConfigurationManager
from core.mode import Mode
from util.file_utils import open_file_at


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


class TailMode(Mode):
    def execute(self):

        config = ConfigurationManager().get()
        f = open_file_at(config.filename)
        log_processor = LogProcessor(config)

        while True:
            where = f.tell()
            line = f.readline()

            if not line:
                time.sleep(0.2)
                f.seek(where)
            else:
                log_processor.println(line)
