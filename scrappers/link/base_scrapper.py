from abc import ABC, abstractmethod
from sqlite3 import Connection, connect
from requests import Session

class BaseLinkScrapper(ABC):
    table_name = "datalink"
    def __init__(self, connection: Connection, session: Session):
        self.connection = connection
        self.session = session
        self.proxies = {}
        
        query = f"create table if not exists {self.table_name}(id integer primary key autoincrement, site varchar(120), link varchar(255))"
        self.connection.execute(query)
        # self.connection.executemany("insert into datalink(site, link) values(?, ?)", [("test", "temp"), ("test1", "temp2")])
        # self.connection.commit()

    @abstractmethod
    def extract_link(self, page:int = None):
        pass

    def insert_links(self, links:list[tuple[str, str]] = []):
        query = f"insert into {self.table_name}(site, link) values(?, ?)"
        self.connection.executemany(query, links)
        self.connection.commit()

    def get_links(self, **kwargs):
        query = f"select * from datalink "
        if kwargs.get("site") is not None: query += f"where site=? "
        if kwargs.get("limit") is not None and kwargs.get("offset") is not None: 
            query += f"limit ? offset ?"

        cursor = self.connection.execute(query, [v for _, v in kwargs.items()])
        return [link for link in cursor.fetchall()]


# conn = connect("temp/data.db", check_same_thread=False)
# base = BaseLinkScrapper(connection=conn)
# print(base.get_links(limit=1, offset=1))