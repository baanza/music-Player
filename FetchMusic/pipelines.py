from itemadapter import ItemAdapter
from libsql_client import create_client
import sqlite3
from .items import Album, Song
import os
from sqlmodel import SQLModel, Session, Field, Relationship, create_engine
# from sqlalchemy.pool import StaticPool
# from sqlalchemy import create_engine
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

class AlbumDb(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    artist: str = Field(index=True)
    runtime: str
    songs: list["SongDb"] = Relationship(back_populates="album")


class SongDb(SQLModel, table=True):
    song_id: int = Field(primary_key=True)
    coverart: str = Field(default=None)
    name: str = Field(index=True)
    artist: str = Field(index=True)
    duration: str = Field(default=None)
    download_link: str = Field(default=None)
    album_id : int | None = Field(default=None, foreign_key="albumdb.id")
    album: AlbumDb | None = Relationship(back_populates="songs")
    


class FetchmusicPipeline:

    def __init__(self):
        load_dotenv()
        self.engine = create_engine(os.environ.get("NEON_URL"))
        SQLModel.metadata.create_all(self.engine)
        # self.dbfunctions()
        auth_manager = SpotifyClientCredentials(client_id=os.environ.get("ID"), client_secret=os.environ.get("SECRET"))
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        
    # async def dbfunctions(self):
    #     db_url = os.environ.get("TURSO_URL")
    #     db_token = os.environ.get("TURSO_TOKEN")
    #     connection = create_client(db_url, auth_token=db_token).connect().cursor().connection
    #     self.engine = create_engine("sqlite://", creator=lambda:connection, poolclass=StaticPool,connect_args={"check_same_thread":True})
    #     SQLModel.metadata.create_all(self.engine)
        

    def process_item(self, item, spider):
        print("processing item ...")
        if isinstance(item, Song):
            self.process_song(item)
        elif isinstance(item, Album):
            adapter = ItemAdapter(item)
            album = AlbumDb(name= adapter.get("name"), artist=adapter.get("artist"), runtime=adapter.get("runtime"))
            for song in item.get("songs"):
                self.insert_song(song, album)

        return item
    
    def process_song(self, item):
        adapter = ItemAdapter(item)
        
        title = adapter.get("name", "unknown")
        if "–" in title :
            parts = title.split("–")
            adapter["name"] = parts[1].strip()
            adapter["artist"] = parts[0].strip()
        self.insert_song(item)
        
    def insert_song(self, item, album: AlbumDb | None = None):
        print("found  a song ...,,tryna add it to the database")
        adapter = ItemAdapter(item)
        if adapter.get("cover") is None:
            adapter["cover"] = self.sp.search(f"artist:{adapter['artist']} track:{adapter['name']}", limit=1)['tracks']['items'][0]['album']["images"][0]['url']
        with Session(self.engine) as session:
           try:
                if album:
                    song = SongDb(coverart=adapter.get("cover"),name=adapter.get("name"), artist=adapter.get("artist"), duration=adapter.get("duration", "empty"), album=album, download_link=adapter.get("Download_link"))
                else:
                    song = SongDb(coverart=adapter.get("cover"),name=adapter.get("name"), artist=adapter.get("artist"), duration=adapter.get("duration", "empty"), download_link=adapter.get("Download_link"))
                session.add(song)
                session.commit()
                session.refresh(song)
           finally:
               session.close()
            
            
        
    
    