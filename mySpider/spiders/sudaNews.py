# -*- coding: utf-8 -*-
import scrapy
import re
from mySpider.items import sudaNewsItem


class SudanewsSpider(scrapy.Spider):
    name = 'sudaNews'
    # allowed_domains = ['http://www.suda.edu.cn/suda_news/sdyw/index.html']
    start_urls = ['http://www.suda.edu.cn/suda_news/sdyw/index.html']
    basic_url = "http://www.suda.edu.cn"

    def parse(self, response):
        node_list = response.xpath(
            "//td[@width='110']")
        # print('3123123')
        # print(node_list.extract())

        for node in node_list:
            item = sudaNewsItem()
            item['newsTime'] = node.xpath(
                './text()').extract()[0] if len(node.xpath(
                    './text()').extract()) > 0 else '1'

            item['newsHref'] = node.xpath(
                '../td[@width="650"]/a/@href').extract()[0] if len(node.xpath(
                    '../td[@width="650"]/a/@href').extract()) > 0 else '1'

            item['newsTitle'] = node.xpath(
                '../td[@width="650"]/a/text()').extract()[0] if len(node.xpath(
                    '../td[@width="650"]/a/text()').extract()) > 0 else '2'

            item['newsDepartMent'] = node.xpath(
                '../td[@width="200"]/text()').extract()[0] if len(node.xpath(
                    '../td[@width="200"]/text()').extract()) > 0 else '3'
            # item['newsDepartMent'] = 3
            print(item)
            print(111)
            yield item
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
            yield scrapy.Request(next_url, self.parse)
