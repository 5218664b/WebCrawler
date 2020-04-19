# -*- coding: utf-8 -*-
import scrapy
import json
import re
import sys
import requests
from pornhub_v2.items import PornhubV2Item
from scrapy_splash import SplashRequest
import sys
import os
sys.path.append(os.path.abspath('../../someTools'))
from mongo.mongo import MongoTools

#   D:/ProgramData/Anaconda3/Scripts/activate.bat erdianqi
#   scrapy crawl pornv2 -o porn.json -s FEED_EXPORT_ENCODING=utf-8
class Pornv2Spider(scrapy.Spider):
    def __init__(self):
        self.mt = MongoTools()

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
            #url = 'https://www.pornhub.com/playlist/39181931'

            lua_script= '''
            function main(splash, args)
                splash:go(splash.args.url)
                splash:wait(1)
                splash:runjs([[
                    test = function()
                    {
                        if(typeof(itemsCount) == 'undefined')
                            return 1;
                        var u = $j('#videoPlaylist');
                        if (u.hasClass('stopLazyload'))
                            return 1;
                        var t = $j('li.videoBox', u).length;
                        if (t >= (itemsCount-10))
                            return 1;
                        var a = window.pageYOffset
                        , i = (window.innerHeight || document.documentElement.clientHeight) + a
                        , l = document.querySelectorAll('#videoPlaylist li')
                        , o = l[l.length - 1];
                        window.scrollTo(0, o.offsetTop+300);
                        return o.offsetTop;
                    }
                ]])
                local i = 0
                while(true) do
                    local tmp = splash:evaljs("test()")
                    if(tmp==1 or i==80) then
                        splash:wait(1)
                        break
                    end
                    splash:wait(1)
                    i = i + 1
                end
                return splash:html()
            end
            '''

            yield SplashRequest(
                url,
                endpoint='execute',
                callback=self.parse_search_result,
                args={
                    "wait": 1,
                    #lua脚本
                    "lua_source": lua_script,
                    #超时
                    'timeout': 250,
                    #不加载图片
                    'images': 0,
                    #资源超时
                    'resource_timeout': 1,
                    #本地v2ray fanqiang代理
                    'proxy' : 'socks5://192.168.99.1:10810'
                }
            )
            currentPageNum = currentPageNum + 1

    def parse_search_result(self,response):
        videoItems = response.xpath('//li[contains(@class, "pcVideoListItem  js-pop videoblock videoBox")]')

        for videoItem in videoItems:
            duration = int(str(videoItem.xpath('.//var[@class="duration"]/text()').extract()[0]).split(':')[0])
            link = str(videoItem.xpath('.//div[contains(@class, "img fade")]/a').xpath('@href').extract()[0])
            title = videoItem.xpath('.//span[@class="title"]/a').xpath('@title').extract()[0]
            if list(self.mt.find('duration_less_link', {'link':'https://www.pornhub.com' + link})) != [] or list(self.mt.find('used_link', {'link':'https://www.pornhub.com' + link})) != []:
                print(u'链接已经爬过了')
                break

            if duration < 40:
                #写入时间不足的链接
                tmp = {'link': 'https://www.pornhub.com' + link, 'title' : title}
                self.mt.insert_one('duration_less_link', tmp)          
                continue
            
            url = 'https://www.pornhub.com' + link

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
                    'timeout': 240,
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
        if response.data['out_video_url'] != "" :
            #写入已爬链接
            tmp = {'link': response.url, 'title' : response.data['out_title']}
            self.mt.insert_one('used_link', tmp) 

            pornhubItem = PornhubV2Item()
            pornhubItem['url'] = response.url
            pornhubItem['title'] = response.data['out_title']
            pornhubItem['videoUrl'] = response.data['out_video_url']
            yield pornhubItem
            
            with open(self.fileName,'a') as f:
                f.write(pornhubItem['videoUrl']+ '\n')
