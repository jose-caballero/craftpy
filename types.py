#!/usr/bin/env python

"""
tools to manipulate types
"""

def string_to_list(s, cast=None):
    """
    convert a string representing a list into an actual list.
    Example: 
        s = "[a,b,c,]"
    """
    if cast:
        l = [ cast(i.strip()) for i in s.strip().strip('][').split(',') ]
    else:
        l = [ i.strip() for i in s.strip().strip('][').split(',') ]
    return l


class PrintableList(list):
    def __str__(self):
        out = ""
        for i in self.__iter__():
            out += '%i\n' %i
        out = out[:-1] # to remove the last \n
        return out
