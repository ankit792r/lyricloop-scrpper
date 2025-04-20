import requests
from bs4 import BeautifulSoup
from string import ascii_lowercase

for alpha in ascii_lowercase:
    try:
        page = requests.get(f"https://www.hindilyrics4u.com/movie/{alpha}.php")
        page.raise_for_status()
        page_soup_temp = BeautifulSoup(page.text, "html.parser")
        text:str = page_soup_temp.find("td", {"class": "alcen w720 bg7f"}).text
        print(text.split(" ").pop())
    except:
        print("failed for ", alpha)