import os
import sqlite3

from MangaLibrary.manga_series import MangaSeries


class DatabaseFunctions:
    """Class that handles all database functions"""

    def __init__(self):
        if not os.path.exists("data"):
            os.makedirs("data")

        self.connection = sqlite3.connect("data/library.db")
        self.cursor = self.connection.cursor()

        self.init_tables()

    def init_tables(self) -> None:
        """Creates all tables if they don't exist"""

        self.cursor.executescript(
            """
            DROP TABLE IF EXISTS Users;
            DROP TABLE IF EXISTS MangaInfo;
            DROP TABLE IF EXISTS Volumes;
            DROP TABLE IF EXISTS UserToVolume;
            
            CREATE TABLE Users (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL UNIQUE,
                FirstName TEXT NOT NULL,
                LastName TEXT NOT NULL
            );
            
            CREATE TABLE MangaInfo (
                MangaID INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT,
                Author TEXT,
                Publisher TEXT,
                Status TEXT,
            --    VolumeType TEXT,
                Year INTEGER,
                Description TEXT,
                NumberOfVolumes INTEGER,
                CoverImage TEXT,
                URL TEXT
            );
            
            CREATE TABLE Volumes (
                VolumeID INTEGER PRIMARY KEY AUTOINCREMENT,
                MangaID INTEGER NOT NULL,
                VolumeNumber INTEGER NOT NULL
            );
            
            CREATE TABLE UserToVolume (
                UserToVolumeID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NOT NULL,
                VolumeID INTEGER NOT NULL
            );
            """
        )

    def populate_volumes(self, manga_series: str) -> None:
        """Populates the Volumes table with all volumes from the MangaInfo table"""

        self.cursor.execute(
            """
            SELECT MangaID, NumberOfVolumes
            FROM MangaInfo
            WHERE Title = ?
            """,
            (manga_series,),
        )

        manga_id, number_of_volumes = self.cursor.fetchone()

        for volume_number in range(1, number_of_volumes + 1):
            self.cursor.execute(
                """
                INSERT INTO Volumes (MangaID, VolumeNumber)
                VALUES (?, ?)
                """,
                (manga_id, volume_number),
            )

    def add_manga(self, manga_series: MangaSeries) -> None:
        """Adds the data from a MangaSeries object into the database

        Args:
            manga_series (MangaSeries): A MangaSeries object
        """

        self.cursor.execute(
            """
            INSERT INTO MangaInfo (Title, Author, Year, Publisher, NumberOfVolumes, Description, Status, CoverImage, 
                                   URL)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                manga_series.title,
                manga_series.author,
                manga_series.year,
                manga_series.publisher,
                manga_series.number_of_volumes,
                manga_series.description,
                manga_series.status,
                manga_series.cover_image,
                manga_series.url,
            ),
        )

        self.populate_volumes(manga_series.title)
        self.connection.commit()

    def add_user(self, username: str, first_name: str, last_name: str) -> None:
        """Adds a user into the database

        Args:
            username (str): User's username
            first_name (str): User's first name
            last_name (str): User's last name
        """
        self.cursor.execute(
            """
            INSERT INTO Users (Username, FirstName, LastName)
            VALUES (?, ?, ?)
            """,
            (username, first_name, last_name),
        )
        self.connection.commit()
