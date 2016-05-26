#/usr/bin/python
import os
from os import listdir
from os.path import isfile, join
from util.file_utils import get_dir

import inspect
import imp


class ExtensionManager(object):

    def __init__(self, dir_name, clazz):
        self._registry = {}
        self._dir_name = dir_name
        self._clazz = clazz

    def _scan(self, folder, clazz):
        dir_name = get_dir(folder)
        listdir(dir_name)

        ff = [f.split('.')[0] for f in listdir(dir_name) \
                if isfile(join(dir_name, f)) and f.endswith('.py')]
        for f in ff:
            module = imp.load_source(f, os.path.join(dir_name, f+'.py'))
            for _, obj in inspect.getmembers(module):
                if hasattr(obj, '__bases__'):
                    if clazz in obj.__bases__ :
                        self.register(obj())

    def on_extension_loaded(self, extension):
        pass

    def load(self):
        self._scan(self._dir_name, self._clazz)
        for _, extension in self._registry.items():
            self.on_extension_loaded(extension)


    def register(self, extension):
        name = extension.__class__.__name__
        self._registry[name] = extension
        print 'Registered: ', name

    def get(self, name):
        return self._registry[name]
