import scrapy


class PozzaSpider(scrapy.Spider):
    name = 'pozza'
    allowed_domains = ['https://slicelife.com/pizza-delivery/ny-new_york']
    start_urls = ['http://https://slicelife.com/pizza-delivery/ny-new_york/']

    def parse(self, response):
        pass
