# -*- coding: utf-8 -*-
import scrapy
import re
from mySpider.items import sudaMainItem
import pymysql


class SudaurlsSpider(scrapy.Spider):
    name = 'sudaurls'
    allowed_domains = ['www.suda.edu.cn', 'http://aff.suda.edu.cn', 'http://eng.suda.edu.cn', 'http://file.suda.edu.cn/',
                       'http://library.suda.edu.cn/', 'http://mail.suda.edu.cn', 'http://csteaching.suda.edu.cn']
    start_urls = ['http://www.suda.edu.cn']
    basic_url = 'http://www.suda.edu.cn'
    table_count = 0

    def parse(self, response):
        print('当前爬取页面'+response.request.url.strip('*/'))
        titles = response.xpath('//a/@href').extract()

        basic_url = response.request.url.strip('*/')

        url_list = []
        # 对于url进行拼接处理
        for url in titles:
            item = sudaMainItem()
            matchTrueUrl = re.match(r'^[http|https]', url, re.M | re.I)
            matchIp = re.match(
                r'^(((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}', url, re.M | re.I)
            matchPart1 = re.match(r'^/', url, re.M | re.I)
            matchPart2 = re.match(r'^\w', url, re.M | re.I)
            matchEmail = re.match(r'.+@.+', url, re.M | re.I)
            if matchEmail == None and url != '':
                if matchTrueUrl or matchIp:
                    true_url = url
                    # print('原始url', true_url)
                elif matchPart1:
                    true_url = basic_url+url
                    # print('拼接url1', true_url)
                elif matchPart2:
                    true_url = basic_url+'/'+url
                    # print('拼接url2', true_url)
                else:
                    true_url = url
                item['father'] = basic_url
                item['url'] = true_url
                yield item
        url_list = self.getDistinctUrls()
        # print(url_list)
        for next_url in url_list:
            if 'http://' in next_url or 'https://' in next_url:
                yield scrapy.Request(next_url, self.parse, dont_filter=True)
            else:
                yield scrapy.Request('http://'+next_url, self.parse, dont_filter=True)
        #         # yield scrapy.FormRequest
        # url_list = self.getUrlFromDatabase(
        #     'spiderurls%s' % (self.table_count), 'spiderurls%s' % (self.table_count+1))

    def getDistinctUrls(self):
        url_list = []
        self.db = pymysql.connect(
            "localhost", "root", "yk84732225", "spiderurl")
        self.cursor = self.db.cursor()
        sql = "SELECT DISTINCT url FROM urllist"
        self.cursor.execute(sql)
        # self.db.commit()  # 重点在这
        alldata = self.cursor.fetchall()
        for data in alldata:
            url_list.append(data[0])
        return url_list
