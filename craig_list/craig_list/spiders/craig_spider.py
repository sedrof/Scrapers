import scrapy


class CraigSpiderSpider(scrapy.Spider):
    name = "craig_spider"
    allowed_domains = ["newyork.craigslist.org"]
    start_urls = ["https://newyork.craigslist.org/search/egr"]

    def parse(self, response):
        pass
