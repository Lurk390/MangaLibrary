"""This file contains functions to get manga data from AniList and Comic Vine. The main
function is get_manga_data(manga_name) and the remaining functions are helper functions
to obtain and parse the data.
"""
import html
import os
import re

import requests
from AnilistPython import Anilist
from fuzzywuzzy import fuzz, process


def al_get_author(manga_name: str) -> str:
    """Gets the author of a manga series using a AniList API v2 GraphQL query

    Args:
        manga_name (str): Name of a manga series

    Returns:
        str: Author of a manga series
    """

    URL = "https://graphql.anilist.co"

    query = """
        query ($search: String) {
            Media(search: $search, type: MANGA) {
                staff {
                    edges {
                        role
                        node {
                            name {
                                full
                            }
                        }
                    }
                }
            }
        }
    """

    HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    variables = {"search": manga_name}

    response = requests.post(
        URL, json={"query": query, "variables": variables}, headers=HEADERS
    )

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        staff = data["data"]["Media"]["staff"]["edges"]

        if staff:
            return staff[0]["node"]["name"]["full"]
        else:
            print("No staff members found for this manga.")
    else:
        print("Error occurred while fetching data:", response.text)


def parse_publisher(description: str) -> str:
    """Parses the publisher from the description of a manga series
    Args:
        description (str): Description of a manga series

    Returns:
        str: Publisher of a manga series
    """

    # Regex pattern to match the publisher
    match = re.search(r"\(Source:\s*(.*?)\)", description)
    if match:
        publisher = match.group(1)
        return publisher
    else:
        print("No publisher found.")


def clean_description(description: str) -> str:
    """Cleans the description of a manga series by removing HTML elements and everything
    after the first newline.

    Args:
        description (str): Description of a manga series

    Returns:
        str: Cleaned description of a manga series
    """

    description = html.unescape(description)
    return description.split("\n", 1)[0]


def get_al_data(manga_name: str, dictionary: dict) -> dict:
    """Gets manga data from AniList, parses it, and stores in the dictionary.

    Args:
        manga_name (str): Name of a manga series
        dictionary (dict): Dictionary to store the manga data

    Returns:
        dict: Dictionary containing the manga data
    """

    # Handle special cases ("Berserk Deluxe Edition")
    if fuzz.partial_ratio(manga_name, "Berserk") > 85:
        manga_name = "Berserk"

    # Connect to AniList and get the manga data
    anilist = Anilist()
    manga_data = anilist.get_manga(manga_name)

    # Parse the data to dictionary
    dictionary["author"] = al_get_author(manga_name)
    dictionary["description"] = clean_description(manga_data["desc"])
    dictionary["publisher"] = parse_publisher(manga_data["desc"])
    dictionary["status"] = manga_data["release_status"]
    return dictionary


def get_cv_data(manga_name: str, dictionary: dict) -> dict:
    """Gets manga data from Comic Vine and parses it. Uses the publisher from AniList
    (which is English) to get the best match from Comic Vine.

    Args:
        manga_name (str): Name of a manga series
        dictionary (dict): Dictionary to store the manga data

    Returns:
        dict: Dictionary containing the manga data
    """

    # TODO: Get the volume type (e.g. Single, Two-in-One, etc.)

    API_KEY = os.getenv("CV_API_KEY")
    search_url = (
        f"https://comicvine.gamespot.com/api/search/?api_key={API_KEY}"
        f"&format=json&query={manga_name}&resources=volume"
    )
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(search_url, headers=HEADERS)

    if response.status_code == 200:
        results = response.json()["results"]
        al_publisher = dictionary["publisher"]
        output_results = []
        count = 0

        # Get the first 3 results
        for result in results:
            output_results.append(result)
            count += 1

            if count == 3:
                break

        # Get the result with "comics" in the name (to match english publisher)
        for result in output_results:

            if "comics" in result["publisher"]["name"].lower():
                dictionary["title"] = result["name"]
                dictionary["year"] = result["start_year"]
                dictionary["number of volumes"] = result["count_of_issues"]
                dictionary["cover image"] = result["image"]["original_url"]
                dictionary["url"] = result["site_detail_url"]
                break

        # If no results, get the best match
        if not dictionary["cover image"]:
            best_match = None
            best_score = 0

            for result in output_results:
                score = process.extractOne(
                    result["publisher"]["name"],
                    [al_publisher],
                    scorer=fuzz.token_set_ratio,
                )[1]

                if score > best_score:
                    best_match = result
                    best_score = score

            # If best match was found, add data
            if best_match:
                dictionary["title"] = best_match["name"]
                dictionary["year"] = best_match["start_year"]
                dictionary["number of volumes"] = best_match["count_of_issues"]
                dictionary["cover image"] = best_match["image"]["original_url"]
                dictionary["url"] = best_match["site_detail_url"]
        return dictionary
    else:
        print(f"Error: {response.status_code}")


def get_manga_data(manga_name: str) -> dict:
    """Culminating function that gets manga data from AniList and Comic Vine

    Args:
        manga_name (str): Name of a manga series

    Returns:
        dict: Dictionary containing the manga data
    """

    manga_data = {
        "title": "",
        "author": "",
        "publisher": "",
        "year": 0,
        "description": "",
        "status": "",
        "number of volumes": 0,
        "cover image": "",
        "url": "",
    }

    get_al_data(manga_name, manga_data)
    get_cv_data(manga_name, manga_data)
    return manga_data
