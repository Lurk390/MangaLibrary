"""
This module stores all the SQL queries.

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

-- Create MangaInfo table
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
"""
