# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from items import InformationItem, TweetsItem, CommentsItem, TransfersItem

class MongoDBPipleline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["Sina"]
        self.Information = db["Information"]
        self.Tweets = db["Tweets"]
        self.Comments = db["Comments"]
        self.Transfers = db["Transfers"]

    def process_item(self, item, spider):
        if isinstance(item, InformationItem):
            try:
                self.Information.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, TweetsItem):
            try:
                self.Tweets.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, CommentsItem):
            try:
                self.Comments.insert(CommentsItems)
            except Exception:
                pass
        elif isinstance(item, TransfersItem):
            try:
                self.Transfers.insert(TransfersItems)
            except Exception:
                pass
        return item
