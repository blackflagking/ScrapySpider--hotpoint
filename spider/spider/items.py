# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bdname = scrapy.Field()
    bdurl = scrapy.Field()
    name360 = scrapy.Field()
    url360 = scrapy.Field()
    weiboname = scrapy.Field()
    weibourl = scrapy.Field()
