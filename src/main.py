from dbconnection import connect
from webscraper import getData


cnxn = connect()
cursor = cnxn.cursor()

MangaID_length = cursor.execute(
    '''SELECT TOP 1 MangaID FROM MangaInfo ORDER BY MangaID DESC''').fetchone()[0]

for i in range(1, MangaID_length + 1):
    url = cursor.execute(
        """SELECT URL FROM MangaInfo WHERE MangaID = %s""" % i).fetchone()[0]

    manga_data = getData(url)

    cursor.execute("""UPDATE MangaInfo SET Title = ?, Author = ?, Year = ?, Publisher = ?, NumberOfVolumes = ?, Description = ?, Status = ? WHERE MangaID = ?""",
                   manga_data['title'], manga_data['author'], manga_data['year'], manga_data['publisher'], manga_data['number of volumes'], manga_data['description'], manga_data['status'], i)

# Print MangaInfo table
# cursor.execute('''SELECT * FROM MangaInfo''')
# for row in cursor.fetchall():
#     print(row)

cnxn.commit()
cursor.close()
cnxn.close()

# *If status == 'Completed', insert data into MangaLibrary.MangaInfo.NumberOfVolumes