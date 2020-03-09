# -*- coding: utf-8 -*-
import scrapy


class SudatestSpider(scrapy.Spider):
    name = 'sudatest'
    # allowed_domains = [''http://oese.suda.edu.cn/0f/b4/c14883a331700/page.htm/main.psp'']
    start_urls = ["http://oese.suda.edu.cn/0f/b4/c14883a331700/page.htm/main.psp"]

    def parse(self, response):
         # print(response.body)
        titles = response.xpath('///a/@href').extract()
        print(titles)
    