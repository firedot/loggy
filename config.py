#!/usr/bin/python

from color import Color

DEFAULT_FILENAME = None
DEFAULT_FILTER_LIST = []
DEFAULT_IGNORE_LIST = []
DEFAULT_NEW_LOG_ENTRY_REGEX = None
DEFAULT_COLOR = Color.WHITE

ERROR_TOKEN = 'ERROR'
INFO_TOKEN = 'INFO'
WARN_TOKEN = 'WARN'
DEBUG_TOKEN = 'DEBUG'
CRITICAL_TOKEN = 'CRITICAL'

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
