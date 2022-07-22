"""
This module executes SQL queries to input data retrieved from get_manga_data() into the
database.

@author: Mahmoud Elbasiouny
"""

from dbconnection import connect
from webscraper import get_manga_data


# Connect to database
cnxn = connect()
cursor = cnxn.cursor()

# Drops tables if they exist, then creates them
# Manually inserts VolumeType and URL info for each manga into database
cursor.execute(
    """
    IF (EXISTS (SELECT *
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_NAME = 'MangaInfo'))
    BEGIN
        DROP TABLE MangaInfo;
    END
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
    """
)

# Finds last row in MangaInfo table and gets its MangaID
MangaID_length = (
    cursor.execute(
        """
        SELECT TOP 1 MangaID FROM MangaInfo ORDER BY MangaID DESC
        """
    ).fetchone()[0]
    + 1
)

# Loops through all MangaInfo rows and gets URL from each row
for i in range(1, MangaID_length):
    url = cursor.execute(
        f"""
        SELECT URL FROM MangaInfo WHERE MangaID = {i}
        """
    ).fetchone()[0]

    # Inserts data from get_manga_data(url) into MangaInfo table
    manga_data = get_manga_data(url)
    cursor.execute(
        """
        UPDATE MangaInfo SET Title = ?,
        Author = ?,
        Year = ?,
        Publisher = ?,
        NumberOfVolumes = ?,
        Description = ?,
        Status = ?,
        CoverImage = ?
        WHERE MangaID = ?
        """,
        (manga_data["title"],
         manga_data["author"],
         manga_data["year"],
         manga_data["publisher"],
         manga_data["number of volumes"],
         manga_data["description"],
         manga_data["status"],
         manga_data["cover image"],
         i,)
    )

# Print MangaInfo table
cursor.execute(
    """
    SELECT * FROM MangaInfo
    """
)
for row in cursor.fetchall():
    print(row)
    print("\n")

# Commit changes and close connection
cnxn.commit()
cursor.close()
cnxn.close()
