from MangaLibrary.database_functions import DatabaseFunctions
from MangaLibrary.manga_series import MangaSeries


def test_init_tables():
    db = DatabaseFunctions()
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    assert db.cursor.fetchall() == [('sqlite_sequence',), ("Users",), ("MangaInfo",), ("VolumeInfo",),
                                    ("UserToVolume",)]
    db.connection.close()


def test_add_user():
    db = DatabaseFunctions()
    db.add_user("John", "Doe")
    db.cursor.execute("SELECT * FROM Users")
    assert db.cursor.fetchall() == [(1, "John", "Doe")]
    db.connection.close()


def test_add_manga():
    db = DatabaseFunctions()
    manga_data = MangaSeries("Berserk Deluxe Edition")
    db.add_manga(manga_data)
    db.cursor.execute("SELECT * FROM MangaInfo")
    assert db.cursor.fetchall() == [
        (1,
         "Berserk Deluxe Edition",
         "Kentarou Miura",
         "Dark Horse",
         "RELEASING",
         2019,
         "His name is Guts, the Black Swordsman, a feared warrior spoken of only in whispers. Bearer of a gigantic "
         "sword, an iron hand, and the scars of countless battles and tortures, his flesh is also indelibly marked "
         "with The Brand, an unholy symbol that draws the forces of darkness to him and dooms him as their sacrifice. "
         "But Guts won't take his fate lying down; he'll cut a crimson swath of carnage through the ranks of the "
         "damned—and anyone else foolish enough to oppose him! Accompanied by Puck the Elf, more an annoyance than a "
         "companion, Guts relentlessly follows a dark, bloodstained path that leads only to death...or vengeance.",
         9,
         "https://comicvine.gamespot.com/a/uploads/original/6/67663/6818216-01.jpg",
         "https://comicvine.gamespot.com/berserk-deluxe-edition/4050-117309/")]
    db.connection.close()
