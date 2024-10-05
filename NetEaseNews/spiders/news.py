import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from NetEaseNews.items import NewsItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging
import time
class News163Spider(CrawlSpider):
    name = 'www.163.com'
    row_count=0
    allowed_domains = ['www.163.com']
    start_urls = ['https://tech.163.com/']
    rules = (
        Rule(LinkExtractor(allow=r'https://www.163.com/dy/article/'), callback='parse_item',
             follow=False),
    )

    def __init__(self, *args, **kwargs):
        super(News163Spider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 运行无头模式
        try:
            self.driver = webdriver.Chrome(options=chrome_options)  # 或者使用其他浏览器驱动
        except Exception as e:
            logging.error(f"Failed to initialize WebDriver: {e}")
            raise





    def parse_item(self, response):
        logging.info(f"Parsing item URL: {response.url}")
        item = NewsItem()
        self.get_title(response, item)
        self.get_time(response, item)
        self.get_source(response, item)
        self.get_source_url(response, item)
        self.get_text(response, item)
        self.get_url(response, item)
        self.get_tag(response, item)
        self.set_modified_timestamp(response, item)
        self.row_count += 1
        if self.row_count >= 100:
            raise scrapy.exceptions.CloseSpider(reason="Reached maximum row count")
        yield item

        # 在发送请求之前检查是否已达到限制

    def get_url(self, response,item):
        url = response.url
        if url:
            item['news_url'] = url

    def get_text(self, response, item):
        text = response.css('.post_body p::text').getall()
        if text:
            logging.info(f"text: {text}")
            item['news_body'] = text

    def get_source_url(self, response, item):

        source_url = response.css("ne_article_source::attr(href)").extract()
        if source_url:
            item['source_url'] = source_url[0]

    def get_source(self, response, item):
        source = response.css("ne_article_source::text").extract()
        if source:
            logging.info(f"source: {source[0]}")
            item['news_source'] = source[0]

    def get_time(self, response, item):
        meta_tag = response.css('meta[property="article:published_time"]')
        if meta_tag:
            published_time = meta_tag.attrib.get('content')
            item['news_time'] = published_time

    def get_title(self, response, item,):
        meta_tag = response.css('meta[property="og:title"]')
        if meta_tag:
            title = meta_tag.attrib.get('content')
            logging.info(f"title: {title}")
            item['news_title'] = title

    def get_tag(self, response, item):
        html_tag = response.css('#ne_wrap')
        if html_tag:
            category = response.css('html[data-category]').attrib.get('data-category')
            item['news_tag']=category
            logging.info(f"news_tag: {item['news_tag']}")
    def get_source(self, response,item):
        post_info = response.css('div.post_info')
        if post_info:
            a_tag = post_info.css('a::text').get()
            item['news_source'] = a_tag.strip()
            logging.info(f"news_source: {item['news_source']}")

    def get_source_url(self, response, item):
        post_info = response.css('div.post_info')
        if post_info:
            a_link = post_info.css('a::attr(href)').get()
            item['source_url'] = a_link.strip()
            logging.info(f"source_url: {item['source_url']}")

    def set_modified_timestamp(self, response, item):
        current_milliseconds_timestamp = int(time.time() * 1000)
        if current_milliseconds_timestamp:
            item['modified_timestamp'] = current_milliseconds_timestamp
    def closed(self, reason):
        self.driver.quit()


