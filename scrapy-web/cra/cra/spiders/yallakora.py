import scrapy


class Crypto(scrapy.Spider):
    name = 'crypto'
    allowed_domains = ['stateofthedapps.com']
    start_urls = ['https://www.stateofthedapps.com/collections/featured']

    def parse(self, response):
        cyrptos = response.xpath("//div[@class='dapp-wrapper']//li")
        for tit in cyrptos:
            totle = tit.xpath(".//p//text()").get()
            descr = tit.xpath(".//h4//text()").get()
            link = tit.xpath(".//@href").get()
            # absolute_url = response.urljoin(link)
            yield response.follow(url=link, callback=self.parse_crypto, meta={'crypto_name': descr})
            
    def parse_crypto(self, response):
        crypto_name = response.request.meta['crypto_name']
        rows = response.xpath("//div[@class='module-wrapper -tier-4']//div[@class='module -dev']")

        for row in rows:
            daily = row.xpath(".//ul//li[1]//span[1]//text()").get()
            visitors = row.xpath(".//ul//li[1]//span[2]//text()").get()
            yield {
                'crypto_name': crypto_name,
                'active_users': daily,
                'visitors': visitors,
            }