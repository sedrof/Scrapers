import scrapy


class UpworkcountrySpider(scrapy.Spider):
    name = "upworkCountry"
    allowed_domains = ["eu-startups.com/directory"]
    start_urls = ["http://www.eu-startups.com/directory"]

    def parse(self, response):
        c = response.xpath("//*[@id='wpbdp-categories']//li")
        for i in c:
            country_name = i.xpath(".//a/text()").get()
            country_link = i.xpath(".//a//@href").get()
            yield response.follow(
                url=country_link,
                callback=self.parse_crypto,
                meta={"country_name": country_name},
            )

    def parse_country(self, response):
        country_name = response.request.meta["country_name"]

        rows = response.xpath(
            "//div[@class='listings wpbdp-listings-list list wpbdp-grid ']"
        )
        for row in rows:
            Company_Name = row.xpath(".//a/text()").get()
            yield {
                "Company_Name": Company_Name,
                "Category": country_name,
                # 'Based_In':
                # 'Tags':
                # 'Founded':
                # 'Description':
            }
