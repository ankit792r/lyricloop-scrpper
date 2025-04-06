import yaml
from os import getenv
from scrapper.app import ScrapperApp
from dotenv import load_dotenv

load_dotenv()

with open("config.yaml", "r") as cfile:
    config = yaml.safe_load(cfile)
    config["db_url"] = getenv("DATABASE_URL")
    config["proxies"] = {
        "http": getenv("PROXY_URL"),
        "https": getenv("PROXY_URL")
    }

if __name__ == "__main__":
    app = ScrapperApp(config)
    app.scrap_links()
    app.scrap_data(workers=config["workers"])
    app.upload()