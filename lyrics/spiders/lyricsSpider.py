from scrapy import Request, Spider
from lyrics.items import Genre
import ipdb

class LyricsSpider(Spider):
    name = 'lyricsSpider'
    allowed_domains = ['www.letras.mus.br']
    start_urls = ['https://www.letras.mus.br']
    music_genres = ['axe', 'forro', 'samba']

    def parse(self, response):
        base_url = self.start_urls[0] + '/estilos/'
        
        for genre in self.music_genres:
            urls = [base_url + genre + '/artistas.html']

            for url in urls:
                request = Request(url=url, callback=self.artist_parse, meta={'genre': genre})
                yield request
    
    def artist_parse(self, response):
        artist_class = response.css('.home-artistas')
        artists_endpoints = artist_class.css('a::attr(href)').getall()
        artist_page_urls = [self.start_urls[0] + i for i in artists_endpoints]

        for url in artist_page_urls:
            yield Request(url=url, callback=self.songs_parse, meta={'genre': response.meta['genre']})

    def songs_parse(self, response):
        songs_selector = response.css('.cnt-list--alp')
        songs_container = songs_selector.css('.list-container')
        songs_endpoints = songs_container.css('a::attr(href)').getall()
        songs_urls = [self.start_urls[0] + i for i in songs_endpoints]
        
        for url in songs_urls:
            yield Request(url=url, callback=self.lyrics_parse, meta={'genre': response.meta['genre']}) 
    
    def lyrics_parse(self, response):
        translate = response.css('.letra-menu a ::attr(data-tt)').get()
        if translate is None:

            lyric_selector = response.css('.cnt-letra')
            lyric = lyric_selector.css('p ::text').getall()

            head_selector = response.css('.cnt-head_title')
            lyric_title = head_selector.css('h1 ::text').get()
            artist_name = head_selector.css('h2 span::text').get()

            composer = response.css('.letra-info_comp ::text').get()

            genre = {
                'name' : response.meta['genre'],
                'artist' : 
                {
                    'name': artist_name, 
                    'song' : 
                    {
                        'title' : lyric_title,
                        'composer': composer,
                        'lyric' : lyric
                    }
                }
            }

            yield Genre(genre)

        
