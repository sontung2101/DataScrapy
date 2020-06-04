from datetime import datetime
import scrapy
from ..items import Dulich24Item
from scrapy.utils.markup import remove_tags

class indexSpider(scrapy.Spider):
    name = 'am_thuc'
    allowed_domains = ["dulich24.com.vn"]
    download_delay = 1
    author = 'tungns2101'

    def start_requests(self):
        urls = [
            'http://dulich24.com.vn/bai-viet/am-thuc',
        ]
        for url in urls:
            yield scrapy.Request(url, self.parse_requests, meta={'page': 1})

    def parse_requests(self, response):
        domain = 'http://dulich24.com.vn'
        items = response.css("div.box-content h3 > a::attr('href')").extract()
        for url in items:
            print(f"#############{url}")
            yield scrapy.Request(domain + url, self.parse)
        page = response.meta.get('page')
        url = domain + f'/bai-viet/am-thuc?page={page}'
        page += 1
        if items:
            yield scrapy.Request(url, self.parse_requests, meta={'page': page})

    def parse(self, response):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        item = Dulich24Item()
        meta_item = dict()
        data_item = dict()
        item['key'] = self.author
        item['domain'] = self.allowed_domains[0]
        item['url'] = response.request.url
        item['category'] = 'bai-viet/am-thuc'

        data_item['title'] = response.css('div.row div.col-xl div h1::text').extract_first().strip()
        data_item['post_by'] = None
        data_item['time_public'] = None
        sapo = [x.replace('\n', '').replace('\r', '').replace('  ', '').replace('\t', '') for x in response.css('div.news-desc ::text').extract()]
        data_item['sapo'] = [x for x in sapo if x][1:]
        content = [x.replace('\n', '').replace('\r', '').replace('\t', '').replace('  ', '') for x in response.css('div.news-content > p ::text').extract()]
        data_item['paragraphs'] = [x for x in content if x]
        image = list(
            {
                'image_url': img.css('img::attr(src)').extract_first(),
                'image_decription': ''.join(img.css('::text').extract()).strip() or None
            } for img in response.css('div.news-content > p') if img.css('img')
        )
        data_item['image'] = image
        item['data'] = data_item

        meta_item['crawled_by'] = self.name
        meta_item['crawled_at'] = dt_string
        item['meta'] = meta_item
        yield item
