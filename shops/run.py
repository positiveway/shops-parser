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
    # process.crawl(TradesySpider)
    process.crawl(EbaySpider)
    process.start()

    csv_files = [EbaySpider.temp_file, TradesySpider.temp_file]
    combined = pd.concat([pd.read_csv(f) for f in csv_files])
    combined.to_excel('Bags.xlsx')


if __name__ == '__main__':
    main()
