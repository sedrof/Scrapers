import scrapy


class CodingScrapSpider(scrapy.Spider):
    name = 'coding_scrap'
    allowed_domains = ['www.codegrepper.com/code-examples/python']
    start_urls = ['http://www.codegrepper.com/code-examples/python/']

    def parse(self, response):
        pass
