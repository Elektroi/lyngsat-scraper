# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Satellite(scrapy.Item):
    continent = scrapy.Field()
    name = scrapy.Field()
    grade = scrapy.Field()
    url = scrapy.Field()
    band = scrapy.Field()
    date = scrapy.Field()


class Satellites(scrapy.Item):
    satellites = scrapy.Field()


class Frequency(scrapy.Item):
    frequency = scrapy.Field()
    url = scrapy.Field()
    beam = scrapy.Field()
    eirp = scrapy.Field()


class Frequencies(scrapy.Item):
    frequencies = scrapy.Field()


class Provider(scrapy.Item):
    provider = scrapy.Field()
    url = scrapy.Field()
    logo_url = scrapy.Field()
    system = scrapy.Field()
    sr_fec = scrapy.Field()
    onid_tid = scrapy.Field()
    cn_lock = scrapy.Field()
    source_updated = scrapy.Field()


class Providers(scrapy.Item):
    providers = scrapy.Field()