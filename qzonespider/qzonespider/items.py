# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QzonespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mood = scrapy.Field()
    mood_tid = scrapy.Field()
    mood_content = scrapy.Field()
    mood_source_name = scrapy.Field()
    mood_created_time = scrapy.Field()
    mood_pics = scrapy.Field()
    mood_like = scrapy.Field()

    article = scrapy.Field()
    photo_album = scrapy.Field()
    comment = scrapy.Field()

    other = scrapy.Field()
    friends = scrapy.Field()
