#!/usr/bin/python

from sys import stdout, exit

# from command import CommandManager
from util.singleton import Singleton
from core.mode import Mode


class CommandManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        if not hasattr(self, '_commands'):
            self._commands = {}

    def parse(self, value):
        if not isinstance(value, str):
            raise ValueError('The value must be a str.')

        key = self._normalize(value)
        if key in self._commands:
            return self._commands[key]
        else:
            return None

    @staticmethod
    def _normalize(key):
        return key.strip().lower()

    def register(self, command):
        key = self._normalize(command.name)
        self._commands[key] = command


class Command(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def execute(self, **args):
        pass


class ResumeCommand(Command):
    def __init__(self):
        super(ResumeCommand, self).__init__("resume")

    def execute(self, **args):
        return "PRINT"


class ExitCommand(Command):
    def __init__(self):
        super(ExitCommand, self).__init__("exit")

    def execute(self, **args):
        exit(0)


cm = CommandManager()
cm.register(ResumeCommand())
cm.register(ExitCommand())


class CommandMode(Mode):
    def execute(self):

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
