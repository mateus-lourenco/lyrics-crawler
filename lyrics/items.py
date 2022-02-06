# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Genre(Item):
        name = Field()
        artist = scrapy{
            'name': Field(),
            'song': {
                'title' : Field(),
                'composer': Field(),
                'lyric' : Field()
            }
        }
