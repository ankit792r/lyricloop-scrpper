from scrappers.link.base_scrapper import BaseLinkScrapper
from bs4 import BeautifulSoup

class LyricsWingLinkScrapper(BaseLinkScrapper):
    scrapper_name = "lyricswing"

    def __init__(self, connection, session):
        super().__init__(connection, session)

    def extract_link(self, page:int = None):
        song_links = []

        for i in range(1, page):
            try:
                page_data = self.session.get(f"https://lyricalwings.com/page/{i}/")

                page_data.raise_for_status()

                page_soup = BeautifulSoup(page_data.text, "html.parser")

                articles = page_soup.find_all("article")

                for article in articles:
                    try:
                        link_tag = article.find("a")
                        if len(song_links) == 30:
                            self.insert_links(song_links)
                            song_links = []
                        song_links.append((self.scrapper_name, link_tag.attrs["href"]))
                    except Exception as e:
                        print(e)

            except Exception as e:
                print(f"failed to fetch page {i}, {e}")
        self.insert_links(song_links)