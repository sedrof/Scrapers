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

class RealestateSpider(scrapy.Spider):
    name = 'realestate'
    allowed_domains = ['www.storagecafe.com']
    start_urls = ['https://www.storagecafe.com/self-storage/us/ar/pulaski-county/72211/?geopicker_type=viewport&viewport=-93.95598880081104%2C33.543502818303644%2C-90.07781497268604%2C36.64841464932909&zoom=9&DetailsPreview=1072408/']

    def __init__(self):
        options = Options()
        # options.add_argument("headless")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(
            executable_path=r"G:\chromedriver", options=options)
        driver.set_window_size(1920, 1080)
        driver.get(
            'https://www.storagecafe.com/self-storage/us/ar/pulaski-county/72211/?geopicker_type=viewport&viewport=-93.95598880081104%2C33.543502818303644%2C-90.07781497268604%2C36.64841464932909&zoom=9&DetailsPreview=1072408/')
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
