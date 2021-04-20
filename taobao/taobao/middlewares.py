# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.http import Request,FormRequest,HtmlResponse
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
import requests
from scrapy.utils.project import get_project_settings
reload(sys)
sys.setdefaultencoding('utf-8')

class TaobaoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TaobaoDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class SeleniumMiddleware():
    def __init__(self):
        ops = Options()
        ops.add_argument('--user-agent=%s' % 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0')
        #ops.add_argument('--proxy-server=http://%s' % 'http://127.0.0.1:8081')
        #ops.page_load_strategy = 'eager'
        
        #PROXY = "127.0.0.1:8081"
        self.settings = get_project_settings()
        
        # 关闭自动测试状态显示 // 会导致浏览器报：请停用开发者模式
        ops.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.driver=webdriver.Chrome(executable_path=r"D:\ProgramData\Anaconda3\envs\erdianqi\chromedriver.exe")
        #self.driver = webdriver.Firefox(executable_path=r"D:\ProgramData\Anaconda3\envs\erdianqi\geckodriver.exe")

    def __del__(self):
        self.driver.close()

    def process_request(self,request,spider):
        PROXY = requests.get(self.settings.get('PROXY_API')).text
        print('PROXY' + PROXY)
        webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
            "httpProxy": PROXY,
            "proxyType": "MANUAL",
        }
        browser=self.driver
        # 通过浏览器的dev_tool在get页面钱将.webdriver属性改为"undefined"
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",
        })
        browser.get(request.url)
        if request.url == 'https://login.taobao.com/member/login.jhtml':
            time.sleep(1)

            username=browser.find_element_by_id("fm-login-id")
            username.send_keys("")

            username=browser.find_element_by_id("fm-login-password")
            username.send_keys("")

            login=browser.find_element_by_class_name('password-login')
            login.click()
        time.sleep(1)
        source=browser.page_source
        
        response=HtmlResponse(url=browser.current_url,body=source,request=request,encoding='utf-8')
        return response