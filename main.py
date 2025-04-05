import yaml
from os import environ
from scrapper.app import ScrapperApp

with open("config.yaml", "r") as cfile:
    config = yaml.safe_load(cfile)
    config["db_url"] = environ["DATABASE_URL"]
    config["workers"] = int(environ["WORKERS"])
    config["proxies"] = {
        "http": environ["PROXIES"],
        "https": environ["PROXIES"]
    }

if __name__ == "__main__":
    app = ScrapperApp(config)
    app.scrap_links()
    app.scrap_data(workers=config["workers"])
    app.upload()