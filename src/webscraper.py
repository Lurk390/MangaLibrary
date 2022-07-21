import requests
from bs4 import BeautifulSoup
import re
from AnilistPython import Anilist


def getData(url):
    title = ""
    year = 0
    publisher = ""
    number_of_volumes = 0
    description = ""
    status = ""
    author = ""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    # Get title
    title = soup.find("a", class_="wiki-title").text
    if title == "Berserk Deluxe Edition":
        title = "Berserk"
    else:
        title = soup.find("a", class_="wiki-title").text

    # Get year
    year = soup.find("table", class_="table").find_all("td")[1].find("div").text
    year = int("".join(year.split()))

    # Get publisher
    publisher = soup.find("table", class_="table").find_all("td")[2].find("div").text
    publisher = " ".join(publisher.split())

    # Get number of volumes
    number_of_volumes = soup.find("span", class_="volume-issue-count").text
    number_of_volumes = int(re.sub("\D", "", number_of_volumes))

    # Get author
    if title == "The Promised Neverland":
        author = soup.find_all("span", class_="relation")[5].text
    else:
        author = soup.find("span", class_="relation").text

    # Get cover image
    cover_image = soup.find("meta", property="og:image")["content"]

    # Anilist API ---------------------------------------------------------------------------------------------------------------------
    anilist = Anilist()
    anilist_manga_info = anilist.get_manga(title)

    # Get description
    description = anilist_manga_info["desc"]
    description = description.split("<", 1)[0]
    description = description.replace("\n", " ")

    # Get status
    status = anilist_manga_info["release_status"]

    manga_data = {
        "title": title,
        "author": author,
        "publisher": publisher,
        "year": year,
        "description": description,
        "status": status,
        "number of volumes": number_of_volumes,
        "cover image": cover_image
    }
    return manga_data
