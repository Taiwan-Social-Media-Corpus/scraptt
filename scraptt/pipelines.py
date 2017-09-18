# -*- coding: utf-8 -*-
"""Scrapy pipeilnes."""
import sqlite3
import logging

logger = logging.getLogger(__name__)


class PTTPipeline:
    """PTT pipeline."""

    table_name = '/tmp/ptt.db'

    def open_spider(self, spider):
        """Build database connection."""
        self.connection = sqlite3.connect(self.table_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ptt
            (id TEXT PRIMARY KEY, board TEXT, author TEXT, time DATETIME, title TEXT, url TEXT, content TEXT)
        ''')  # noqa
        logger.debug('DB connected.')

    def close_spider(self, spider):
        """Close database connectoin."""
        self.connection.commit()
        self.connection.close()
        logger.debug('DB disconnected.')

    def process_item(self, item, spider):
        """Insert data into database."""
        return item
