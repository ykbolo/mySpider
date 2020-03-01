# -*- coding: utf-8 -*-
import scrapy
import re
from mySpider.items import sudaMainItem


class SudaurlsSpider(scrapy.Spider):
    name = 'sudaurls'
    allowed_domains = ['www.suda.edu.cn']
    start_urls = ['http://www.suda.edu.cn/', ]
    basic_url = 'http://www.suda.edu.cn'

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
                    print('原始url', true_url)
                elif matchPart1:
                    true_url = basic_url+url
                    print('拼接url1', true_url)
                elif matchPart2:
                    true_url = basic_url+'/'+url
                    print('拼接url2', true_url)
                else:
                    true_url = url
                item['father'] = basic_url
                item['url'] = true_url
                url_list.append(true_url)
                yield item

        for nextUrl in url_list:
            if nextUrl:
                yield scrapy.Request(url=nextUrl, callback=self.parse2)
        #         # yield scrapy.FormRequest

    def parse2(self, response):
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
                    print('原始url', true_url)
                elif matchPart1:
                    true_url = basic_url+url
                    print('拼接url1', true_url)
                elif matchPart2:
                    true_url = basic_url+'/'+url
                    print('拼接url2', true_url)
                else:
                    true_url = url
                item['father'] = basic_url
                item['url'] = true_url
                url_list.append(true_url)
                yield item
