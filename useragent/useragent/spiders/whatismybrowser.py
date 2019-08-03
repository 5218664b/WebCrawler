# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link
from useragent.items import UseragentItem
import re

#scrapy crawl whatismybrowser -o whatismybrowser.json -s FEED_EXPORT_ENCODING=utf-8
class WhatismybrowserSpider(CrawlSpider):
    name = 'whatismybrowser'
    allowed_domains = ['whatismybrowser.com']
    start_urls = ['https://developers.whatismybrowser.com/useragents/explore/']

    rules = [Rule(LinkExtractor(allow=('/useragents/explore/.+/.+/')),callback='parse_type', follow=False)]

    def parse_type(self, response):
        maxPage = response.xpath('//div[@id="pagination"]/a[last()]/@href').extract()[0].rsplit('/',1)[1]
        for i in range(1,int(maxPage)):
            link = response.urljoin(str(i)) 
            yield scrapy.Request(
                link
                ,method='GET'
                ,callback=self.parse_useragent
            )            

    def parse_useragent(self, response):
        linkEx = LinkExtractor(restrict_xpaths='//td[@class="useragent"]/a')
        links = linkEx.extract_links(response)
        tmp = []
        for link in links:
            tmp.append(link.text)
        useragentItem = UseragentItem()
        useragentItem['useragent'] = tmp
        yield useragentItem


