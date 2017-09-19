# -*- coding: utf-8 -*-
"""Meta crawler."""

import scrapy


class MetaSpider(scrapy.Spider):
    """Get all PTT boards."""

    name = 'meta'
    allowed_domains = ['ptt.cc']
    start_urls = ['https://www.ptt.cc/cls/1']

    def parse(self, response):
        """Parse DOM."""
        for _ in response.dom('.b-ent a').items():
            href = _.attr('href')
            flag = '/index.html'
            if href.endswith(flag):
                board_name = href.replace(flag, '').split('/')[-1]
                self.logger.info(board_name)
            else:
                yield scrapy.Request(href, self.parse)
