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


class UpworkTenderSpider(scrapy.Spider):
    name = 'upwork_tender'
    start_urls = [
        'https://bidstats.uk/tenders/?q=Embedded&ntype=tender']

    def remove_charachters(self, value):
        return value.strip(' \u00a3').strip('-\u00a3').strip('\u00a3').strip('0-\u00a3')

    def __init__(self):
        options = Options()
        # options.add_argument("headless")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(
            executable_path=r"G:\chromedriver", options=options)
        driver.set_window_size(1920, 1080)
        driver.get(
            'https://bidstats.uk/tenders/?q=Embedded&ntype=tender')
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        time.sleep(6)
        self.html = driver.page_source

    def parse(self, response):
        response = Selector(text=self.html)
        url = response.xpath(
            "//div[@class='nl-batch']//li//a//@href").extract()
        print(url, 'jjjjjjjjjj')
        for product in url:
            prod = f'https://www.wyndhamhotels.com{product}'
            yield Request(
                prod,
                meta={"url": prod},
                callback=self.parse_festival
            )

    def parse_festival(self, response):
        # self.driver.get(
        #     response.meta['url'])
        # button = self.driver.
        yield{
            'Title': self.remove_charachters(response.xpath("//h1//text()").get()),
            'Name_of_the_company': response.xpath("//li[@class='loc-card loc-card-buyer']//a//text()").extract(),
            'Request_Category': response.xpath("//ul[@class='ctags-list']//a//text()").extract(),
            'Description': self.remove_charachters(response.xpath("//section[@id='notice-descrip']//p//text()").get()),
            'Estimated_Value': self.remove_charachters(response.xpath("//*[@id='notice-keydata']/div[1]/dl/dd[4]//text()").get()),
            'Supplier_info': response.xpath("//ul[@class='ctags-list']//a//text()").extract(),
            'Link': response.meta['url'],
            'Keyword': 'IoT'
        }
