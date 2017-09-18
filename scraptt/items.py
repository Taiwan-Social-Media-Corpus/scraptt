# -*- coding: utf-8 -*-
"""Scrapy scraped items."""
import scrapy


class PostItem(scrapy.Item):
    '''Item for "POST".'''
    author = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
