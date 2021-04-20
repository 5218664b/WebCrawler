# -*- coding: utf-8 -*-
import scrapy
#from scrapy_splash import SplashRequest
from taobao.items import TaobaoItem

# scrapy crawl taobao -o taobao.json -s FEED_EXPORT_ENCODING=utf-8
class TaobaospiderSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['taobao.com']
    start_urls = ['https://login.taobao.com/member/login.jhtml']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(0, self.settings.get('MAX_PAGE')):
                url = 'https://s.taobao.com/search?q=' + keyword + '&s=' + str(page * 44)
                yield scrapy.Request(url=url, callback=self.parse1)

    def parse1(self, response):
        taobaoitem = TaobaoItem()
        item = response.xpath('//*[@class="items"]').extract()
        for one_item in item:
            taobaoitem['img_link'] = one_item.xpath('.///div[@class="pic"]/a/img/@src').extract()
            taobaoitem['title'] = one_item.xpath('.///div[@class="row row-2 title"]/a/text()').extract()
            yield taobaoitem