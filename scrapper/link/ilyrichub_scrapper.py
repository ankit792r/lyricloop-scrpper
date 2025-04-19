from scrapper.link.base_scrapper import BaseLinkScrapper
from bs4 import BeautifulSoup
from logger import logger

class ILyricHubLinkScrapper(BaseLinkScrapper):
    scrapper_name = "ilyrichub"

    def __init__(self, connection, session, page):
        super().__init__(connection, session)
        self.page = page

    def extract_link(self):
        links = []

        for i in range(1, self.page):
            try:
                page = self.session.get(f"https://www.ilyricshub.com/hindi/page/{i}")
                
                page_soup = BeautifulSoup(page.text, "html.parser")

                link_tags = page_soup.find_all("a", {"class": "block bg-white shadow-md rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-200"})

                for a in link_tags:
                    if len(links) == 10:
                        self.insert_links(links=links)
                        links = []
                    links.append((self.scrapper_name, a.attrs["href"]))
            except:
                logger.error(f"failed to extract links from page {i}")
        self.insert_links(links=links)