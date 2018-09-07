# -*- coding: utf-8 -*-
import scrapy
import json
import re
import sys
import requests
from novelDownload.items import NoveldownloadItem
from scrapy.conf import settings

#scrapy crawl novelDown -o novelDownload.json -s FEED_EXPORT_ENCODING=utf-8
class NoveldownSpider(scrapy.Spider):
    if sys.version_info.major < 3:
        reload(sys)
        sys.setdefaultencoding('utf-8')

    name = 'novelDown'
    allowed_domains = ['www.toptxt.net']
    urlDomain = 'http://www.toptxt.net/'
    #urlStr = 'toptxt/0/502/'
    fileName = ''
    searchDomain = 'http://www.toptxt.net/modules/article/search.php'
    #搜索关键词之后在网页上获取到的，注意前面加个问号
    searchKey = '?searchtype=articlename&searchkey=%B5%C1%C4%B9%B1%CA%BC%C7&Submit=+%CB%D1+%CB%F7+'
    #下载路径，需要修改为自己电脑的路径
    downloadPath = 'D:/pachong/novelDownload/download/'

    novelList = []

    #请求搜索结果页面
    def start_requests(self):
        url = self.searchDomain + self.searchKey
        yield scrapy.Request(
            url,
            callback=self.parse_searchPage,
            headers={
                'Cookie' : 'jieqiVisitTime=jieqiArticlesearchTime%3D1534963500',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            }
            )
    #请求搜索结果的第一页
    def parse_searchPage(self,response):
        self.pageCount = int(str(response.css('.last').xpath('text()').extract())[3:-2])
        self.currentPageNum = 1
        url = self.searchDomain + self.searchKey + '&page=' + str(self.currentPageNum)
        yield scrapy.Request(
        url,
        callback=self.parse_searchRest
        )
    #解析搜索结果
    def parse_searchRest(self,response):
        print str(response.css('tr .even a'))
        for nodeLink in response.css('tr .even a'):
            self.novelList.append(str(nodeLink.xpath('@href').extract())[25:-2])

        self.currentPageNum = self.currentPageNum + 1
        if self.currentPageNum < self.pageCount:
            url = self.searchDomain + self.searchKey + '&page=' + str(self.currentPageNum)
            yield scrapy.Request(
            url,
            callback=self.parse_searchRest
            )
        else:
            #遍历搜索结果中所有的小说的首页地址
            for urlStr in self.novelList:
                if urlStr.strip() != '':
                    url = self.urlDomain + urlStr
                    self.urlStr = urlStr
                    yield scrapy.Request(
                    url,
                    callback=self.start_requests2
                    )

    def start_requests2(self,response):
        novelItems = NoveldownloadItem()
        novelItems['novelName'] = response.xpath('//*[@id="wp"]/div/div[2]/h1/text()').extract()
        yield novelItems

        #获取第一章的pagenum
        pageNum = int(str(response.xpath('//*[@id="wp"]/div/div[3]/div[1]/ul/li[1]/a/@href').extract())[3:-7])
        #获取总页数，这里有多的页，直接tr数量乘4
        endPageNum = pageNum + len(response.css('.novel_list').extract())*4
        fileName = self.downloadPath + str(novelItems['novelName']).decode('unicode_escape')[3:-2] + '.txt'
        print fileName + '5555'
        with open(fileName, 'wb') as f:
            f.write(str(novelItems['novelName']).decode('unicode_escape')[3:-2])
        
        url = response.url + str(pageNum) + '.html'
        #请求第一章
        yield scrapy.Request(
        url,
        meta={'fileName' : fileName,'endPageNum' : endPageNum},
        callback=self.parse
        )
            
    def parse(self, response):
        novelItems = NoveldownloadItem()
        novelItems['novelChapter'] = response.xpath('//*[@id="content"]/div[1]/h1/text()').extract()
        novelItems['novelContent'] = response.xpath('//*[@id="novel_content"]/text()').extract()
        yield novelItems

        fileName = response.meta['fileName']
        endPageNum = response.meta['endPageNum']

        with open(fileName, 'a') as f:
            f.write(str(novelItems['novelChapter']).decode('unicode_escape')[3:-2].replace('\', u\'',''))
            f.write(str(novelItems['novelContent']).decode('unicode_escape')[3:-2].replace('\', u\'',''))

        tmpNum = response.url.rfind("/") + 1
        
        pageNum=int(response.url[tmpNum:-5])+1
        if pageNum < endPageNum:
            url = response.url[0:tmpNum] + str(pageNum) + '.html'
            yield scrapy.Request(
            url,
            meta={'fileName' : fileName,'endPageNum' : endPageNum},
            callback=self.parse
            )
