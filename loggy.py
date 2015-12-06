#!/usr/bin/python

import sys

from config import ConfigurationManager
from mode import Modes

if __name__ == '__main__':
    print 'Hello!'
    print 'This is loggy :)'
    print 'Loading configuration...'
    configManager = ConfigurationManager()
    configManager.load()
    config = configManager.get()
    print 'Done'

    print "You are following: %s" % config.filename

    mode = Modes.PRINT_MODE

    while True:
        try:
            mode = mode.execute()
        except KeyboardInterrupt:
            mode.handle_keyboard_interrupt()
        except Exception, ex:
            print 'Something has gone wrong...'
            print ex
            sys.exit(1)
