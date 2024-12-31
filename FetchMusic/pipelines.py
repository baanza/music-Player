from itemadapter import ItemAdapter
import sqlite3
from .items import Album, Song


class FetchMusicPipeline:

    def __init__(self):
        pass

    def create_db(self):
        self.conn = sqlite3.connect("../server.db")
        self.curr = self.conn.cursor()
    
    def create_tables(self):
        self.curr.executescript("create_tables.sql")

    def process_item(self, item, spider):
        if isinstance(item, Song):
            adapter = ItemAdapter(item)
            if "-" in adapter.get("name"):
                adapter["name"] = adapter["name"].split("-")[0]
                print(adapter["name"])
        return item