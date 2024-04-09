from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import string


class GasolineSpiderSpider(CrawlSpider):
    name = "gasoline_spider"
    allowed_domains = ["tenax66.net"]
    start_urls = ["https://tenax66.net"]

    rules = (Rule(LinkExtractor(allow=r".*"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        item = {}
        item["title"] = response.xpath("//title/text()").get()

        # extract body text without html tags
        item["body"] = " ".join(
            list(
                filter(
                    # TODO: normalize text
                    lambda x: x != "",
                    map(
                        self._normalize,
                        response.xpath("//body//p//text()").getall(),
                    ),
                )
            )
        )
        return item

    def _normalize(self, input: str) -> str:
        translation_table = str.maketrans(
            string.punctuation, " " * len(string.punctuation)
        )

        return input.replace("\n", " ").strip().translate(translation_table)
