# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LyricsItem(Item):
    genre = Field()
    artist_name = Field()
    album_name = Field()
    album_year = Field()
    song_name = Field()
    composer = Field()
    lyric = Field()

