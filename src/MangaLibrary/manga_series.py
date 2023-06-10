import html
import os
import re

import requests
from AnilistPython import Anilist
from dotenv import load_dotenv
from fuzzywuzzy import fuzz, process


class MangaSeries:
    """Class that stores data about a manga series using the AniList and Comic Vine APIs."""
    title = ""
    author = ""
    year = 0
    publisher = ""
    number_of_volumes = 0
    description = ""
    status = ""
    cover_image = ""
    url = ""

    def __init__(self, manga_name: str) -> None:
        self.get_al_data(manga_name)
        self.get_cv_data(manga_name)

    def get_al_data(self, manga_name: str) -> None:
        """Gets manga data from AniList, parses it, and stores in the dictionary.

        Args:
            manga_name (str): Name of a manga series
        """

        # Handle special cases ("Berserk Deluxe Edition")
        if fuzz.partial_ratio(manga_name, "Berserk") > 85:
            manga_name = "Berserk"

        # Connect to AniList and get the manga data
        anilist = Anilist()
        manga_data = anilist.get_manga(manga_name)

        # Parse the data to dictionary
        self.author = self.al_get_author(manga_name)
        self.description = self.clean_description(manga_data["desc"])
        self.publisher = self.parse_publisher(manga_data["desc"])
        self.status = manga_data["release_status"]

    def get_cv_data(self, manga_name: str) -> None:
        """Gets manga data from Comic Vine and parses it. Uses the publisher from AniList
        (which is English) to get the best match from Comic Vine.

        Args:
            manga_name (str): Name of a manga series
        """
        load_dotenv()
        API_KEY = os.getenv("CV_API_KEY")

        search_url = f"https://comicvine.gamespot.com/api/search/?api_key={API_KEY}" \
                     f"&format=json&query={manga_name}&resources=volume"
        HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                          "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(search_url, headers=HEADERS)

        if response.status_code == 200:
            results = response.json()["results"]
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
                    self.title = result["name"]
                    self.year = int(result["start_year"])
                    self.number_of_volumes = result["count_of_issues"]
                    self.cover_image = result["image"]["original_url"]
                    self.url = result["site_detail_url"]
                    break

            # If no results, get the best match
            if not self.cover_image:
                best_match = None
                best_score = 0

                for result in output_results:
                    score = process.extractOne(
                        result["publisher"]["name"], [self.publisher], scorer=fuzz.token_set_ratio
                    )[1]

                    if score > best_score:
                        best_match = result
                        best_score = score

                # If best match was found, add data
                if best_match:
                    self.title = best_match["name"]
                    self.year = int(best_match["start_year"])
                    self.number_of_volumes = best_match["count_of_issues"]
                    self.cover_image = best_match["image"]["original_url"]
                    self.url = best_match["site_detail_url"]
        else:
            print(f"Error: {response.status_code}")

    @staticmethod
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

        response = requests.post(URL, json={"query": query, "variables": variables}, headers=HEADERS)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return data["data"]["Media"]["staff"]["edges"][0]["node"]["name"]["full"]
        else:
            print("Error occurred while fetching data:", response.text)

    @staticmethod
    def parse_publisher(description: str) -> str:
        """Parses the publisher from the description of the manga series

        Args:
            description (str): Description of the manga series

        Returns:
            str: Publisher of the manga series
        """

        # Matches "(Source: <publisher>)"
        match = re.search(r"\(Source:\s*(.*?)\)", description)

        if match:
            publisher = match.group(1)
            return publisher
        else:
            print("No publisher found.")
            return ""

    @staticmethod
    def clean_description(description: str) -> str:
        """Removes HTML elements and unnecessary information from the raw description

        Args:
            description (str): Description of a manga series

        Returns:
            str: Cleaned description of a manga series
        """

        # Remove HTML tags
        description = re.sub(r"<.*?>", "", description)

        # Remove HTML entities
        description = html.unescape(description)

        # Everything after the first newline is extra information and is not needed
        return description.split("\n", 1)[0]
