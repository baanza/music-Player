from itemadapter import ItemAdapter
import sqlite3
from .items import Album, Song
import os


class FetchmusicPipeline:

    def __init__(self):
        self.create_db()
        self.create_tables()
        

    def create_db(self):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "server.db"))
        self.curr = self.conn.cursor()
    
    def create_tables(self):
        self.curr.executescript("""
                -- Create the Song table if it does not exist
CREATE TABLE IF NOT EXISTS Song (
    song_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for each song
    coverart TEXT,                               -- Cover art URL or path
    song_no INTEGER,                             -- Song number in the album
    name TEXT,                                   -- Name of the song
    artist TEXT,                                 -- Artist of the song
    duration INTEGER,                            -- Duration of the song in seconds
    download_link TEXT                           -- Link to download the song
);

-- Create the Album table if it does not exist
CREATE TABLE IF NOT EXISTS Album (
    album_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for each album
    name TEXT,                                   -- Name of the album
    artistName TEXT,                             -- Name of the artist
    runtime INTEGER,                             -- Total runtime of the album in seconds
    song_list TEXT                               -- List of song IDs (could be a comma-separated string or a JSON array)
);

-- Create a junction table for the many-to-many relationship if it does not exist
CREATE TABLE IF NOT EXISTS AlbumSong (
    album_id INTEGER,
    song_id INTEGER,
    PRIMARY KEY (album_id, song_id),
    FOREIGN KEY (album_id) REFERENCES Album(album_id),
    FOREIGN KEY (song_id) REFERENCES Song(song_id)
);


""")

    def process_item(self, item, spider):
        print("processing item ...")
        if isinstance(item, Song):
            self.process_song(item)
        elif isinstance(item, Album):
            ids = []
            for song in item.get("songs"):
                self.insert_song(song)
                self.curr.execute("SELECT song_id FROM Song WHERE name = ? AND artist = ?", (song.get("name"), song.get("artist")))
                song_id = self.curr.fetchone()
                ids.append(song_id)
            self.insert_album(item, ids)

        return item
    
    def process_song(self, item):
        adapter = ItemAdapter(item)

        title = adapter.get("name")
        artist = adapter.get("artist")
        if "-" in title:
            adapter["name"] = title.split("-")[0].strip()
            adapter["artist"] = title.split("-")[1].strip()
            print("cleaner")
        self.insert_song(item)

    def insert_song(self, item):
        print("found  a song ...,,tryna add it to the database")
        self.curr.execute(""" INSERT INTO Song (coverart, song_no, name, artist, duration, download_link) VALUES (?, ?, ?, ?, ?, ?) """, 
            ( item.get('cover'), item.get('song_no'), item.get('name'), item.get('artist'), item.get('duration'), item.get('Download_link') ))
        self.conn.commit()
        
    
    def insert_album_song(self, album_id, song_id):
        self.curr.execute("""
            INSERT INTO AlbumSong (album_id, song_id)
            VALUES (?, ?)
        """, (album_id, song_id))
        self.conn.commit()
    
    def insert_album(self, item, ids):
        print("just spotted an album")
        self.curr.execute("""
                INSERT INTO Album (name, artistName, runtime, song_list)
                VALUES (?, ?, ?, ?)
            """, (
                item.get("name"),
                item.get("artist"),
                item.get("runtime"),
                ",".join(str(id) for id in ids)
            ))
        self.conn.commit()
        
