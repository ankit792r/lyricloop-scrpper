from extractors import lyricmint
from requests import Session, RequestException
from json import dump, load
import concurrent.futures
from functools import partial
import os

TMEP_FILE_PATH = "temp/data.json"

def execute_scraping(session, url):
    try:
        return lyricmint(session, url)
    except RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def scrap_data(url_list: list):
    data = []
    session = Session()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10, thread_name_prefix="work") as executor:
        scrap_function = partial(lyricmint, session)
        for result in executor.map(scrap_function, url_list):
            print("extracted - ", "\r")
            if result:
                print(result["name"])
                data.append(result)

    with open(TMEP_FILE_PATH, "w+") as file:
        dump(obj=data, fp=file, indent=2)

def upload_to_web(url:str):
    try:
        data_file = open(TMEP_FILE_PATH, "r")
        session = Session()
        response = session.post(url=url, data=load(data_file))
        if (response.status_code == 201):
            print("data uploaded")
            data_file.close()
            os.remove(TMEP_FILE_PATH)
            session.close()
            return True
        else: return False
    except RequestException as e:
        print(e)
        return False

def upload_to_db(url:str):
    from mysql import connector
    from urllib.parse import urlparse
    parsed = urlparse(url)

    config = {
        "host": parsed.hostname,
        "port": parsed.port or 3306,
        "user": parsed.username,
        "password": parsed.password,
        "database": parsed.path.lstrip("/"),
    }

    try:
        data = []
        data_file = open(TMEP_FILE_PATH, "r")
        for song in load(data_file):
            data.append((song["name"], song["album"], song["lyricsBy"], song["sungBy"], song["slug"], song["image"], song["lyrics"], song["video"]))

        database = connector.connect(**config)
        cursor = database.cursor()
        
        query = "INSERT INTO song (name, album, lyrics_by, sung_by, slug, image, lyrics, video) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        
        cursor.executemany(query, data)
        database.commit()
        database.close()
        return True

    except Exception as e:
        print(e)
        return False


