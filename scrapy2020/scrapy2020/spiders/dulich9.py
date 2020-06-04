from datetime import datetime
import scrapy
from bs4 import BeautifulSoup

from ..items import Dulich24Item
from scrapy.utils.markup import remove_tags


class indexSpider(scrapy.Spider):
    name = 'dulich9'
    allowed_domains = ["dulich9.com"]
    download_delay = 1
    author = 'tungns2101'

    def start_requests(self):
        urls = [
            'https://dulich9.com/am-thuc',
        ]
        for url in urls:
            yield scrapy.Request(url, self.parse_requests)

    def parse_requests(self, response):
        items = response.css(".entry-header h2 > a::attr('href')").extract()
        for url in items:
            yield scrapy.Request(url, self.parse)
        next_page = response.css(" li.pagination-next > a::attr('href')").extract_first()
        if next_page:
            url = next_page
            yield scrapy.Request(url, self.parse_requests)

    def parse(self, response):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        soup = BeautifulSoup(response.body, 'html.parser')
        item = Dulich24Item()
        meta_item = dict()
        data_item = dict()
        item['key'] = self.author
        item['domain'] = self.allowed_domains[0]
        item['url'] = response.request.url
        item['category'] = 'am-thuc'
        data_item['title'] = response.css('.entry-header h1 ::text').extract_first().strip()
        data_item['post_by'] = None
        data_item['time_update'] = response.css("time.entry-modified-time::attr('datetime')").get()
        content_sapo = soup.select('div#ftwp-postcontent > *:first-child')
        sapo = ''
        for sp in content_sapo:
            sapo += sp.text
        data_item['sapo'] = sapo
        #---start----bs4-get-paragraphs------------
        content = []
        div_content = soup.select("div#ftwp-postcontent > *")
        for link in div_content[1:]:
            if len(link.find_all('img')) >= 1:
                continue
            if len(link.find_all('a')) >= 1:
                for a_tag in link.find_all('a'):
                    a_tag.string = "<url link='" + a_tag.get('href') + "'>" + a_tag.text + "</url> "
                a = [' '.join([' '.join(x.replace('\xa0', ' ').replace('\n', '').split())
                               for x in list(link._all_strings(strip=True))])]
                content += a
                continue
            else:
                content += [' '.join(x.replace('\xa0', ' ').replace('\n', '').split())
                            for x in list(link._all_strings(strip=True))]
        data_item['paragraphs'] = content
        # ---end----bs4-get-paragraphs------------
        image = list(
            {
                'image_url': img.css('picture img::attr(src),figure img::attr(src)').extract_first(),
                'image_decription': ''.join(img.css('figcaption.wp-caption-text ::text').extract()).strip() or None
            } for img in response.css('.wp-caption.aligncenter')
        )
        data_item['image'] = image
        item['data'] = data_item
        meta_item['crawled_by'] = self.name
        meta_item['crawled_at'] = dt_string
        item['meta'] = meta_item
        yield item
