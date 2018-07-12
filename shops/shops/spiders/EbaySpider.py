import re
import scrapy


class EbaySpider(scrapy.Spider):
    name = 'ebay'
    temp_file = 'ebay.csv'

    custom_settings = {
        'FEED_URI': temp_file,
    }

    brands = ['Alexander%2520McQueen', 'Alexander%2520Wang', 'Anya%2520Hindmarch', 'Balenciaga',
              'Bottega%2520Veneta', 'Burberry', 'Bvlgari', 'Cartier', 'C%25C3%2589LINE', 'CHANEL', 'Chlo%25C3%25A9',
              'Dior', 'Dolce%2526Gabbana', 'Fendi', 'Furla', 'Givenchy', 'Goyard', 'Gucci', 'HERM%25C3%2588S',
              'kate%2520spade%2520new%2520york', 'Lanvin', 'Loewe', 'Louis%2520Vuitton', 'Michael%2520Kors',
              'Miu%2520Miu', 'Mulberry', 'PRADA', 'Proenza%2520Schouler', 'Salvatore%2520Ferragamo', 'valentino',
              'Versace']

    last_brand_page = {brand: '' for brand in brands}

    def start_requests(self):
        open(self.temp_file, 'w').close()

        url = 'https://www.ebay.com/sch/Women-s-Handbags-and-Bags/169291/i.html?_fsrp=1&Brand={}&_sacat=169291&_dcat=169291&_ipg=200'

        for brand in self.brands:
            request = scrapy.Request(url=url.format(brand), callback=self.parse)
            request.meta['brand'] = brand
            yield request

    def parse(self, response):
        brand = response.meta['brand']

        next_page = response.css(
            '#srp-river-results-SEARCH_PAGINATION_MODEL_V2 > div.s-pagination > nav > a:nth-child(4)::attr(href)').extract_first()
        next_page = response.urljoin(next_page)

        if next_page != self.last_brand_page[brand]:
            self.last_brand_page[brand] = next_page

            request = scrapy.Request(url=next_page, callback=self.parse)
            request.meta['brand'] = brand
            yield request

        for bag_link in response.css('div > div.s-item__info.clearfix > a::attr(href)').extract():
            yield response.follow(bag_link, callback=self.parse_bag)

    def parse_bag(self, response):
        condition = response.css('#vi-itm-cond::text').extract_first()
        brand = response.xpath('//td[contains(text(), "Brand:")]/following-sibling::td/*/span/text()').extract_first()
        color = response.xpath('//td[contains(text(), "Colo")]/following-sibling::td/*/text()').extract_first()
        type = response.xpath('//td[contains(text(), "Style")]/following-sibling::td/*/text()').extract_first()
        fabric = response.xpath('//td[contains(text(), "Material")]/following-sibling::td/*/text()').extract_first()

        number_re = re.compile('[.,\d]+')

        length = response.xpath('//td[contains(text(), "Length")]/following-sibling::td/*/text()').extract_first('')
        try:
            length = number_re.search(length).group(0)
        except AttributeError:
            length = None

        height = response.xpath('//td[contains(text(), "Height")]/following-sibling::td/*/text()').extract_first('')
        try:
            height = number_re.search(height).group(0)
        except AttributeError:
            height = None

        depth = response.xpath('//td[contains(text(), "Depth")]/following-sibling::td/*/text()').extract_first('')
        try:
            depth = number_re.search(depth).group(0)
        except AttributeError:
            depth = None

        size = None
        if length and height and depth:
            size = '{}" x {}" x {}"'.format(length, height, depth)

        price = response.xpath('//*[@itemprop="price"]/@content').extract_first()
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
