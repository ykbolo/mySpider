# -*- coding: utf-8 -*-
# 用于将网页读取到txt中
import scrapy
import pymysql 
from mySpider.items import sudaMainItem
import json
# import '../../sudaNewsText'
class ReadtotxtSpider(scrapy.Spider):
    name = 'readToTxt'
    allowed_domains = ['www.suda.edu.cn']
    start_urls = ['http://www.suda.edu.cn']
    url_pool = []
    count=0
    index=0
    def parse(self, response):
        self.url_pool=self.readFromDB()
       
        print(self.url_pool)
        # self.writeFile(index,response.body)
        # print(url_pool)
        
        yield scrapy.FormRequest(url=self.url_pool[0],callback=self.parse2)

    def parse2(self,response):
        
        self.index = self.index+1
        
        # print(response.meta)
        # print(response.body.decode('utf-8'))
        self.writeFile(self.index,response.body)
        for target in self.url_pool:
            yield scrapy.FormRequest(url=target,callback=self.parse2)
    def readFromDB(self):
      db = pymysql.connect(
          "localhost", "root", "yk84732225", "spiderurl")
      cursor = db.cursor()
      sql_geturl = "SELECT url from sudanews"
      cursor.execute(sql_geturl)
      info = cursor.fetchall()
      url_pool=[]
      
      for x in info:
        url_pool.append(x[0])
        self.count=self.count+1
        if self.count==100:
          break
      return url_pool
    def writeFile(self,index,content):
      # f = open("../../sudaNewsText"+str(index)+'.txt', 'w', encoding='utf-8')
      # f.write(content)
      print('./sudaNewsText/index'+str(index)+'.txt')
      with open('./sudaNewsText/index'+str(index)+'.txt', 'w', encoding='utf-8') as f:
            # content = json.dumps(dict(),ensure_ascii=False)
            f.write(str(content.decode("utf-8")))
            f.close()