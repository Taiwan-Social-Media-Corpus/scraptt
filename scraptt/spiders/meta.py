# -*- coding: utf-8 -*-
"""Meta crawler."""

import scrapy

from ..items import MetaItem


class MetaSpider(scrapy.Spider):
    """Get all PTT boards."""

    name = 'meta'
    allowed_domains = ['ptt.cc']
    start_urls = ['https://www.ptt.cc/cls/1']
    custom_settings = {
        'ITEM_PIPELINES': {
            'cockroach.pipelines.MetaPipeline': 300
        }
    }

    def parse(self, response):
        """Parse DOM."""
        for _ in response.dom('.b-ent a').items():
            href = _.attr('href')
            flag = '/index.html'
            if href.endswith(flag):
                board_name = href.replace(flag, '').split('/')[-1]
                if board_name == 'ALLPOST':
                    # "ALLPOST" always return 404, so it's pointless to
                    # crawl this board.
                    return
                yield MetaItem(name=board_name)
            else:
                yield scrapy.Request(href, self.parse)
