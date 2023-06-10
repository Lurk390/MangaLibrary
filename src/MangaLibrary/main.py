"""This module executes SQL queries to input data retrieved from get_manga_data() into
the database. It also contains the function print_table() to print the contents of a
table.
"""
import os
import sqlite3

from src.MangaLibrary.database_setup import INITIALIZE_TABLES
from src.MangaLibrary.manga_series import MangaSeries


def main():
    # List of manga to test the program
    TEST_HARNESS = [
        "Assassination Classroom",
        "Berserk Deluxe Edition",
        "Berserk",
        "Chainsaw Man",
        "Dorohedoro",
        "Spy x Family",
        "The Promised Neverland",
        "Uzumaki",
        "Vinland Saga",
    ]

    # Check if data folder exists and connect to database
    if not os.path.exists("data"):
        os.makedirs("data")
    connection = sqlite3.connect("data/library.db")
    cursor = connection.cursor()

    # Creates tables if they don't exist
    cursor.executescript(INITIALIZE_TABLES)

    # Loops through TEST_HARNESS and inserts data from get_manga_data into MangaInfo
    for manga in TEST_HARNESS:
        manga_data = MangaSeries(manga)
        cursor.execute(
            """
            INSERT INTO MangaInfo (Title, Author, Year, Publisher, NumberOfVolumes,
                                   Description, Status, CoverImage, URL)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
               manga_data.title,
               manga_data.author,
               manga_data.year,
               manga_data.publisher,
               manga_data.number_of_volumes,
               manga_data.description,
               manga_data.status,
               manga_data.cover_image,
               manga_data.url,
            ),
            )

    # Commit changes and close connection
    connection.commit()
    cursor.close()
    connection.close()
