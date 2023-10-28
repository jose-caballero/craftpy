#!/usr/bin/env python

from datetime import datetime

def str_to_seconds(date_str):
    """
    convert a string into seconds since epoch
    :param str date_str: example  '27-10-2023 07:00:00'
    :return int: seconds since epoch
    """
    date_format = '%d-%m-%Y %H:%M:%S'
    d = datetime.strptime(date_str, date_format)
    seconds = int(d.timestamp())
    return seconds




