# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
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
        try:
            composer = adapter['composer'].split(':').pop()
        except:
            composer = ''
        song = {
            'genre': adapter['genre'],
            'artist_name': adapter['artist_name'],
            'composer': composer.strip(),
            'song_name': adapter['song_name'],
            'lyric': adapter['lyric']
        }
        lyric = self.db.lyrics.find_one({
                                            "genre": song.genre,
                                            "song_name": song.song_name, 
                                            "artist_name": song.artist_name
                                        })
        if lyric is None:
            self.db[self.collection_name].insert_one(song)

        return adapter
