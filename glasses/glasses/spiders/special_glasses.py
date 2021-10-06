import scrapy


class SpecialGlassesSpider(scrapy.Spider):
    name = 'special_glasses'
    allowed_domains = ['www.glassesshop.com/bestsellers']
    start_urls = ['http://www.glassesshop.com/bestsellers/']

    def parse(self, response):
        glass_div = response.xpath("//div[@class='row pt-lg-5 product-list column-1']//div[@class='col-12 pb-5 mb-lg-3 col-lg-4 product-list-row text-center product-list-item']")
        for row in glass_div:
            yield {
                'name': row.xpath("normalize-space(.//div[@class='p-title']//a//text())").get(),
                'url' : row.xpath(".//div[@class='p-title'][1]//@href").get()

            }

