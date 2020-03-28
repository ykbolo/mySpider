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
        self.f = open("sudaNews3.json", 'w', encoding='utf-8')

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
            "localhost", "root", "password", "spiderurl")
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


class MyspiderPipeline3(object):
    def __init__(self):
        self.f = open("sudaAUrls.json", 'a', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)+',\n'
        self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.close()



class txt2jsonPipeline(object):
    def __init__(self):
        # self.f = open("sudaAUrls.json", 'a', encoding='utf-8')
        self.index=0
    def process_item(self, item, spider):
        if item:
          print(dict(item))
          content = json.dumps(dict(item), ensure_ascii=False)+',\n'
          self.writeFile(self.index,content)
          self.index = self.index+1

    def close_spider(self, spider):
        pass
    def writeFile(self,index,content):
      print('./txt2json/index'+str(index)+'.json')
      with open('./txt2json/index'+str(index)+'.json', 'w', encoding='utf-8') as f:
            # content = json.dumps(dict(),ensure_ascii=False)
            f.write(content)
            f.close()
class readjsondbPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(
            "localhost", "root", "password", "spiderurl",charset="utf8")
        self.cursor = self.db.cursor()
        self.count = 0
    def process_item(self, item, spider):
        # print(dict(item))
        
        content = json.dumps(dict(item), ensure_ascii=False)
        requireJson = pymysql.escape_string(content)  
        sql = "INSERT INTO content0328(json) VALUE ('%s')" % (requireJson)
        # print(content)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except pymysql.Warning as e:
            pass
            
        return item
        #   self.index = self.index+1

    def close_spider(self, spider):
        self.db.close()
    
