from abc import ABC, abstractmethod
from sqlite3 import Connection
from requests import Session

class BaseDataScrapper(ABC):
    table_name = "song_data"
    def __init__(self, connection: Connection, session: Session):
        self.connection = connection
        self.session = session

        query = f"create table if not exists {self.table_name}(slug varchar(200), name varchar(200), lyrics varchar(255), album varchar(120), sungBy varchar(150), lyricsBy varchar(150), image varchar(200), video varchar(200))"
        self.connection.execute(query)

    @abstractmethod
    def scrap_data(self, link:str)-> list | None:
        pass
