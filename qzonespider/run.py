# -*- coding: utf-8 -*-

import scrapy
from scrapy.crawler import CrawlerProcess
from qzonespider.spiders.public_method import QzoneMessage
from qzonespider.spiders.public_method import qqMessage
from scrapy.utils.project import get_project_settings

#账号
account = '1141802674'
#密码
password = 'liujinyiren'
qm = QzoneMessage()
#获取cookie
[cookies, cookieStr] = qm.getCookie(account, password)
gtk = qm.getGTK(cookies)

process = CrawlerProcess(get_project_settings())
process.crawl('comment', {'cookie' : cookieStr,'gtk':gtk})
#process.crawl('mood', {'cookie' : cookieStr,'gtk':gtk})
process.start() # the script will block here until all crawling jobs are finished