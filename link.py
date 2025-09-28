import requests
from bs4 import BeautifulSoup

from database import Database

BASE_URL = "https://lyricsmint.com"
BASE_ARTIST_URL = lambda page: f"https://lyricsmint.com/artists?page={page}"

def extract_links(db_instance, from_page: int=1, to_page:int=10):
    for i in range(from_page, to_page):
        try:
            artists_page =  requests.get(BASE_ARTIST_URL(i))
            artists_page.raise_for_status()
            artists_page_soup = BeautifulSoup(artists_page.text, "html.parser")
            artists_div = artists_page_soup.find("div", {"class": "flex flex-wrap m-0 mt-4 overflow-hidden"})
            artists_links_tags = artists_div.find_all("a")
            artists_links = [(None, BASE_URL + link.attrs["href"]) for link in artists_links_tags]
            db_instance.insert_links(artists_links)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    db = Database()
    extract_links(db)
    db.close_db()