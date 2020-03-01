# -*- coding: utf-8 -*-
import scrapy

from mySpider.items import sudaMainItem


class SudamainSpider(scrapy.Spider):
    name = 'sudaMain'
    # allowed_domains = ['suda.edu.cn']
    start_urls = ['http://www.suda.edu.cn/']

    def parse(self, response):
        # print(response.body)
        titles = response.xpath('///a/@href').extract()
        for i in titles:
            item = sudaMainItem()
            item['father'] = 'suda.edu.cn'
            item['url'] = i
            yield item
        # pass
        next_url = response.xpath("//input[@value='后页']/@onclick").extract()[0]
        if next_url:
            # next_url = re.replace('javascript:goto(')
            # next_url = "javascript:goto('/suda_news/sdyw/index_1.html')"
            # p1 = re.compile(r"[('](.*?)[')]", re.S)  # 最小匹配
            p2 = re.compile("'(.*)'")
            next_url2 = re.findall(p2, next_url)
            # next_url2[0] = next_url2[0].replace(r'\'', '')
            next_url = self.basic_url+next_url2[0]
            print(self.basic_url+next_url2[0])
            yield scrapy.Request(next_url, self.parse2)

    def parse(self, response):
