#!/usr/bin/python

import time
from sys import stdout, exit

from command import CommandManager
from config import ConfigurationManager
from file_processor import LogProcessor
from util.file_utils import open_file_at

SEPARATOR = 80 * '-'


class Mode(object):
    def execute(self):
        pass

    def handle_keyboard_interrupt(self):
        pass


class PrintMode(Mode):
    def execute(self):
        print SEPARATOR

        config = ConfigurationManager().get()
        f = open_file_at(config.filename)
        log_processor = LogProcessor(config)

        try:
            while True:
                where = f.tell()
                line = f.readline()

                if not line:
                    time.sleep(0.2)
                    f.seek(where)
                else:
                    log_processor.println(line)
        except KeyboardInterrupt:
            return Modes.COMMAND_MODE

    def handle_keyboard_interrupt(self):
        pass


class CommandMode(Mode):
    def __init__(self):
        super(CommandMode, self).__init__()

    @staticmethod
    def execute():
        print
        print SEPARATOR

        while True:
            stdout.write('[command]: ')
            raw_command = raw_input()

            command = CommandManager().parse(raw_command)

            if command:
                result = command.execute()
                if result:
                    return Modes.PRINT_MODE
            else:
                print "\tUnknown command: %s" % raw_command

    def handle_keyboard_interrupt(self):
        print
        print SEPARATOR
        print 'Bye, bye! :)'
        exit(0)


class Modes(object):
    PRINT_MODE = PrintMode()
    COMMAND_MODE = CommandMode()
