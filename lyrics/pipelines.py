# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlite3 import adapters
from itemadapter import ItemAdapter
from scrapy.logformatter import logging
import pymongo


class MongoPipeline(object):

    collection_name = "lyrics"

    def __init__(self, mongo_db, mongo_uri):
        self.mongo_db = mongo_db
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        if adapter is not None:

            try:
                composer = adapter['composer'].split(':').pop()
            except:
                composer = ''

            genre = {
                'name': adapter['genre'],
                'artist': {
                    'name': adapter['artist_name'],
                    'album': {
                        'title' : adapter['album_name'],
                        'year' : adapter['album_year'].strip(),
                        'song' : {
                            'title': adapter['song_name'],
                            'composer': composer.strip(),
                            'lyric': adapter['lyric']
                        }
                    }
                }
            }
            
            filter_by = {   
                            'genre.name': genre['name'], 
                            'genre.artist.name': genre['artist']['name'], 
                            'genre.artist.album.song.title': genre['artist']['album']['song']['title']
                        }

            lyric = self.db.lyrics.find_one(filter_by)

            if lyric is None:
                self.db[self.collection_name].insert_one({'genre':genre})

        return adapter
