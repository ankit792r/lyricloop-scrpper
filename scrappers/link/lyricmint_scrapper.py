from scrappers.link.base_scrapper import BaseLinkScrapper
from bs4 import BeautifulSoup

class LyricMintLinkScrapper(BaseLinkScrapper):
    scrapper_name ="lyricsmint"

    def __init__(self, connection, session):
        super().__init__(connection, session)

    def extract_link(self, page = None):
        links = []
        base_url = "https://lyricsmint.com"
        for i in range(1, page + 1):
            try:
                album_list_page = self.session.get(f"https://lyricsmint.com/albums?page={i}", proxies=self.proxies)

                album_list_page.raise_for_status()

                album_list_page_soup = BeautifulSoup(album_list_page.text, "html.parser")

                album_link_tags = album_list_page_soup.find_all("a", {"class": "h-auto w-full block text-black font-bold bg-white no-underline mt-1"})

                album_links = [base_url + link.attrs["href"] for link in album_link_tags]

                for album in album_links:
                    try: 
                        songs_list_page = self.session.get(album, proxies=self.proxies)

                        songs_list_page.raise_for_status()

                        songs_list_page_soup = BeautifulSoup(songs_list_page.text, "html.parser")

                        link_tags = songs_list_page_soup.find_all("a", {"class": "song h-auto w-full block text-black no-underline song"})

                        for link in link_tags:
                            if len(links) == 30:
                                self.insert_links(links=links)
                                links = []
                            print(link.attrs["href"])
                            links.append((self.scrapper_name, base_url + link.attrs["href"]))

                    except:
                        print(f"failed to extract links from {album}")
            except:
                print(f"failed to extract links from page {i}")