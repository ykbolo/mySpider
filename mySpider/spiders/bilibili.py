# -*- coding: utf-8 -*-
import scrapy


class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    # allowed_domains = ['https://www.bilibili.com/video/av86983604?spm_id_from=333.851.b_62696c695f7265706f72745f646f756761.3']
    start_urls = [
        'https://api.bilibili.com/x/v1/dm/list.so?oid=148642480']

    def parse(self, response):
        # print(response.body)
        titles = response.xpath(
            '//d/text()').extract()
        # print(titles)
        count = 0
        for i in titles:
            count = count+1
            print(i)
        print('总弹幕：', count)
