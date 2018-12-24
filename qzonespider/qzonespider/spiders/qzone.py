# -*- coding: utf-8 -*-
import scrapy
import os
import json
import re
import sys
import requests
from qzonespider.items import QzonespiderItem
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from public_method import QzoneMessage
from public_method import qqMessage
import json

#scrapy crawl qzone -o qzone.json -s FEED_EXPORT_ENCODING=utf-8
class QzoneSpider(scrapy.Spider):
    if sys.version_info.major < 3:
        reload(sys)
        sys.setdefaultencoding('utf-8')

    name = 'qzone'
    allowed_domains = ['qq.com']
    start_urls = ['https://user.qzone.qq.com/1141802674']

    #账号
    account = ''
    #密码
    password = ''
    qm = QzoneMessage()
    #获取cookie
    [cookies, cookieStr] = qm.getCookie(account, password)
    gtk = qm.getGTK(cookies)

    def parse(self, response):
        url = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=%s&pos=%d&num=20&g_tk=%s' % (self.account, 0, self.gtk)
        yield scrapy.Request(
            url
            ,method='GET'
            ,cookies=self.cookieStr
            ,callback=self.request_mood
            #,meta={}
        )
            
    def request_mood(self, response):
        #print str(response.text)[11:-2]
        json_body = json.loads(str(response.text)[10:-2])
        print json_body['total']
        page = 1
        totalPage = int(json_body['total']) / 20 + 1
        while page < totalPage:
            url = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=%s&pos=%d&num=20&g_tk=%s' % (self.account, (page - 1) * 20, self.gtk)
            yield scrapy.Request(
                url
                ,method='GET'
                ,headers={}
                ,cookies=self.cookieStr
                ,meta={}
                ,callback=self.parse_mood
            )
            page = page + 1

    def parse_mood(self, response):
        json_body = json.loads(str(response.text)[10:-2])
        for msg in json_body['msglist']:
            qzItems = QzonespiderItem()
            qzItems['mood_content'] = msg['content']
            qzItems['mood_source_name'] = msg['source_name']
            qzItems['mood_created_time'] = msg['created_time']
            tid = msg['tid']
            qzItems['mood_tid'] = tid
            if msg.has_key('pic'):
                mood_pics = []
                for pic in msg['pic']:
                    mood_pics.append(pic['url3'])
                    match = re.compile("http://user\.qzone\.qq\.com/[0-9]+/photo/(.*)/(.*)\^\|\|\^0$")
                    result = re.search(match, pic['curlikekey'])
                    if result != None:
                        unilikekey1 = result.group(1)
                        unilikekey2 = result.group(2)
                        url = 'https://user.qzone.qq.com/proxy/domain/plist.photo.qq.com/fcgi-bin/cgi_floatview_photo_list_v2\
?g_tk=%s\
&topicId=%s_%s_1\
&picKey=%s%%2C%s%%2C%s%%2C%s\
&cmtNum=10\
&inCharset=utf-8\
&outCharset=utf-8\
&uin=%s\
&appid=311\
&hostUin=%s' % (self.gtk, self.account ,tid, tid, self.account, unilikekey1, unilikekey2, self.account, self.account)

                        yield scrapy.Request(
                            url
                            ,method='GET'
                            ,cookies=self.cookieStr
                            ,meta={'tid':tid}
                            ,callback=self.parse_like
                        )
                    qzItems['mood_pics'] = ','.join(mood_pics)
            yield qzItems

    def parse_like(self,response):
        json_body = json.loads(str(response.text)[10:-2])
        tid = response.meta['tid']
        tmp = []
        if json_body.has_key('data'):
            for like in json_body['data']['photos'][0]['likeList']:
                likeList = {}
                likeList['nick'] = like['nick']
                likeList['uin'] = like['uin']
                tmp.append(likeList)
            qzItems = QzonespiderItem()
            qzItems['mood_tid'] = tid
            qzItems['mood_like'] = tmp
            yield qzItems

