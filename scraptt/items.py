# -*- coding: utf-8 -*-
"""Scrapy scraped items."""
import scrapy


class PostItem(scrapy.Item):
    """Item for "POST"."""

    id = scrapy.Field()
    board = scrapy.Field()
    author = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    ip = scrapy.Field()
    quote = scrapy.Field()
    comments = scrapy.Field()
    count = scrapy.Field()


class MetaItem(scrapy.Item):
    """Item for "META"."""

    name = scrapy.Field()
