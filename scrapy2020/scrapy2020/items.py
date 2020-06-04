# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapy2020Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Dulich24Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url =scrapy.Field()
    key = scrapy.Field()
    domain = scrapy.Field()
    category = scrapy.Field()
    data = scrapy.Field()
    meta = scrapy.Field()


class BazaarvietnamItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url =scrapy.Field()
    key = scrapy.Field()
    domain = scrapy.Field()
    category = scrapy.Field()
    data = scrapy.Field()
    meta = scrapy.Field()