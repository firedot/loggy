#!/usr/bin/python


import sys
from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError
from os.path import expanduser

from color import Color
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

    CONFIG_FILE = '.loggy.cfg'

    def __init__(self):
        self._configuration = None

    def load(self):
        # 1. Load the initial configuration from the
        # config file (if exists)
        file_path = expanduser('~') + '/' + self.CONFIG_FILE
        file_configurator = FileConfigurator(file_path)
        self._configuration = file_configurator.get()

        # 2. Update the configuration according to the
        # command line args
        args_configurator = ArgsConfigurator(sys.argv)
        args_configurator.update(self._configuration)

    def get(self):
        return self._configuration


class Configurator(object):
    def get(self): pass

    def update(self, config): pass

    def set(self, config): pass

    def save(self): pass


class FileConfigurator(Configurator):
    CATEGORY_BASIC = 'Basic'
    CATEGORY_COLOR = 'Color'

    def __init__(self, filename):
        super(FileConfigurator, self).__init__()
        self._filename = filename

    def get(self):
        config = Configuration()
        return self.update(config)

    def update(self, config):
        cp = SafeConfigParser()
        cp.read(self._filename)

        self._load_option(cp, config, self.CATEGORY_BASIC, ConfigurationProperty.FILENAME)
        self._load_option(cp, config, self.CATEGORY_BASIC, ConfigurationProperty.FILTER_LIST)
        self._load_option(cp, config, self.CATEGORY_BASIC, ConfigurationProperty.IGNORE_LIST)
        self._load_option(cp, config, self.CATEGORY_BASIC, ConfigurationProperty.NEW_LOG_ENTRY_REGEX)
        self._load_option(cp, config, self.CATEGORY_BASIC, ConfigurationProperty.DEFAULT_COLOR)

        return config

    @staticmethod
    def _load_option(config_parser, config, section, option):
        try:
            value = config_parser.get(section, option)
            config.set(option, value)
        except (NoSectionError, NoOptionError):
            pass

    def set(self, configuration):
        # TODO Implement
        pass

    def save(self):
        # TODO Implement
        pass


class ArgsConfigurator(Configurator):
    def __init__(self, args):
        super(ArgsConfigurator, self).__init__()
        self._args = args

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
