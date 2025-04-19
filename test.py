import requests
from bs4 import BeautifulSoup

page = requests.get(f"https://www.ilyricshub.com/hindi/page/2")
                
page_soup = BeautifulSoup(page.text, "html.parser")

link_tags = page_soup.find_all("a", {"class": "block bg-white shadow-md rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-200"})


for a in link_tags:
    print(a.attrs["href"])