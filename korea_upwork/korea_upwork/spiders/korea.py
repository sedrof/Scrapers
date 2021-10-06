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


class KoreaSpider(scrapy.Spider):
    name = 'korea'
    start_urls = ['http:shop497n244n117j7.1688.com']

    def __init__(self):
        options = Options()
        # options.add_argument("headless")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(
            executable_path=r"G:\chromedriver", options=options)
        self.driver.set_window_size(1920, 1080)
        self.driver.get(
            'https://shop497n244n117j7.1688.com/page/offerlist.htm?no_cache=true&spm=a2615.7691456.autotrace-paginator.2.325668d7T0b5YV&tradenumFilter=false&sampleFilter=false&sellerRecommendFilter=false&videoFilter=false&mixFilter=false&privateFilter=false&mobileOfferFilter=%24mobileOfferFilter&groupFilter=false&sortType=wangpu_score&pageNum=1#search-bar/')
        # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(30)

        pages = []
        for x in range(1):
            self.driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)
            button = self.driver.find_element_by_xpath("//a[text()='下一页']")
            self.next = self.driver.execute_script(
                "arguments[0].click();", button)
            # self.next.click()
            time.sleep(8)
            pages.append(self.driver.page_source)

        self.html = pages

    def parse(self, response):
        for re in self.html:
            response = Selector(text=re)
            clinics = response.xpath(
                "//ul[@class='offer-list-row']//li[@class='offer-list-row-offer']//div[@class='title-new']//@href").extract()
            for clinic in clinics:
                url = clinic
                yield{
                    "url": url
                }
                yield Request(
                    url,
                    meta={"url": url},
                    callback=self.parse_festival
                )

    def parse_festival(self, response):
        self.driver.get(response.meta['url'])
        time.sleep(6)
        html = self.driver.page_source
        response = Selector(text=html)

        pass
        yield{
            "Company_name": response.xpath("//h1[@class='d-title']").extract(),
            # "Company_website": response.xpath("//div[@class='job_listing-url']//@href").extract(),
            # "Practitioner_names": re.sub(' +', ' ',  response.xpath("//p[@class='practician_name']//text()").get()),
            # "url": response.meta['url'],

            # "Company_address": response.xpath("//div[@class='content-single-job_listing-hero-inner row']//div[@class='job_listing-location job_listing-location-none']//text()").extract()
        }
