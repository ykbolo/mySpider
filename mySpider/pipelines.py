# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import re
import pymysql
from warnings import filterwarnings
filterwarnings("error", category=pymysql.Warning)


class MyspiderPipeline(object):
    def __init__(self):
        self.f = open("sudaNews2.json", 'w', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)+',\n'
        flag = self.judge_suda(item['url'])
        if flag:
            self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.close()

    def judge_suda(self, url):
        flag = True
        re_suda = r'.*suda\.edu\.cn.*'
        re_ip = r'.*((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?).*'
        re_unformat = r".*[@|'|,].*"
        if re.match(re_suda, url, re.I | re.M) or re.match(re_ip, url, re.I | re.M):
            if re.match(re_unformat, url, re.I | re.M) == None:
                flag = True
            else:
                flag = False
        else:
            flag = False
        # print(url, ':', '满足入库要求' if(flag) else '不满足要求')
        return flag


class MyspiderPipeline2(object):

    def __init__(self):
        self.db = pymysql.connect(
            "localhost", "root", "yk84732225", "spiderurl")
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        flag = self.judge_suda(item['url'])
        if flag:
            sql = "INSERT IGNORE INTO urllist(url,father) VALUE ('%s','%s')" % (
                item['url'], item['father'])
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except pymysql.Warning as e:
                pass
        return item

    def close_spider(self, spider):
        # self.db.commit()
        self.db.close()

    def judge_suda(self, url):
        flag = True
        re_suda = r'.*suda\.edu\.cn.*'
        re_ip = r'.*((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?).*'
        re_unformat = r".*[@|'|,].*"
        if re.match(re_suda, url, re.I | re.M) or re.match(re_ip, url, re.I | re.M):
            if re.match(re_unformat, url, re.I | re.M) == None:
                flag = True
            else:
                flag = False
        else:
            flag = False
        # print(url, ':', '满足入库要求' if(flag) else '不满足要求')
        return flag
