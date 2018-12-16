# -*- coding: utf-8 -*-
import pymongo
import redis

class MongodbTool(object):
    
    def __init__(self):
        self.db = pymongo.MongoClient('localhost', 27017)['QQ']
        self.rconn = redis.Redis('localhost', 6379)  # 存放种子和Cookie