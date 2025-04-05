from mysql import connector
from urllib.parse import urlparse
from sqlite3 import Connection
from logger import logger

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

        query = "INSERT IGNORE INTO song (name, album, lyrics_by, sung_by, slug, image, lyrics, video) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        lite_cursor = conn.execute("select * from song_data")
        for res in lite_cursor.fetchmany(30):
            cursor.executemany(query, res)
            database.commit()

        database.close()
        logger.info(f"Successfully uploaded to {url}")
    except Exception as e:
        print(e)


