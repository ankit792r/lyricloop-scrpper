from scrapper.link.base_scrapper import BaseLinkScrapper
from bs4 import BeautifulSoup
from logger import logger
from string import ascii_lowercase

class HindiLyrics4u(BaseLinkScrapper):
    scrapper_name = "hindilyrics4u"

    def __init__(self, connection, session, page):
        super().__init__(connection, session)
        self.page = page

    def extract_link(self):
        links = []
        alpha_limit = {}

        for alpha in ascii_lowercase:
            try:
                page = self.session.get(f"https://www.hindilyrics4u.com/movie/{alpha}.php")
                page.raise_for_status()
                page_soup_temp = BeautifulSoup(page.text, "html.parser")
                text:str = page_soup_temp.find("td", {"class": "alcen w720 bg7f"}).text
                alpha_limit[alpha] = text.split(" ").pop()
            except:
                print("failed to grab limit of alpha ", alpha)
            
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