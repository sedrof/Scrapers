
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


class BcaSpider(scrapy.Spider):
    name = 'bca'
    # allowed_domains = ['www.bca.gov.sg']
    # start_urls = ['https://www.bca.gov.sg/BCADirectory/Search/Result?pCLSSelected=,83|C3&pBLSSelected=,141&pGrading=NONE&page=-1&d=0&pCLSCondition=AND&pBLSCondition=AND']

    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.bca.gov.sg/BCADirectory/Search/Result?pCLSSelected=,83|C3&pBLSSelected=,141&pGrading=NONE&page=-1&d=0&pCLSCondition=AND&pBLSCondition=AND',
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        urls = response.xpath('//tbody//td//a//@href').extract()
        absolute_url = 'www.bca.gov.sg'
        for url in urls:
            uri = absolute_url + url
            print(uri, "asssssssssssssssssssssss")
            yield SeleniumRequest(
                uri,
                callback=self.parse_company
            )
        next = response.xpath("//a[text()='Next'][1]").get()

        if next:
            next_page = f"www.bca.gov.sg{next}"
            yield SeleniumRequest(
                url=next_page,
                wait_time=3,
                callback=self.parse
            )

    def parse_company(self, response):
        yield{
            "name": response.xpath("//div[@class='body-bluetext bold']//text()").extract_first(),
            "adress": response.xpath("/html/body/div/div[4]/div[2]/div[2]/div/div[1]/div[3]//text()").strip('Adress : '),

        }


# //a[text()='Next'][1]
# https://www.bca.gov.sg/
# https://www.bca.gov.sg/BCADirectory/Search/Result?pCLSSelected=,83|C3&pBLSSelected=,141&pGrading=NONE&page=-1&d=0&pCLSCondition=AND&pBLSCondition=AND
# //tbody//td//a//@href
