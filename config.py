#!/usr/bin/python

from color import Color

DEFAULT_FILENAME = '/var/log/vmware/vsan-health/vmware-vsan-health-service.log'
DEFAULT_FILTER = 'VsanVcClusterConfigSystemImpl'
DEFAULT_NEW_LOG_ENTRY_REGEX = '2015'
DEFAULT_COLOR = Color.WHITE

ERROR_TOKEN = 'ERROR'
INFO_TOKEN = 'INFO'
WARN_TOKEN = 'WARN'
DEBUG_TOKEN = 'DEBUG'
CRITICAL_TOKEN = 'CRITICAL'

COLOR_MAP = {
      'CRITICAL' : Color.RED,
      'ERROR'    : Color.RED,
      'INFO'     : Color.WHITE,
      'WARN'     : Color.YELLOW,
      'DEBUG'    : Color.PURPLE
}

class Configuration(object):
   def __init__(self, filename=DEFAULT_FILENAME, filter=DEFAULT_FILTER, \
         new_log_entry_regex=DEFAULT_NEW_LOG_ENTRY_REGEX):
      self.filename = filename
      self.filter = filter
      self.new_log_entry_regex = new_log_entry_regex
      self.color_map = COLOR_MAP.copy()
      self.default_color = DEFAULT_COLOR

