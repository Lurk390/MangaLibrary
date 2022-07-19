from dbconnection import connect
from webscraper import getData

getData('https://comicvine.gamespot.com/chainsaw-man/4050-130799/')     #Chainsaw Man
getData('https://comicvine.gamespot.com/made-in-abyss/4050-107931/')    #Made in Abyss

#==========================================================================

cnxn = connect()
cursor = cnxn.cursor()

cursor.execute("""
    SELECT * FROM MangaInfo
    """)
for i in cursor:
    print(i)
cursor.close()
cnxn.close()