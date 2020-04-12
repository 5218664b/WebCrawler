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

#   D:/ProgramData/Anaconda3/Scripts/activate.bat erdianqi
#   scrapy crawl porn -o porn.json -s FEED_EXPORT_ENCODING=utf-8
class PornSpider(scrapy.Spider):
    def __init__(self):
        self.webkit_session = None

    name = 'porn'
    start_urls = ['www.baidu.com']
    fileName = 'pornhub.links'
    searchKey = 'japanese'

    def start_requests(self):
        currentPageNum = 1
        endPageNum = 1
        while currentPageNum <= endPageNum:
            url = 'https://www.pornhub.com/video/search?search=' + self.searchKey + '&page=' + str(currentPageNum)
            #url = 'https://jp.pornhub.com/video'
            yield scrapy.Request(
                url,
                callback=self.parse_search_result,
                headers={
                    'Cookie' : 'bs=p6za8azsjwg9ijyn970f8vgx3ehieuc4; ss=430400793297104506; ua=db71e63d841d64be86149f315e465d5f; platform_cookie_reset=pc; platform=pc; RNKEY=1447123*1687583:3567443335:1032885732:1; RNLBSERVERID=ded6942',
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
                }
            )
            currentPageNum = currentPageNum + 1

    def parse_search_result(self,response):
        links = response.xpath('//div[@class="img fade fadeUp videoPreviewBg"]/a')
        for link in links:
            url = 'https://www.pornhub.com' + str(link.xpath('@href').extract())[3:-2]
            yield scrapy.Request(
                url,
                callback=self.parse_video_link
            )

    def parse_video_link(self, response):
        find_quality = ['quality_1080p', 'quality_720p', 'quality_480p', 'quality_240p']
        for quality in find_quality:
            video_url = self.webkit_session.evaluate(quality)
            if video_url[0] is not None:
                break

        pornhubItem = PornhubItem()
        pornhubItem['url'] = response.url
        pornhubItem['title'] = response.xpath('@title').extract()
        pornhubItem['videoUrl'] = str(video_url[0])
        yield pornhubItem
        
        with open(self.fileName,'a') as f:
            f.write(pornhubItem['videoUrl']+ '\n')