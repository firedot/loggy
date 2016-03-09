#!/usr/bin/python


from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError
from os.path import expanduser

from core.config import Configurator, ConfigurationManager, Configuration, ConfigurationProperty


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
        self._filepath = expanduser('~') + '/' + self._filename

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

print 'Iported: ', __file__

ConfigurationManager().register(FileConfigurator())
