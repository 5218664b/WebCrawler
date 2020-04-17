# -*- coding: utf-8 -*-
import scrapy
import json
import re
import sys
import requests
from pornhub_v2.items import PornhubV2Item
from scrapy_splash import SplashRequest

#   D:/ProgramData/Anaconda3/Scripts/activate.bat erdianqi
#   scrapy crawl pornv2 -o porn.json -s FEED_EXPORT_ENCODING=utf-8
class Pornv2Spider(scrapy.Spider):
    name = 'pornv2'
    start_urls = ['www.baidu.com']
    fileName = 'pornhub.links'
    searchKey = u'japan1'

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
                    'Cookie' : 'ua=5eaddbe64bb311a7ba788adfd9ffdfcb; bs=jps337ohz67g0q842m9vstklwrprryr9; ss=385066655867412139; RNLBSERVERID=ded6094; lang=en; platform_cookie_reset=pc; platform=pc; RNKEY=1170583*1420697:1654534310:2344856441:1',
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
                }
            )
            currentPageNum = currentPageNum + 1

    def parse_search_result(self,response):
        videoItems = response.xpath('//li[contains(@class, "pcVideoListItem  js-pop videoblock videoBox")]')

        for videoItem in videoItems:
            duration = videoItem.xpath('.//var[@class="duration"]/text()').extract()
            if int(str(duration[0]).split(':')[0]) < 40:
                continue
            link = videoItem.xpath('.//div[contains(@class, "img fade fadeUp")]/a')
            url = 'https://www.pornhub.com' + str(link.xpath('@href').extract()[0])

            lua_script= '''
            function main(splash, args)
                splash:go(splash.args.url)
                find_quality = {"quality_240p", "quality_480p", "quality_720p", "quality_1080p"}
                video_url = ""
                for i,v in ipairs(find_quality) do
                    local ok ,e = pcall(function() video_url = splash:evaljs(v) end)
                    if not ok then
                        break
                    end
                end
                title = splash:evaljs("document.title")
                return{
                out_title = title,
                out_video_url = video_url
                }
            end
            '''
            yield SplashRequest(
                url=url,
                endpoint="execute",
                args={
                    "wait": 1,
                    #lua脚本
                    "lua_source": lua_script,
                    #超时
                    'timeout': 120,
                    #不加载图片
                    'images': 0,
                    #资源超时
                    'resource_timeout': 1,
                    #本地v2ray fanqiang代理
                    'proxy' : 'socks5://192.168.99.1:10810'
                    },
                callback=self.parse_video_link,
            )

    def parse_video_link(self, response):
        print(response.data['out_video_url'])

        pornhubItem = PornhubV2Item()
        pornhubItem['url'] = response.url
        pornhubItem['title'] = response.data['out_title']
        pornhubItem['videoUrl'] = response.data['out_video_url']
        yield pornhubItem
        
        with open(self.fileName,'a') as f:
            f.write(pornhubItem['videoUrl']+ '\n')
