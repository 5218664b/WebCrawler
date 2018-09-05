# -*- coding: utf-8 -*-
import scrapy
import json
import re
import sys
import requests
from scrapy.conf import settings
from customRule import *
import customRule
from movieHeaven.items import MovieheavenItem

class MovieSpider(scrapy.Spider):
    if sys.version_info.major < 3:
        reload(sys)
        sys.setdefaultencoding('utf-8')

    name = 'movie'
    allowed_domains = ['dytt8.net']
    start_urls = ['http://dytt8.net/']

    urls = ['http://www.dytt8.net/html/gndy/jddy/20160320/50523.html',
            'http://www.dytt8.net/html/gndy/dyzz/list_23_1.html']
    methodNameList = ['get_page_count',
                      'set_request_url',
                      'get_request_url',
                      'get_movie_link']

    classCount = dir(customRule).index('__builtins__')
    classList = dir(customRule)[0:classCount]

    #获取类和类的方法，将类作为key，方法数组作为value
    searchDict = {}
    for className in classList:
        methodList = []
        classObj = getattr(customRule,className)
        methodList.append(classObj)
        for method in methodNameList:
            methodList.append(getattr(classObj,method))
        searchDict[className] = methodList

    def start_requests(self):
        for index,url in enumerate(self.urls):
            yield scrapy.Request(
                url,
                callback=self.request_per_page,
                meta={'index' : index}
            )

    def request_per_page(self, response):
        index = response.meta['index']
        className = self.classList[int(index)]
        #第0号元素是类本身
        classObj = self.searchDict[className][0]
        methodObj = self.searchDict[className][1]
        pageCount = methodObj(classObj(),response)

        currentPageNum = 1
        
        #请求每个页面
        while currentPageNum <= pageCount:
            className = self.classList[int(index)]
            #第0号元素是类本身
            classObj = self.searchDict[className][0]
            methodObj = self.searchDict[className][2]
            url = methodObj(classObj(),response,currentPageNum)
            yield scrapy.Request(
                url,
                callback=self.get_page_link,
                meta={'index':index}
            )
            currentPageNum = currentPageNum + 1
            
    def get_page_link(self,response):
        index = response.meta['index']
        className = self.classList[int(index)]
        #第0号元素是类本身
        classObj = self.searchDict[className][0]
        methodObj = self.searchDict[className][3]
        links = methodObj(classObj(),response)

        for link in links:
            yield scrapy.Request(
                link,
                callback=self.get_movie_link,
                dont_filter=True,
                meta={'index':index}
            )

    def get_movie_link(self,response):
        index = response.meta['index']
        className = self.classList[int(index)]
        #第0号元素是类本身
        classObj = self.searchDict[className][0]
        methodObj = self.searchDict[className][4]
        movieDict = methodObj(classObj(),response)

        movieItem = MovieheavenItem()
        movieItem['moviePageUrl'] = movieDict['moviePageUrl']
        movieItem['movieName'] = movieDict['movieName']
        movieItem['movieLink'] = movieDict['movieLink']
        yield movieItem
        
