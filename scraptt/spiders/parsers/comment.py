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
    return re.sub('\d+\.\d+\.\d+\.\d+', '', string)
