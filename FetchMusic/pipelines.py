# myproject/pipelines.py

import os
import sqlite3
import requests
from scrapy.pipelines.files import FilesPipeline

class DownloadFilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        # Custom file path for the downloaded files
        return f'downloads/{item["name"]}.mp3'

    def item_completed(self, results, item, info):
        for ok, result in results:
            if ok:
                item['file_path'] = result['path']
        return item

class SQLitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('music.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                song_no TEXT,
                name TEXT,
                artist TEXT,
                duration TEXT,
                download_link TEXT,
                file_path TEXT
            )
        ''')
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT INTO songs (song_no, name, artist, duration, download_link, file_path) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            item.get('song_no'),
            item.get('name'),
            item.get('artist'),
            item.get('duration'),
            item.get('Download_link'),
            item.get('file_path')
        ))
        self.connection.commit()
        return item
