from abc import ABC
from datetime import datetime
import scrapy
from ..items import BazaarvietnamItem


class indexSpider(scrapy.Spider, ABC):
    name = 'anh_dep'
    allowed_domains = ["bazaarvietnam.vn"]
    download_delay = 1
    author = 'tungns2101'

    def start_requests(self):
        urls = ['https://bazaarvietnam.vn/fashion-beauty-spread/',
                ]
        for url in urls:
            yield scrapy.Request(url, self.parse_request)

    def parse_request(self, response):
        for url in response.css(
                "div.category-content-wrapper article header.article-header h2.h2 > a::attr('href')").extract():
            yield scrapy.Request(url, self.parse)
        next_page = response.css(".page-navigation ol li.bpn-next-link > a::attr('href')").extract_first()
        if next_page:
            url = next_page
            yield scrapy.Request(url, self.parse_request)

    def parse(self, response):
        data = {}
        meta = {}
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        category = response.css("header.article-header ul.post-categories li > a::attr('href')").extract()
        category = str(category).replace("['https://bazaarvietnam.vn/", "")
        category = category.replace("/']", "")
        item = BazaarvietnamItem()
        try:
            item['key'] = self.author
            item['domain'] = self.allowed_domains[0]
            item['url'] = response.request.url
            item['category'] = category
            data['title'] = response.css("h1.entry-title.single-title::text").get()
            name_post = response.css("div.authorship span.author a::text").getall()
            info_post = response.css("div.authorship span.author > a::attr('href')").extract()
            data['post_by'] = {}
            data['post_by']['name_post'] = name_post
            data['post_by']['info_post'] = info_post
            data['time_public'] = response.css("div.authorship time.time::text").get()
            data['sapo'] = response.css("p.standfirst::text").getall()
            data['paragraphs'] = response.css(
                ".entry-content.clearfix > p::text,.entry-content.clearfix > ul > li ::text,.entry-content.clearfix > p *:not(script)::text,.entry-content.clearfix > h2 ::text,.entry-content.clearfix > h3 ::text,.entry-content.clearfix h4 ::text,.entry-content.clearfix > table ::text").extract()
            if response.css(".tab-pane p"):
                data['paragraphs'] = response.css(
                    ".tab-pane > p::text,.tab-pane > p *:not(script)::text,h2 ::text,h3 ::text").extract()
            if response.css("div.container article.related-featured"):
                data['paragraphs'] = data['paragraphs'][:-1]
            if response.css(".recent_post_wrap h3"):
                data['paragraphs'] = data['paragraphs'][:-1]
            if response.css(".article-footer h3"):
                data['paragraphs'] = data['paragraphs'][:-1]
            for i in range(5):
                for para in data['paragraphs']:
                    index = data['paragraphs'].index(para)
                    if "\n" in para:
                        print(f'#################### {index}')
                        del data['paragraphs'][index]
                i += 1
            for i in range(5):
                for para in data['paragraphs']:
                    index = data['paragraphs'].index(para)
                    if "ĐƯỢC YÊU THÍCH" in para:
                        del data['paragraphs'][index]
                i += 1
            for i in range(5):
                for para in data['paragraphs']:
                    index = data['paragraphs'].index(para)
                    if "Liên hệ" in para:
                        del data['paragraphs'][index]
                i += 1
            image = list(
                {
                    'image_url': img.css("img::attr('src')").extract_first(),
                    'image_decription': img.css("p ::text").extract_first()
                } for img in response.css('div.wp-caption.aligncenter ')
            )
            for img in response.css(".entry-content.clearfix > img::attr('src')").extract():
                image.append({
                    'image_url': img,
                    'image_decription': None
                })
            for img in response.css("section.entry-content.clearfix > a > img::attr('src')").extract():
                image.append({
                    'image_url': img,
                    'image_decription': None
                })
            for img in response.css("section.entry-content.clearfix > p > a > img::attr('src')").extract():
                image.append({
                    'image_url': img,
                    'image_decription': None
                })
            for img in response.css("section.entry-content.clearfix > p > img::attr('src')").extract():
                image.append({
                    'image_url': img,
                    'image_decription': None
                })
            # runway
            for img in response.css(".instagram-gallery figure "):
                image.append({
                    'image_url': img.css("a > img::attr('src')").extract_first(),
                    'image_decription': img.css("figcaption > p ::text").extract_first()
                })
            for img in response.css(".wp-caption.alignnone "):
                image.append({
                    'image_url': img.css("img::attr('src')").extract_first(),
                    'image_decription': img.css("p ::text").extract_first()
                })
            for img in response.css("section.entry-content.clearfix > div > dl "):
                image.append({
                    'image_url': img.css("dt > img::attr('src')").extract_first(),
                    'image_decription': None
                })
            data['images'] = image
            item['data'] = data
            meta['crawled_by'] = self.name
            meta['crawled_at'] = dt_string
            item['meta'] = meta
        except Exception as e:
            print(f'#{e} : {response.request.url}')
        yield item