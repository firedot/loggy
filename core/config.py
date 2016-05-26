#!/usr/bin/python


from core.color import Color
from util.singleton import Singleton
import os
from os import listdir
from os.path import isfile, join
from pprint import pprint

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


class ConfigurationManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self._configurations = {}
        self._configurators = []

    def load(self):
        self._scan()
        for configurator in self._configurators:
            configurator.setup()
            configs = configurator.get_all()
            # TODO [kaleksandrov] This will override existing configurations
            # with the same name
            pprint(configs)
            if isinstance(configs, dict):
                self._configurations.update(configs)

    def register(self, configurator):
        self._configurators.append(configurator)
        print 'Registered: ', configurator.__class__.__name__

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

    def _scan(self):
        dir_name = get_dir('config')
        listdir(dir_name)
        ff = [f.split('.')[0] for f in listdir(dir_name) \
                if isfile(join(dir_name, f)) and f.endswith('.py')]
        import inspect
        import imp
        for f in ff:
            module = imp.load_source(f, os.path.join(dir_name, f+'.py'))
            for _, obj in inspect.getmembers(module):
                if hasattr(obj, '__bases__'):
                    if Configurator in obj.__bases__ :
                        self.register(obj())



class Configurator(object):

    def setup(self): pass

    def get(self, name): pass

    def get_all(self): pass

    def update(self, name, config): pass

    def set(self, name, config): pass

    def save(self): pass


def get_dir(dir_name):
    current_file_path = os.path.realpath(__file__)
    current_dir_name = os.path.dirname(current_file_path)
    current_dir_name = os.path.dirname(current_dir_name)
    return os.path.join(current_dir_name, dir_name)
