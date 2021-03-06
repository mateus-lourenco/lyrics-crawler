# -*- coding: utf-8 -*-

from pymongo import MongoClient, ASCENDING
import json

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client.local
    lyrics = db.lyrics
    cursor = lyrics.find({'genre.name':'forro'}).sort("genre.artist.album.year", ASCENDING)
    
    def process_fields(song):
        record = {
            "title": song.title.strip(),
            "artist": song.artist.strip(),
            "composer": song.composer.strip(),
            "album": song.album.strip(),
            "album_year": int(song.album_year) if song.album_year is not "" else 0,
            "lyric": ('').join(i + '\n' for i in song.lyric)
        }
        
        return record
    
    with open('lyrics_df.json', mode='w', encoding='utf-8') as file:
        count = 0
        _id = 1
        
        file.write('{ "dataset": [')
        
        for document in cursor:
            
            song = {
                "title":        document["genre"]["artist"]["album"]["song"]["title"],
                "artist":       document["genre"]["artist"]["name"],
                "composer":     document["genre"]["artist"]["album"]["song"]["composer"],
                "album":        document["genre"]["artist"]["album"]["title"],      
                "album_year":   document["genre"]["artist"]["album"]["year"],
                "lyric":        document["genre"]["artist"]["album"]["song"]["lyric"]
            }
            
            rec = process_fields(song)
            
            line = {'id': _id, "song": rec}
            json.dump(
                    line, 
                    file, 
                    ensure_ascii=False,
                    indent=3)
            
            file.write(',')
            file.write('\n')
            
            print(f'{count} documents processed')
            count+=1
            _id+=1
        
        file.write(']}')
        