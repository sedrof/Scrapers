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


class LicensSpider(scrapy.Spider):
    name = 'licens'
    start_urls = ["https://search.dca.ca.gov/results/"]

    def __init__(self):
        options = Options()
        # options.add_argument("headless")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(
            executable_path=r"G:\chromedriver", options=options)
        driver.set_window_size(1920, 1080)

        driver.get(
            'https://search.dca.ca.gov/results')
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(5)
        search = driver.find_element_by_xpath(
            "//div[@class='searchFeatures']//input[@type='submit']")
        search.click()
        time.sleep(5)
        for i in range(1):
            driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(10)
        self.html = driver.page_source

    def parse(self, response):
        abosolute_url = 'https://search.dca.ca.gov'
        response = Selector(text=self.html)
        contact = response.xpath(
            "//div[@id='main']//ul[@class='actions md']//a[@class='button newTab']//@href").extract())
        for product in url:
            prod = f'{abosolute_url}{product}'
            yield Request(
                prod,
                meta={"url": prod},
                callback=self.parse_festival
            )

    def parse_festival(self, response):
        first_name = response.xpath(
            '//div[@class="detailContainer"]//p[@id="name"]//text()').get()
        yield{
            'first_name': response.xpath('//div[@class="detailContainer"]//p[@id="name"]//text()').get(),
            # 'last_name': response.xpath("//li[@class='loc-card loc-card-buyer']//a//text()").extract(),
            'License_Status': response.xpath("//span[@class='status_1']//text()").extract(),
            # 'Secondary_Status': self.remove_charachters(response.xpath("//section[@id='notice-descrip']//p//text()").get()),
            # 'License_Number': self.remove_charachters(response.xpath("//*[@id='notice-keydata']/div[1]/dl/dd[4]//text()").get()),
            'Full_Address': response.xpath("//div[@class='addContainer']//p[@class='wrapWithSpace'][2]//text()").extract(),
            # 'Link': response.meta['url'],
        }
