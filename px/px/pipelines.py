# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import time
import os
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class PxPipeline(object):
    def process_item(self, item, spider):
        return item

class MyImagesPipeline(ImagesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        ImagesPipeline.__init__(self, store_uri, download_func, settings)
        file_path = './crawlImage/'
        dir_list = os.listdir(file_path)
        dir_list1 = [str(dir).split('-')[1] for dir in dir_list]
        self.file_time =  time.strftime("./%Y%m%d-0",time.localtime())
        if os.path.exists(os.path.abspath(file_path + self.file_time)):
            self.file_time = self.file_time[:-1] + str(int(max(dir_list1))+1)

    #下载图片
    def get_media_requests(self, item, info):
        for image_url in item['imgUrl']:
            print('image_url:' + image_url)
            yield scrapy.Request(image_url,meta={'item':item,'imgIndex' : item['imgUrl'].index(image_url)})

    #文件改名
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        imgName = item['imgName']
        imgIndex = request.meta['imgIndex']
        down_file_name = '{0}/{1}'.format(self.file_time, imgName[imgIndex])
        return down_file_name

    #获取图片存储路径
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
