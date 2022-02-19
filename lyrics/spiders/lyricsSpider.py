from scrapy import Request, Spider
from lyrics.items import LyricsItem
import ipdb

class LyricsSpider(Spider):
    name = 'lyricsSpider'
    allowed_domains = ['www.letras.mus.br']
    start_urls = ['https://www.letras.mus.br']
    music_genres = ['axe', 'forro', 'samba']

    def parse(self, response):

        base_url = self.start_urls[0] + '/estilos/'
        
        for genre in self.music_genres:
            url = base_url + genre + '/todosartistas.html'
            request = Request(url=url, callback=self.artist_parse, meta={'genre': genre})
            yield request
    
    def artist_parse(self, response):

        artists_endpoints = response.css('li a::attr(href)').getall()
        artist_page_urls = [self.start_urls[0] + i for i in artists_endpoints]

        for url in artist_page_urls:
            yield Request(url=url, callback=self.album_parse, meta={'genre': response.meta['genre']})

    def album_parse(self, response):

        albums_link = response.css('.artista-albuns h3 a::attr(href)').get()

        if (albums_link is not None):

            albums_endpoint = self.start_urls[0] + albums_link
            
            yield Request(url=albums_endpoint, callback=self.song_parse, meta={'genre': response.meta['genre']})

    def song_parse(self, response):

        dicography_selector = response.css('.discography-container')
        albums_selector = dicography_selector.css("div[data-type='album']")

        genre = {}
        album = {}

        for selector in albums_selector:

            genre['name'] = response.meta['genre']
            album_name = selector.css("h1 a::text").get()
            album_year = selector.css(".header-info::text").get()
            songs_urls = selector.css("li::attr(data-shareurl)").getall()

            album['name'] = album_name
            album['year'] = album_year

            genre['album'] = album

            for url in songs_urls:

                url_parts = url.split("#")

                yield Request(url=url_parts[0], callback=self.lyrics_parse, meta={'genre': genre}) 
   
    def lyrics_parse(self, response):

        lyric_main = response.css('.letra-menu')

        if lyric_main is not None: 

            translate = lyric_main.css('a ::attr(data-tt)').get()

            if translate is None:
            
                item = None

                head_selector = response.css('.cnt-head_title')
                artist_name = head_selector.css('h2 span::text').get()

                if artist_name is not None:

                    lyric_title = head_selector.css('h1 ::text').get()
                    lyric = response.css(".cnt-letra p::text").getall()

                    composer = response.css('.letra-info_comp ::text').get()

                    item = {
                        'genre' : response.meta['genre']['name'],
                        'artist_name': artist_name, 
                        'album_name': response.meta['genre']['album']['name'],
                        'album_year': response.meta['genre']['album']['year'],
                        'song_name' : lyric_title,
                        'composer': composer,
                        'lyric' : lyric
                    }

                    yield LyricsItem(item)

        
