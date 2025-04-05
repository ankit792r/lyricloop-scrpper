from requests import Session
from sqlite3 import connect
from importlib import import_module
from scrapper.uploader import upload_to_db
from scrapper.link.base_scrapper import BaseLinkScrapper
from scrapper.data.base_scrapper import BaseDataScrapper
from concurrent.futures import ThreadPoolExecutor, wait
from scrapper.utils import get_links, save_data

class ScrapperApp:
    db_name = "data.db"
    def __init__(self, configs:dict):
        self.configs = configs
        self.session = Session()
        self.session.proxies = configs["proxies"]
        self.conn = connect(f"temp/{self.db_name}", check_same_thread=False)

        self.data_scrappers, self.link_scrappers = self.load_scrappers()

    def load_scrappers(self):
        data_scrappers:dict[str, BaseDataScrapper] = {}

        for scrapper in self.configs["data_scrappers"]:
            ref = import_module(scrapper["path"])
            klass = getattr(ref, scrapper["class"])
            data_scrappers[scrapper["name"]] = klass(self.conn, self.session)

        link_scrappers:dict[str, BaseLinkScrapper] = {}

        for scrapper in self.configs["link_scrappers"]:
            ref = import_module(scrapper["path"])
            klass = getattr(ref, scrapper["class"])
            link_scrappers[scrapper["name"]] = klass(self.conn, self.session)

        return data_scrappers, link_scrappers
    
    def scrap_links(self, page = 1):
        with ThreadPoolExecutor(max_workers=len(self.link_scrappers.keys())) as executor:
            futures = []
            for key in self.link_scrappers.keys():
                scrapper_class:BaseLinkScrapper = self.link_scrappers[key]
                futures.append(executor.submit(scrapper_class.extract_link, page))
            wait(futures)

    def __resolve_scrapper(self, row:tuple[str, str]):
        return self.data_scrappers[row[0]].scrap_data(row[1])

    def scrap_data(self, workers=10):
        with ThreadPoolExecutor(max_workers=workers) as executor:
            for result in executor.map(self.__resolve_scrapper, get_links(self.conn)):
                if result:
                    save_data(self.conn, result)

    def upload(self):
        upload_to_db(self.configs["db_url"], self.conn)
