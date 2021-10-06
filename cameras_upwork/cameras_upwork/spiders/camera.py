import scrapy
from scrapy.http import Request


class CameraSpider(scrapy.Spider):
    name = 'camera'
    allowed_domains = [
        'www.theimagingsource.com']
    start_urls = [
        'https://www.theimagingsource.com/products/industrial-cameras/']

    def parse(self, response):
        links = response.xpath(
            "//section[1]/div/div/div/div/div/div/ul/li/a//@href").extract()

        for link in links:
            a_url = "https://www.theimagingsource.com"
            absolute_url = a_url + link
            yield Request(
                url=absolute_url, callback=self.parse_camera_1
            )

    def parse_camera_1(self, response):
        model = response.xpath(
            "//div//div//div[2]//section[1]//div[3]//div//div//div[1]//h3//text()").extract()
        links = response.xpath(
            "//div[1]/div/table/tbody/tr/td/a//@href").extract()
        code = response.xpath(
            "//div[1]/div/table/tbody/tr/td/a//text()").extract()
        a_url = 'https://www.theimagingsource.com'
        for link in links:
            absolute_urll = a_url + link
            print(absolute_urll)
            yield Request(
                url=absolute_urll,
                callback=self.parse_camera_1_details,
                meta={'url': absolute_urll}
            )

    def parse_camera_1_details(self, response):
        yield{
            "Description": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            "Vision_standard": response.xpath("//*[@id='tab_specification']/table/tbody/tr[2]/td[2]//img").extract(),
            "Dynamic_range": response.xpath("//*[@id='tab_specification']/table/tbody/tr[3]/td[2]//text()").extract(),
            "Frame_rate": response.xpath("//*[@id='tab_specification']/table/tbody/tr[5]/td[2]/span//text()").extract(),
            "Video_outpy_format": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "Ir_cut_filter": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "Sensor_type": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "Sensor_application": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "shutter": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "Format": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "pixel_size": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "Lens_mount": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "Interface": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "Supply_voltage": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "Current_consuption": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "Auto_Iris_control": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "Trigger": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "i/Os": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "Diemnsions": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "mass": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "Shutter": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "Temperature(operating)": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "Temperature(storage)": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            # "Humidity(operating)": response.xpath("//section[1]/div[2]/div[2]/ul/li//text()").extract(),
            "url": response.meta['url'],
        }
