import scrapy
from scrapy.http.request import Request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


class UpworkTenderSpider(scrapy.Spider):
    name = 'news'
    start_urls = [
        'https://www.lefigaro.fr/elections/presidentielles/en-desaccord-sur-tout-melenchon-et-zemmour-se-livrent-a-un-debat-conflictuel-sur-l-identite-francaise-20210923']

    def __init__(self):
        options = Options()
        # options.add_argument("headless")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.page_load_strategy = 'none'
        driver = webdriver.Chrome(
            executable_path=r"G:\chromedriver", options=options)
        driver.set_window_size(1920, 1080)
        driver.get('https://www.lefigaro.fr/elections/presidentielles/en-desaccord-sur-tout-melenchon-et-zemmour-se-livrent-a-un-debat-conflictuel-sur-l-identite-francaise-20210923')
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='tabbar']/div/button").click()
        time.sleep(2)
        # driver.find_element_by_xpath(
        #     "//div[@class='figc__wrapper figc__wrapper--list']").click()
        for i in range(50):
            driver.find_element_by_xpath(
                "//div[@class='figc__wrapper figc__wrapper--list']").click()
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
        # try:
        next = driver.find_elements_by_xpath(
            "//div[@class='figc-comments']//button[@aria-expanded='false']")
        for n in next:
            try:
                next.click()
            except ElementClickInterceptedException:
                print("errors ssssssssssssssssssssssssssssssssssssssss")
        # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        # driver.execute_script("arguments[0].scrollIntoView(true)", ele)

        time.sleep(20)
        self.html = driver.page_source

    def parse(self, response):
        response = Selector(text=self.html)
        comments = response.xpath(
            "//div[@class='figc-comments']//p[@class='figc-comment__text']//text()").extract()
        for comment in comments:
            yield{
                "comment": comment
            }
            # yield Request(
            #     prod,
            #     meta={"url": prod},
            #     callback=self.parse_festival
            # )

    # def parse_festival(self, response):
    #     # value = response.xpath(
    #     #     "//*[@id='notice-keydata']/div[1]/dl/dd[4]//text()").extract()
    #     # if value
    #     yield{
    #         'Title': self.remove_charachters(response.xpath("//h1//text()").get()),
    #         'Name_of_the_company': response.xpath("//li[@class='loc-card loc-card-buyer']//a//text()").extract(),
    #         'Request_Category': response.xpath("//ul[@class='ctags-list']//a//text()").extract(),
    #         'Description': self.remove_charachters(response.xpath("//section[@id='notice-descrip']//p//text()").get()),
    #         'Estimated_Value': self.remove_charachters(response.xpath("//*[@id='notice-keydata']/div[1]/dl/dd[4]//text()").get()),
    #         'Supplier_info': response.xpath("//ul[@class='ctags-list']//a//text()").extract(),
    #         'Link': response.meta['url'],
    #         'Keyword': 'IoT'
    #     }
