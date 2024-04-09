# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pandas as pd
from scrapy.exceptions import DropItem


class CrawlerPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append((item["url"], item["body"]))
        return item

    def close_spider(self, spider):
        print(self.items)
        df = pd.DataFrame(self.items, columns=["URL", "body"])
        df.to_parquet("output.parquet", index=False)

        # DataFrameを.parquetファイルに書き込む
        try:
            df.to_parquet("output.parquet", index=False)
        except Exception as e:
            raise DropItem(f"Failed to write items to parquet file: {e}")

        return None
