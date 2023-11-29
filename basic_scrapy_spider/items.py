# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()


class ReviewItem(scrapy.Item):
    company = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()
    job_role = scrapy.Field()
    job_status = scrapy.Field()
    rating = scrapy.Field()
    work_balance = scrapy.Field()
    benefits = scrapy.Field()
    security_adv = scrapy.Field()
    management = scrapy.Field()
    culture = scrapy.Field()
    pros = scrapy.Field()
    cons = scrapy.Field()
