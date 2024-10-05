import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    news_title = scrapy.Field()
    news_url = scrapy.Field()
    news_time = scrapy.Field()
    news_source = scrapy.Field()
    source_url = scrapy.Field()
    news_body = scrapy.Field()
    news_tag = scrapy.Field()
    modified_timestamp = scrapy.Field()

