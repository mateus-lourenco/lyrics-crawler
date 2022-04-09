# -*- coding: utf-8 -*-

from asyncore import write
from pymongo import MongoClient, ASCENDING
import csv

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client.local
    lyrics = db.lyrics
    cursor = lyrics.find({'genre.name':'forro'}).sort("genre.artist.album.year", ASCENDING)
    
    def process_fields(id, song):
        record = {
            "id": id,
            "title": song['title'].strip(),
            "artist": song['artist'].strip() if song['artist'] != "" else "",
            "composer": song['composer'].strip() if song['composer'] != "" else "",
            "album": song['album'].strip(),
            "year": int(song['year']) if song['year'] != "" else 0,
            "lyric": (' ').join(i for i in song['lyric'])
        }
        
        return record
    
    with open('lyrics.csv', mode='w', encoding='utf-8') as file:
        header = ['id','title','artist','composer','album','year','lyric']
        writer = csv.DictWriter(file, fieldnames=header, delimiter=';')
        writer.writeheader()
        
        count = 0
        _id = 1
        
        for document in cursor:
            
            song = {
                "title":        document["genre"]["artist"]["album"]["song"]["title"],
                "artist":       document["genre"]["artist"]["name"],
                "composer":     document["genre"]["artist"]["album"]["song"]["composer"],
                "album":        document["genre"]["artist"]["album"]["title"],      
                "year":         document["genre"]["artist"]["album"]["year"],
                "lyric":        document["genre"]["artist"]["album"]["song"]["lyric"]
            }
            
            rec = process_fields(_id, song)
        
            writer.writerow(rec)
            
            print(f'{count} documents processed')
            count+=1
            _id+=1