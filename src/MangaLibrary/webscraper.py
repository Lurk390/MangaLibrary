"""
This module contains the function get_manga_data(url) and its dependant functions.

@author: Mahmoud Elbasiouny
"""

import re

import requests
from AnilistPython import Anilist
from bs4 import BeautifulSoup


def cv_get_title(soup):
    """Gets the title of a manga series from a Comic Vine URL

    Args:
        soup (BeautifulSoup): BeautifulSoup object of a Comic Vine URL

    Returns:
        string: Title of a manga series
    """

    title = soup.find("a", class_="wiki-title").text
    if title == "Berserk Deluxe Edition":
        return "Berserk"
    else:
        return soup.find("a", class_="wiki-title").text


def cv_get_year(soup):
    """Gets the year of a manga series from a Comic Vine URL

    Args:
        soup (BeautifulSoup): BeautifulSoup object of a Comic Vine URL

    Returns:
        int: Year of a manga series
    """

    year = soup.find("table", class_="table").find_all("td")[1].find("div").text
    return int("".join(year.split()))


def cv_get_publisher(soup):
    """Gets the publisher of a manga series from a Comic Vine URL

    Args:
        soup (BeautifulSoup): BeautifulSoup object of a Comic Vine URL

    Returns:
        string: Publisher of a manga series
    """

    publisher = soup.find("table", class_="table").find_all("td")[2].find("div").text
    return " ".join(publisher.split())


def cv_get_number_of_volumes(soup):
    """Gets the number of volumes of a manga series from a Comic Vine URL

    Args:
        soup (BeautifulSoup): BeautifulSoup object of a Comic Vine URL

    Returns:
        int: Number of volumes of a manga series
    """

    number_of_volumes = soup.find("span", class_="volume-issue-count").text
    return int(re.sub(r"\D", "", number_of_volumes))


def cv_get_author(soup):
    """Gets the author of a manga series from a Comic Vine URL

    Args:
        soup (BeautifulSoup): BeautifulSoup object of a Comic Vine URL

    Returns:
        string: Author of a manga series
    """

    return soup.find("span", class_="relation").text


def cv_get_cover_image(soup):
    """Gets the cover image of a manga series from a Comic Vine URL

    Args:
        soup (BeautifulSoup): BeautifulSoup object of a Comic Vine URL

    Returns:
        string: Cover image of a manga series
    """

    return str(soup.find("meta", property="og:image")["content"])


def al_get_description(al_manga_data):
    """Gets the description of a manga series from the Anilist API

    Args:
        al_manga_data (Dictionary): Dictionary containing data of a manga series

    Returns:
        string: Description of a manga series
    """

    description = str(al_manga_data["desc"])
    return description.split("<", 1)[0].replace("\n", " ")


def al_get_status(al_manga_data):
    """Gets the status of a manga series from the Anilist API

    Args:
        al_manga_data (Dictionary): Dictionary containing data of a manga series

    Returns:
        string: Status of a manga series
    """

    return str(al_manga_data["release_status"])


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

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")

    title = cv_get_title(soup)
    year = cv_get_year(soup)
    publisher = cv_get_publisher(soup)
    number_of_volumes = cv_get_number_of_volumes(soup)
    author = cv_get_author(soup)
    cover_image = cv_get_cover_image(soup)

    # Anilist API ----------------------------------------------------------------------
    anilist = Anilist()
    al_manga_data = anilist.get_manga(title)

    description = al_get_description(al_manga_data)
    status = al_get_status(al_manga_data)

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
