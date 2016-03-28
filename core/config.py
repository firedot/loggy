#!/usr/bin/python


from core.color import Color
from util.singleton import Singleton
import os
from os import listdir
from os.path import isfile, join

COLOR_MAP = {
    'CRITICAL': Color.RED,
    'ERROR': Color.RED,
    'INFO': Color.WHITE,
    'WARN': Color.YELLOW,
    'DEBUG': Color.PURPLE
}


class ConfigurationProperty(object):
    FILENAME = 'filename'
    FILTER_LIST = 'filter_list'
    IGNORE_LIST = 'ignore_list'
    NEW_LOG_ENTRY_REGEX = 'new_log_entry_regex'
    COLOR = 'color'
    DEFAULT_COLOR = 'default_color'


class Configuration(object):
    SEPARATOR_TOKEN = ','
    SEPARATOR_TAG_COLOR = '='

    def __init__(self):
        self.filename = None
        self.filter_list = []
        self.ignore_list = []
        self.new_log_entry_regex = None
        self.color_map = {}
        self.default_color = None
        self.color_map = COLOR_MAP.copy()
        self.default_color = Color.WHITE

    def set(self, prop, value):
        if prop == ConfigurationProperty.FILENAME:
            self.filename = value
        elif prop == ConfigurationProperty.FILTER_LIST:
            self.filter_list = self._tokenize(value)
        elif prop == ConfigurationProperty.IGNORE_LIST:
            self.ignore_list = self._tokenize(value)
        elif prop == ConfigurationProperty.NEW_LOG_ENTRY_REGEX:
            self.new_log_entry_regex = value
        elif prop == ConfigurationProperty.DEFAULT_COLOR:
            self.default_color = Color.parse(value)

    def add(self, prop, value):
        if prop == ConfigurationProperty.FILTER_LIST:
            self.filter_list.extend(self._tokenize(value))
        elif prop == ConfigurationProperty.IGNORE_LIST:
            self.ignore_list.extend(self._tokenize(value))
        elif prop == ConfigurationProperty.COLOR:
            tag, color = self._parse_tag_color_pair(value)
            self.color_map[tag] = color

    def reset(self, prop):
        if prop == ConfigurationProperty.FILENAME:
            self.filename = ''
        elif prop == ConfigurationProperty.FILTER_LIST:
            self.filter_list = []
        elif prop == ConfigurationProperty.IGNORE_LIST:
            self.ignore_list = []
        elif prop == ConfigurationProperty.NEW_LOG_ENTRY_REGEX:
            self.new_log_entry_regex = None
        elif prop == ConfigurationProperty.COLOR:
            self.color_map.clear()
        elif prop == ConfigurationProperty.DEFAULT_COLOR:
            self.default_color = None

    @classmethod
    def _parse_tag_color_pair(cls, value):
        tokens = value.split(cls.SEPARATOR_TAG_COLOR)

        if len(tokens) != 2:
            raise Exception('Wrong format of COLOR configuration!')

        tag = tokens[0].strip()
        color = Color.parse(tokens[1].strip())

        return tag, color

    @classmethod
    def _tokenize(cls, value):
        return [token.strip() for token in value.split(cls.SEPARATOR_TOKEN)]


class ConfigurationManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self._configurations = {}
        self._configurators = []

    def load(self):
        self._scan()
        for configurator in self._configurators:
            configurator.setup()
            configs = configurator.get()
            # TODO [kaleksandrov] This will override existing configurations
            # with the same name
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

    def _get_dir(self, dir_name):
        current_file_path = os.path.realpath(__file__)
        current_dir_name = os.path.dirname(current_file_path)
        current_dir_name = os.path.dirname(current_dir_name)
        return os.path.join(current_dir_name, dir_name)

    def _scan(self):
        dir_name = self._get_dir('config')
        listdir(dir_name)
        ff = [f.split('.')[0] for f in listdir(dir_name) if isfile(join(dir_name, f)) and f.endswith('.py')]
        import inspect
        import imp
        for f in ff:
            module = imp.load_source(f, os.path.join(dir_name, f+'.py'))
            for name, obj in inspect.getmembers(module):
                if hasattr(obj, '__bases__'):
                    if Configurator in obj.__bases__ :
                        self.register(obj())



class Configurator(object):

    def setup(self): pass

    def get(self): pass

    def update(self, config): pass

    def set(self, config): pass

    def save(self): pass
