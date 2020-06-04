# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class Scrapy2020Pipeline(object):
    def process_item(self, item, spider):
        return item
# mongo db
# class MongoPipeline(object):
#     collection_name = 'runway'
#
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         ## pull in information from settings.py
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE')
#         )
#
#     def open_spider(self, spider):
#         ## initializing spider
#         ## opening db connection
#         self.client = MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     def close_spider(self, spider):
#         ## clean up when spider is closed
#         self.client.close()
#
#     def process_item(self, item, spider):
#         ## how to handle each post
#         self.db[self.collection_name].insert(dict(item))
#         logging.debug("Post added to MongoDB")
#         return item

# push api
# class MongoPipeline(object):
#     def __init__(self):
#         self.API_ENDPOINT = "api link"
#
#     def process_item(self, item, spider):
#         data = dict(item)
#         r = requests.post(url=self.API_ENDPOINT, json=data)
#         return item
