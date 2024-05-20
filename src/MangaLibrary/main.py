from MangaLibrary.database_functions import DatabaseFunctions
from MangaLibrary.manga_series import MangaSeries


def main():
    TEST_HARNESS = [
        "Assassination Classroom",
        "Berserk Deluxe Edition",
        "Berserk",
        "Chainsaw Man",
        "Dorohedoro",
        "Fire Punch",
        "The Promised Neverland",
        "Spy x Family",
        # "Tatsuki Fujimoto Before Chainsaw Man: 17-21",
        # "Tatsuki Fujimoto Before Chainsaw Man: 22-26",
        "Uzumaki",
        "Vinland Saga",
    ]

    db = DatabaseFunctions()

    db.add_user("Lurk390", "Mahmoud", "Elbasiouny")

    for manga in TEST_HARNESS:
        manga_data = MangaSeries(manga)
        db.add_manga(manga_data)

    volumes = {
        "Berserk Deluxe Edition": [1, 2],
        "Uzumaki": [1],
        "Vinland Saga": [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12],
        "Assassination Classroom": list(range(1, 13)),
        "Dorohedoro": [1, 2],
        "Fire Punch": [1, 3, 5],
        "The Promised Neverland": list(range(1, 21)),
        "Spy x Family": list(range(1, 10)),
        # "Tatsuki Fujimoto Before Chainsaw Man: 17-21": [1],
        # "Tatsuki Fujimoto Before Chainsaw Man: 22-26": [1],
    }

    for manga, volumes_list in volumes.items():
        for volume in volumes_list:
            db.add_volume_to_user("Lurk390", manga, volume)

    print("\nLurk390's manga:")
    for x in db.get_user_volumes("Lurk390"):
        print(x)

    db.connection.close()
