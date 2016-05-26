#!/usr/bin/python

import os
from os import listdir
from os.path import isfile, join


def open_file_at(filename, where=None):
    f = open(filename, 'r')

    if not where:
        file_stats = os.stat(filename)
        where = file_stats[6]  # file size

    f.seek(where)
    return f


def get_dir(dir_name):
    current_file_path = os.path.realpath(__file__)
    current_dir_name = os.path.dirname(current_file_path)
    current_dir_name = os.path.dirname(current_dir_name)
    return os.path.join(current_dir_name, dir_name)
