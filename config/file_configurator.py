#!/usr/bin/python


from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError
from os.path import expanduser, join

from core.config import Configurator, Configuration
from core.color import Color


class ConfigurationProperty(object):
    FILENAME = 'filename'
    FILTER_LIST = 'filter_list'
    IGNORE_LIST = 'ignore_list'
    NEW_LOG_ENTRY_REGEX = 'new_log_entry_regex'
    COLOR = 'color'
    DEFAULT_COLOR = 'default_color'


class FileConfigurator(Configurator):
    CATEGORY_BASIC = 'Basic'
    CATEGORY_COLOR = 'Color'
    CONFIG_FILE = '.loggy.cfg'

    def __init__(self, filename=None):
        super(FileConfigurator, self).__init__()
        if filename:
            self._filename = filename
        else:
            self._filename = self.CONFIG_FILE
        self._filepath = None

    def setup(self):
        self._filepath = join(expanduser('~'),self._filename)

    def get(self, name):
        return self.update(name, Configuration())

    def get_all(self):
        return {'default': self.get('default')}

    def update(self, name, config):
        cp = SafeConfigParser()
        cp.read(self._filename)

        load_option(cp, config, self.CATEGORY_BASIC, ConfigurationProperty.FILENAME)
        load_option(cp, config, self.CATEGORY_BASIC, ConfigurationProperty.FILTER_LIST)
        load_option(cp, config, self.CATEGORY_BASIC, ConfigurationProperty.IGNORE_LIST)
        load_option(cp, config, self.CATEGORY_BASIC, ConfigurationProperty.NEW_LOG_ENTRY_REGEX)
        load_option(cp, config, self.CATEGORY_BASIC, ConfigurationProperty.DEFAULT_COLOR)

        return config

    def set(self, name, configuration):
        # TODO Implement
        pass

    def save(self):
        # TODO Implement
        pass


SEPARATOR_TOKEN = ','


def tokenize(value):
    return [token.strip() for token in value.split(SEPARATOR_TOKEN)]

def load_option(config_parser, config, section, option):
    try:
        value = config_parser.get(section, option)
        set_prop(config, option, value)
    except (NoSectionError, NoOptionError):
        pass

def set_prop(config, prop, value):
    if prop == ConfigurationProperty.FILENAME:
        config.filename = value
    elif prop == ConfigurationProperty.FILTER_LIST:
        config.filter_list = tokenize(value)
    elif prop == ConfigurationProperty.IGNORE_LIST:
        config.ignore_list = tokenize(value)
    elif prop == ConfigurationProperty.NEW_LOG_ENTRY_REGEX:
        config.new_log_entry_regex = value
    elif prop == ConfigurationProperty.DEFAULT_COLOR:
        config.default_color = Color.parse(value)
