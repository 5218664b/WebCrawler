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
import json

#scrapy crawl comment -o comment.json -s FEED_EXPORT_ENCODING=utf-8
class CommentSpider(scrapy.Spider):
    def __init__(self, *args,  **kwargs):
        super(CommentSpider, self).__init__(**kwargs)
        self.cookieStr = args[0]['cookie']
        self.gtk = args[0]['gtk']

    name = 'comment'
    allowed_domains = ['qq.com']
    start_urls = ['https://user.qzone.qq.com/1141802674']

    #账号
    account = '1141802674'

    def parse(self, response):
        url = 'https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb\
?uin=%s&hostUin=%s&num=10&start=1&inCharset=utf-8&outCharset=utf-8&format=jsonp&g_tk=%s' % (self.account, self.account,self.gtk)
        yield scrapy.Request(
            url
            ,method='GET'
            ,callback=self.request_comment
            ,cookies=self.cookieStr
        )

    def request_comment(self, response):
        json_body = json.loads(str(response.text)[10:-2])['data']
        comment_total = int(json_body['total'])
        for index in range(comment_total/10+1):
            url = 'https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb\
?uin=%s&hostUin=%s&num=10&start=%s&inCharset=utf-8&outCharset=utf-8&format=jsonp&g_tk=%s' % (self.account, self.account, index*10, self.gtk)
            yield scrapy.Request(
                url
                ,method='GET'
                ,callback=self.parse_comment
                ,cookies=self.cookieStr
            )

    def parse_comment(self, response):
        json_body = json.loads(str(response.text)[10:-2])['data']
        for commentOne in json_body['commentList']:
            commentItems = QzonespiderItem()
            comment = {}
            comment['id'] = commentOne['id']
            comment['pubtime'] = commentOne['pubtime']
            comment['uin'] = commentOne['uin']
            comment['nickname'] = commentOne['nickname']
            comment['htmlContent'] = commentOne['htmlContent']
            comment['ubbContent'] = commentOne['ubbContent']
            comment['replyList'] = commentOne['replyList']

            commentItems['comment'] = comment
            yield commentItems