import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class TradesySpider(scrapy.Spider):
    name = "tradesy"
    start_urls = [
        'https://www.tradesy.com/bags/?brand=louis-vuitton|gucci|chanel|prada|burberry|saint-laurent|givenchy|valentino|celine|versace|proenza-schouler|kate-spade|salvatore-ferragamo|loewe|fendi|alexander-mcqueen|cartier|lanvin|furla|mulberry|bvlgari|anya-hindmarch|miu-miu|goyard|alexander-wang|bottega-veneta|chloe|dior|balenciaga|hermes|michael-kors|dolce-and-gabbana'
    ]

    def parse(self, response):
        pass


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(TradesySpider)
    process.start()
