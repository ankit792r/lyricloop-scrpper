from scrapper.link.base_scrapper import BaseLinkScrapper
from bs4 import BeautifulSoup
from logger import logger

class HindiTracksLinkScrapper(BaseLinkScrapper):
    scrapper_name = "hinditrack"

    def __init__(self, connection, session, page):
        super().__init__(connection, session)
        self.page = page

    def extract_link(self):
        links = []

        for i in range(1, self.page):
            try:
                page = self.session.get(f"https://www.hinditracks.in/lyrics/page/{i}")
                
                page_soup = BeautifulSoup(page.text, "html.parser")

                articles = page_soup.find_all("article")

                for art in articles:
                    if len(links) == 10:
                        self.insert_links(links=links)
                        links = []
                    links.append(art.find("a").attrs["href"])
            except:
                logger.error(f"failed to extract links from page {i}")