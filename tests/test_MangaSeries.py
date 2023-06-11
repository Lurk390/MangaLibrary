import pytest
from dotenv import load_dotenv

from src.MangaLibrary.manga_series import MangaSeries

from AnilistPython import Anilist


load_dotenv()
anilist = Anilist()


@pytest.fixture
def manga_series():
    return MangaSeries("Berserk Deluxe Edition")


def test_get_al_data(manga_series):
    assert manga_series.author == "Kentarou Miura"
    assert (
        manga_series.description == "His name is Guts, the Black Swordsman, a feared warrior spoken of only in "
        "whispers. Bearer of a gigantic sword, an iron hand, and the scars of "
        "countless battles and tortures, his flesh is also indelibly marked with The "
        "Brand, an unholy symbol that draws the forces of darkness to him and dooms "
        "him as their sacrifice. But Guts won't take his fate lying down; he'll cut a "
        "crimson swath of carnage through the ranks of the damned—and anyone else "
        "foolish enough to oppose him! Accompanied by Puck the Elf, more an annoyance "
        "than a companion, Guts relentlessly follows a dark, bloodstained path that "
        "leads only to death...or vengeance."
    )
    assert manga_series.publisher == "Dark Horse"
    assert manga_series.status == "RELEASING"


def test_get_cv_data(manga_series):
    # Case with publisher with "comics" in the name
    assert manga_series.title == "Berserk Deluxe Edition"
    assert manga_series.year == 2019
    assert manga_series.number_of_volumes == 9
    assert manga_series.cover_image == "https://comicvine.gamespot.com/a/uploads/original/6/67663/6818216-01.jpg"
    assert manga_series.url == "https://comicvine.gamespot.com/berserk-deluxe-edition/4050-117309/"

    # Case with "normal" publisher
    manga_series = MangaSeries("Assassination Classroom")
    assert manga_series.title == "Assassination Classroom"
    assert manga_series.year == 2014
    assert manga_series.number_of_volumes == 21
    assert manga_series.cover_image == "https://comicvine.gamespot.com/a/uploads/original/6/67663/4253038-01.jpg"
    assert manga_series.url == "https://comicvine.gamespot.com/assassination-classroom/4050-78567/"


def test_al_get_author(manga_series):
    assert manga_series.al_get_author("Chainsaw Man") == "Tatsuki Fujimoto"


def test_parse_publisher(manga_series):
    # Case with publisher
    assert manga_series.parse_publisher(anilist.get_manga("Berserk")["desc"]) == "Dark Horse"

    # Case without publisher
    assert manga_series.parse_publisher(anilist.get_manga("Sofa-chan")["desc"]) == ""


def test_clean_description(manga_series):
    target_description = (
        "The master spy codenamed <Twilight> has spent his days on undercover missions,"
        " all for the dream of a better world. But one day, he receives a particularly "
        "difficult new order from command. For his mission, he must form a temporary fa"
        "mily and start a new life?! A Spy/Action/Comedy about a one-of-a-kind family!"
    )

    raw_description = anilist.get_manga("Spy Family")["desc"]

    assert manga_series.clean_description(raw_description) == target_description
