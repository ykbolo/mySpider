# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
from warnings import filterwarnings
filterwarnings("error", category=pymysql.Warning)


class MyspiderPipeline(object):
    def __init__(self):
        self.f = open("sudaNews.json", 'w', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)+',\n'
        self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.close()


class MyspiderPipeline2(object):
    def __init__(self):
        self.db = pymysql.connect(
            "localhost", "root", "yk84732225", "spiderurl")
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):

        sql = "INSERT IGNORE INTO urllist(url,father) VALUE ('%s','%s')" % (
            item['url'], item['father'])
        try:
            self.cursor.execute(sql)
        except pymysql.Warning as e:
            print(e)
        return item

    def close_spider(self, spider):
        self.db.commit()
        self.db.close()
