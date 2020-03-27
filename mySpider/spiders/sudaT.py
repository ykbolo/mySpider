# -*- coding: utf-8 -*-
import scrapy
import re
from mySpider.items import sudaMainItem
import pymysql
import copy
from urllib.request import urlparse
from urllib.parse import urljoin


class SudaMainSpider(scrapy.Spider):
    name = 'sudaT'
    allowed_domains = ["tec.suda.edu.cn",
 
"textile.suda.edu.cn",
 
"tjxh.suda.edu.cn",
 
"twzsy.suda.edu.cn",
 
"tyxy.suda.edu.cn",
 
"tzb.suda.edu.cn",
 
"uninews.suda.edu.cn",
 
"welcome.suda.edu.cn",
 
"wg.suda.edu.cn",
 
 
"wx.suda.edu.cn",
 
"wxy.suda.edu.cn",
 
"xb.suda.edu.cn",
 
"xcb.suda.edu.cn",
 
"xdgx.suda.edu.cn",
 
"xiaoqing.suda.edu.cn",
 
"xjj.suda.edu.cn",
 
"xk.suda.edu.cn",
 
"xlzx.suda.edu.cn",
 
"xsc.suda.edu.cn",
 
"xsh.suda.edu.cn",
 
"yanhui.suda.edu.cn",
 
"yjs.suda.edu.cn",
 
"youth.suda.edu.cn",
 
"ysxy.suda.edu.cn",
 
"yxbfzb.suda.edu.cn",
 
"zbzx.suda.edu.cn",
 
"zcpt.gzc.suda.edu.cn",
 
"zjc.suda.edu.cn",
 
"zqsy.suda.edu.cn",
 
"zsb.suda.edu.cn",
 
"zzb.suda.edu.cn",
 
]
    start_urls = ["http://tec.suda.edu.cn",]
    # basic_url_init = 'http://www.suda.edu.cn'
    # basic_url = 'http://www.suda.edu.cn'
    # table_count = 0
    url_pool = set((
 "http://tec.suda.edu.cn",
 
"http://textile.suda.edu.cn",
 
"http://tjxh.suda.edu.cn",
 
"http://twzsy.suda.edu.cn",
 
"http://tyxy.suda.edu.cn",
 
"http://tzb.suda.edu.cn",
 
"http://uninews.suda.edu.cn",
 
"http://welcome.suda.edu.cn",
 
"http://wg.suda.edu.cn",
 
 
"http://wx.suda.edu.cn",
 
"http://wxy.suda.edu.cn",
 
"http://xb.suda.edu.cn",
 
"http://xcb.suda.edu.cn",
 
"http://xdgx.suda.edu.cn",
 
"http://xiaoqing.suda.edu.cn",
 
"http://xjj.suda.edu.cn",
 
"http://xk.suda.edu.cn",
 
"http://xlzx.suda.edu.cn",
 
"http://xsc.suda.edu.cn",
 
"http://xsh.suda.edu.cn",
 
"http://yanhui.suda.edu.cn",
 
"http://yjs.suda.edu.cn",
 
"http://youth.suda.edu.cn",
 
"http://ysxy.suda.edu.cn",
 
"http://yxbfzb.suda.edu.cn",
 
"http://zbzx.suda.edu.cn",
 
"http://zcpt.gzc.suda.edu.cn",
 
"http://zjc.suda.edu.cn",
 
"http://zqsy.suda.edu.cn",
 
"http://zsb.suda.edu.cn",
 
"http://zzb.suda.edu.cn",
 
))
    custom_settings = {'DOWNLOAD_DELAY': 1,  # 下载延迟 3s
                       'ITEM_PIPELINES': {
                           'mySpider.pipelines.MyspiderPipeline6': 300
                       },
                       'DOWNLOAD_TIMEOUT': 5
                       }
    def parse(self, response):
        # self.count = self.count+1
        #print('这是第', self.count, '个页面')
        print('当前爬取页面'+response.request.url.strip('*/'))
        print('当前集合大小', len(self.url_pool))
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
        url_pool_copy = copy.deepcopy(self.url_pool)
        # url_pool_copy = list(self.url_pool)

        for next_url in url_pool_copy:
            # print('这是第', index, '个元素')
            if 'http://' in next_url or 'https://' in next_url:
                yield scrapy.Request(next_url, self.parse, dont_filter=False)
            else:
                yield scrapy.Request('http://'+next_url, self.parse, dont_filter=False)

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
