# -*- coding: utf-8 -*-
"""Main crawler."""
import re
from datetime import datetime

import scrapy


class PttSpider(scrapy.Spider):
    """Crawler for PTT."""

    name = 'index'
    allowed_domains = ['ptt.cc']

    def __init__(self, *args, **kwargs):
        """__init__ method.

        :params: boards: comma-separated board list
        """
        self.boards = kwargs.pop('boards').strip().split(',')

    def start_requests(self):
        """Request handler."""
        for board in self.boards:
            url = f'https://www.ptt.cc/bbs/{board}/index.html'
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        """Parse DOM."""
        # exclude "置底文"
        topics = response.dom('.r-list-sep').prev_all('.r-ent .title a')
        for topic in topics.items():
            title = topic.text()
            href = topic.attr('href')
            timestamp = re.search(r'(\d{10})', href).group(1)
            time = datetime.fromtimestamp(int(timestamp))
            print(title, href, time)
