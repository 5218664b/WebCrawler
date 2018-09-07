# -*- coding: utf-8 -*-
import scrapy

#scrapy crawl spiderName -o spiderName.json -s FEED_EXPORT_ENCODING=utf-8 
class SpidernameSpider(scrapy.Spider):
    name = 'spiderName'
    allowed_domains = ['domain.com']
    start_urls = ['http://domain.com/']

    def parse(self, response):
        pass
