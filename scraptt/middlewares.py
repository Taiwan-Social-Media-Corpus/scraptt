# -*- coding: utf-8 -*-
"""Middlewares."""
from pyquery import PyQuery


class PyqueryMiddleware:
    """Inject pyquery object into Scrapy `response`."""

    def process_response(self, request, response, spider):  # noqa
        response.dom = PyQuery(response.text).make_links_absolute(
                'https://www.ptt.cc/bbs/')
        return response
