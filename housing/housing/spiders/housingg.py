import scrapy


class HousinggSpider(scrapy.Spider):
    name = 'housingg'
    allowed_domains = ['lims.bchousing.org/']
    start_urls = ['https://lims.bchousing.org/LIMSPortal/registry/Newhomes']

    def parse(self, response):

        search = 
        for product in response.xpath("//div[@class="row col-md-4"]//option"):

