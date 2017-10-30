# -*- coding: utf-8 -*-
import scrapy


# Scrapy torrent item model
class Torrent(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    upload_date = scrapy.Field()
    size = scrapy.Field()
    seeders = scrapy.Field()
    leechers = scrapy.Field()
    uploader = scrapy.Field()
