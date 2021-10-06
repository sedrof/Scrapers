# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BathUpworkItem(scrapy.Item):
    # define the fields for your item here like:
    files_url = scrapy.Field()
    files = scrapy.Field()
