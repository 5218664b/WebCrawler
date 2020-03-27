# -*- coding: utf-8 -*-
import scrapy
import json
import re
import sys
import requests
from pornhub.items import PornhubItem

'''
python 2.7
pip install --user PyQt4-4.11.4-cp27-cp27m-win_amd64.whl
pip install Ghost.py
'''

#    scrapy crawl porn -o porn.json -s FEED_EXPORT_ENCODING=utf-8 
class PornSpider(scrapy.Spider):
    def __init__(self):
        self.webkit_session = None

    name = 'porn'
    start_urls = ['www.baidu.com']
    fileName = 'pornhub.links'
    searchKey = 'japanese'

    def start_requests(self):
        currentPageNum = 1
        endPageNum = 2
        while currentPageNum < endPageNum:
            url = 'https://www.pornhub.com/video/search?search=' + self.searchKey + '&page=' + str(currentPageNum)
            #url = 'https://jp.pornhub.com/video'
            yield scrapy.Request(
                url,
                callback=self.parse_search_result,
                headers={
                    'Cookie' : 'ua=5eaddbe64bb311a7ba788adfd9ffdfcb; bs=jps337ohz67g0q842m9vstklwrprryr9; ss=385066655867412139; RNLBSERVERID=ded6094; platform_cookie_reset=pc; platform=pc; RNKEY=1587959*1617373:4268689879:419590820:1; lang=en',
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
                }
            )
            currentPageNum = currentPageNum + 1

    def parse_search_result(self,response):
        links = response.xpath('//div[@class="img fade fadeUp videoPreviewBg"]/a')
        pornhubItem = PornhubItem()
        
        for link in links:
            pornhubItem['title'] = link.xpath('@title').extract()
            pornhubItem['url'] = link.xpath('@href').extract()
            yield pornhubItem

            url = 'https://www.pornhub.com' + str(link.xpath('@href').extract())[3:-2]
            yield scrapy.Request(
                url,
                callback=self.parse_video_link
            )
    
    def parse_video_link(self, response):
        pornhubItem = PornhubItem()
        
        quality_240p  = self.webkit_session.evaluate('quality_240p')
        quality_480p  = self.webkit_session.evaluate('quality_480p')
        quality_720p  = self.webkit_session.evaluate('quality_720p')
        quality_1080p  = self.webkit_session.evaluate('quality_1080p')
        
        if quality_1080p[0] != None:
            pornhubItem['videoUrl'] = str(quality_1080p[0])
        elif quality_720p[0] != None:
            pornhubItem['videoUrl'] = str(quality_720p[0])
        elif quality_480p[0] != None:
            pornhubItem['videoUrl'] = str(quality_480p[0])
        else:
            pornhubItem['videoUrl'] = str(quality_240p[0])
        yield pornhubItem
        
        with open(self.fileName,'a') as f:
            f.write(pornhubItem['videoUrl']+ '\n')