# -*- coding: utf-8 -*-
import scrapy
import json
import re
import sys
import requests
from px.items import PxItem
from scrapy.conf import settings 

class PxsSpider(scrapy.Spider):
    if sys.version_info.major < 3:
        reload(sys)
        sys.setdefaultencoding('utf-8')

    name = 'pxs'
    allowed_domains = ['500px.com']
    #start_urls = ['https://500px.com/']
    cookie = settings['COOKIE']
    imgName = ''
    Gindex = 0
    def start_requests(self):
        pageCount = 100 + 11 + 1
        global url
        pageNum = 11
        searchKey = 'woman'
        while pageNum < pageCount:
            url = 'https://api.500px.com/v1/photos/search?type=photos&term=' +  searchKey + '&image_size%5B%5D=1&image_size%5B%5D=2&image_size%5B%5D=32&image_size%5B%5D=31&image_size%5B%5D=33&image_size%5B%5D=34&image_size%5B%5D=35&image_size%5B%5D=36&image_size%5B%5D=2048&image_size%5B%5D=4&image_size%5B%5D=14&include_states=true&formats=jpeg%2Clytro&include_tags=true&exclude_nude=true&rpp=50&page=' + str(pageNum)
            yield scrapy.Request(
                url, 
                method='OPTIONS',
                headers={
                    'Host' : 'api.500px.com',
                    'Connection' : 'keep-alive',
                    'Access-Control-Request-Method': 'GET',
                    'Origin' : 'https://500px.com',
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
                    'Access-Control-Request-Headers': 'x-csrf-token',
                    'Access-Control-Request-Method': 'GET',
                    'Accept-Encoding' : 'gzip, deflate, br',
                    'Accept': '*/*',
                    'Accept-Language' : 'zh-CN,zh;q=0.9,en;q=0.8'
                },
                callback=self.parse_auth,
                meta={'url':url}
            )
            pageNum=pageNum+1
    def parse_auth(self, response):
        yield scrapy.Request(
            response.meta['url'], 
            method='GET',
            headers={
                'Host' : 'api.500px.com',
                'Connection' : 'keep-alive',
                'Accept' : 'application/json, text/javascript, */*; q=0.01',
                'Origin' : 'https://500px.com',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
                'Referer' : 'https://500px.com/editors',
                'X-CSRF-Token' : '6tx8YGX7TPSYe/WLJ38xYw7fv3yG6S9ALFIksj3oe5Ipe/kcvYEWpzWwQUU/FQ/steg0oDgVRjQxcTMyALfx/w==',
                'Accept-Encoding' : 'gzip, deflate, br',
                'Accept-Language' : 'zh-CN,zh;q=0.9,en;q=0.8'
            },
            cookies=self.cookie,
            callback=self.parse_moment
        )
    #使用open存储图片，很慢
    def parse_moment_bak(self, response):
        json_body = json.loads(str(response.text))
        items = PxItem()
        photos = json_body['photos']
        i = 0
        for photo in photos:
            self.imgName = str(i) + photo['user']['fullname'] + '.jpg'
            i = i + 1
            imgUrls=photo['image_url']

            items['imgName'] = self.imgName
            items['imgUrl'] = imgUrls[len(imgUrls)-2]
            yield items
            #存储抓到的图片到本地
            with open('D:/pachong/px/500px抓取/' + self.imgName, 'wb') as f:
                req = requests.get(items['imgUrl'], verify=False)
                f.write(req.content)

    #使用scrapy的管道进行存储，比较快
    def parse_moment(self, response):
        json_body = json.loads(str(response.text))
        items = PxItem()
        photos = json_body['photos']
        imgUrl = []
        imgName = []
        for photo in photos:
            imgUrls=photo['image_url']
            imgName.append(str(self.Gindex) + photo['user']['fullname'] + '.jpg')
            imgUrl.append(imgUrls[len(imgUrls)-2])
            self.Gindex = self.Gindex + 1
        items['imgUrl'] = imgUrl
        items['imgName'] = imgName
        #存储json
        yield items
            