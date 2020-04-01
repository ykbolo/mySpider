# -*- coding: utf-8 -*-
import scrapy
import re
from mySpider.items import sudaMainItem
import pymysql
import copy
from urllib.request import urlparse
from urllib.parse import urljoin
import random
import time

class SudaMainSpider(scrapy.Spider):
    name = 'sudaA'
    allowed_domains = ['ac.suda.edu.cn',
'aff.suda.edu.cn',
'alumni.suda.edu.cn',
'arch.suda.edu.cn',
'archives.suda.edu.cn',
'audit.suda.edu.cn',
'bjwx.suda.edu.cn',
'bsh.suda.edu.cn',
'bwc.suda.edu.cn',
'bwcx.suda.edu.cn',
'card.suda.edu.cn',
'career.suda.edu.cn',
'cgpt.suda.edu.cn',
'chemistry.suda.edu.cn',
'cicrm.suda.edu.cn',
'cps.suda.edu.cn',
'ctmi.suda.edu.cn',
 
'cusg.suda.edu.cn'
 ,
'cwc.suda.edu.cn',
 
'cxcyzx.suda.edu.cn',
 
'dangxiao.suda.edu.cn'
 ,
'db.suda.edu.cn',
 
'ddh.suda.edu.cn',
 
'disciplinfo.suda.edu.cn',
 
'dsj.suda.edu.cn',
 
'dwshy.suda.edu.cn',
 
'dwzx.suda.edu.cn',
 
'dxpx.suda.edu.cn',
 
'dxyqgl.suda.edu.cn',
 
'dxyqglxt.suda.edu.cn',
 
'dzxx.suda.edu.cn',
 
'eeac.suda.edu.cn',
 
'energy.suda.edu.cn',

'eng.suda.edu.cn']
    start_urls = ['http://ac.suda.edu.cn']
    # basic_url_init = 'http://www.suda.edu.cn'
    # basic_url = 'http://www.suda.edu.cn'
    # table_count = 0
    parseCount=0
    url_pool = set(('http://ac.suda.edu.cn',
'http://aff.suda.edu.cn',
'http://alumni.suda.edu.cn',
'http://arch.suda.edu.cn',
'http://archives.suda.edu.cn',
'http://audit.suda.edu.cn',
'http://bjwx.suda.edu.cn',
 
'http://bsh.suda.edu.cn',
 
'http://bwc.suda.edu.cn',
 
'http://bwcx.suda.edu.cn',
 
'http://card.suda.edu.cn',
 
'http://career.suda.edu.cn',
 
'http://cgpt.suda.edu.cn',
 
'http://chemistry.suda.edu.cn',
 
'http://cicrm.suda.edu.cn',
 
'http://cps.suda.edu.cn',
 
'http://ctmi.suda.edu.cn',
 
'http://cusg.suda.edu.cn'
 ,
'http://cwc.suda.edu.cn',
 
'http://cxcyzx.suda.edu.cn',
 
'http://dangxiao.suda.edu.cn'
 ,
'http://db.suda.edu.cn',
 
'http://ddh.suda.edu.cn',
 
'http://disciplinfo.suda.edu.cn',
 
'http://dsj.suda.edu.cn',
 
'http://dwshy.suda.edu.cn',
 
'http://dwzx.suda.edu.cn',
 
'http://dxpx.suda.edu.cn',
 
'http://dxyqgl.suda.edu.cn',
 
'http://dxyqglxt.suda.edu.cn',
 
'http://dzxx.suda.edu.cn',
 
'http://eeac.suda.edu.cn',
 
'http://energy.suda.edu.cn',
 
'http://eng.suda.edu.cn'))
    custom_settings = {
                       'ITEM_PIPELINES': {
                           'mySpider.pipelines.MyspiderPipeline3': 300
                       }
                       }
    
    def parse(self,response):
        self.parseCount = self.parseCount+1
        print("### %d 次循环 ###" % self.parseCount)
        print("### url_池大小 %d ###" % len(self.url_pool))
        url_pool_copy = copy.deepcopy(self.url_pool)
        for target in url_pool_copy:
            yield scrapy.FormRequest(target,callback=self.parsePage)
        yield scrapy.Request('http://localhost', self.parse, dont_filter=True)
        print("### %d 次循环 ###" % self.parseCount)
        print("### url_池大小 %d ###" % len(self.url_pool))
    def parsePage(self, response):
        # self.count = self.count+1
        #print('这是第', self.count, '个页面')
        print('当前爬取页面'+response.request.url.strip('*/'))
        randomdelay=random.randint(0,4)
        time.sleep(randomdelay)
        print("### random delay: %s s ###" % (randomdelay))
        # print('当前集合大小', len(self.url_pool))
        titles = response.xpath('//a/@href').extract()

        basic_url = response.request.url.strip('*/')

        # 对于url进行拼接处理
        for url in titles:
            # print(url)
            item = sudaMainItem()
            matchFullUrl = re.match(
                r'^(http|https)://([\w.]+/?)\S*', url, re.M | re.I)
            # matchRelateUrl = re.match(r'^/([\w.]?/?)\S*', url, re.M | re.I)
            # matchRelateUrl2 = re.match(r'^[^/]([\w.]?/?)\S*', url, re.M | re.I)
            matchUselessUrl = re.match(r'^#([\w.]?/?)\S*', url, re.M | re.I)
            # matchParams = re.match(r'^\?([\w.]?/?)\S*', url, re.M | re.I)
            if url:
                if matchFullUrl:
                    true_url = url
                    # print('原始url', true_url)
                elif matchUselessUrl:
                    true_url = basic_url
                else:
                    true_url = urljoin(basic_url, url)
                    # print('未处理且未匹配', true_url)
                if self.judge_suda(true_url):
                    item['father'] = basic_url
                    item['url'] = true_url
                    self.url_pool.add(true_url)
                    yield item
                # if true_url not in self.url_pool:
                #     item['distinct_url'] = true_url

                # else:
                #     item['distinct_url'] = 'duplicate'
                # yield item
        # url_list = self.getDistinctUrls()
        # print(url_list)
        # url_pool_copy = copy.deepcopy(self.url_pool)
        # # url_pool_copy = list(self.url_pool)

        # for next_url in url_pool_copy:
        #     # print('这是第', index, '个元素')
        #     if 'http://' in next_url or 'https://' in next_url:
        #         yield scrapy.Request(next_url, self.parse, dont_filter=False)
        #     else:
        #         yield scrapy.Request('http://'+next_url, self.parse, dont_filter=False)

    def getDistinctUrls(self):
        url_list = []
        self.db = pymysql.connect(
            "localhost", "root", "password", "spiderurl")
        self.cursor = self.db.cursor()
        sql = "SELECT DISTINCT url FROM urllist"
        self.cursor.execute(sql)
        # self.db.commit()  # 重点在这
        alldata = self.cursor.fetchall()
        for data in alldata:
            url_list.append(data[0])
        return url_list

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
        return flag
