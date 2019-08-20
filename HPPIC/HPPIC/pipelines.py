# -*- coding: utf-8 -*-
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request

class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for links in item['links']:
            yield Request(links, meta={'item':item})  #'index':item['links'].index(links)

    def file_path(self, request, response=None, info=None):
        #image_path = [x['path'] for ok, x in results if ok]
        #if not image_path:
         #   raise DropItem('下载失败  %s'%image_path)
        item = request.meta['item']
        #index = request.meta['index']
        image_name = item['nums']
        return '%s.jpg'%(image_name)

class HppicPipeline(object):
    def __init__(self):
        host = '127.0.0.1'
        port = 27017
        dbname = 'HP'
        sheetname = 'pic_info'
        client = pymongo.MongoClient(host=host, port=port)
        mydb = client[dbname]
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
