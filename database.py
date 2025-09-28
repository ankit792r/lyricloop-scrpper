from sqlite3 import Connection, Cursor, connect

DATA_TABLE_NAME = "song_lyrics"
DATA_TABLE_QUERY = f"""CREATE TABLE IF NOT EXISTS {DATA_TABLE_NAME}(
id INTEGER PRIMARY KEY AUTOINCREMENT,
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
id INTEGER PRIMARY KEY AUTOINCREMENT,
link VAR_CHAR(150) NOT NULL
)
"""

LINK_INSERT_QUERY = f"""INSERT INTO {LINK_TABLE_NAME} values(?, ?)"""
DATA_INSERT_QUERY = f"INSERT INTO {DATA_TABLE_NAME} values(?, ?, ?, ?, ?, ?, ?, ?, ?)"

LINK_SELECT_QUERY = lambda limit: f"SELECT * FROM {LINK_TABLE_NAME} LIMIT {limit}"
LINK_DELETE_QUERY = f"DELETE FROM {LINK_TABLE_NAME} WHERE id=?"

class Database:
    def __init__(self):
        self.connection: Connection  = connect("test.sqlite3", check_same_thread=False)
        self.connection.execute(LINK_TABLE_QUERY)
        self.connection.execute(DATA_TABLE_QUERY)
        self.connection.commit()

    def insert_links(self, links:list[tuple[None, str]]):
        """params: [link]"""
        self.connection.executemany(LINK_INSERT_QUERY, links)
        self.connection.commit()

    def insert_data(self, data:list[tuple[None, str, str, str, str, str, str, str, str]]):
        """params: [None, album, image, lyrics, lyrics_by, name, slug, sung_by, video]"""
        self.connection.executemany(DATA_INSERT_QUERY, data)
        self.connection.commit()

    def get_link(self, limit:int=2):
        cursor: Cursor = self.connection.execute(LINK_SELECT_QUERY(limit))
        return [(link[0], link[1]) for link in cursor.fetchall()]
    
    def delete_link(self, link_ids:list[int]):
        self.connection.executemany(LINK_DELETE_QUERY, [(i, ) for i in link_ids])
        self.connection.commit()

    def close_db(self):
        self.connection.commit()
        self.connection.close()