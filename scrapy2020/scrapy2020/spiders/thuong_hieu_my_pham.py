from abc import ABC
from datetime import datetime
import scrapy
from ..items import BazaarvietnamItem


class indexSpider(scrapy.Spider, ABC):
    name = 'thuong_hieu_my_pham'
    allowed_domains = ["bazaarvietnam.vn"]
    download_delay = 1
    author = 'tungns2101'

    def start_requests(self):
        urls = [
            'https://bazaarvietnam.vn/brand-category/thuong-hieu-my-pham/']
        for url in urls:
            yield scrapy.Request(url, self.hot_news)

    def hot_news(self, response):
        for url in response.css("div.row div.alpha-category-articles a::attr('href')").extract():
            yield scrapy.Request(url, self.parse_hot_news)

    def parse_hot_news(self, response):
        data = {}
        meta = {}
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        item = BazaarvietnamItem()
        try:
            item['key'] = self.author
            item['domain'] = self.allowed_domains[0]
            item['url'] = response.request.url
            item['category'] = 'thuong-hieu'
            data['title'] = response.css("h1.category-title.barred-heading > span::text").get()
            data['paragraphs'] = response.css(".tab-content > div > div > p ::text").extract()
            for i in range(10):
                for para in data['paragraphs']:
                    index = data['paragraphs'].index(para)
                    if "\n" in para:
                        del data['paragraphs'][index]
                i += 1
            image = list(
                {
                    'image_url': img.css("img::attr('src')").extract_first(),
                    'image_decription': None
                } for img in response.css('div.carousel-inner > .item > figure > a')
            )
            for img in response.css("div.tab-content div.brand_page_tab .wp-caption "):
                image.append({
                    'image_url': img.css("a > img::attr('src')").extract_first(),
                    'image_decription': img.css("p ::text").extract_first()
                })
            for img in response.css("div.tab-content div.slideshow-gallery-text > p img::attr(src)").extract():
                image.append({
                    'image_url': img,
                    'image_decription': None
                })
            for img in response.css("div.tab-content div.slideshow-gallery-text > div > p img::attr(src)").extract():
                image.append({
                    'image_url': img,
                    'image_decription': None
                })
            item['data'] = data
            data['images'] = image
            meta['crawled_by'] = self.name
            meta['crawled_at'] = dt_string
            item['meta'] = meta
        except Exception as e:
            print(f'#{e} : {response.request.url}')
        yield item
