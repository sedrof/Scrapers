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


class ClinicsSpider(scrapy.Spider):
    name = 'clinics'
    start_urls = [
        'https://concussioncareproviders.com/']

    def __init__(self):
        options = Options()
        # options.add_argument("headless")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(
            executable_path=r"G:\chromedriver", options=options)
        driver.set_window_size(1920, 1080)
        driver.get(
            'https://concussioncareproviders.com/listings/?search_location=&search_categories%5B%5D=&search_radius=100&search_lat=0&search_lng=0')
        # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(6)

        pages = []
        for x in range(92):
            driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)
            self.next = driver.find_element_by_xpath("//a[text()='→']").click()
            # self.next.click()
            time.sleep(8)
            pages.append(driver.page_source)

        self.html = pages

    def parse(self, response):
        for re in self.html:
            response = Selector(text=re)
            clinics = response.xpath(
                "//ul[@class='job_listings listing-cards-anchor--active']//a//@href").extract()
            for clinic in clinics:
                url = clinic
                # yield SeleniumRequest{
                #     "url": url
                # }
                yield Request(
                    url,
                    meta={"url": url},
                    callback=self.parse_festival
                )
        # next_page_url = response.xpath(
        #     "//a[text()='→']").extract()
        # if next_page_url:
        #     yield Request(next_page_url,
        #                   callback=self.parse)

    def parse_festival(self, response):
        # value = response.xpath(
        #     "//*[@id='notice-keydata']/div[1]/dl/dd[4]//text()").extract()
        # if value
        # re.sub(' +', ' ', r)
        # print(re.sub(' +', ' ', r))
        yield{
            "Company_name": response.xpath("//h1//text()").extract(),
            "Company_website": response.xpath("//div[@class='job_listing-url']//@href").extract(),
            "Practitioner_names": re.sub(' +', ' ',  response.xpath("//p[@class='practician_name']//text()").get()),
            "url": response.meta['url'],

            "Company_address": response.xpath("//div[@class='content-single-job_listing-hero-inner row']//div[@class='job_listing-location job_listing-location-none']//text()").extract()
        }
