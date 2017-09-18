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

        :param: boards: comma-separated board list
        :param: since: start crawling from this date (format: YYYYMMDD)
        """
        self.boards = kwargs.pop('boards').strip().split(',')
        since = kwargs.pop('since', None)
        self.since = (
            datetime.strptime(since, '%Y%m%d').date()
            if since
            else datetime.now().date()
        )

    def start_requests(self):
        """Request handler."""
        for board in self.boards:
            url = f'https://www.ptt.cc/bbs/{board}/index.html'
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        """Parse DOM."""
        # exclude "置底文"
        item_css = '.r-ent .title a'
        if response.url.endswith('index.html'):
            topics = response.dom('.r-list-sep').prev_all(item_css)
        else:
            topics = response.dom(item_css)
        # reverse order to conform to timeline
        for topic in reversed(list(topics.items())):
            title = topic.text()
            href = topic.attr('href')
            timestamp = re.search(r'(\d{10})', href).group(1)
            time = datetime.fromtimestamp(int(timestamp))
            if time.date() < self.since:
                return
            print('+ ', title, href, time)
        prev_url = response.dom('.btn.wide:contains("上頁")').attr('href')
        yield scrapy.Request(prev_url, self.parse)
