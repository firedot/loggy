#!/usr/bin/python

from sys import exit

from util.singleton import Singleton


class CommandManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        print '__init__'

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
        print "Registering %s" % command.name
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
