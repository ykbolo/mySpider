# -*- coding: utf-8 -*-
import scrapy


class SudamainSpider(scrapy.Spider):
    name = 'sudaMain'
    # allowed_domains = ['suda.edu.cn']
    start_urls = ['http://www.suda.edu.cn/suda_news/sdyw/index.html']

    def parse(self, response):
        # print(response.body)
        titles = response.xpath('//td[3]/a/text()').extract()
        for i in titles:
            print(i)

        # pass
