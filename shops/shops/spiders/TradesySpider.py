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
        for bag in response.css('a.item-image[href^="/i/"]::attr(href)').extract():
            yield response.follow(bag, callback=self.parse_bag)

    def parse_bag(self, response):
        brand = response.css('#idp-brand > a.tags::text').extract_first()

        model = response.css('#idp-title::text').extract_first()
        model = model.strip()

        size = response.css('#idp-size-id > span.item-size::text').extract_first()
        size = size.strip()

        price = response.css('#idp-price > div.idp-price-wrapper > div > div.item-price::text').extract_first()
        price = re.search('[.,\d]+', price).group(0)
        price = price.replace(',', '')
        price = float(price)

        condition = response.css(
            '#idp-info > div:nth-child(1) > div.idp-condition.idp-info-accordion > div > b::text').extract_first()

        yield {
            'brand': brand,
            'model': model,
            'size': size,
            'price': price,
            'condition': condition,
            'url': response.url,
        }


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(TradesySpider)
    process.start()
