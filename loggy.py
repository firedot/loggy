#!/usr/bin/python

import sys

from pprint import pprint
from core.config import configuration_manager
from core.mode import mode_manager

from util.constants import SEPARATOR


if __name__ == '__main__':
    print 'Hello!'
    print 'This is loggy :)'
    print 'Loading configuration...'
    configuration_manager.load()
    configs = configuration_manager.get_all()

    pprint(configs)

    if not configs:
        print 'No configuration found...'
        sys.exit(2)
    elif len(configs.values()) == 1:
        config = configs.values()[0]

    print 'Done'

    pprint(config)

    print SEPARATOR
    print 'You are using loggy with the following configuration:'
    print "You are following: %s" % config.filename
    print "Filter: %s" % config.filter_list
    print "New line reges: %s" % config.new_log_entry_regex


    mode_manager.load()
    TAIL_MODE = mode_manager.get('TailMode')
    COMMAND_MODE = mode_manager.get('CommandMode')
    mode = TAIL_MODE

    while True:
        try:
            print
            print SEPARATOR
            mode = mode.execute()
        except KeyboardInterrupt:
            if mode is COMMAND_MODE:
                print
                print SEPARATOR
                print 'Bye, bye! :)'
                exit(0)
            else:
                mode = COMMAND_MODE
        except Exception, ex:
            print 'Something has gone wrong...'
            print ex
            sys.exit(1)
