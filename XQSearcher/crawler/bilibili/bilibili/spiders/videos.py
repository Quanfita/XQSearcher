# -*- coding: utf-8 -*-
import scrapy
from ..items import BilibiliItem


class VideosSpider(scrapy.Spider):
    name = 'videos'
    item = BilibiliItem()
    allowed_domains = ['bilibili.com']
    #start_urls = ['http://www.bilibili.com/video/av109900']

    def start_requests(self):
        urls = ['https://www.bilibili.com/video/av'+str(x) for x in range(300000,500000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #/html/head/title
        self.item['url'] = str(response).split(' ')[-1].split('>')[0]
        self.item['title'] = response.xpath('/html/head/title/text()').extract()[0].split('_')[0]
        self.item['target'] = response.xpath('/html/head/title/text()').extract()[0].split('_')[-1].split('-bilibili')[0]
        self.item['site'] = response.xpath('/html/head/title/text()').extract()[0].split('-')[-1]
        self.item['uid'] = '/bili_'+str(response).split(' ')[-1].split('>')[0].split('/')[-1]
        try:
            self.item['content'] = str(response.xpath('//*[@id="v_desc"]/div/text()').extract()[0])
        except:
            self.item['content'] = ''
        yield self.item

    def check(self):
        urls = ['https://www.bilibili.com/video/av'+str(x) for x in range(40000000)]
        for url in urls:
            scrapy.Request(url=url, callback=self.parse)
