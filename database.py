import os
from sqlite3 import Connection, Cursor, connect
from mysql import connector
from mysql.connector import MySQLConnection

DATA_TABLE_NAME = "song_lyrics"
DATA_TABLE_QUERY = f"""CREATE TABLE IF NOT EXISTS {DATA_TABLE_NAME}(
id INTEGER PRIMARY KEY AUTO_INCREMENT,
album VARCHAR(120),
image VARCHAR(150),
lyrics TEXT NOT NULL,
lyrics_by VARCHAR(100) DEFAULT NULL,
name VARCHAR(100),
slug VARCHAR(150) NOT NULL,
sung_by VARCHAR(120) DEFAULT NULL,
video VARCHAR(100),
UNIQUE (slug)
)
"""

LINK_TABLE_NAME = "artist_links"
LINK_TABLE_QUERY = f"""CREATE TABLE IF NOT EXISTS {LINK_TABLE_NAME}(
id INTEGER PRIMARY KEY AUTO_INCREMENT,
link VARCHAR(150) NOT NULL,
UNIQUE (link)
)
"""

LINK_INSERT_QUERY = f"""INSERT INTO {LINK_TABLE_NAME}(id, link) values(%s, %s)"""
DATA_INSERT_QUERY = f"INSERT INTO {DATA_TABLE_NAME} values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

LINK_SELECT_QUERY = lambda limit: f"SELECT * FROM {LINK_TABLE_NAME} LIMIT {limit}"
LINK_DELETE_QUERY = f"DELETE FROM {LINK_TABLE_NAME} WHERE id=%s"


class Database:
    def __init__(self):
        name = os.getenv("DB_NAME")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        user = os.getenv("DB_USER")
        passwd = os.getenv("DB_PASSWORD")

        if all([name, host, port, user, passwd]):
            print("Connecting to remote database")
            self.connection = connector.connect(
                host=host,
                port=port,
                user=user,
                passwd=passwd,
                database=name
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute(LINK_TABLE_QUERY)
            self.cursor.execute(DATA_TABLE_QUERY)
            self.connection.commit()
            print("database initialized")

    def insert_links(self, links: list[tuple[None, str]]):
        """params: [link]"""
        self.cursor.executemany(LINK_INSERT_QUERY, links)
        self.connection.commit()

    def insert_data(self, data: list[tuple[None, str, str, str, str, str, str, str, str]]):
        """params: [None, album, image, lyrics, lyrics_by, name, slug, sung_by, video]"""
        self.cursor.executemany(DATA_INSERT_QUERY, data)
        self.connection.commit()

    def get_link(self, limit: int = 2):
        self.cursor.execute(LINK_SELECT_QUERY(limit))
        return [(link[0], link[1]) for link in self.cursor.fetchall()]

    def delete_link(self, link_ids: list[int]):
        self.cursor.executemany(LINK_DELETE_QUERY, [(i,) for i in link_ids])
        self.connection.commit()

    def close_db(self):
        self.connection.commit()
        self.connection.close()
