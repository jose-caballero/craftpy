#!/usr/bin/env python

"""
ancillaries for argparse
"""

class _HelpAction(argparse._HelpAction):
    """
    class to implement a decent help functionality
    when creating subcommands with argparse

    Usage:
        parser.add_argument('-h', '--help', action=_HelpAction, help='show this help message and exit')
    """
    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        # retrieve subparsers from parser
        subparsers_actions = [
            action for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)]
        # there will probably only be one subparser_action,
        # but better save than sorry
        for subparsers_action in subparsers_actions:
            # get all subparsers and print help
            for choice, subparser in subparsers_action.choices.items():
                print("Subparser '{}'".format(choice))
                print(subparser.format_help())
        parser.exit()


