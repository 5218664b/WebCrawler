# -*- coding: utf-8 -*-
import scrapy


class SpidernameSpider(scrapy.Spider):
    name = 'spiderName'
    allowed_domains = ['domain.com']
    start_urls = ['http://domain.com/']

    def parse(self, response):
        pass
