# -*- coding: utf-8 -*-
import os
# Scrapy settings for px project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'px'

SPIDER_MODULES = ['px.spiders']
NEWSPIDER_MODULE = 'px.spiders'

COOKIE = {'_vwo_uuid': 'DBAF2318FACB08235080E62F93B5FE924', '_vwo_ds': '3%3Aa_0%2Ct_0%3A0%241529164517%3A3.16917445%3A%3A%3A3_0', '_vis_opt_s': '1%7C', 'amplitude_id500px.com': 'eyJkZXZpY2VJZCI6IjY5OWMwNWFhLTNiOTktNDk5Ny1iZmY3LWQyMzA4YjYwNDNhM1IiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTUyOTIzNDk0ODcwMSwibGFzdEV2ZW50VGltZSI6MTUyOTIzNDk0ODcwMSwiZXZlbnRJZCI6OCwiaWRlbnRpZnlJZCI6Miwic2VxdWVuY2VOdW1iZXIiOjEwfQ', 'device_uuid': 'f7d766f5-7a2e-4891-bf95-e849539600c5', '_gat_unifiedTracker': '1', '__hssrc': '1', '_hpx1': 'BAh7C0kiD3Nlc3Npb25faWQGOgZFVEkiJTVmNjkyMWIxNTM4YzA2MGNkNDZkMTk2M2JmMTg4ODg5BjsAVEkiCWhvc3QGOwBGIg41MDBweC5jb21JIhl1c2Vfb25ib2FyZGluZ19tb2RhbAY7AEZUSSIYc3VwZXJfc2VjcmV0X3BpeDNscwY7AEZGSSIQX2NzcmZfdG9rZW4GOwBGSSIxdzZlRmZOaDZXbE90eTdUT0dHbytqN3MzaTl5Ky9HbDBIU01YZ0QxZmltMD0GOwBGSSIRcHJldmlvdXNfdXJsBjsARkkiDS9lZGl0b3JzBjsAVA%3D%3D--a16ca1e6dc4832437b1ec153f21aba879ae76c75', '_ga': 'GA1.2.1554153299.1529164505', '_gat': '1', '_vwo_uuid_v2': 'DBAF2318FACB08235080E62F93B5FE924|048a1549b4932bfae51817e36822b218', '_vis_opt_test_cookie': '1', '_gid': 'GA1.2.2074596523.1529164505', 'hubspotutk': 'd4ee4550408db7431e63c5c666660735', '__hstc': '133410001.d4ee4550408db7431e63c5c666660735.1529164526544.1529164526544.1529202990782.2', '_parsely_visitor': '{%22id%22:%22e07efba0-3245-4494-aaf7-6c1ff1cbe91e%22%2C%22session_count%22:1%2C%22last_session_ts%22:1529205475239}'}
IMAGES_STORE = os.path.abspath('.') + '/crawlImage/'   # 图片存储路径

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'px (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'px.middlewares.PxSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'px.middlewares.RandomUserAgentMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None, #这里要设置原来的scrapy的useragent为None，否者会被覆盖掉
}
RANDOM_UA_TYPE='random'

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'px.pipelines.PxPipeline': 300,
    'px.pipelines.MyImagesPipeline' : 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
