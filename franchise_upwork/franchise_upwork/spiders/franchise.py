import scrapy
from scrapy.http import Request


class FranchiseSpider(scrapy.Spider):
    name = 'franchise'
    allowed_domains = ['entrepreneur.com']
    start_urls = ['https://www.entrepreneur.com/franchise500']

    def parse(self, response):
        # absolute_url = 'https://www.entrepreneur.com/franchise500'
        products = response.xpath(
            "//div[@class='min-w-0 flex-1 items-center px-4 md:grid md:grid-cols-4 auto-cols-max md:gap-4']//a[@class='block']//@href").extract()
        # print(products, 'ssssssssssssssssssssssssssssssssssssssssssssssssss')
        for product in products:
            prod = f"https://www.entrepreneur.com/franchise500{product}"
            # print(prod, 'vvvvvvvvvvvvvvv')
            yield Request(prod, callback=self.parse_shoe)

        next_page = response.xpath(
            "//a[@class='ga-click relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50']//@href").get()
        print(next_page)
        if next_page:
            abs_url = f"https://www.entrepreneur.com{next_page}"
            print(abs_url, "fffffffff")
            yield Request(
                abs_url,
                callback=self.parse)

    def parse_shoe(self, response):
        # product_name = response.xpath(
        #     '//div[@class='lg: flex lg: items-baseline lg: justify-between text-2xl leading-8 font-semibold text-white']//span').extract()
        product_name = response.xpath(
            "//span[contains(text(),'#')]//text()").get()
        # if len(product_name) > 0:
        #     rank = product_name.split()[0].strip('#')
        #     print(rank, "fffffffffffffffff")

        yield{"name": product_name}
# rank.split()[9].strip('#')
