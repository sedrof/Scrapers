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


class HotelSpider(scrapy.Spider):
    name = 'hotel'
    start_urls = [
        'http://www.wyndhamhotels.com/locations?ICID=IN%3AUM%3A20190422%3AHPCM2%3AGREATSTAY%3ALOCATIONS%3ANA/']

    def parse(self, response):
        pass

    def __init__(self):
        # proxy = "124.240.187.80:82"

        # webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        #     "httpProxy": proxy,
        #     "ftpProxy": proxy,
        #     "sslProxy": proxy,
        #     "noProxy": None,
        #     "proxyType": "MANUAL",
        #     "class": "org.openqa.selenium.Proxy",
        #     "autodetect": False
        # }
        options = Options()
        # options.add_argument("headless")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(
            executable_path=r"G:\chromedriver", options=options)
        self.driver.set_window_size(1920, 1080)
        self.driver.get(
            'http://www.wyndhamhotels.com/locations?ICID=IN%3AUM%3A20190422%3AHPCM2%3AGREATSTAY%3ALOCATIONS%3ANA/')
        time.sleep(6)
        for i in range(6):
            self.driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight)")
            self.driver.execute_script(
                "window.scrollTo(0,document.body.scrollTop)")
            time.sleep(.5)

            self.driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight)")

        # time.sleep(6)
        self.html = self.driver.page_source

    def parse(self, response):
        response = Selector(text=self.html)
        url = response.xpath(
            "//div[@class='state-container']//li[@class='property']//a[2]//@href").extract()
        print(url, 'jjjjjjjjjj')
        for product in url:
            prod = f'https://www.wyndhamhotels.com{product}'
            yield Request(
                prod,
                meta={"url": prod},
                callback=self.parse_festival
            )

    def parse_festival(self, response):
        self.driver.get(
            response.meta['url'])
        time.sleep(3)
        button = self.driver.find_element_by_xpath(
            '//*[@id="rewardspricefilter"]/div/label[2]/span/span')
        button.click()
        time.sleep(3)
        yield{
            # 'Title': self.remove_charachters(response.xpath("//h1//text()").get()),
            'Name_of_the_company': response.xpath("//div[@class='property-name mobile-edit-dates']//span[@class='prop-name']//text()").extract(),
            # 'Request_Category': response.xpath("//ul[@class='ctags-list']//a//text()").extract(),
            # 'Description': self.remove_charachters(response.xpath("//section[@id='notice-descrip']//p//text()").get()),
            # 'Estimated_Value': self.remove_charachters(response.xpath("//*[@id='notice-keydata']/div[1]/dl/dd[4]//text()").get()),
            # 'Supplier_info': response.xpath("//ul[@class='ctags-list']//a//text()").extract(),
            # 'Link': response.meta['url'],
            # 'Keyword': 'IoT'
        }
