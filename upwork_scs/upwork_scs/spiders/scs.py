# -*- coding: utf-8 -*-
import json
from scrapy import Spider
from scrapy.http import Request


class ShoesSpider(Spider):
    name = 'scs'
    allowed_domains = ['sustainablesupply.com']
    start_urls = [
        'https://www.sustainablesupply.com/collections/adhesives-tape-sealants']

    def parse(self, response):
        absolute_url = 'www.sustainablesupply.com'
        products = response.xpath(
            '//section//div//div[2]//div//div//a///@href').extract()
        print(products, 'ssssssssssssssssssssssssssssssssssssssssssssssssss')
        for product in products:
            prod = f"{absolute_url}{product}"
            yield Request(prod,
                          callback=self.parse_shoe)
        next_page = response.xpath(
            '//a[@data-test-paginate-next="true"]/@href').get()

        next_page_url = response.xpath(
            '//*[@id="searchspring-content"]/section/div/div[3]/div/div/div/a//@href').extract()
        if next_page_url:
            yield Request(next_page_url,
                          callback=self.parse)

    def parse_shoe(self, response):
        product_name = response.xpath(
            '//div[@class="product-meta"]//h1//text()').extract()

        yield{"name": product_name}
