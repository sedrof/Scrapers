from time import sleep
from typing import Text
import scrapy
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["www.humber.ca/"]
    start_urls = ["https://www.humber.ca"]

    def __init__(self):
        options = Options()
        # options.add_argument("headless")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(executable_path=r"G:\chromedriver", options=options)
        driver.set_window_size(1920, 1080)
        driver.get('https://https://www.fatsoma.com/search?page=1')
        search_bar = driver.find_element_by_xpath("//*[@id='edit-submit-staff']")
        search_bar.click()
        # self.search_btn = self.driver.find_element_by_xpath(
        #     "//*[@id='nav-search-submit-button']"
        # )
        # self.search_btn.click()

        self.html = driver.page_source
        driver.close()

        # print(sel)

    def parse(self, response):
        resp = Selector(text=self.html)
        # print(resp)
        names = resp.xpath("//div/table/tbody/tr/td[1]/div")
        for name in names:
            b = name.xpath(".//a//text()").get()
            print(
                b,
                "sdsdsdsdsdsdsdsdsdsdsdsdsdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
            )
            yield {
                "name": name.xpath(".//a//text()").get(),
                "email": name.xpath(".//a//@href").get(),
            }

        # self.next_page = sel.xpath(
        #     "//*[@id='block-system-main']/div/div/div[3]/ul/li[11]/a"
        # ).get()

        # """to stop at the last page"""
        # if self.next_page:
        #     yield scrapy.Request(
        #         url=self.next_page,
        #         callback=self.start_requests,
        #     )

        # yield Request(url, callback=self.parse_book)

        # while True:
        #     try:
        #         next_page = self.driver.find_element_by_xpath(
        #             "//*[@id='block-system-main']/div/div/div[3]/ul/li[11]/a"
        #         )
        #         sleep(3)
        #         self.logger.info("Sleeping for 3 seconds.")
        #         next_page.click()

        #         sel = Selector(text=self.driver.page_source)
        #         books = sel.xpath("//table/tbody/tr/td[1]/div/a/text()").get()
        #         for lap in books:
        #             url = "https://humber.ca/directory/" + lap
        #             yield Request(url, callback=self.parse_book)

        #     except NoSuchElementException:
        #         self.logger.info("No more pages to load.")
        #         self.driver.quit()
        #         break

    # def parse_book(self, response):
    #     pass
