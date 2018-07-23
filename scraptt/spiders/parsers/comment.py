# -*- coding: utf-8 -*-
"""PTT COMMENT parsers."""
import re
from collections import defaultdict


def comment_counter(comments):
    """."""
    counter = defaultdict(int)
    for comment in comments:
        counter[comment['type']] += 1
    return counter


def remove_ip(string):
    """Remove ip strings."""
    ips = re.findall(r'\d{,3}\.\d{,3}\.\d{,3}\.\d{,3}', string)
    if ips:
        ip = ips[-1]
        string = string.replace(ip, '')
    else:
        ip = None
    return string, ip
