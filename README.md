# WebCrawler
各种爬虫

### 1.目前写了以下几个网站的爬取

500px.com

pornhub.com

dytt8.net

toptxt.net

whatismybrowser.com

qzone.qq.com

### 2.代码运行说明：

在windows下安装anaconda和scrapy，参考[博客](http://www.purepure.top/index.php/%E7%88%AC%E8%99%AB/91.html)

进入项目路径，例如

    cd ./WebCrawler/px/

    scrapy crawl pxs -o pxs.json -s FEED_EXPORT_ENCODING=utf-8 

运行命令都在spilders/xxx.py文件的class上面写着

### 3.项目创建备注
    #无需创建文件夹
    scrapy startproject sina
    scrapy genspider sinaSpider sina.com

### 4.爬虫代理说明

#### 代理ip和useragent使用http接口的方式下发，调用此接口即可获取随机的可用代理ip和useragent

#### 抓取whatismubrower网站的useragent存储到mongo DB，并为其设置http接口

#### 使用了github上的proxy_pool获取可用代理ip并启用http api接口

### scrapy配置使用随机useragent和代理ip，详情参考useragent爬虫添加方式，总结如下

#### 1.如果可以自己运行爬虫useragent抓取whatismybrower到mongo,直接下一步，否则首先在mongo DB下创建whatismybrower，然后导入数据proxy.json

#### 2.启动http api接口

    cd ./proxy_pool/
    python Run/main.py

#### 3.在middlewares.py文件中添加两个Middleware，导入必要的模块，代码如下

    import random
    import scrapy
    import os
    import requests
    from scrapy.utils.project import get_project_settings

    class RandomUserAgentMiddleware(object):
        def __init__(self, crawler):
            super(RandomUserAgentMiddleware, self).__init__()

        @classmethod
        def from_crawler(cls, crawler):
            return cls(crawler)

        def process_request(self, request, spider):
            user_agent_random=get_random_useragent
            request.headers.setdefault('User-Agent', user_agent_random) #这样就是实现了User-Agent的随即变换

        '''通过http接口获取useragent'''
        def get_random_useragent(self):
            settings = get_project_settings()
            return requests.get(settings.get('USERAGENT_API')).text

    class ProxyMiddleWare(object):
        def __init__(self):
            super(ProxyMiddleWare, self).__init__()

        """docstring for ProxyMiddleWare"""
        def process_request(self,request, spider):
            '''对request对象加上proxy'''
            proxy = 'http://' + self.get_random_proxy()
            if proxy != '1' :
                print("this is request ip:"+proxy)
                request.meta['proxy'] = proxy
    
        def process_response(self, request, response, spider):
            '''对返回的response处理'''
            # 如果返回的response状态不是200，重新生成当前request对象
            if response.status != 200:
                proxy = self.get_random_proxy()
                if proxy != '' :
                    print("this is response ip:"+proxy)
                    # 对当前reque加上代理
                    request.meta['proxy'] = proxy 
                return request
            return response
    
        def get_random_proxy(self):
            '''调用http接口获取proxy ip'''
            settings = get_project_settings()
            return requests.get(settings.get('PROXY_API')).text

#### 4.项目setting配置

    #代理ip获取api接口
    PROXY_API = 'http://localhost:5010/get/proxy'
    USERAGENT_API = 'http://localhost:5010/get/useragent'
    # Enable or disable downloader middlewares
    # See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
    DOWNLOADER_MIDDLEWARES = {
        'useragent.middlewares.RandomUserAgentMiddleware': 543,
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None, #这里要设置原来的scrapy的useragent为None，否者会被覆盖掉
        'useragent.middlewares.ProxyMiddleWare':125,
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':None,
    }

#### 5.启动爬虫即可