import pytest

from MangaLibrary.database_functions import DatabaseFunctions
from MangaLibrary.manga_series import MangaSeries


@pytest.fixture
def db():
    return DatabaseFunctions()


class TestDatabaseFunctions:
    def test_init_tables(self, db):
        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        assert db.cursor.fetchall() == [
            ("sqlite_sequence",),
            ("Users",),
            ("MangaInfo",),
            ("Volumes",),
            ("UserToVolume",),
        ]

        db.connection.close()

    def test_add_and_delete_manga(self, db):
        # Test adding manga
        db.add_manga(MangaSeries("Assassination Classroom"))
        db.cursor.execute("SELECT * FROM MangaInfo")
        assert db.cursor.fetchall() == [
            (
                1,
                "Assassination Classroom",
                "Yuusei Matsui",
                "Viz Media",
                "FINISHED",
                2014,
                "Meet the would-be assassins of class 3-E: Sugino, who let his grades slip "
                "and got kicked off the baseball team. Karma, who’s doing well in his "
                "classes but keeps getting suspended for fighting. And Okuda, who lacks both "
                "academic and social skills, yet excels at one subject: chemistry. Who has "
                "the best chance of winning that reward? Will the deed be accomplished "
                "through pity, brute force or poison...? And what chance does their teacher "
                "have of repairing his students’ tattered self-esteem?",
                21,
                "https://comicvine.gamespot.com/a/uploads/original/6/67663/4253038-01.jpg",
                "https://comicvine.gamespot.com/assassination-classroom/4050-78567/"
            )
        ]

        db.cursor.execute("SELECT * FROM Volumes")
        assert db.cursor.fetchall() == [
            (1, 1, 1), (2, 1, 2), (3, 1, 3), (4, 1, 4), (5, 1, 5), (6, 1, 6), (7, 1, 7), (8, 1, 8), (9, 1, 9),
            (10, 1, 10), (11, 1, 11), (12, 1, 12), (13, 1, 13), (14, 1, 14), (15, 1, 15), (16, 1, 16), (17, 1, 17),
            (18, 1, 18), (19, 1, 19), (20, 1, 20), (21, 1, 21)
        ]

        # Test deleting manga
        db.delete_manga("Assassination Classroom")
        db.cursor.execute("SELECT * FROM MangaInfo")
        assert db.cursor.fetchall() == []

        db.cursor.execute("SELECT * FROM Volumes")
        assert db.cursor.fetchall() == []

        db.connection.close()

    def test_add_and_delete_user(self, db):
        # Test adding user
        db.add_user("JohnDoe123", "John", "Doe")
        db.cursor.execute("SELECT * FROM Users")
        assert db.cursor.fetchall() == [(1, "JohnDoe123", "John", "Doe")]

        # Test deleting user
        db.delete_user("JohnDoe123")
        db.cursor.execute("SELECT * FROM Users")
        assert db.cursor.fetchall() == []

        db.connection.close()

    def test_add_volume_to_user(self, db):
        # Test adding volume to user
        db.add_user("JohnDoe123", "John", "Doe")
        db.add_manga(MangaSeries("Assassination Classroom"))
        db.add_volume_to_user("JohnDoe123", "Assassination Classroom", 1)
        db.add_volume_to_user("JohnDoe123", "Assassination Classroom", 2)
        db.cursor.execute("SELECT * FROM UserToVolume")
        assert db.cursor.fetchall() == [(1, 1), (1, 2)]

        # Test deleting volume from user
        db.delete_volume_from_user("JohnDoe123", "Assassination Classroom", 1)
        db.cursor.execute("SELECT * FROM UserToVolume")
        assert db.cursor.fetchall() == [(1, 2)]

        db.connection.close()

    def test_get_user_id(self, db):
        db.add_user("JohnDoe123", "John", "Doe")
        assert db.get_user_id("JohnDoe123") == 1

        db.add_user("JaneDoe123", "Jane", "Doe")
        assert db.get_user_id("JaneDoe123") == 2

    def test_get_manga_id(self, db):
        db.add_manga(MangaSeries("Assassination Classroom"))
        assert db.get_manga_id("Assassination Classroom") == 1

        db.add_manga(MangaSeries("One Piece"))
        assert db.get_manga_id("One Piece") == 2

    def test_get_user_volumes(self, db):
        db.add_user("JohnDoe123", "John", "Doe")
        db.add_manga(MangaSeries("Chainsaw Man"))
        db.add_volume_to_user("JohnDoe123", "Chainsaw Man", 1)
        db.add_volume_to_user("JohnDoe123", "Chainsaw Man", 2)

        db.add_user("JaneDoe123", "Jane", "Doe")
        db.add_manga(MangaSeries("One Piece"))
        db.add_volume_to_user("JaneDoe123", "One Piece", 1)
        db.add_volume_to_user("JaneDoe123", "One Piece", 2)

        assert db.get_user_volumes("JohnDoe123") == [("Chainsaw Man", 1), ("Chainsaw Man", 2)]
        assert db.get_user_volumes("JaneDoe123") == [("One Piece", 1), ("One Piece", 2)]
