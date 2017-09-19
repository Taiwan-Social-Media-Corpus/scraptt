# -*- coding: utf-8 -*-
"""Scrapy pipeilnes."""
import sqlite3
import logging

DB_PATH = '/usr/local/var/ptt.db'

logger = logging.getLogger(__name__)


class PTTPipeline:
    """PTT pipeline."""

    def open_spider(self, spider):
        """Build database connection."""
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()
        # create table for "POST"
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS post
            (
                id TEXT PRIMARY KEY,
                board TEXT,
                author TEXT,
                publisehd DATETIME,
                crawled DATETIME,
                title TEXT,
                url TEXT,
                content TEXT
            )
        ''')
        # create table for "COMMENT"
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS comment
            (
                post_id TEXT,
                type TEXT,
                author TEXT,
                publisehd DATETIME,
                crawled DATETIME,
                content TEXT,
                FOREIGN KEY (post_id) REFERENCES post(id)
            )
        ''')
        self.connection.commit()
        logger.debug('DB connected.')

    def close_spider(self, spider):
        """Close database connectoin."""
        self.connection.close()
        logger.debug('DB disconnected.')

    def process_item(self, item, spider):
        """Insert data into database."""
        self.cursor.execute(f'''
            INSERT OR IGNORE INTO post
            (id, board, author, publisehd, crawled, title, url, content)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
                item['id'], item['board'], item['author'],
                item['time']['published'], item['time']['published'],
                item['title'], item['url'], item['content']
            )
        )
        for comment in item['comments']:
            self.cursor.execute(f'''
                INSERT OR IGNORE INTO comment
                (post_id, type, author, publisehd, crawled, content)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                item['id'], comment['type'], comment['author'],
                comment['time']['published'], comment['time']['published'],
                comment['content']
                )
            )
        self.connection.commit()
        logger.debug('commited')
        return item


class MetaPipeline:
    """Meta pipeline."""

    def open_spider(self, spider):
        """Build database connection."""
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()
        # create table for "meta"
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS meta
            (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                translate TEXT
            )
        ''')
        self.connection.commit()
        logger.debug('DB connected.')

    def close_spider(self, spider):
        """Close database connectoin."""
        self.connection.close()
        logger.debug('DB disconnected.')

    def process_item(self, item, spider):
        """Insert data into database."""
        self.cursor.execute(f'''
            INSERT OR IGNORE INTO meta
            (name)
            VALUES (?)
        ''', (item['name'], )
        )
        self.connection.commit()
        logger.debug('commited')
        return item
