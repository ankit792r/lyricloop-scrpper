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

        query = "INSERT IGNORE INTO song (slug, name, lyrics, album, sung_by, lyrics_by, image, video) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        batch_size =50
        offset = 0

        while True:
            lite_cursor = conn.execute("select * from song_data limit ? offset ?", (batch_size, offset, ))
            rows = lite_cursor.fetchall()
            if not rows: break

            cursor.executemany(query, rows)
            database.commit()
            logger.info(f"Successfully uploaded offset {offset}")
            offset += batch_size

        database.close()
        logger.info(f"Successfully uploaded all data to remote")
    except Exception as e:
        logger.error(f"something went wrong to upload {e}")


