import os
import sqlite3
from typing import List, Tuple

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
                UserID INTEGER NOT NULL REFERENCES Users(UserID),
                VolumeID INTEGER NOT NULL REFERENCES Volumes(VolumeID)
            );
            """
        )

        self.connection.commit()

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

        # Populate the Volumes table with the manga series' volumes
        self.cursor.execute(
            """
            SELECT MangaID, NumberOfVolumes
            FROM MangaInfo
            WHERE Title = ?
            """,
            (manga_series.title,),
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

        self.connection.commit()

    def delete_manga(self, manga_series: str) -> None:
        """Deletes a manga series from the database

        Args:
            manga_series (str): Manga series title
        """
        manga_id = self.get_manga_id(manga_series)

        # delete corresponding volumes in UserToVolume
        self.cursor.execute(
            """
            DELETE FROM UserToVolume
            WHERE VolumeID IN (
                SELECT VolumeID
                FROM Volumes
                WHERE MangaID = ?
            )
            """,
            (manga_id,),
        )

        # delete all the manga's volumes in Volumes
        self.cursor.execute(
            """
            DELETE FROM Volumes
            WHERE MangaID = ?
            """,
            (manga_id,),
        )

        self.cursor.execute(
            """
            DELETE FROM MangaInfo
            WHERE Title = ?
            """,
            (manga_series,),
        )

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

    def delete_user(self, username: str) -> None:
        """Deletes a user from the database

        Args:
            username (str): User's username
        """
        user_id = self.get_user_id(username)

        # Delete all the user's volumes in UserToVolume first
        self.cursor.execute(
            """
            DELETE FROM UserToVolume
            WHERE UserID = ?
            """,
            (user_id,),
        )

        # Delete the user
        self.cursor.execute(
            """
            DELETE FROM Users
            WHERE Username = ?
            """,
            (username,),
        )

        self.connection.commit()

    def add_volume_to_user(self, username: str, manga_series: str, volume_number: int) -> None:
        """Adds a volume to a user

        Args:
            username (str): User's username
            manga_series (str): Manga series title
            volume_number (int): Volume number
        """
        user_id = self.get_user_id(username)
        manga_id = self.get_manga_id(manga_series)

        # Get volume id
        self.cursor.execute(
            """
            SELECT VolumeID
            FROM Volumes
            WHERE MangaID = ? AND VolumeNumber = ?
            """,
            (manga_id, volume_number),
        )
        volume_id = self.cursor.fetchone()[0]

        # Add volume to user
        self.cursor.execute(
            """
            INSERT INTO UserToVolume (UserID, VolumeID)
            VALUES (?, ?)
            """,
            (user_id, volume_id),
        )

        self.connection.commit()

    def delete_volume_from_user(self, username: str, manga_series: str, volume_number: int) -> None:
        """Deletes a volume from a user

        Args:
            username (str): User's username
            manga_series (str): Manga series title
            volume_number (int): Volume number
        """
        user_id = self.get_user_id(username)
        manga_id = self.get_manga_id(manga_series)

        # Get volume id
        self.cursor.execute(
            """
            SELECT VolumeID
            FROM Volumes
            WHERE MangaID = ? AND VolumeNumber = ?
            """,
            (manga_id, volume_number),
        )
        volume_id = self.cursor.fetchone()[0]

        # Delete volume from user
        self.cursor.execute(
            """
            DELETE FROM UserToVolume
            WHERE UserID = ? AND VolumeID = ?
            """,
            (user_id, volume_id),
        )

        self.connection.commit()

    def get_user_id(self, username: str) -> int:
        """Gets the user id from a username

        Args:
            username (str): User's username

        Returns:
            int: User's id
        """
        self.cursor.execute(
            """
            SELECT UserID
            FROM Users
            WHERE Username = ?
            """,
            (username,),
        )
        return self.cursor.fetchone()[0]

    def get_manga_id(self, manga_series: str) -> int:
        """Gets the manga id from a manga series title

        Args:
            manga_series (str): Manga series title

        Returns:
            int: Manga id
        """
        self.cursor.execute(
            """
            SELECT MangaID
            FROM MangaInfo
            WHERE Title = ?
            """,
            (manga_series,),
        )
        return self.cursor.fetchone()[0]

    def get_user_volumes(self, username: str) -> List[Tuple[str, int]]:
        """Gets all the volumes a user has

        Args:
            username (str): User's username

        Returns:
            List[Tuple[str, int]]: List of tuples containing the manga series title and volume number
        """
        user_id = self.get_user_id(username)

        self.cursor.execute(
            """
            SELECT Title, VolumeNumber
            FROM MangaInfo
            JOIN Volumes USING (MangaID)
            JOIN UserToVolume USING (VolumeID)
            WHERE UserID = ?
            """,
            (user_id,),
        )
        return self.cursor.fetchall()
