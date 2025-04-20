from abc import ABC, abstractmethod
from sqlite3 import Connection
from requests import Session
from scrapper.utils import initilize_sqlite_db

class BaseDataScrapper(ABC):
    table_name = "song_data"
    def __init__(self, connection: Connection, session: Session):
        self.connection = connection
        self.session = session

        initilize_sqlite_db(self.connection, self.table_name)

    @abstractmethod
    def scrap_data(self, link:str)-> list | None:
        pass
