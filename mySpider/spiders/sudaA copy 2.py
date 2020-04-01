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
    name = 'sudaM'
    parseCount=0
    allowed_domains = [
 
"marxism.suda.edu.cn",
 
"math.suda.edu.cn",
 
"medical.suda.edu.cn",
 
"museum.suda.edu.cn",
 
"music.suda.edu.cn",
 
"my.suda.edu.cn",
 
"mycs.suda.edu.cn",
 
"nano.suda.edu.cn",
 
"neuroscience.suda.edu.cn",
 
"oa.suda.edu.cn",
 
"oese.suda.edu.cn",
 
"oversea.suda.edu.cn",
 
"pac.suda.edu.cn",
 
"pharm.suda.edu.cn",
 
"physics.suda.edu.cn",
 
"qzdgw.suda.edu.cn",
 
"report.suda.edu.cn",
 
"rsc.suda.edu.cn",
 
"rules.suda.edu.cn",
 
"rurc.suda.edu.cn",
 
"sbc.suda.edu.cn",
 
"sc.suda.edu.cn",
 
"scit.suda.edu.cn",
 
"scst.suda.edu.cn",
 
"sdbn.suda.edu.cn",
 
"sdgcxl.suda.edu.cn",
 
"sdh.suda.edu.cn",
 
"sdkjy.suda.edu.cn",
 
"sdss.suda.edu.cn",
 
"sdttc.suda.edu.cn",
 
"sdxb.suda.edu.cn",
 
"sdzy.suda.edu.cn",
 
"sfl.suda.edu.cn",
 
"shpg.suda.edu.cn",
 
"shxy.suda.edu.cn",
 
"skc.suda.edu.cn",
 
"snfz.suda.edu.cn",
 
"ssis.suda.edu.cn",
 
"sudabao.suda.edu.cn",
 
"sutt.suda.edu.cn",
 
"sxy.suda.edu.cn",
 
"sylc.suda.edu.cn",
 
"szdxrwb.suda.edu.cn",
 
"szdxyy.suda.edu.cn",]
    start_urls = ["http://marxism.suda.edu.cn",]
    # basic_url_init = 'http://www.suda.edu.cn'
    # basic_url = 'http://www.suda.edu.cn'
    # table_count = 0
    url_pool = set((
 
"http://marxism.suda.edu.cn",
 
"http://math.suda.edu.cn",
 
"http://medical.suda.edu.cn",
 
"http://museum.suda.edu.cn",
 
"http://music.suda.edu.cn",
 
"http://my.suda.edu.cn",
 
"http://mycs.suda.edu.cn",
 
"http://nano.suda.edu.cn",
 
"http://neuroscience.suda.edu.cn",
 
"http://oa.suda.edu.cn",
 
"http://oese.suda.edu.cn",
 
"http://oversea.suda.edu.cn",
 
"http://pac.suda.edu.cn",
 
"http://pharm.suda.edu.cn",
 
"http://physics.suda.edu.cn",
 
"http://qzdgw.suda.edu.cn",
 
"http://report.suda.edu.cn",
 
"http://rsc.suda.edu.cn",
 
"http://rules.suda.edu.cn",
 
"http://rurc.suda.edu.cn",
 
"http://sbc.suda.edu.cn",
 
"http://sc.suda.edu.cn",
 
"http://scit.suda.edu.cn",
 
"http://scst.suda.edu.cn",
 
"http://sdbn.suda.edu.cn",
 
"http://sdgcxl.suda.edu.cn",
 
"http://sdh.suda.edu.cn",
 
"http://sdkjy.suda.edu.cn",
 
"http://sdss.suda.edu.cn",
 
"http://sdttc.suda.edu.cn",
 
"http://sdxb.suda.edu.cn",
 
"http://sdzy.suda.edu.cn",
 
"http://sfl.suda.edu.cn",
 
"http://shpg.suda.edu.cn",
 
"http://shxy.suda.edu.cn",
 
"http://skc.suda.edu.cn",
 
"http://snfz.suda.edu.cn",
 
"http://ssis.suda.edu.cn",
 
"http://sudabao.suda.edu.cn",
 
"http://sutt.suda.edu.cn",
 
"http://sxy.suda.edu.cn",
 
"http://sylc.suda.edu.cn",
 
"http://szdxrwb.suda.edu.cn",
 
"http://szdxyy.suda.edu.cn"))
    custom_settings = {
                       'ITEM_PIPELINES': {
                           'mySpider.pipelines.MyspiderPipeline5': 300
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
