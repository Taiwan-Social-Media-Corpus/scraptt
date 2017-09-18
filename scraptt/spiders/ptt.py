# -*- coding: utf-8 -*-
"""Main crawler."""
import re
from datetime import datetime
from itertools import groupby

import scrapy
import dateutil.parser as dp

from .parsers.post import mod_content, extract_author
from .parsers.comment import comment_counter, remove_ip


class PttSpider(scrapy.Spider):
    """Crawler for PTT."""

    name = 'ptt'
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
            yield scrapy.Request(url, self.parse_index)

    def parse_index(self, response):
        """Parse index pages."""
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
            yield scrapy.Request(href, self.parse_post)
        prev_url = response.dom('.btn.wide:contains("上頁")').attr('href')
        yield scrapy.Request(prev_url, self.parse_index)

    def parse_post(self, response):
        """Parse PTT post (PO文)."""
        content = (
            response.dom('#main-content')
            .clone()
            .children()
            .remove('span[class^="article-meta-"]')
            .remove('div.push')
            .end()
            .html()
        )
        meta = dict(
            (_.text(), _.next().text())
            for _
            in response.dom('.article-meta-tag').items()
        )
        ref = {
            '作者': 'author',
            '時間': 'published',
            '標題': 'title',
            '看板': 'board',
            '站內': 'board'
        }
        post = dict()
        post['content'] = mod_content(content)
        post['url'] = response.url
        meta_mod = dict()
        for k in meta.keys():
            if k in ref:
                meta_mod[ref[k]] = meta[k]
            else:
                raise Exception(f'Unknown key: {k}')
        comments = []
        for _ in response.dom('.push').items():
            comment = {
                'type': _('.push-tag').text(),
                'author': extract_author(_('.push-userid').text()),
                'content': _('.push-content').text().lstrip(' :'),
                'time': {
                    'published': _('.push-ipdatetime').text(),
                    'crawled': datetime.now().replace(microsecond=0),
                }
            }
            comments.append(comment)

        post.update(meta_mod)
        post['author'] = extract_author(post['author'])
        post['time'] = {
            'published': dp.parse(post.pop('published'))
        }
        post['comments'] = comments

        # Merge comments with consecutive comments with the same author.
        con = []
        for author, group in groupby(comments, key=lambda x: x['author']):
            d = {}
            for comment in group:
                if d:
                    d['content'] += comment['content']
                else:
                    d = comment
            con.append(d)

        # add YEAR to comments
        year = post['time']['published'].year
        latest_month = post['time']['published'].month
        for comment in comments:
            published = dp.parse(remove_ip(comment['time']['published']))
            if published.month < latest_month:
                year += 1
            comment['time']['published'] = published.replace(year=year)
            latest_month = published.month

        # quotes
        msg = post['content']
        qs = re.findall('※ 引述.*|\n: .*', msg)
        for q in qs:
            msg = msg.replace(q, '')
        qs = '\n'.join([i.strip('\n') for i in qs])
        post['content'] = msg.strip('\n ')
        if qs:
            post['quote'] = qs
        post['time']['crawled'] = datetime.now().replace(microsecond=0)

        # 推噓文數量
        post.update(
            {'count': comment_counter(post['comments'])}
        )
        print('-------------')
        import json
        print(
            json.dumps(
                post, indent=4, ensure_ascii=False, default=lambda x: str(x)
            )
        )
        print('-------------')
