"""
This module executes SQL queries to input data retrieved from get_manga_data() into the
database. It also contains the function print_table() to print the contents of a table.

@author: Mahmoud Elbasiouny
"""

from dbconnection import connect
from sqlqueries import INITIALIZE_TABLES, MAX_MANGAID_ROW
from webscraper import get_manga_data


def print_table(table_name):
    """Prints the contents of a table. Must also be connected to the database.

    Args:
        table_name (string): Must be a table name that exists in the database
    """

    print(f"{table_name}:")
    cursor.execute(f"""SELECT * FROM {table_name}""")
    for row in cursor.fetchall():
        print(row)
    print("\n")


# Connect to database
cnxn = connect()
cursor = cnxn.cursor()

# Creates tables if they don't exist
cursor.execute(INITIALIZE_TABLES)

# Finds last row in MangaInfo table and gets its MangaID
MangaID_length = cursor.execute(MAX_MANGAID_ROW).fetchone()[0]

# Loops through all MangaInfo rows and gets URL from each row
for i in range(1, MangaID_length + 1):
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
        (
            manga_data["title"],
            manga_data["author"],
            manga_data["year"],
            manga_data["publisher"],
            manga_data["number of volumes"],
            manga_data["description"],
            manga_data["status"],
            manga_data["cover image"],
            i,
        ),
    )

# ======================================================================================
# Create a for loop that inserts MangaID and VolumeNumber into the VolumeInfo table for
# each series in the MangaInfo table.
# ======================================================================================

# Print MangaInfo table
print_table("MangaInfo")
print_table("VolumeInfo")

# Commit changes and close connection
cnxn.commit()
cursor.close()
cnxn.close()
