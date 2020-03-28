# -*- coding: utf-8 -*-
import scrapy
# 吧文本结构化存储到json文件中
import html as ht
import pymysql 
import json
import random
import time
from lxml import html
from mySpider.items import txt2jsonItem
class JsondbSpider(scrapy.Spider):
    name = 'jsondb'
    # allowed_domains = [''http://oese.suda.edu.cn/0f/b4/c14883a331700/page.htm/main.psp'']
    start_urls = ["http://www.suda.edu.cn",]
    url_pool = []# url池
    count=0
    index=0
    # 特殊设置
    custom_settings = {
        'ITEM_PIPELINES' :{'mySpider.pipelines.readjsondbPipeline':300},
        
    }
    # db=
    def parse(self,response):
        self.url_pool=self.readFromDB()
        for target in self.url_pool:
          yield scrapy.FormRequest(target,callback=self.getInfo)
    def getInfo(self, response):
        # self.url_pool.pop(0)
        # print(response.status)
        print(response.request.url.strip('*/'))
        print("###: url_pool %d  ###" % (len(self.url_pool)))
        self.count = self.count+1
        randomdelay=random.randint(0,4)
        time.sleep(randomdelay)
        print("%d ### random delay: %s s ###" % (self.count,randomdelay))
        item = txt2jsonItem()
        tree = html.fromstring(response.body)
        ele = tree.xpath('//script | //noscript| //style') 
        for e in ele:
          e.getparent().remove(e)
        treetxt = tree.xpath('//text()')
        # 将空格制表符替换掉
        for index in range(len(treetxt)):
          treetxt[index]=treetxt[index].strip().replace('\t','').replace('\n','').replace('\r','')
        # 提取有效信息
        title = tree.xpath('//title/text()')
        description = tree.xpath("//meta[@name='description']/@content")
        keywords= tree.xpath("//meta[@name='keywords']/@content")
        imgs = tree.xpath("//img/@alt")
        url = response.request.url.strip('*/')
        # join可以把列表中的元素连接起来
        item['url'] = url
        item['title'] = ''.join(title)
        item['description']=''.join(description)
        item['keywords']=''.join(keywords)
        item['imgs']=''.join(imgs)
        item['body']=''.join(treetxt)
        # print(dict(item))
        yield item
        
        
        # print(url,end="\\\")
        # print('title')
        # print(''.join(title))
        # print('description')
        # print(''.join(description))
        # print('keywords')
        # print(''.join(keywords))
        # print('imgs')
        # print(''.join(imgs))
        # print('treetxt')
        # print(''.join(treetxt))
        # content = json.dumps(dict(item), indent=1,ensure_ascii=False)+'\n'
        # self.writeFile(self.index,content)

        # for target in self.url_pool:
        #   yield scrapy.Request(target,self.parse2,dont_filter=False)
    # 读取数据库中的url
    def readFromDB(self):
      db = pymysql.connect(
          "localhost", "root", "password", "spiderurl")
      cursor = db.cursor()
      sql_geturl = "SELECT url from TEMP0327_distinct_copy"
      cursor.execute(sql_geturl)
      info = cursor.fetchall()
      url_pool=[]
      
      for x in info:
        url_pool.append(x[0])
      return url_pool
    # 写文件
    # def writeFile(self,index,content):
    #   # f = open("../../sudaNewsText"+str(index)+'.txt', 'w', encoding='utf-8')
    #   # f.write(content)
    #   print('F://txt2json/index'+str(index)+'.json')
    #   with open('F://txt2json/index'+str(index)+'.json', 'w', encoding='utf-8') as f:
    #         # content = json.dumps(dict(),ensure_ascii=False)
    #         f.write(content)
    #         f.close()