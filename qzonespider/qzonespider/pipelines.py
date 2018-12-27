# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter

class QzonespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonExporterPipleline(object):
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False, indent=1)
        self.exporter.start_exporting()
    #def open_spider(self, spider):
    #    self.file = open(spider.name + '.json', 'wb')
    #    self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False, indent=1)
    #    self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting() 
        self.file.close() 
    def process_item(self, item, spider): 
        self.exporter.export_item(item) 
        return item