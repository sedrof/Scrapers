
import scrapy
from typing import Text
from scrapy.http.request import Request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class HamltonSpider(scrapy.Spider):
    name = 'hamlton'
    allowed_domains = ['www.hamiltonwatch.com']
    start_urls = ['https://www.hamiltonwatch.com/en-int/filter-by.html?p=1']

    # def remove_charachters(self, value):
    #     return value.strip(' \u00a3').strip('-\u00a3').strip('\u00a3').strip('0-\u00a3')

    # def __init__(self):
    #     options = Options()
    #     # options.add_argument("headless")
    #     options.add_experimental_option("excludeSwitches", ["enable-logging"])
    #     driver = webdriver.Chrome(
    #         executable_path=r"G:\chromedriver", options=options)
    #     driver.set_window_size(1920, 1080)
    #     driver.get(
    #         'https://www.hamiltonwatch.com/en-int/filter-by.html?p=1/')
    #     driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    #     time.sleep(8)
    #     self.html = driver.page_source

    def parse(self, response):
        # response = Selector(text=self.html)
        urls = response.xpath(
            "//a[@class='product-item-link']//@href").extract()
        print(urls, 'jjjjjjjjjj')
        for url in urls:
            # yield{
            #     "url": url
            # }
            yield Request(
                url,
                meta={"url": url},
                callback=self.parse_watch
            )

        next_page = response.xpath("//a[@role='next']//@href").extract_first()
        print(next_page, "ssddsssssssssssssssssss")
        if next_page:
            yield Request(
                next_page,
                callback=self.parse
            )

    def parse_watch(self, response):
        yield{
            'Model': response.xpath("//span[@data-ui-id='page-title-wrapper']//text()").get(),
            'Reference_number': response.xpath("//td[@data-th='Reference']//text()").extract(),
            'Collection': response.xpath("//td[@data-th='Collection']//text()").extract(),
            'Color_Case': response.xpath("//td[@data-th='Dial color']//text()").extract(),
            'Color_Strap': response.xpath("//td[@data-th='Strap color']//text()").extract(),
            'Description_Gender': response.xpath("//td[@data-th='Gender']//text()").extract(),
            'Case_Diameter_Case_material': response.xpath("//td[@data-th='Case material']//text()").extract(),
            'Material_Strap': response.xpath("//td[@data-th='Strap type']//text()").extract(),
            'Description_Movement': response.xpath("//div[@class='col-1-2-m']//p//text()").extract(),
            'caliber_Time_display/function': response.xpath("//td[@data-th='Power reserve']//text()").extract(),
            'Type_Clasp': response.xpath("//td[@data-th='Crystal']//text()").extract(),
            'Water_Resistant': response.xpath("//td[@data-th='Water Resistance']//text()").extract(),
            'Dial_description': response.xpath("//div[@data-content-type='text']//p//text()").extract(),
            'Link_product': response.meta['url'],
        }
