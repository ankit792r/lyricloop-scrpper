from scrapper.data.base_scrapper import BaseDataScrapper
from bs4 import BeautifulSoup
from logger import logger

class LyricsMintDataScrapper(BaseDataScrapper): 

    def __init__(self, connection, session):
        super().__init__(connection, session)

    def scrap_data(self, link) ->list | None:
        try:
            page = self.session.get(link)

            page.raise_for_status()

            soup = BeautifulSoup(page.text, "html.parser")

            slug = link.split('/').pop()

            name = soup.find("span", "current").text

            x = soup.find("div", "text-base lg:text-lg pb-2 text-center md:text-left")
            lyrics = ''.join(str(p) for p in x.find_all('p')) if x else ""; 

            info_soup = soup.find_all("td", "w-3/4 px-5 font-bold border-b border-grey-light", limit=4)

            album = info_soup[1].get_text(separator="", strip=True)

            sungBy = info_soup[0].get_text(separator="", strip=True)

            lyricsBy = info_soup[2].get_text(separator="", strip=True)

            thumb_link = soup.find("img", "absolute w-full h-full border shadow-lg outline-none pin")

            if thumb_link is not None : 
                video = "https://www.youtube.com/watch?v="+str(thumb_link.attrs["src"][27:38])
                image = str(thumb_link.attrs["src"].replace("mq","maxres"))
            else:
                video = ""
                image = ""
            return [slug, name, lyrics, album, sungBy, lyricsBy, image, video]
        except Exception as e:
            logger.error(f"failed to scrap {link}, {e}")
            return None