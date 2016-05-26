#!/usr/bin/python


from core.color import Color
import os
from os import listdir
from os.path import isfile, join
from pprint import pprint
from extension import ExtensionManager


COLOR_MAP = {
    'CRITICAL': Color.RED,
    'ERROR': Color.RED,
    'INFO': Color.WHITE,
    'WARN': Color.YELLOW,
    'DEBUG': Color.PURPLE
}


class Configuration(object):

    def __init__(self):
        self.name=None
        self.filename = None
        self.filter_list = []
        self.ignore_list = []
        self.new_log_entry_regex = None
        self.color_map = COLOR_MAP.copy()
        self.default_color = Color.WHITE

    def __str__(self):
        return "%s(name: %s, filename: %s, filter_list: %s, ignore_list: %s, new_log_entry_regex: %s, default_color: %s)"\
                % (self.__class__.__name__, self.name, self.filename, self.filter_list, self.ignore_list, self.new_log_entry_regex, self.default_color)

    def __repr__(self):
        return self.__str__()

class Configurator(object):

    def setup(self): pass

    def get(self, name): pass

    def get_all(self): pass

    def update(self, name, config): pass

    def set(self, name, config): pass

    def save(self): pass


class ConfigurationManager(ExtensionManager):

    def __init__(self):
        super(ConfigurationManager, self).__init__('config', Configurator)
        self._configurations = {}

    def on_extension_loaded(self, extension):
        extension.setup()
        configs = extension.get_all()
        # TODO [kaleksandrov] This will override existing configurations
        # with the same name
        pprint(configs)
        if isinstance(configs, dict):
            self._configurations.update(configs)

    def get(self, profile=None):
        if profile:
            if profile in self._configurations.keys:
                return self._configurations[profile]
            else:
                return None
        else:
            if len(self._configurations) == 1:
                return self._configurations.values()[0]
            else:
                return None
    def get_all(self):
        return self._configurations

configuration_manager = ConfigurationManager()
