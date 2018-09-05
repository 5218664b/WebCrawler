# -*- coding: utf-8 -*-
class interface:
    #获取总页数
    def get_page_count(self,response):
        pass
    #设置每页的url
    def set_request_url(self,response,currentPageNum):
        pass
    #获取资源页的url
    def get_request_url(self,response):
        pass
    #获取电影链接
    def get_movie_link(self,response):
        pass
#   IMDB评分8分以上影片300余部
class Dytt1(interface):
    #获取总页数
    def get_page_count(self,response):
        pageContent = str(response.xpath('//center').extract()).decode('unicode_escape')
        tmpStr = pageContent.split(':')
        pageCount = int(tmpStr[0][12:-1])
        return pageCount

    #设置每页的url
    def set_request_url(self,response,currentPageNum):
        if currentPageNum == 1 :
            url = response.url
        else:
            url = response.url[0:-5] + '_' + str(currentPageNum) + '.html'
        return url

    #获取资源页的url
    def get_request_url(self,response):
        return response.xpath('//p/a/@href').extract()

    #获取电影链接
    def get_movie_link(self,response):
        movieDict = {}
        movieDict['moviePageUrl'] = response.url
        movieDict['movieName'] = response.xpath('//div[@class="title_all"]/h1/font/text()').extract()
        movieDict['movieLink'] = response.xpath('//table/tbody/tr/td//a/@href').extract()
        return movieDict

class Dytt2(interface):
    #获取总页数
    def get_page_count(self,response):
        return len(response.xpath('//select[@name="sldd"]/option').extract())

    #设置每页的url
    def set_request_url(self,response,currentPageNum):
        appendIndex = response.url.rfind('_')
        url = response.url[0:appendIndex] + '_' + str(currentPageNum) + '.html'
        return url

    #获取资源页的url
    def get_request_url(self,response):
        prefixStr = 'http://www.dytt8.net'
        links = response.xpath('//td/b/a/@href').extract()
        return map(lambda x: prefixStr + x, links)
        
    #获取电影链接
    def get_movie_link(self,response):
        filePath = 'D:/pachong/movieHeaven/movie.Links'
        movieDict = {}
        movieDict['moviePageUrl'] = response.url
        movieDict['movieName'] = response.xpath('//div[@class="title_all"]/h1/font/text()').extract()
        movieDict['movieLink'] = response.xpath('//p/a/@href').extract()
        if movieDict['movieLink'] == [] :
            movieDict['movieLink'] = response.xpath('//table/tbody/tr/td//a/@href').extract()
        with open(filePath,'a') as f:
            f.write(str(movieDict['movieLink']).decode('unicode_escape')[3:-2] + '\n')

        return movieDict