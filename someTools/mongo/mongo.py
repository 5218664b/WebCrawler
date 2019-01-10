# -*- coding: utf-8 -*-

import pymongo
from scrapy.utils.project import get_project_settings

class MongoTools(object):
    def __init__(self, mongo_uri=None, mongo_db=None):
        settings = get_project_settings()
        # 从配置文件中获取数据库连接信息
        mongo_uri = settings.get('MONGO_URI')
        mongo_db = settings.get('MONGO_DATABASE', 'items')
        if mongo_uri is None or mongo_db is None:
            print u'请在setting中设置【MONGO_URI】【MONGO_DATABASE】'
        else:
            self.conn = pymongo.MongoClient(mongo_uri)
            self.db = self.conn[mongo_db]

    def close(self):
        if self.get_state():
            self.conn.close()
            
    def get_state(self):
        return self.conn is not None and self.db is not None

    def insert_one(self, collection, data):
        if self.get_state():
            ret = self.db[collection].insert_one(data)
            return ret.inserted_id
        else:
            return ""

    def insert_many(self, collection, data):
        if self.get_state():
            ret = self.db[collection].insert_many(data)
            return ret.inserted_id
        else:
            return ""

    def update(self, collection, data):
        # data format:
        # {key:[old_data,new_data]}
        data_filter = {}
        data_revised = {}
        for key in data.keys():
            data_filter[key] = data[key][0]
            data_revised[key] = data[key][1]
        if self.get_state():
            return self.db[collection].update_many(data_filter, {"$set": data_revised}).modified_count
        return 0

    def find(self, col, condition, column=None):
        if self.get_state():
            if column is None:
                return self.db[col].find(condition)
            else:
                return self.db[col].find(condition, column)
        else:
            return None

    def delete(self, col, condition):
        if self.get_state():
            return self.db[col].delete_many(filter=condition).deleted_count
        return 0