from requests import sessions
from sqlite3 import connect
from importlib import import_module


class ScrapperApp:
    db_name = "scrap_data.db"
    def __init__(self, configs:dict):
        self.configs = configs
        self.session = sessions()
        # TODO add proxy
        self.conn = connect(f"temp/{self.db_name}", check_same_thread=False)
        

    def scrap_links(self):
        pass

    def scrap_data(self):
        pass

    

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

# with open("config.yaml", "r") as cfile:
#     config = yaml.safe_load(cfile)

# print(config)

