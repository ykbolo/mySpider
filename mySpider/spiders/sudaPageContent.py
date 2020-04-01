# -*- coding: utf-8 -*-
import scrapy


class SudapagecontentSpider(scrapy.Spider):
    name = 'sudaPageContent'
    # allowed_domains = ['www.suda.edu.cn']
    start_urls = ['http://www.suda.edu.cn/']

    def parse(self, response):
        print(response)
