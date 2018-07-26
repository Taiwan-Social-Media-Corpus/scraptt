# -*- coding: utf-8 -*-
"""PTT POST parsers."""
import re
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    """HTML tag stripper.

    ref: http://stackoverflow.com/a/925630/1105489
    """

    def __init__(self):  # noqa
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):  # noqa
        self.fed.append(d)

    def get_data(self):  # noqa
        return ''.join(self.fed)

    @classmethod
    def strip_tags(cls, html):  # noqa
        s = cls()
        s.feed(html)
        return s.get_data()


def mod_content(content):
    """Remove unnecessary info from a PTT post."""
    content = MLStripper.strip_tags(content)
    content = re.sub(
        r"※ 發信站.*|※ 文章網址.*|※ 編輯.*", '', content
    ).strip('\r\n-')
    return content


def extract_author(string):
    """Extract author id."""
    return string.split(' ')[0]


def extract_ip(string):
    """Extract IP address.

    The strategy is to find as many IPs as possible, and return the last one
    as the IP info is usually at the bottom of the content.
    """
    ips = re.findall(r'\d{,3}\.\d{,3}\.\d{,3}\.\d{,3}', string)
    if ips:
        ip = ips[-1]
    else:
        ip = None
    return ip
