#!/usr/bin/python

import sys

from core.config import ConfigurationManager
from mode.command import CommandMode
from mode.tail import TailMode

SEPARATOR = 80 * '-'

class Modes(object):
    TAIL_MODE = TailMode()
    COMMAND_MODE = CommandMode()

if __name__ == '__main__':
    print 'Hello!'
    print 'This is loggy :)'
    print 'Loading configuration...'
    configManager = ConfigurationManager()
    configManager.load()
    config = configManager.get()
    print 'Done'

    print SEPARATOR
    print 'You are using loggy with the following configuration:'
    print "You are following: %s" % config.filename
    print "Filter: %s" % config.filter_list
    print "New line reges: %s" % config.new_log_entry_regex

    mode = Modes.TAIL_MODE

    while True:
        try:
            print
            print SEPARATOR
            mode = mode.execute()
        except KeyboardInterrupt:
            if mode is Modes.COMMAND_MODE:
                print
                print SEPARATOR
                print 'Bye, bye! :)'
                exit(0)
            else:
                mode = Modes.COMMAND_MODE
        except Exception, ex:
            print 'Something has gone wrong...'
            print ex
            sys.exit(1)
