from MangaLibrary.database_functions import DatabaseFunctions
from MangaLibrary.manga_series import MangaSeries


def main():
    TEST_HARNESS = [
        "Assassination Classroom",
        "Berserk Deluxe Edition",
        "Berserk",
        "Chainsaw Man",
        "Dorohedoro",
        "Spy x Family",
        "The Promised Neverland",
        "Uzumaki",
        "Vinland Saga",
    ]

    db = DatabaseFunctions()

    db.add_user("Lurk390", "Mahmoud", "Elbasiouny")

    for manga in TEST_HARNESS:
        manga_data = MangaSeries(manga)
        db.add_manga(manga_data)

    db.connection.close()
