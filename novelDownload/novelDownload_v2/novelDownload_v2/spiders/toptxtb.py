# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from novelDownload_v2.items import NoveldownloadV2Item
import sys
import os
import re
from chardet import detect

# scrapy crawl toptxtb -o toptxtb.json -s FEED_EXPORT_ENCODING=utf-8
class ToptxtbSpider(CrawlSpider):
    if sys.version_info.major < 3:
        reload(sys)
        sys.setdefaultencoding('utf-8')

    name = 'toptxtb'
    allowed_domains = [
        'toptxta.com',
        'toptxt.net',
        'toptxtb.net'
    ]

    fileName = ''
    urlDomain = 'http://www.toptxt.net'
    searchDomain = '/modules/article/search.php?'
    #搜索关键词之后在网页上获取到的，注意前面加个问号
    searchType = 'searchtype=articlename&'
    searchKey = 'searchkey=%B7%B2%C8%CB&action=login&submit=%26%23160%3B%CB%D1%26%23160%3B%26%23160%3B%CB%F7%26%23160%3B'
    #下载路径，需要修改为自己电脑的路径
    downloadPath = os.path.abspath('.') + '/download/'
    start_urls = [
        urlDomain + searchDomain + searchType + searchKey
        #,'https://www.toptxta.com/toptxt/76/76898/'
    ]

    rules = [
        Rule(LinkExtractor(allow=['https://www.toptxta.com/toptxt/[0-9]+/[0-9]+/', searchDomain + searchKey + '&page=[0-9]+']), callback='parse_novel', follow=True, process_links='links_handle'),
        Rule(LinkExtractor(allow=['https://www.toptxta.com/booktxt/[0-9]+.shtml']),callback='parse_novel',follow=False, process_links='links_handle')
    ]

    novelCount = 0
    needCount = 20

    # 限制抓取总数
    def links_handle(self, links):
        if self.novelCount > self.needCount:
            return []
        for link in links:
            url = link.url
            if re.search('page', url) == None:
                self.novelCount = self.novelCount + 1
        return links

    def parse_novel(self, response):
        novelNameList = response.xpath('//*[@id="wp"]/div/div[2]/h1/text()').extract()
        if len(novelNameList) != 0:
            novelItems = NoveldownloadV2Item()
            novelItems['novelName'] = novelNameList[0]
            yield novelItems

            #获取第一章的pagenum
            firstChaperUrl = response.xpath('//*[@id="wp"]/div/div[3]/div[1]/ul/li[1]/a/@href').extract()[0]
            
            fileName = self.downloadPath + novelItems['novelName'] + '.txt'
            with open(fileName, 'wb') as f:
                f.write(novelItems['novelName'])
            
            url = response.url + firstChaperUrl
            #请求第一章
            yield scrapy.Request(
            url,
            meta={'fileName' : fileName},
            callback=self.chapter_parse
            )
    
    def chapter_parse(self, response):
        chapterName = response.xpath('//*[@id="content"]/div[1]/h1/text()').extract()
        if len(chapterName) != 0:
            novelItems = NoveldownloadV2Item()
            novelItems['novelChapter'] = chapterName[0]
            novelItems['novelContent'] = response.xpath('//*[@id="novel_content"]/text()').extract()
            yield novelItems

            fileName = response.meta['fileName']
            nextChapterUrl = './'

            with open(fileName, 'a') as f:
                f.write(novelItems['novelChapter'])
                for content in novelItems['novelContent']:
                    if content != '\r\n':
                        f.write(content)

            tmpNum = response.url.rfind("/") + 1
            responseHtml = response.xpath('//*[@id="content"]').extract()
            nextChapterUrl = re.search(u'<a href="(./|([0-9]+_[0-9]+|[0-9]+).html)">(第二页|下一页|返回列表)</a>', ''.join(responseHtml)).group(1)

            if nextChapterUrl != './':
                url = response.url[0:tmpNum] + nextChapterUrl
                yield scrapy.Request(
                url,
                meta={'fileName' : fileName},
                callback=self.chapter_parse
                )