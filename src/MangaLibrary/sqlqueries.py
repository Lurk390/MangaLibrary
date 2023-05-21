"""
This module stores all of the SQL queries used to create and access tables in the
database.

@author: Mahmoud Elbasiouny
"""


INITIALIZE_TABLES = """
-- Drop tables if they exist
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS MangaInfo;
DROP TABLE IF EXISTS VolumeInfo;
DROP TABLE IF EXISTS UserToVolume;

-- Create Users table
CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL
);

-- Insert data into Users table
INSERT INTO Users (FirstName, LastName) VALUES('Mahmoud', 'Elbasiouny');
INSERT INTO Users (FirstName, LastName) VALUES('Alex', 'House');

-- Create MangaInfo table
CREATE TABLE MangaInfo (
    MangaID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT,
    Author TEXT,
    Publisher TEXT,
    Status TEXT,
    VolumeType TEXT,
    Year INTEGER,
    Description TEXT,
    NumberOfVolumes INTEGER,
    CoverImage TEXT,
    URL TEXT
);

-- Insert data into MangaInfo table
INSERT INTO MangaInfo (VolumeType, URL) VALUES('Single', 'https://comicvine.gamespot.com/assassination-classroom/4050-78567/');
INSERT INTO MangaInfo (VolumeType, URL) VALUES('3-in-1', 'https://comicvine.gamespot.com/berserk-deluxe-edition/4050-117309/');
INSERT INTO MangaInfo (VolumeType, URL) VALUES('Single', 'https://comicvine.gamespot.com/berserk/4050-18867/');
INSERT INTO MangaInfo (VolumeType, URL) VALUES('Single', 'https://comicvine.gamespot.com/chainsaw-man/4050-130799/');
INSERT INTO MangaInfo (VolumeType, URL) VALUES('Single', 'https://comicvine.gamespot.com/dorohedoro/4050-32093/');
INSERT INTO MangaInfo (VolumeType, URL) VALUES('Single', 'https://comicvine.gamespot.com/spy-x-family/4050-127643/');
INSERT INTO MangaInfo (VolumeType, URL) VALUES('Single', 'https://comicvine.gamespot.com/the-promised-neverland/4050-106538/');
INSERT INTO MangaInfo (VolumeType, URL) VALUES('3-in-1', 'https://comicvine.gamespot.com/uzumaki/4050-68740/');
INSERT INTO MangaInfo (VolumeType, URL) VALUES('2-in-1', 'https://comicvine.gamespot.com/vinland-saga/4050-69157/');

-- Create VolumeInfo table
CREATE TABLE VolumeInfo (
    VolumeID INTEGER PRIMARY KEY AUTOINCREMENT,
    MangaID INTEGER NOT NULL,
    VolumeNumber INTEGER NOT NULL
);

-- Create UserToVolume table
CREATE TABLE UserToVolume (
    UserToVolumeID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL,
    VolumeID INTEGER NOT NULL
);

-- Insert data into UserToVolume table (example)
INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 1);
INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 2);
-- Add more INSERT statements as needed
    """

MAX_MANGAID_ROW = """
    SELECT MangaID FROM MangaInfo ORDER BY MangaID DESC LIMIT 1
    """
