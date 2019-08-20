# -*- coding: utf-8 -*-
import scrapy
from HPPIC.items import HppicItem
from scrapy.selector import Selector
from scrapy.http import Request
from urllib.parse import urljoin

class HpscrapySpider(scrapy.Spider):
    name = 'hpscrapy'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/photos/photo/443406457/']

    def parse(self, response):
        item = HppicItem()
        selector = Selector(response)
        pic = selector.xpath('//div[@class="article"]')
        for p in pic:
            links = p.xpath('div[@class="photo-show"]/div[@class="photo-wp"]/a/img/@src').extract()
            #nums = p.xpath('div[@class="opt-bar-line clearfix"]/span/text()').extract()
            nums = links[0].split('/')[-1].replace('.jpg','')
            item['links'] = links
            item['nums'] = nums
            yield item
        next_link = selector.xpath('//span[@class="opt-mid"]/a[@id="next_photo"]/@href').extract()
        print('内容已爬取')
        if next_link:
            next_link = next_link[0]
            yield Request(next_link, callback =self.parse)
