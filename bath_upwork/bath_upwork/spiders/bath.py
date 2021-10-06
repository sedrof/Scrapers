import scrapy
from scrapy import loader
from scrapy.http import Request
from scrapy.loader import ItemLoader
from bath_upwork.items import BathUpworkItem


class BathSpider(scrapy.Spider):
    name = 'bath'
    allowed_domains = ['fairmontdesigns.com']
    start_urls = ['https://www.fairmontdesigns.com/bath/products']

    def parse(self, response):
        products = response.xpath(
            "//div[@class='tri_box']//h2//@href").extract()
        for product in products:
            yield Request(product,
                          callback=self.parse_product)

    def parse_product(self, response):
        product_name = response.xpath('//h2//@href').extract()
        for product in product_name:
            yield Request(product,
                          callback=self.parse_product_2)

    def parse_product_2(self, response):
        product_name = response.xpath('//h2//@href').extract()
        for product in product_name:
            yield Request(product,
                          callback=self.parse_product_3)

    def parse_product_3(self, response):
        product_name = response.xpath('//h2//@href').extract()
        for product in product_name:
            yield Request(product,
                          callback=self.parse_product_4)

    def parse_product_4(self, response):
        product_name = response.xpath('//h2//@href').extract()
        for product in product_name:
            yield Request(product,
                          meta={"url": product},
                          callback=self.parse_product_5)

    def remove_space(self, value):
        if type(value) == str:
            return value.replace('\xa030', ' ')
        return value

    def parse_product_5(self, response):
        # product_name = response.xpath('//h2//@href').extract()
        link= response.xpath('//*[@id="specs1"]/a/@href').get()
        # loader = ItemLoader(item=BathUpworkItem(), selector=link)
        # loader.add_value('files_url',link)
        yield Request(
            link,
            callback=self.pdf_download
        )



    def pdf_download(self, response):
        """ Save pdf files """
        path = response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as file:
            file.write(response.body)

        # Dimention = self.remove_space(response.xpath(
        #     "//following::*[@id='details1']/p[2]/text()[1]").get())
        # # Dimention.replace('\xa030', ' ')

        # Finish = response.xpath("//div[@id='details1']/p[2]/text()").extract()[2]
        # Materials = self.remove_space(response.xpath(
        #     '//*[@id="specs1"]/p[1]/text()[1]').get())
        # drawer = self.remove_space(response.xpath(
        #     '//*[@id="specs1"]/p[1]/text()[3]').get())
        # drawer_box = self.remove_space(response.xpath(
        #     '//*[@id="specs1"]/p[1]/text()[5]').extract()[0])
        # yield{
        #     "url": response.meta['url'],
        #     "SKU": response.xpath("//h2[@class='small_title']//text()").extract(),
        #     "Product Title": response.xpath("//div[@class='row page_title']//h1//text()").extract(),
        #     "Description": response.xpath("//div[@id='details1']//p[1]//text()").extract(),
        #     "Dimensions": Dimention,
        #     "Finish": Finish,
        #     "Specification 1": f"Materials:{Materials}",
        #     "Specification 2": f"Drawer:{drawer}",
        #     "Specification 3": f"Drawer_box:{drawer_box}"

        # }
