# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class sudaNewsItem(scrapy.Item):
    # define the fields for your item here like:
    newsTime = scrapy.Field()
    newsHref = scrapy.Field()
    newsTitle = scrapy.Field()
    newsDepartMent = scrapy.Field()


class sudaMainItem(scrapy.Item):
    father = scrapy.Field()
    url = scrapy.Field()
