#!/usr/bin/python


import sys

from core.config import Configurator


class ArgsConfigurator(Configurator):
    def __init__(self, args=None):
        super(ArgsConfigurator, self).__init__()
        if args:
            self._args = args
        else:
            self._args = sys.argv

    def update(self, config):
        # TODO Implement
        pass

    def get(self):
        # TODO Implement
        pass

    def set(self, config):
        # TODO Implement
        pass

    def save(self):
        # TODO Implement
        pass
