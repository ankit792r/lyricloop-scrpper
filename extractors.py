from bs4 import BeautifulSoup

# check ip at http://jsonip.com

# past proxy address
proxies = {
    "http": "http://username:password@host:port",
    "https": "http://username:password@host:port"
}

def lyricmint(request, page_url)->dict:
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