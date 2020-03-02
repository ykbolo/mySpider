# -*- coding: utf-8 -*-
import scrapy
import re
from mySpider.items import sudaMainItem
import pymysql


class SudaurlsSpider(scrapy.Spider):
    name = 'sudaurls'
    allowed_domains = ['www.suda.edu.cn']
    start_urls = ['http://www.suda.edu.cn/', ]
    basic_url = 'http://www.suda.edu.cn'
    table_count = 0

    def parse(self, response):
        print('当前爬取页面'+response.request.url.strip('*/'))
        titles = response.xpath('//a/@href').extract()
        titles.append('192.124.33.22')
        titles.append('mailto:szdx@suda.edu.cn')
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
                url_list.append(true_url)
                yield item

        self.db = pymysql.connect(
            "localhost", "root", "yk84732225", "spiderurl")
        self.cursor = self.db.cursor()
        sql2 = "SELECT DISTINCT url FROM spiderurls"
        self.cursor.execute(sql2)

        alldata = self.cursor.fetchall()
        for data in alldata:
            url_list.append(data[0])
        print('first', url_list)

        sql = "CREATE TABLE spiderurls0 AS SELECT DISTINCT url FROM spiderurls"
        self.cursor.execute(sql)
        self.db.commit()  # 重点在这
        count = 0
        # print(len(url_list))
        for nextUrl in url_list[1:5]:
            if nextUrl:
                count = count+1
                print("count:", count)

                yield scrapy.Request(url=nextUrl, callback=self.parse)
        #         # yield scrapy.FormRequest
        url_list = self.getUrlFromDatabase(
            'spiderurls%s' % (self.table_count), 'spiderurls%s' % (self.table_count+1))

    def parse2(self, response):
        print('当前爬取页面'+response.request.url.strip('*/'))
        titles = response.xpath('//a/@href').extract()
        titles.append('192.124.33.22')
        titles.append('mailto:szdx@suda.edu.cn')
        basic_url = response.request.url.strip('*/')
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

    def getUrlFromDatabase(self, table_before, table_after):
        url_list = []
        self.table_count = self.table_count+1
        self.db = pymysql.connect(
            "localhost", "root", "yk84732225", "spiderurl")
        self.cursor = self.db.cursor()
        sql = "CREATE TABLE %s AS SELECT DISTINCT url FROM %s" % (
            table_after, table_before)
        sql2 = "SELECT url From %s" % (table_after)
        self.cursor.execute(sql)
        self.cursor.execute(sql2)
        # self.db.commit()  # 重点在这
        alldata = self.cursor.fetchall()
        for data in alldata:
            url_list.append(data[0])
        print('url已去重，重置url_list', url_list)
        return url_list
