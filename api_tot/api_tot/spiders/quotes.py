from scrapy import Spider
import json


class QuotesSpider(Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://developers.upwork.com/_static/js/apidocs.json"]

    def parse(self, response):
        pass
