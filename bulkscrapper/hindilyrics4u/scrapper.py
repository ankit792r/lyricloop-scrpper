import requests
from bs4 import BeautifulSoup
from string import ascii_lowercase
from requests import Session
from sqlite3 import connect, Connection
from utils import save_data, initilize_sqlite_db, upload_to_db
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from os import environ
from time import sleep
from re import findall

load_dotenv()

database_url = environ.get("DATABASE_URL")
if database_url is None:
    raise Exception("database url is not provided")

base_url:str = "https://www.hindilyrics4u.com"
alpha_limit:dict[str, int] = dict()
song_links:list[str] = list()

session:Session = requests.session() 

for alpha in ascii_lowercase:
    try:
        page = session.get(f"https://www.hindilyrics4u.com/movie/{alpha}.php")
        page.raise_for_status()
        page_soup_temp = BeautifulSoup(page.text, "html.parser")
        text:str = page_soup_temp.find("td", {"class": "alcen w720 bg7f"}).text
        numbers = findall(r'\d+', text)
        alpha_limit[alpha] = max(map(int, numbers)) if numbers else 1
    except:
        print("failed to scrap alpha limit ", alpha)

for alpha in ascii_lowercase:
    for page_num in range(1, alpha_limit[alpha] + 1):
        try:
            page = session.get(f"https://www.hindilyrics4u.com/movie/{alpha}.php?page={page_num}")
            page.raise_for_status()

            page_soup = BeautifulSoup(page.text, "html.parser")

            link_tags = page_soup.find_all("a", {"class": "thumb"})

            for link_tag in link_tags:
                album_page_link = f"{base_url}{link_tag.attrs["href"]}"
                
                try:
                    album_page = session.get(album_page_link)
                    album_page.raise_for_status()
                    album_page_soup = BeautifulSoup(album_page.text, "html.parser")

                    link_tags = album_page_soup.find_all("a", {"itemprop": "url"})
                    for link in link_tags:
                        song_links.append(f"{base_url}{link.attrs["href"]}")

                except Exception as e:
                    print(f"failed to load page ", album_page)

        except Exception as e:
            print(f"Failed to scrap page {page_num} and alpha {alpha}", e)

def scrapp_data(song_link:str):
    try:
        page = session.get(song_link)
        page.raise_for_status()

        page_soup = BeautifulSoup(page.text, "html.parser")

        search = song_link[len(base_url):]
        name = page_soup.find("a", {"href": search, "itemprop": "url"}).text

        slug = name.lower().replace(" ", "-")

        sung_by = page_soup.find("span", {"itemprop": "byArtist"}).text

        album = page_soup.find("td", {"itemprop": "inAlbum"}).text

        lyrics_by = page_soup.find("span", {"itemprop": "lyricist"}).text

        lyrics_span = page_soup.find("span", {"itemprop": "lyrics"})

        lyrics = lyrics_span.find("span", {"itemprop": "text"}).text

        iframe = page_soup.find("iframe")

        if iframe:
            vid_id = iframe.attrs["src"].split("/").pop()
            image = f"https://img.youtube.com/vi/{vid_id}/hqdefault.jpg"
            video = f"https://www.youtube.com/watch?v={vid_id}"
        else:
            image, video = "", ""
        sleep(2)
        return [slug, name, lyrics, album, sung_by, lyrics_by, image, video]
    except Exception as e:
        print(f"failed to scrap song of {song_link}", e)
        return None

connection:Connection = connect("temp/data.db", check_same_thread=False)
initilize_sqlite_db(conn=connection)

with ThreadPoolExecutor(100, 'bulk-hindi-') as executor:
    for result in executor.map(scrapp_data, song_links):
        if result:
            save_data(conn=connection, data=result)

upload_to_db(url=database_url, conn=connection)

connection.close()

