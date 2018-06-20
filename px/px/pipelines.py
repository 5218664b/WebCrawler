# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import time
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class PxPipeline(object):
    def process_item(self, item, spider):
        return item

class MyImagesPipeline(ImagesPipeline):
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
        down_file_name = '{0}/{1}'.format(time.strftime("%Y-%m-%d",time.localtime()), imgName[imgIndex])
        return down_file_name

    #获取图片存储路径
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
