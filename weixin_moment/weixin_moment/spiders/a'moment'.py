# -*- coding: utf-8 -*-
import scrapy
import json
import re
import sys
from weixin_moment.items import WeixinMomentItem

class AmomentSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = 'moment'
    allowed_domains = ['chushu.la']
    #start_urls = ['http://chushu.la/']
    
    bookid = '728395594'
    start_urls = ['http://chushu.la/api/book/chushula-728395594?isAjax=1']

    def start_request(self):
        #url = 'http://chushu.la/api/book/chushula-{0}?isAjax=1'.format(self.bookid)
        url = ''
        yield scrapy.Request(
            url,
            headers={
                #'Referer' : 'https://chushu.la/book/chushula-728395594',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
            },
            callback= self.parse)
    def parse(self, response):
        json_body = json.loads(str(response.text))
        catalogs = json_body['book']['catalogs']
        url = 'http://chushu.la/api/book/wx/chushula-{0}/pages?isAjax=1'.format(self.bookid)
        start_page = int(catalogs[0]['month'])
        for catalog in catalogs:
            year = catalog['year']
            month = catalog['month']
            formdata = {
                "type" : 'year_month',
                "year" : str(year),
                "month" : str(month),
                "index" : str(start_page),
                "value" : 'v_{0}{1}'.format(year, month)
            }
            start_page += 1
            yield scrapy.FormRequest(
                url, 
                method='POST',
                body=json.dumps(formdata),
                headers={
                    'Host' : 'chushu.la',
                    'Connection' : 'keep-alive',
                    'Accept' : 'application/json, text/javascript, */*; q=0.01',
                    'Origin' : 'https://chushu.la',
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
                    'Content-Type' : 'application/json',
                    'Referer' : 'https://chushu.la/book/chushula-728395594',
                    'Accept-Encoding' : 'gzip, deflate, br',
                    'Accept-Language' : 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Cookie' : 'bookId=chushula-728395594; Hm_lvt_a64b0c58cf35c32b2f7fd256b188b238=1529115220; JSESSIONID=A602405E2D0B7DBB5D204030492FB7AB; _token=36e70b8441cc2c203c40cac5c0889f05; Hm_lpvt_a64b0c58cf35c32b2f7fd256b188b238=1529121815'
                },
                callback=self.parse_moment
            )
    def parse_moment(self, response):
        json_body = json.loads(response.text)
        pages = json_body['pages']
        pattern = re.compile(u"[\u4e00-\u9fa5]+")   #匹配中文
        items = WeixinMomentItem()
        for page in pages :
            if (page['type'] == "weixin_moment_page"):    #仅抓取朋友圈分页数据
                paras = page['data']['paras']
                if paras:
                    moment = ''
                    for content in paras[0]['rows']:
                        result = re.findall(pattern, content['data'])   #使用正则匹配所有中文朋友圈内容
                        moment += ''.join(result)
                imgs = page['data']['imgs']
                if imgs:
                    img = ''
                    for imgUrl in imgs:
                        img += ',' + imgUrl['src']
                items['moment'] = moment
                items['date'] = page['data']['dateText'] #获取时间
                items['imgUrl'] = img.lstrip(',')
                yield items