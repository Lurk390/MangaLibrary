"""
This module stores all of the SQL queries used to create and access tables in the
database.

@author: Mahmoud Elbasiouny
"""


INITIALIZE_TABLES = '''
    IF (EXISTS (SELECT *
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_NAME = 'Users'
                OR  TABLE_NAME = 'MangaInfo'
                OR  TABLE_NAME = 'VolumeInfo'
                OR  TABLE_NAME = 'UserToVolume'))
    BEGIN
        DROP TABLE Users
        DROP TABLE MangaInfo
        DROP TABLE VolumeInfo
        DROP TABLE UserToVolume
    END

    ------------------------------------------------------------------------------------

    CREATE TABLE Users (
        UserID INT IDENTITY,
        FirstName VARCHAR(30) NOT NULL,
        LastName VARCHAR(30) NOT NULL,
        PRIMARY KEY(UserID)
    );

    INSERT INTO Users (FirstName, LastName) VALUES('Mahmoud', 'Elbasiouny');
    INSERT INTO Users (FirstName, LastName) VALUES('Alex', 'House');

    ------------------------------------------------------------------------------------

    CREATE TABLE MangaInfo (
    MangaID INT IDENTITY,
    Title VARCHAR(100),
    Author VARCHAR(30),
    Publisher VARCHAR(30),
    Status VARCHAR(10),
    VolumeType VARCHAR(10),
    Year INT,
    Description VARCHAR(MAX),
    NumberOfVolumes INT,
    CoverImage VARCHAR(100),
    URL VARCHAR(100),
    PRIMARY KEY(MangaID)
    );

    INSERT INTO MangaInfo (VolumeType, URL) VALUES('Single',
                                                   'https://comicvine.gamespot.com/assassination-classroom/4050-78567/')
    INSERT INTO MangaInfo (VolumeType, URL) VALUES('3-in-1',
                                                   'https://comicvine.gamespot.com/berserk-deluxe-edition/4050-117309/')
    INSERT INTO MangaInfo (VolumeType, URL) VALUES('Single',
                                                   'https://comicvine.gamespot.com/berserk/4050-18867/')
    INSERT INTO MangaInfo (VolumeType, URL) VALUES('Single',
                                                   'https://comicvine.gamespot.com/chainsaw-man/4050-130799/')
    INSERT INTO MangaInfo (VolumeType, URL) VALUES('Single',
                                                   'https://comicvine.gamespot.com/dorohedoro/4050-32093/')
    INSERT INTO MangaInfo (VolumeType, URL) VALUES('Single',
                                                   'https://comicvine.gamespot.com/spy-x-family/4050-127643/')
    INSERT INTO MangaInfo (VolumeType, URL) VALUES('Single',
                                                   'https://comicvine.gamespot.com/the-promised-neverland/4050-106538/')
    INSERT INTO MangaInfo (VolumeType, URL) VALUES('3-in-1',
                                                   'https://comicvine.gamespot.com/uzumaki/4050-68740/')
    INSERT INTO MangaInfo (VolumeType, URL) VALUES('2-in-1',
                                                   'https://comicvine.gamespot.com/vinland-saga/4050-69157/')

    ------------------------------------------------------------------------------------

    CREATE TABLE VolumeInfo (
    VolumeID INT IDENTITY,
    MangaID INT NOT NULL,
    VolumeNumber INT NOT NULL,
    PRIMARY KEY(VolumeID)
    );

    ------------------------------------------------------------------------------------

    CREATE TABLE UserToVolume (
    UserToVolumeID INT IDENTITY,
    UserID INT NOT NULL,
    VolumeID INT NOT NULL,
    PRIMARY KEY(UserToVolumeID)
    );

    --Assassination Classroom
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 1);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 2);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 3);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 4);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 5);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 6);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 7);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 8);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 9);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 10);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 11);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 12);

    --Berserk
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 22);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 23);

    --Berserk
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 33);

    --Chainsaw Man
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 35);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 36);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 37);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 38);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 39);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 41);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 42);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 43);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 44);

    --Dorohedoro
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 45);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 46);

    --Spy x Family
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 73);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 74);

    --The Promised Neverland
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 76);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 77);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 78);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 79);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 80);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 81);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 82);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 83);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 84);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 85);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 86);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 87);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 88);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 89);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 90);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 91);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 92);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 93);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 94);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 95);

    --Uzumaki
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 96);

    --Vinland Saga
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 97);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 98);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 100);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 101);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 104);
    INSERT INTO UserToVolume (UserID, VolumeID) VALUES(1, 105);
    '''

MAX_MANGAID_ROW = '''
    SELECT TOP 1 MangaID FROM MangaInfo ORDER BY MangaID DESC
    '''
