import re

import os
import pandas
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class TradesySpider(scrapy.Spider):
    name = "tradesy"
    temp_file = 'Bags.csv'

    def start_requests(self):
        open(self.temp_file, 'w').close()

        url = 'https://www.tradesy.com/bags/?brand=louis-vuitton|gucci|chanel|prada|burberry|saint-laurent|givenchy|valentino|celine|versace|proenza-schouler|kate-spade|salvatore-ferragamo|loewe|fendi|alexander-mcqueen|cartier|lanvin|furla|mulberry|bvlgari|anya-hindmarch|miu-miu|goyard|alexander-wang|bottega-veneta|chloe|dior|balenciaga|hermes|michael-kors|dolce-and-gabbana&page={}&num_per_page=192'
        for page in range(1, 2):
            yield scrapy.Request(url=url.format(page), callback=self.parse)

    def parse(self, response):
        for bag in response.css('a.item-image[href^="/i/"]::attr(href)').extract():
            yield scrapy.Request(response.urljoin(bag), callback=self.parse_bag)

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

        details = response.css('#idp-info > div:nth-child(1) > div.idp-details.idp-info-accordion > div')

        fabric = details.xpath(
            '//*[@id="idp-info"]/div[1]/div[4]/div/div/p[.="Fabric:"]/following-sibling::p/text()').extract_first()
        try:
            fabric = fabric.strip()
        except AttributeError:
            pass

        colors = details.css('div:nth-child(2) > p.small-7.plus-8.columns > a::text').extract()
        colors = list(set(colors))
        colors = ' '.join(colors)

        collection = details.css('a.tags[href^="/search/?q="]::text').extract_first()

        type = details.css('div:nth-last-child(2)> p.small-7.plus-8.columns > a::text').extract_first()
        tags = details.css('div:nth-last-child(1)> p.small-7.plus-8.columns > a::text').extract()
        tags = ' '.join(tags)

        condition = response.css(
            '#idp-info > div:nth-child(1) > div.idp-condition.idp-info-accordion > div > b::text').extract_first()

        yield {
            'Brand': brand,
            'Color': colors,
            'Condition': condition,
            'Fabric': fabric,
            'Type': type,
            'Model': model,
            'Price': price,
            'Size': size,
            'Style Collection': collection,
            'Style Tags': tags,
            'url': response.url,
        }

    def closed(self, reason):
        pandas.read_csv(self.temp_file).to_excel(self.temp_file.replace('csv', 'xlsx'))

        os.remove(self.temp_file)


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(TradesySpider)
    process.start()
