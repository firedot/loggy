#!/usr/bin/python


from core.color import Color
from util.singleton import Singleton

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
        self._configuration = None
        self._configurators = []

    def load(self):
        self._scan()
        config = Configuration()
        for configurator in self._configurators:
            configurator.setup()
            configurator.update(config)
        self._configuration = config

    def register(self, configurator):
        self._configurators.append(configurator)

    def get(self):
        return self._configuration

    def _scan(self):
        from importlib import import_module
        import_module("config")


class Configurator(object):

    def setup(self): pass

    def get(self): pass

    def update(self, config): pass

    def set(self, config): pass

    def save(self): pass
