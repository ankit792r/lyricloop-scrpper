from sqlite3 import Connection

def get_links(conn:Connection, **kwargs)-> list[tuple[str, str]]:
    query = f"select site, link from data_link "
    if kwargs.get("site") is not None: query += f"where site=? "
    if kwargs.get("limit") is not None and kwargs.get("offset") is not None: 
        query += f"limit ? offset ?"

    cursor = conn.execute(query, [v for _, v in kwargs.items()])
    return [link for link in cursor.fetchall()]

def save_data(conn:Connection, data:list):
    query = f"insert into song_data(slug, name, lyrics, album, sungBy, lyricsBy, image, video) values(?, ?, ?, ?, ?, ?, ?, ?)"
    conn.execute(query, data)
    conn.commit()
    print("saved -", data[0])