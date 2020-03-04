# -*- coding: utf-8 -*-
import scrapy
import re
from mySpider.items import sudaMainItem
import pymysql


class SudaurlsSpider(scrapy.Spider):
    name = 'sudaurls'
    allowed_domains = ['www.suda.edu.cn', 'aff.suda.edu.cn', 'eng.suda.edu.cn', 'file.suda.edu.cn/',
                       'library.suda.edu.cn/', 'mail.suda.edu.cn', 'csteaching.suda.edu.cn']
    start_urls = ['http://www.suda.edu.cn']
    basic_url = 'http://www.suda.edu.cn'
    table_count = 0
    count = 0

    def parse(self, response):
        self.count = self.count+1
        #print('这是第', self.count, '个页面')
        # print('当前爬取页面'+response.request.url.strip('*/'))
        titles = response.xpath('//a/@href').extract()

        basic_url = response.request.url.strip('*/')

        url_list = []
        # 对于url进行拼接处理
        for url in titles:
            print(url)
            item = sudaMainItem()
            matchFullUrl = re.match(
                r'^(http|https)://([\w.]+/?)\S*', url, re.M | re.I)
            matchRelateUrl = re.match(r'^/([\w.]?/?)\S*', url, re.M | re.I)
            matchRelateUrl2 = re.match(r'^[^/]([\w.]?/?)\S*', url, re.M | re.I)

            if url:
                if matchFullUrl:
                    true_url = url
                    print('原始url', true_url)
                elif matchRelateUrl:
                    true_url = basic_url+url
                    print('拼接url1', true_url)
                elif matchRelateUrl2:
                    true_url = basic_url+'/'+url
                    print('拼接url2', true_url)
                else:
                    true_url = url
                    print('未处理且未匹配', true_url)
                item['father'] = basic_url
                item['url'] = true_url
                yield item
        url_list = self.getDistinctUrls()
        print(url_list)
        for next_url in url_list:
            if 'http://' in next_url or 'https://' in next_url:
                yield scrapy.Request(next_url, self.parse, dont_filter=True)
            else:
                yield scrapy.Request('http://'+next_url, self.parse, dont_filter=True)

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
