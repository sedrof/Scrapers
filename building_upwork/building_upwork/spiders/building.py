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
import re


class BuildingSpider(scrapy.Spider):
    name = 'building'
    start_urls = [
        'https://concussioncareproviders.com/']

    def __init__(self):
        options = Options()
        # options.add_argument("headless")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(
            executable_path=r"G:\chromedriver", options=options)
        # self.driver.set_window_size(1920, 1080)
        self.driver.get('https://seedfund.nsf.gov/awardees/phase-1')
        # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(5)
        self.html = self.driver.page_source

    def parse(self, response):
        res = Selector(text=self.html)

        abos = 'https://seedfund.nsf.gov'
        products = res.xpath(
            "//div[@class='usa-accordion awardees-details-accordion']")
        for product in products:
            section = product.xpath(".//span[@class='accordion-tech-topic']//text()").get()
            (".//@href")
            url = f"{abos}{p}"
            # yield{
            #     "Url": url,
            #     "section": response.meta['section']
            # }
            yield Request(url,
                          meta={'url': url, "section": v},
                          callback=self.parse_shoe)

    def parse_shoe(self, response):
        self.driver.get(response.meta['url'])
        time.sleep(3)
        source = self.driver.page_source
        res = Selector(text=source)
        product_name = res.xpath(
            "//div[@class='usa-grid usa-section']//h1[@class='h2 awardeeName usa-sr-only']//text()").get()
        leader_first_name = res.xpath(
            "//div[@class='mb5']//p[@class='piName font-bold']//a//text()").get()
        leader_last_name = res.xpath(
            "//div[@class='mb5']//p[@class='piName font-bold']//a//text()").get()

        yield {
            "Section": response.meta['section'],
            "Product name": product_name,
            "First name": leader_first_name,
            "Last name": leader_last_name,
            "Phone": response.xpath("//div[@class='mb5']//p[2]//a//text()").get(),
            "Mail": response.xpath("//*[@id='akrobotix-llc']/div[2]/div[1]/address/div[1]/p[1]/a//@href").get(),
            "Title": response.xpath("//*[@id='akrobotix-llc']/div[2]/div[1]/address/div[1]/p[3]//text()").get(),
            "Project name": response.xpath("//*[@id='akrobotix-llc']/div[1]/h2//text()").get(),

        }
