from os.path import dirname, abspath

from sys import path
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import pandas as pd

work_dir = dirname(abspath(__file__))  # first shops dir
path.append(work_dir)

from shops.spiders.EbaySpider import EbaySpider
from shops.spiders.TradesySpider import TradesySpider


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(EbaySpider)
    process.crawl(TradesySpider)
    process.start()

    csv_files = [pd.read_csv(f) for f in [EbaySpider.temp_file, TradesySpider.temp_file]]
    combined = pd.concat(csv_files, ignore_index=True, sort=False)
    combined.to_excel('Bags.xlsx', index=False)


if __name__ == '__main__':
    main()
