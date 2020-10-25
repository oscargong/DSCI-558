# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ComedyItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    url = scrapy.Field()
    timestamp_crawl = scrapy.Field()
    title = scrapy.Field()
    genres = scrapy.Field()
    languages = scrapy.Field()
    release_date = scrapy.Field()
    budget = scrapy.Field()
    gross = scrapy.Field()
    runtime = scrapy.Field()


class CastItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    timestamp_crawl = scrapy.Field()
    name = scrapy.Field()
    date_of_birth = scrapy.Field()
    place_of_birth = scrapy.Field()
    date_of_death = scrapy.Field()
    place_of_death = scrapy.Field()
    mini_bio = scrapy.Field()