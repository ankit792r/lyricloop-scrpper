from concurrent.futures import ThreadPoolExecutor
from scrappers.data.base_scrapper import BaseDataScrapper

def resolve_scrappers(scrappers:dict[str, BaseDataScrapper],):
    pass

def init_scrapping(scrappers:dict[str, BaseDataScrapper] ,links:list[tuple[str, str]]=[], workers=10):
    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="worker_") as executor:
        executor.map((...), links)

