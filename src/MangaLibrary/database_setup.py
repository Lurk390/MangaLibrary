"""This module stores the SQL queries to set up the database."""


INITIALIZE_TABLES = """
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS MangaInfo;
DROP TABLE IF EXISTS VolumeInfo;
DROP TABLE IF EXISTS UserToVolume;

CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
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

CREATE TABLE VolumeInfo (
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
