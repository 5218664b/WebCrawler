# -*- coding: utf-8 -*-

import pymongo

if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb =  myclient["testDB"]

    mycol = mydb["col1"]

    mydict = {"name" : ["123","456"], "age" : "23"}

    x = mycol.insert_one(mydict)
    print x