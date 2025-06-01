import scrapy
from ..items import Album, Song


class KitSpider(scrapy.Spider):
    name = "kit"
    allowed_domains = ["hiphopkit.com"]
    start_urls = ["https://hiphopkit.com"]

    def parse(self, response):
        post = response.css("article.a-file")
        for article in post:
            link = article.css("a::attr(href)").get()
            title = article.css("a::text").get()
            if "Album" in title:
                yield response.follow(link, callback= self.parse_album)
            else:
                yield response.follow(link, callback= self.parse_song)
        next_page = response.css("span.a-page a[title='Next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            print("no next page")
    
    def parse_album(self, response):
        tracks = []

        for every_song in response.css("div.mu-o-unit-c"):
            song = Song()
            song["song_no"] = every_song.css("span.rindx::text").get()
            song["name"] = every_song.css("h4.mu-o-title a::text").get()
            song["artist"] = every_song.css("div.mu-o-prod strong::text").get()
            song["duration"] = every_song.css("div.album-side-2 span::text").get()
            song["Download_link"] = every_song.css("div.mu-o-act a::attr(href)").get()
            tracks.append(song)
            
        album = Album()
        album["name"] = response.css("figure.song-thumbnail img::attr(alt)").get()
        album["artist"] =response.css("div.song-id3-con li a::text").get()
        album["runtime"] =response.css("div.song-id3-con li::text").get()
        album["songs"] = tracks
        
        yield album
    
    def parse_song(self, response):
        song = Song()
    
        song["cover"] = response.css("figure.song-thumbnail img::attr(src)").get()
        song["name"] = response.css("figure.song-thumbnail img::attr(alt)").get()
        song["Download_link"] = response.css("p.song-download a::attr(href)").get()
        
        yield song


