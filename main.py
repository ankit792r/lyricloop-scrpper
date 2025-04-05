import yaml

from scrapper.app import ScrapperApp

with open("config.yaml", "r") as cfile:
    config = yaml.safe_load(cfile)

if __name__ == "__main__":
    app = ScrapperApp(config)
    app.scrap_links()
    app.scrap_data(workers=config["workers"])
    #app.upload()