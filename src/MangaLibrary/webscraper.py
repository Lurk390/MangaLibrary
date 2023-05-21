"""
This module contains the function get_manga_data(url).

@author: Mahmoud Elbasiouny
"""

import re
import requests

from AnilistPython import Anilist
from bs4 import BeautifulSoup


def get_manga_data(url):
    """Gets manga data from a Comic Vine URL and the Anilist API and returns data as a
    dictionary

    Args:
        url (string): Must be a Comic Vine URL pointing to a specific manga series
                      ex. https://comicvine.gamespot.com/berserk/4050-18867/

    Returns:
        Dictionary: Contains title, author, publisher, year, description, status, number
                    of volumes, and cover image data for a specific manga series
    """

    title = ""
    author = ""
    publisher = ""
    year = 0
    description = ""
    status = ""
    number_of_volumes = 0
    cover_image = ""

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    req = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(req.content, "html.parser")

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
    number_of_volumes = (re.sub(r"\D", "", number_of_volumes))

    # Get author
    if title == "The Promised Neverland":
        author = soup.find_all("span", class_="relation")[5].text
    else:
        author = soup.find("span", class_="relation").text

    # Get cover image
    cover_image = str(soup.find("meta", property="og:image")["content"])

    # Anilist API ----------------------------------------------------------------------
    anilist = Anilist()
    anilist_manga_data = anilist.get_manga(title)

    # Get description
    description = str(anilist_manga_data["desc"])
    description = description.split("<", 1)[0]
    description = description.replace("\n", " ")

    # Get status
    status = str(anilist_manga_data["release_status"])

    manga_data = {
        "title": title,
        "author": author,
        "publisher": publisher,
        "year": year,
        "description": description,
        "status": status,
        "number of volumes": number_of_volumes,
        "cover image": cover_image,
    }
    return manga_data
