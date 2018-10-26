# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from movieHeaven_v2.items import MovieheavenV2Item
import sys
import os

class MovieSpider(CrawlSpider):
    if sys.version_info.major < 3:
        reload(sys)
        sys.setdefaultencoding('utf-8')
    name = 'movie'
    allowed_domains = [
                        'dytt8.net',
                        'ygdy8.com',    
                    ]
    start_urls = [
                    'http://www.dytt8.net/html/gndy/dyzz/list_23_1.html',
                    'http://www.dytt8.net/html/gndy/jddy/20160320/50523.html'
                ]
    rules = [
        Rule(LinkExtractor(allow=('/html/gndy/dyzz/[0-9]+/[0-9]+.html','list_[0-9]+_[0-9]+.html',)), callback='parse_dyzz', follow=True),
        Rule(LinkExtractor(allow=['http://www.ygdy8.com/html/gndy/(jddy|dyzz)/[0-9]+/[0-9]+.html']),callback='parse_jddy',follow=True)
    ]
    filePath = os.path.abspath('.') + '/movie.Links'

    def parse_dyzz(self, response):
        title = response.xpath('//title/text()').extract()[0]
        if title.find('您的访问出错了') == -1 and title.find('免费电影') == -1:
            movieItem = MovieheavenV2Item()
            movieItem['moviePageUrl'] = response.url
            movieItem['movieName'] = response.xpath('//div[@class="title_all"]/h1/font/text()').extract()

            #magnet磁力链存储
            magnetLinks = response.xpath('//p/a/@href').extract()
            for magnetLink in magnetLinks:
                if len(magnetLink) > 8 :
                    if magnetLink[0:6] == 'ftp://' or magnetLink[0:8] == 'magnet:?':
                        movieItem['movieLink'] = magnetLink.replace('<br />','')
                        with open(self.filePath,'a') as f:
                            f.write(movieItem['movieLink'] + '\n')
                        return movieItem

            #ftp地址,有可能多个，取一个
            ftpLinks = response.xpath('//table/tbody/tr/td//a/@href').extract()
            for ftpLink in ftpLinks:
                if len(ftpLink) > 8:
                    if ftpLink[0:6] == 'ftp://' or ftpLink[0:8] == 'magnet:?':
                        movieItem['movieLink'] = ftpLink.replace('<br />','')
                        with open(self.filePath,'a') as f:   
                            f.write(movieItem['movieLink'] + '\n')
                        return movieItem
        else:
            pass

    def parse_jddy(self, response):
        title = response.xpath('//title/text()').extract()[0]
        if title.find('您的访问出错了') == -1 and title.find('免费电影') == -1:
            movieItem = MovieheavenV2Item()
            movieItem['moviePageUrl'] = response.url
            movieItem['movieName'] = response.xpath('//div[@class="title_all"]/h1/font/text()').extract()
            movieItem['movieLink'] = response.xpath('//table/tbody/tr/td//a/@href').extract()
            return movieItem