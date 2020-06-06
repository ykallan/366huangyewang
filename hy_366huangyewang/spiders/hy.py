# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import Hy366HuangyewangItem


class HySpider(scrapy.Spider):
    name = 'hy'
    # name : hy336
    start_urls = ['http://www.366x24.com/com/', 'http://www.366x24.com/gq/']
    contact_tail = 'contact/'
    mobile_header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[1], callback=self.gongqiu)

    def gongqiu(self, response):
        hangyes = response.xpath('//div[@class="homecatlist"]/ul/li/a/@href').getall()
        for hangye in hangyes:
            yield scrapy.Request(url=hangye, callback=self.things_list)

    def things_list(self, response):
        things = response.xpath('//td[@align="left"]//a/@href').getall()
        for thing in things:
            yield scrapy.Request(url=thing, callback=self.thing_detail)

    def thing_detail(self, response):
        mobile_html = re.findall(r'format=html5;url=(.*?)">', response.text)[0]
        yield scrapy.Request(url=mobile_html, callback=self.mobile_page, headers=self.mobile_header)

    def mobile_page(self, response):
        com_name = response.xpath('//div[@id="c_2"]/div/ul/li[1]/a/text()').get()
        cont_person = response.xpath('//div[@id="c_2"]/div/ul/li[3]/text()').get()
        cont_phone = response.xpath('//div[@id="c_2"]/div/ul/li[4]/a/text()').get()
        if cont_phone is None:
            try:
                cont_phone = re.findall(r'href="tel:(\d{11})">', response.text)[0]
            except IndexError as e:
                cont_phone = None
        if cont_phone is None:
            try:
                cont_phone = re.findall(r'href="tel:(\d{4}-\d)">', response.text)[0]
            except IndexError :
                cont_phone = '空'
        loc = response.xpath('//div[@id="c_2"]/div/ul/li[last()-1]/text()').get()
        address_detail = response.xpath('//div[@id="c_2"]/div/ul/li[last()]/a/text()').get()
        item = Hy366HuangyewangItem()
        item['com_name'] = com_name
        item['cont_person'] = cont_person
        item['cont_phone'] = cont_phone
        item['loc'] = loc
        item['address_detail'] = address_detail
        # print(com_name, cont_person, cont_phone, loc, address_detail)
        yield item









