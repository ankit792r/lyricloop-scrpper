from bs4 import BeautifulSoup
import requests, time, json
from requests import RequestException

# check ip at http://jsonip.com

# past proxy address
proxies = {
    "http": "http://username:password@host:port",
    "https": "http://username:password@host:port"
}

def lyricmint(request, page_url)->dict:
    try:
        page = request.get(page_url, proxies=proxies)

        page.raise_for_status()

        soup = BeautifulSoup(page.text, "html.parser")

        song_data = {}

        song_data["slug"] = page_url.split('/').pop()

        song_data["name"] = soup.find("span", "current").text

        x = soup.find("div", "text-base lg:text-lg pb-2 text-center md:text-left")
        song_data["lyrics"] = ''.join(str(p) for p in x.find_all('p')) if x else ""; 

        info_soup = soup.find_all("td", "w-3/4 px-5 font-bold border-b border-grey-light", limit=4)

        song_data["album"] = info_soup[1].get_text(separator="", strip=True)

        song_data["sungBy"] = info_soup[0].get_text(separator="", strip=True)

        song_data["lyricsBy"] = info_soup[2].get_text(separator="", strip=True)

        thumb_link = soup.find("img", "absolute w-full h-full border shadow-lg outline-none pin")

        if thumb_link is not None : 
            song_data["video"] = "https://www.youtube.com/watch?v="+str(thumb_link.attrs["src"][27:38])
            song_data["image"] = str(thumb_link.attrs["src"].replace("mq","maxres"))
        else:
            song_data["video"] = ""
            song_data["image"] = ""

        return song_data

    except:
        print(f"failed to fetch {page_url}")
        return None

def song_link_extractor():
    page = 20
    base_url = "https://lyricsmint.com"
    song_links = []

    for i in range(1, page):
        try:
            album_list_page = requests.get(f"https://lyricsmint.com/albums?page={i}", proxies=proxies)

            album_list_page.raise_for_status()

            album_list_page_soup = BeautifulSoup(album_list_page.text, "html.parser")

            album_link_tags = album_list_page_soup.find_all("a", {"class": "h-auto w-full block text-black font-bold bg-white no-underline mt-1"})

            album_links = [base_url + link.attrs["href"] for link in album_link_tags]

            for album in album_links:
                time.sleep(0.5)
                try: 
                    songs_list_page = requests.get(album, proxies=proxies)

                    songs_list_page.raise_for_status()

                    songs_list_page_soup = BeautifulSoup(songs_list_page.text, "html.parser")

                    link_tags = songs_list_page_soup.find_all("a", {"class": "song h-auto w-full block text-black no-underline song"})

                    for link in link_tags:
                        print(link.attrs["href"])
                        song_links.append(base_url + link.attrs["href"])

                except:
                    pass
        except:
            pass

    with open("temp/song_links.json", "w+") as file:
        json.dump(song_links, file)


# song_link_extractor()