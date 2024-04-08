from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class GasolineSpiderSpider(CrawlSpider):
    name = "gasoline_spider"
    allowed_domains = ["tenax66.net"]
    start_urls = ["https://tenax66.net"]

    rules = (Rule(LinkExtractor(allow=r".*"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        item = {}
        item["title"] = response.xpath("//title/text()").get()
        item["body"] = response.xpath("//body").extract()
        return item
