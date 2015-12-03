#!/usr/bin/python

from color import Color
from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError
from os.path import expanduser

DEFAULT_FILENAME = None
DEFAULT_FILTER_LIST = []
DEFAULT_IGNORE_LIST = []
DEFAULT_NEW_LOG_ENTRY_REGEX = None
DEFAULT_COLOR = Color.WHITE

SEPARATOR_TOKEN = ','
SEPARATOR_TAG_COLOR = '='

COLOR_MAP = {
   'CRITICAL' : Color.RED,
   'ERROR'    : Color.RED,
   'INFO'     : Color.WHITE,
   'WARN'     : Color.YELLOW,
   'DEBUG'    : Color.PURPLE
}

class ConfigurationProperty(object):
   FILENAME = 'filename'
   FILTER_LIST = 'filter_list'
   IGNORE_LIST = 'ignore_list'
   NEW_LOG_ENTRY_REGEX = 'new_log_entry_regex'
   COLOR = 'color'
   DEFAULT_COLOR = 'default_color'

class Configuration(object):
   def __init__(self):
      self.filename = None
      self.filter_list = []
      self.ignore_list = []
      self.new_log_entry_regex = None
      self.color_map = {}
      self.default_color = None

      # TODO Remove when file configuration is implemented
      self.color_map = COLOR_MAP.copy()
      self.default_color = DEFAULT_COLOR

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

   @staticmethod
   def _parse_tag_color_pair(value):
      tokens = value.split(SEPARATOR_TAG_COLOR)

      if len(tokens) != 2:
         raise Exception('Wrong format of COLOR configuration!')

      tag = tokens[0].strip()
      color = Color.parse(tokens[1].strip())

      return (tag, color)

   @staticmethod
   def _tokenize(value):
      return [token.strip() for token in value.split(SEPARATOR_TOKEN)]

class ConfigurationManager(object):
   CONFIG_FILE = '.loggy.cfg'

   def __init__(self):
      self._configuration = None

   def load(self):
      file_path = expanduser('~') + '/' + self.CONFIG_FILE
      fileConfigurator = FileConfigurator(file_path)
      self._configuration = fileConfigurator.get()

   def get(self):
      return self._configuration

class Configurator(object):
   def get(self): pass
   def update(self, config):pass
   def set(self, config):pass
   def save(self):pass


class FileConfigurator(Configurator):

   def __init__(self, filename):
      super(FileConfigurator, self).__init__()
      self._filename = filename

   def get(self):
      config = Configuration()
      return self.update(config)

   def update(self, config):
      cp = SafeConfigParser()
      cp.read(self._filename)

      self._load_option(cp, config, 'Basic', ConfigurationProperty.FILENAME)
      self._load_option(cp, config, 'Basic', ConfigurationProperty.FILTER_LIST)
      self._load_option(cp, config, 'Basic', ConfigurationProperty.IGNORE_LIST)
      self._load_option(cp, config, 'Basic', ConfigurationProperty.NEW_LOG_ENTRY_REGEX)
      self._load_option(cp, config, 'Basic', ConfigurationProperty.DEFAULT_COLOR)

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
