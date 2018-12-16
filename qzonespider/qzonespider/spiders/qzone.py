# -*- coding: utf-8 -*-
import scrapy


class QzoneSpider(scrapy.Spider):
    name = 'qzone'
    allowed_domains = ['qzone.qq.com']
    start_urls = ['https://user.qzone.qq.com/1141802674']

    def parse(self, response):
        pass
