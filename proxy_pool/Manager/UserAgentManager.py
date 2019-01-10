# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.abspath('../../someTools'))
from mongo.mongo import MongoTools
import random
class UserAgentManager(object):
    def __init__(self):
        self.mt = MongoTools(mongo_uri='mongodb://localhost:27017/', mongo_db='useragent')
        self.collection = 'whatismybrowser'

    def get(self):
        item_array = [p['useragent'] for p in self.mt.find(self.collection, {})]
        if item_array:
            return random.choice(random.choice(item_array))
        return None

if __name__ == '__main__':
    uam = UserAgentManager()
    print uam.get()