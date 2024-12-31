# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from pydantic import BaseModel
from typing import Annotated

class FetchmusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Album(scrapy.Item):
    name = scrapy.Field()
    artist = scrapy.Field()
    runtime = scrapy.Field()
    songs = scrapy.Field()

class Song(scrapy.Item):
    cover = scrapy.Field() 
    song_no = scrapy.Field()
    name  = scrapy.Field()
    artist= scrapy.Field()
    duration = scrapy.Field()
    Download_link = scrapy.Field()
    file_path = scrapy.Field()
