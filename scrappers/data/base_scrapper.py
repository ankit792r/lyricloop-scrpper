from abc import ABC, abstractmethod
from sqlite3 import Connection, connect
from requests import Session

class BaseDataScrapper(ABC):
    table_name = "songdata"
    def __init__(self, connection: Connection, session: Session):
        self.connection = connection
        self.session = session
        self.proxies = {}

        query = f"create table if not exists {self.table_name}(id integer primary key autoincrement, slug varchar(200), name varchar(200), lyrics varchar(255), album varchar(120), sungBy varchar(150), lyricsBy varchar(150), image varchar(200), video varchar(200))"
        self.connection.execute(query)

    @abstractmethod
    def scrap_data(self, link:str):
        pass
    
    def save_data(self, data:list):
        query = f"insert into {self.table_name}(slug, name, lyrics, album, sungBy, lyricsBy, image, video), values(?, ?, ?, ?, ?, ?, ?, ?)"
        self.connection.execute(query, data)


# conn = connect("temp/data.db")
# bas = BaseDataScrapper(connection=conn)
