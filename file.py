#!/usr/bin/env python

"""
functionalities to manage files
"""

def insertline(filename, n, line):
    """
    insert a new line at a given position
    :param st flename: 
    :param int n: line number where to insert new content
    :param str line: line to be inserted
    """
    with open(filename) as f:
        lines = f.readlines()
    lines.insert(n, line)
    with open(filename, 'w') as f:
        f.writelines(lines)


