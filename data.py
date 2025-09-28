from bs4 import BeautifulSoup
import requests

BASE_URL = "https://lyricsmint.com"

def extract_lyrics(links: list[str]):
    lyrics_data = []
    for link in links:
        try:
            page = requests.get(link)
            page.raise_for_status()
            page_soup = BeautifulSoup(page.text, "html.parser")

            slug = link.split('/').pop()

            name = page_soup.find("span", "current").text

            x = page_soup.find("div", "text-base lg:text-lg pb-2 text-center md:text-left")
            lyrics = ''.join(str(p) for p in x.find_all('p')) if x else ""; 

            info_soup = page_soup.find_all("td", "w-3/4 px-5 font-bold border-b border-grey-light", limit=4)

            album = info_soup[1].get_text(separator="", strip=True)

            sung_by = info_soup[0].get_text(separator="", strip=True)

            lyrics_by = info_soup[2].get_text(separator="", strip=True)

            thumb_link = page_soup.find("img", "absolute w-full h-full border shadow-lg outline-none pin")

            if thumb_link is not None : 
                video = "https://www.youtube.com/watch?v="+str(thumb_link.attrs["src"][27:38])
                image = str(thumb_link.attrs["src"].replace("mq","maxres"))
            else:
                video = ""
                image = ""

            lyrics_data.append((None, album, image, lyrics, lyrics_by, name, slug, sung_by, video))

        except Exception as e:
            print(e)

    return lyrics_data
    


def extract_data(db_instace, limit:int=2):
    last_extracted = ""
    links = db_instace.get_link(limit)
    print("links", links)
    for link in links:
        try:
            for i in range(100, 200):
                page_link = link[1] + f"?page={i}"
                _page = requests.get(page_link)
                _page.raise_for_status()
                _page_soup = BeautifulSoup(_page.text, "html.parser")
                links_tags = _page_soup.find_all("a", {"class": "song h-auto w-full block text-black no-underline song"})
                lyrics_links = [BASE_URL + tag.attrs["href"]  for tag in links_tags]

                if last_extracted == links[-1]:
                    print("reached to last page")
                    break
                else:
                    last_extracted = links[-1]

                lyrics_data = extract_lyrics(lyrics_links)
                print("data", lyrics_data)
                db_instace.insert_data(lyrics_data)

        except Exception as e:
            print(e)
