import requests
from bs4 import BeautifulSoup

base_url = "https://www.hindilyrics4u.com"
song_url = f"{base_url}/song/jaanaa_thaa_hamase_dur_bahaane.htm"
page = requests.get(song_url)
page.raise_for_status()

page_soup = BeautifulSoup(page.text, "html.parser")

search = song_url[len(base_url):]
name = page_soup.find("a", {"href": search, "itemprop": "url"}).text

slug = name.lower().replace(" ", "-")

sung_by = page_soup.find("span", {"itemprop": "byArtist"}).text

album = page_soup.find("td", {"itemprop": "inAlbum"}).text

lyric_by = page_soup.find("span", {"itemprop": "lyricist"}).text

lyrics_span = page_soup.find("span", {"itemprop": "lyrics"})

lyrics = lyrics_span.find("span", {"itemprop": "text"}).text

iframe = page_soup.find("iframe")

if iframe:
    vid_id = iframe.attrs["src"].split("/").pop()
    image = f"https://img.youtube.com/vi/{vid_id}/hqdefault.jpg"
    video = f"https://www.youtube.com/watch?v={vid_id}"
