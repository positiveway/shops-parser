import re

import os
import pandas
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class EbaySpider(scrapy.Spider):
    name = 'ebay'
    temp_file = 'Bags.csv'

    def start_requests(self):
        open(self.temp_file, 'a+').close()

        url = 'https://www.ebay.com/sch/Women-s-Handbags-and-Bags/169291/i.html?_fsrp=1&Brand=Alexander%2520McQueen%7CAlexander%2520Wang%7CAnya%2520Hindmarch%7CBalenciaga%7CBottega%2520Veneta%7CBurberry%7CBvlgari%7CCartier%7CC%25C3%2589LINE%7CCHANEL%7CChlo%25C3%25A9%7CDior%7CDolce%2526Gabbana%7CFendi%7CFurla%7CGivenchy%7CGoyard%7CGucci%7CHERM%25C3%2588S%7Ckate%2520spade%2520new%2520york%7CLanvin%7CLoewe%7CLouis%2520Vuitton%7CMichael%2520Kors%7CMiu%2520Miu%7CMulberry%7CPRADA%7CProenza%2520Schouler%7CSalvatore%2520Ferragamo%7Cvalentino%7CVersace&_sacat=169291&_dcat=169291&_ipg=200'

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # next_page = response.css(
        #     '#srp-river-results-SEARCH_PAGINATION_MODEL_V2 > div.s-pagination > nav > a:nth-child(4)::attr(href)').extract_first()
        # response.follow(next_page)

        for bag_link in response.css('div > div.s-item__info.clearfix > a::attr(href)').extract():
            yield response.follow(bag_link, callback=self.parse_bag)

    def parse_bag(self, response):
        condition = response.css('#vi-itm-cond::text').extract_first()
        brand = response.xpath('//td[contains(text(), "Brand:")]/following-sibling::td/*/span/text()').extract_first()
        color = response.xpath('//td[contains(text(), "Colo")]/following-sibling::td/*/text()').extract_first()
        type = response.xpath('//td[contains(text(), "Style")]/following-sibling::td/*/text()').extract_first()
        fabric = response.xpath('//td[contains(text(), "Material")]/following-sibling::td/*/text()').extract_first()

        inch_size = re.compile('([.,\d]+).*inch')

        length = response.xpath('//td[contains(text(), "Length")]/following-sibling::td/*/text()').extract_first()
        if length:
            length = inch_size.search(length).group(1)

        height = response.xpath('//td[contains(text(), "Height")]/following-sibling::td/*/text()').extract_first()
        if height:
            height = inch_size.search(height).group(1)

        depth = response.xpath('//td[contains(text(), "Depth")]/following-sibling::td/*/text()').extract_first()
        if depth:
            depth = inch_size.search(depth).group(1)

        size = '{}" {}" {}"'.format(length, height, depth)

        price = response.xpath('//*[@itemprop="price"]/@content')
        model = response.css('#itemTitle::text').extract_first()

        yield {
            'Brand': brand,
            'Color': color,
            'Condition': condition,
            'Fabric': fabric,
            'Type': type,
            'Model': model,
            'Price': price,
            'Size': size,
            'Style Collection': None,
            'Style Tags': None,
            'url': response.url,
        }

    def closed(self, reason):
        pandas.read_csv(self.temp_file).to_excel(self.temp_file.replace('csv', 'xlsx'))

        os.remove(self.temp_file)


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(EbaySpider)
    process.start()
