# -*- coding: utf-8 -*-
import scrapy
# 吧文本结构化存储到json文件中
import html as ht
from lxml import html
class SudatestSpider(scrapy.Spider):
    name = 'sudatest'
    # allowed_domains = [''http://oese.suda.edu.cn/0f/b4/c14883a331700/page.htm/main.psp'']
    start_urls = ["http://www.suda.edu.cn",]

    def parse(self, response):
        tree = html.fromstring(response.body)
        ele = tree.xpath('//script | //noscript| //style') 
        for e in ele:
          e.getparent().remove(e)
        # Html= html.tostring(tree).decode()   #tostring()返回的是bytes类型，decode()转成字符串
        # print(ht.unescape(Html))    #unescape()将字符串中的uncode变化转成中文
        treetxt = tree.xpath('//text()')
        for index in range(len(treetxt)):
          treetxt[index]=treetxt[index].strip().replace('\t','').replace('\n','').replace('\r','')
        # print(''.join(treetxt))
        title = tree.xpath('//title/text()')
        description = tree.xpath("//meta[@name='description']/@content")
        keywords= tree.xpath("//meta[@name='keywords']/@content")
        imgs = tree.xpath("//img/@alt")
        url = response.request.url.strip('*/')
        # print(''.join(title))
        # print(''.join(description))
        # print(''.join(keywords))
        # print(''.join(imgs))
        # print(''.join(treetxt))
        dict={}
        dict['x']=1

    