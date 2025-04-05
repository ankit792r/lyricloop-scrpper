from sqlite3 import Connection

from bs4 import BeautifulSoup
from requests import Session
from scrapper.data.base_scrapper import BaseDataScrapper
import re


def extract_video_id(url: str) -> str:
    match = re.search(r"embed/([^?]+)", url)
    return match.group(1) if match else ""


class LyricsWingDataScrapper(BaseDataScrapper):
    def __init__(self, connection: Connection, session: Session):
        super().__init__(connection, session)

    def scrap_data(self, link:str) -> list | None:
        try:
            page = self.session.get(link)

            page.raise_for_status()

            soup = BeautifulSoup(page.text, "html.parser")

            try:
                iframe = soup.find("iframe")

                video_id = extract_video_id(iframe.attrs["src"])

                thumbnail = f"https://i.ytimg.com/vi_webp/{video_id}/maxresdefault.webp"

                video = f"https://www.youtube.com/watch?v={video_id}"
            except:
                thumbnail = ""

                video = ""

            lyrics_tag = soup.find("div", {"id": "englishlyrics"})

            lyrics = "".join([str(i) for i in lyrics_tag.find_all("p")])

            table_tag = soup.find("table", {"id": "topic_table"})

            td_tags = table_tag.find_all("td", {"style": "width: 70%; height: 19px;"}, limit=4)

            name = td_tags[0].text
            album = td_tags[1].text
            sungBy = td_tags[2].text
            lyricsBy = td_tags[3].text

            slug = name.replace(" ", "-").lower() + album.replace(" ", "-").lower() + sungBy.replace(" ", "-").lower()

            return [slug, name, lyrics, album, sungBy, lyricsBy, thumbnail, video]
        except Exception as e:
            print(e)