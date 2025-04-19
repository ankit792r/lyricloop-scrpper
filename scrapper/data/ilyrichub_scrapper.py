from scrapper.data.base_scrapper import BaseDataScrapper
from bs4 import BeautifulSoup
from logger import logger
import re


pattern = r'youtube\.com/vi/([a-zA-Z0-9_-]{11})|ytimg\.com/vi/([a-zA-Z0-9_-]{11})'

class ILyricHubDataScrapper(BaseDataScrapper):
    

    def __init__(self, connection, session):
        super().__init__(connection, session)

    def scrap_data(self, link) ->list | None:
        try:
            page = self.session.get(link)

            page.raise_for_status()

            soup = BeautifulSoup(page.text, "html.parser")

            slug = link.split('/').pop()

            x = soup.find("div", {"class": "song-lyrics"})
            lyrics = ''.join(str(p) for p in x.find_all('p')) if x else ""; 

            song_info = {}

            info_table_rows = soup.select("table tr", {"class": "min-w-full bg-white"})

            for row in info_table_rows:
                header = row.select_one('td.font-medium')
                data_cell = row.select_one('td.py-2:nth-of-type(2)')
                if not header or not data_cell:
                    continue
                
                label = header.get_text(strip=True).rstrip(':')
                
                if label == 'Song':
                    song_info['name'] = data_cell.get_text(strip=True)
                
                elif label == 'Album':
                    album_name = data_cell.select_one('[itemprop="name"]')
                    if album_name:
                        song_info['album'] = album_name.get_text(strip=True)
                
                elif label == 'Singers':
                    singers = [span.get_text(strip=True) for span in data_cell.select('[itemprop="name"]')]
                    song_info['singers'] = singers
                
                elif label == 'Lyricists':
                    lyricists = [span.get_text(strip=True) for span in data_cell.select('[itemprop="name"]')]
                    song_info['lyricists'] = lyricists

            img_tag = soup.find("img", "absolute inset-0 w-full h-full object-cover rounded-lg shadow-md youtube-thumbnail")
            thumb_link = img_tag.attrs["src"]

            match = re.search(pattern=pattern, string=thumb_link)

            if thumb_link is not None and match : 
                link = match.group(1) if match.group(1) else match.group(2)
                video = f"https://www.youtube.com/watch?v={link}"
            else:
                video = ""
                thumb_link = ""

            return [slug, song_info['name'], lyrics, song_info['album'], ", ".join(song_info['singers']), ", ".join(song_info['lyricists']), thumb_link, video]
        except Exception as e:
            logger.error(f"failed to scrap {link}, {e}")
            return None


# import sqlite3
# import requests

# conn = sqlite3.connect("temp/data.db")
# sess  = requests.Session()

# test = ILyricHubDataScrapper(connection=conn, session=sess)
# d = test.scrap_data("https://www.ilyricshub.com/zohra-jabeen-sikandar/")
# print(d)