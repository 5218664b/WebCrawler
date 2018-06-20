# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    imgName = scrapy.Field()
    imgUrl = scrapy.Field()
    image_paths = scrapy.Field()
