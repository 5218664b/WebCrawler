# -*- coding: utf-8 -*-
import scrapy
import json
import re
import sys
import requests
from pornhub.items import PornhubItem
from scrapy.conf import settings
from scrapy_splash import SplashRequest

class PornSpider(scrapy.Spider):
    if sys.version_info.major < 3:
        reload(sys)
        sys.setdefaultencoding('utf-8')

    name = 'porn'
    allowed_domains = ['pornhub.com']
    start_urls = ['www.baidu.com']
    fileName = 'pornhub.links'

    def start_requests(self):
        currentPageNum = 1
        endPageNum = 5
        while currentPageNum < endPageNum:
            url = 'https://www.pornhub.com/video/search?search=japan&page=' + str(currentPageNum)
            yield scrapy.Request(
                url,
                callback=self.parse_search_result,
                headers={
                    'Cookie' : 'FastPopSessionRequestNumber=11; FPSRN=5; ua=a54eb83090ed984332f4eca22d3ec5e4; platform=pc; bs=s1uhrhm327ql445dyccz9xdmdspt6i04; ss=181406473308429550; RNLBSERVERID=ded6696; FastPopSessionRequestNumber=9; FPSRN=4',
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
            #splash_args = {
            #'wait': '2',
            #}
            #yield SplashRequest(
            #    url,
            #    self.parse_video_link,
            #    endpoint='render.html',
            #    args=splash_args
            #)
            yield scrapy.Request(
                url,
                callback=self.parse_video_link
            )
    
    def parse_video_link(self, response):
        pornhubItem = PornhubItem()
        #pornhubItem['videoUrl'] = response.xpath('//source/@src').extract()
        scriptStr = str(response.xpath('//div[@id="player"]/script').extract())
        find720Str = '"quality":"720","videoUrl":"'
        find480Str = '"quality":"480","videoUrl":"'
        find240Str = '"quality":"240","videoUrl":"'

        ret720 = scriptStr.find(find720Str)
        ret480 = scriptStr.find(find480Str)
        ret240 = scriptStr.find(find240Str)

        if ret720 > 0:
            startIndex = ret720 + len(find720Str)
            endIndex = scriptStr.find('"',startIndex)
        elif ret480 > 0:
            startIndex = ret480 + len(find480Str)
            endIndex = scriptStr.find('"',startIndex)
        elif ret240 > 0:
            startIndex = ret240 + len(find240Str)
            endIndex = scriptStr.find('"',startIndex)
        else:
            return

        pornhubItem['videoUrl'] = scriptStr[startIndex:endIndex]
        yield pornhubItem
        with open(self.fileName,'a') as f:
            f.write(scriptStr[startIndex:endIndex].replace('\\','') + '\n')