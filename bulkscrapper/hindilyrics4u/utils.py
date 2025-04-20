from sqlite3 import Connection
from mysql import connector
from urllib.parse import urlparse
from sqlite3 import Connection

def upload_to_db(url:str, conn: Connection):
    parsed = urlparse(url)

    config = {
        "host": parsed.hostname,
        "port": parsed.port or 3306,
        "user": parsed.username,
        "password": parsed.password,
        "database": parsed.path.lstrip("/"),
    }

    try:
        database = connector.connect(**config)
        cursor = database.cursor()

        query = "INSERT IGNORE INTO song (slug, name, lyrics, album, sung_by, lyrics_by, image, video) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        batch_size =50
        offset = 0

        while True:
            lite_cursor = conn.execute("select * from song_data limit ? offset ?", (batch_size, offset, ))
            rows = lite_cursor.fetchall()
            if not rows: break

            cursor.executemany(query, rows)
            database.commit()
            print(f"Successfully uploaded offset {offset}")
            offset += batch_size

        database.close()
        print(f"Successfully uploaded all data to remote")
    except Exception as e:
        print(f"something went wrong to upload {e}")

def save_data(conn:Connection, data:list):
    query = f"insert into song_data(slug, name, lyrics, album, sungBy, lyricsBy, image, video) values(?, ?, ?, ?, ?, ?, ?, ?)"
    conn.execute(query, data)
    conn.commit()

def initilize_sqlite_db(conn:Connection, table_name:str = "song_data"):
    query = f"create table if not exists {table_name}(slug varchar(200), name varchar(200), lyrics varchar(255), album varchar(120), sungBy varchar(150), lyricsBy varchar(150), image varchar(200), video varchar(200))"
    conn.execute(query)

