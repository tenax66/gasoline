from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import string


class GasolineSpiderSpider(CrawlSpider):
    name = "gasoline_spider"
    allowed_domains = []
    start_urls = [
        "https://example.com",
        "http://paavlaytlfsqyvkg3yqj7hflfg5jw2jdg2fgkza5ruf6lplwseeqtvyd.onion/",
    ]

    rules = (Rule(LinkExtractor(allow=r".*"), callback="parse_item", follow=False),)

    def parse_item(self, response):
        item = {}
        item["url"] = response.url

        # extract body text without html tags
        item["content"] = " ".join(
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
