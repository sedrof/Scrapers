import scrapy
from scrapy.http.request import Request
from scrapy_selenium import SeleniumRequest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



class FestivalSpider(scrapy.Spider):
    name = 'festival'

    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.fatsoma.com/search?page=1&query=manchester',
            wait_time=20,
            # screenshot=True,
            wait_until=EC.element_to_be_clickable(
                (By.XPATH, '//a[text()="Next →"]')),
            callback=self.parse
        )

    def parse(self, response):
        absolute_url = 'www.fatsoma.com'
        products = response.xpath('//h3//@href').getall()
        for product in products:
            prod = f'https://fatsoma.com{product}'
            yield Request(
                prod,
                callback=self.parse_festival
            )
        next_page = response.xpath(
            '//a[@data-test-paginate-next="true"]/@href').get()
        print(next_page, "nextttttttttttttttttttttt")
        if next_page:
            abs_url = f'https://fatsoma.com{next_page}'
            yield SeleniumRequest(
                url=abs_url,
                wait_time=6,
                wait_until=EC.element_to_be_clickable(
                    (By.XPATH, '//a[text()="Next →"]')),
                callback=self.parse
            )

    def parse_festival(self, response):
        name = response.xpath('//h1//text()').extract()
        price = response.xpath(
            '//div[@class="_info_18h6hu"][3]//text()[3]').extract()
        location = response.xpath(
            '//div[@class="_info_18h6hu"][2]//text()[3]').extract()
        date_of_festival = response.xpath(
            'div[@class="_info_18h6hu"]//span//text()').extract_first()
        yield{
            "name": name,
            "date_of_festival": date_of_festival,
            "location": location,
            "price": price
        }

//div[@class='psrk-popup-header']//a[@class='_flyout-header__expand']//@href