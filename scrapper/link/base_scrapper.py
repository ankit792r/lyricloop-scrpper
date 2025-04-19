from abc import ABC, abstractmethod
from sqlite3 import Connection, connect
from requests import Session

class BaseLinkScrapper(ABC):
    scrapper_name = "base_scrapper"
    table_name = "data_link"
    def __init__(self, connection: Connection, session: Session):
        self.connection = connection
        self.session = session
        
        query = f"create table if not exists {self.table_name}(site varchar(120), link varchar(255))"
        self.connection.execute(query)

    @abstractmethod
    def extract_link(self, page:int = None):
        pass

    def insert_links(self, links:list[tuple[str, str]] = []):
        query = f"insert into {self.table_name}(site, link) values(?, ?)"
        self.connection.executemany(query, links)
        self.connection.commit()

# conn = connect("temp/data.db", check_same_thread=False)
# base = BaseLinkScrapper(connection=conn)
# print(base.get_links(limit=1, offset=1))