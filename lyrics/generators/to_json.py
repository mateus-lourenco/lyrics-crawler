from pymongo import MongoClient
import json

mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['local']
songs = db.lyrics.find({})

with open('lyrics_db.json', mode='w', encoding='utf-8') as file:
    count = 0

    for song in songs:

        line = {
            "genre" : {
                "name" : song['genre']['name'],
                "artist" : {
                    "name" : song['genre']['artist']['name'],
                    "album" : {
                        "title" : song['genre']['artist']['album']['title'],
                        "year" : song['genre']['artist']['album']['year'],
                        "song" : {
                            "title" : song['genre']['artist']['album']['song']['title'],
                            "composer" : song['genre']['artist']['album']['song']['composer'],
                            "lyric" : song['genre']['artist']['album']['song']['lyric']
                        }
                    }
                }
            }
        }


        json.dump(line, file, separators=(',', ':'), indent=4)
        count += 1
        print(f'{count} processed')