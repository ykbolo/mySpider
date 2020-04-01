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
    name = 'sudaF'
    parseCount=0
    allowed_domains = ["file.suda.edu.cn",
 
"fineng.suda.edu.cn",
 
"forensic.suda.edu.cn",
 
"funsom.suda.edu.cn",
 
"fxcs.suda.edu.cn",
 
"fyxy.suda.edu.cn",
 
"fzb.suda.edu.cn",
 
"garden.suda.edu.cn",
 
"ggw.suda.edu.cn",
 
"gh.suda.edu.cn",
 
"gkyjs.suda.edu.cn",
 
"gwxy.suda.edu.cn",
 
"gysk.suda.edu.cn",
 
"gzc.suda.edu.cn",
 
"hlxy.suda.edu.cn",
 
"hospital-admin.suda.edu.cn",
 
"hqglc.suda.edu.cn",
 
"hris.suda.edu.cn",
 
"hysgl.suda.edu.cn",
 
"hzb.suda.edu.cn",
 
"iai.suda.edu.cn",
 
"ibms.suda.edu.cn",
 
"ics.suda.edu.cn",
 
"international.suda.edu.cn",
 
"its.suda.edu.cn",
 
"jdxy.suda.edu.cn",
 
"jfsx.suda.edu.cn",
 
"jgdgw.suda.edu.cn",
 
"jjs.suda.edu.cn",
 
"jsgzb.suda.edu.cn",
 
"jsyb.suda.edu.cn",
 
"jsyd.suda.edu.cn",
 
"jtxy.suda.edu.cn",
 
"jwb.suda.edu.cn",
 
"jwsy.suda.edu.cn",
 
"jxjy.suda.edu.cn",
 
"jxjylx.suda.edu.cn",
 
"jxjyzs.suda.edu.cn",
 
"jysw.suda.edu.cn",
 
"jyxy.suda.edu.cn",
 
"labcenter.suda.edu.cn",
 
"laowo.suda.edu.cn",
 
"law.suda.edu.cn",
 
"library.suda.edu.cn",
 
"lst.suda.edu.cn",
 
"ltc.suda.edu.cn",
 
"lxyz.suda.edu.cn"]
    start_urls = ["http://file.suda.edu.cn"]
    # basic_url_init = 'http://www.suda.edu.cn'
    # basic_url = 'http://www.suda.edu.cn'
    # table_count = 0
    url_pool = set(("http://file.suda.edu.cn",
 
"http://fineng.suda.edu.cn",
 
"http://forensic.suda.edu.cn",
 
"http://funsom.suda.edu.cn",
 
"http://fxcs.suda.edu.cn",
 
"http://fyxy.suda.edu.cn",
 
"http://fzb.suda.edu.cn",
 
"http://garden.suda.edu.cn",
 
"http://ggw.suda.edu.cn",
 
"http://gh.suda.edu.cn",
 
"http://gkyjs.suda.edu.cn",
 
"http://gwxy.suda.edu.cn",
 
"http://gysk.suda.edu.cn",
 
"http://gzc.suda.edu.cn",
 
"http://hlxy.suda.edu.cn",
 
"http://hospital-admin.suda.edu.cn",
 
"http://hqglc.suda.edu.cn",
 
"http://hris.suda.edu.cn",
 
"http://hysgl.suda.edu.cn",
 
"http://hzb.suda.edu.cn",
 
"http://iai.suda.edu.cn",
 
"http://ibms.suda.edu.cn",
 
"http://ics.suda.edu.cn",
 
"http://international.suda.edu.cn",
 
"http://its.suda.edu.cn",
 
"http://jdxy.suda.edu.cn",
 
"http://jfsx.suda.edu.cn",
 
"http://jgdgw.suda.edu.cn",
 
"http://jjs.suda.edu.cn",
 
"http://jsgzb.suda.edu.cn",
 
"http://jsyb.suda.edu.cn",
 
"http://jsyd.suda.edu.cn",
 
"http://jtxy.suda.edu.cn",
 
"http://jwb.suda.edu.cn",
 
"http://jwsy.suda.edu.cn",
 
"http://jxjy.suda.edu.cn",
 
"http://jxjylx.suda.edu.cn",
 
"http://jxjyzs.suda.edu.cn",
 
"http://jysw.suda.edu.cn",
 
"http://jyxy.suda.edu.cn",
 
"http://labcenter.suda.edu.cn",
 
"http://laowo.suda.edu.cn",
 
"http://law.suda.edu.cn",
 
"http://library.suda.edu.cn",
 
"http://lst.suda.edu.cn",
 
"http://ltc.suda.edu.cn",
 
"http://lxyz.suda.edu.cn"))
    custom_settings = {'DOWNLOAD_DELAY': 1,  # 下载延迟 3s
                       'ITEM_PIPELINES': {
                           'mySpider.pipelines.MyspiderPipeline4': 300
                       }
                       }
    
    def parse(self,response):
        self.parseCount = self.parseCount+1
        print("### %d 次循环 ###" % self.parseCount)
        print("### url_池大小 %d ###" % len(self.url_pool))
        
        url_pool_copy = copy.deepcopy(self.url_pool)
        for target in url_pool_copy:
            yield scrapy.FormRequest(target,callback=self.parsePage)
        print("### %d 次循环 ###" % self.parseCount)
        print("### url_池大小 %d ###" % len(self.url_pool))
        yield scrapy.Request('http://www.suda.edu.cn', self.parse, dont_filter=True)
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
