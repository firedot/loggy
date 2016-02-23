#!/usr/bin/python

# Represents the different action mode that the program can execute.
class Mode(object):
    # This method is executed when the mode is activated. Most of the cases
    # you would want to start an infinite loop that will handle
    # user interaction
    def execute(self):
        pass