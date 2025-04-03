from requests import Session
from sqlite3 import connect
from importlib import import_module
from scrappers.link.base_scrapper import BaseLinkScrapper
from scrappers.data.base_scrapper import BaseDataScrapper
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from pprint import pprint
import yaml
from threading import Thread

class ScrapperApp:
    db_name = "scrap_data.db"
    def __init__(self, configs:dict):
        self.configs = configs
        self.session = Session()
        # TODO add proxy
        self.conn = connect(f"temp/{self.db_name}", check_same_thread=False)

        data_scrappers, link_scrappers = self.load_scrappers()

        self.scrap_links(link_scrappers)


    def load_scrappers(self):
        data_scrappers = {}

        for scrapper in self.configs["data_scrappers"]:
            ref = import_module(scrapper["path"])
            klass = getattr(ref, scrapper["class"])
            data_scrappers[scrapper["name"]] = klass(self.conn, self.session)

        link_scrappers = {}

        for scrapper in self.configs["link_scrappers"]:
            ref = import_module(scrapper["path"])
            klass = getattr(ref, scrapper["class"])
            link_scrappers[scrapper["name"]] = klass(self.conn, self.session)

        return data_scrappers, link_scrappers
    
    def scrap_links(self, link_scrappers:dict):

        with ThreadPoolExecutor(max_workers=len(link_scrappers.keys())) as executor:
            futures = []
            
            for key in link_scrappers.keys():
                scrapper_class:BaseLinkScrapper = link_scrappers[key]
                futures.append(executor.submit(scrapper_class.extract_link, 1))

            as_completed(futures)

            print("after that")

            # for i in as_completed(futures):
            #     pprint(i.result())
            

    def scrap_data(self):
        pass

with open("config.yaml", "r") as cfile:
    config = yaml.safe_load(cfile)

ScrapperApp(config)

