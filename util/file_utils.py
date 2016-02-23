#!/usr/bin/python

import os


def open_file_at(filename, where=None):
    f = open(filename, 'r')

    if not where:
        file_stats = os.stat(filename)
        where = file_stats[6]  # file size

    f.seek(where)
    return f
