import scrapy


class ExeerSpider(scrapy.Spider):
    name = 'exeer'
    allowed_domains = ['worldpopulationreview.com']
    start_urls = ['http://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        rows = response.xpath("//table//tbody//tr")
        for row in rows:
            yield {
            'country_name' : row.xpath(".//td[1]//a//text()").get(),
            'country_debt' : row.xpath(".//td[2]//text()").get()
            }
