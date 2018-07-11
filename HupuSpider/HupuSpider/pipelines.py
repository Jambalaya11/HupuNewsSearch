# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
import scrapy
import os
import pandas as pd
import redis
redis_db = redis.Redis(host=settings.REDIS_HOST, port=6379, db=4, password=settings.REDIS_PWD)
redis_data_dict = "f_uuids"

import sys
sys.path.append('..')
from models.es_type import HupuType

class HupuspiderPipeline(object):
    def process_item(self, item, spider):
        filename = item['newstitle']
        filename += ".txt"

        savepath = 'hupunews' + '/' + item['teamname'] + '/' + item['newstitle'] + '/' + filename
        fp = open(savepath, 'w', encoding='utf-8')
        fp.write(item['content'])
        fp.close()

        return item


class HupuImagesPipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get("IMAGES_STORE")

    def get_media_requests(self, item, info):
        image_url = item["imageurl"]
        yield scrapy.Request(image_url[0])

    def item_completed(self, results, item, info):
        image_path = [x["path"] for ok, x in results if ok]

        # 每张新闻配图放到对应的球队文件夹中
        os.rename(
            self.IMAGES_STORE + "/" + image_path[0],
            self.IMAGES_STORE + "/" + item["teamname"] + "/" +
            item["newstitle"] + "/" + item["newstitle"] + ".jpg")

        return item

class ElasticsearchPipeline(object):

    def process_item(self, item, spider):

        article = HupuType()

        article.teamname = item["teamname"]
        article.teamurl = item["teamurl"]
        article.newstitle = item["newstitle"]
        article.newsurl = item["newsurl"]
        article.content = item["content"]
        article.imageurl = item["imageurl"]

        
        article.save()
        return item

class DuplicatePipeline(object):
    """
    去重(redis)
    """

    def __init__(self):
        if redis_db.hlen(redis_data_dict) == 0:
            sql = "SELECT uuid FROM f_data"
            df = pd.read_sql(sql, engine)
            for uuid in df['uuid'].get_values():
                redis_db.hset(redis_data_dict, uuid, 0)

    def process_item(self, item, spider):

        if redis_db.hexists(redis_data_dict, item['uuid']):
             raise DropItem("Duplicate item found:%s" % item)

        return item

