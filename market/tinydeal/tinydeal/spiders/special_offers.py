import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = "special_offers"
    allowed_domains = ["www.cigabuy.com"]
    start_urls = ["https://www.cigabuy.com/specials.html"]

    # def start_requests(self):
    #     yield scrapy.Request(url='https://www.cigabuy.com/specials.html', callback=self.parse,
    #          headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'})

    def parse(self, response):
        for product in response.xpath(
            "//ul[@class='productlisting-ul']//div[@class='p_box_wrapper']"
        ):
            if (
                product.xpath(".//div[@class='p_box_price cf']//span[1]//text()").get()
                == None
            ):
                yield {
                    "Title": product.xpath(".//a[2]//text()").get(),
                    "U_r_l": product.xpath(".//a[2]//@href").get(),
                    "Discount_price": product.xpath(
                        ".//div[@class='p_box_price cf']//text()"
                    ).get(),
                    # 'User-Agent'    : response.request.headers['User-Agent']
                }
            yield {
                "Title": product.xpath(".//a[2]//text()").get(),
                "U_r_l": product.xpath(".//a[2]//@href").get(),
                "Discount_price": product.xpath(
                    ".//div[@class='p_box_price cf']//span[1]//text()"
                ).get(),
                "original_price": product.xpath(
                    ".//div[@class='p_box_price cf']//span[2]//text()"
                ).get(),
                # 'User-Agent'    : response.request.headers['User-Agent']
            }

        """Pagination rule - we look for the Next page button"""
        next_page = response.xpath("//div[@class='digg']//a[5]//@href").get()

        """to stop at the last page"""
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse,
            )
            #  headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'})
# Home Type	City	Builder	Builder Warranty Number	Warranty Commencement Date	Warranty provider	Address	City	Post Code	Legal Description	PID