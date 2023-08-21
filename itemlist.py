#!/usr/bin/env python

"""
Little library to help converting input arguments to scripts
into a list.
The input arguments can be a list of items and/or read from a file
Examples:
    $ myprogram a b c

    $ myprogram --file f
    $ cat f
    a
    b
    c

    $ myprogram --file f z x y
"""
import braceexpand
import argparse

def expand(arg):
    """
    expand bash-like arguments compressed in brackets.
    Examples:
        foo_{01,02,03}_bar --> foo_01_bar foo_02_bar foo_03_bar
        "foo_{01..03}_bar" --> foo_01_bar foo_02_bar foo_03_bar !! Note the quotes !!
    input: string
    output: list
    """
    return list( braceexpand.braceexpand(arg) )


def getlist(args_l):
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    parser.add_argument('items', nargs='*')
    args, unknown = parser.parse_known_args(args_l)
    out = args.items
    out = _parse_positional(args.items)
    if args.file:
        # there could be more than one file, split by comma
        for filename in args.file.split(','):
            out = _parse_file(out, filename)
    return out

def _parse_positional(arg_l):
    out = []
    for arg in arg_l:
        new_arg_l = expand(arg)
        for new_arg in new_arg_l:
            if new_arg not in out:
                out.append(new_arg)
    return out

def _parse_file(out, filename):
    f = open(filename)
    for line in f.readlines():
        line = line.strip()
        if line.startswith('#'):
            continue
        if line == '':
            continue
        arg_l = expand(line)
        for arg in arg_l:
            if arg not in out:
                out.append(arg)
    return out
