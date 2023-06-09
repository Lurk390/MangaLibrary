"""This module tests the functions in manga_data_fetcher.py."""

from dotenv import load_dotenv

from src.MangaLibrary.manga_data_fetcher import *
from AnilistPython import Anilist

load_dotenv()
anilist = Anilist()


def test_al_get_author():
    assert al_get_author("Chainsaw Man") == "Tatsuki Fujimoto"


def test_parse_publisher():
    # Case with publisher
    assert parse_publisher(anilist.get_manga("Berserk")["desc"]) == "Dark Horse"

    # Case without publisher
    assert parse_publisher(anilist.get_manga("Sofa-chan")["desc"]) == ""


def test_clean_description():
    target_description = (
        "The master spy codenamed <Twilight> has spent his days on undercover missions,"
        " all for the dream of a better world. But one day, he receives a particularly "
        "difficult new order from command. For his mission, he must form a temporary fa"
        "mily and start a new life?! A Spy/Action/Comedy about a one-of-a-kind family!"
    )

    raw_description = anilist.get_manga("Spy Family")["desc"]

    assert clean_description(raw_description) == target_description


def test_get_al_data():
    dictionary = {}
    al_data = get_al_data("Berserk Deluxe Edition", dictionary)

    assert al_data["author"] == "Kentarou Miura"
    assert (
        al_data["description"] == "His name is Guts, the Black Swordsman, a feared warr"
        "ior spoken of only in whispers. Bearer of a gigantic sword, an iron hand, and "
        "the scars of countless battles and tortures, his flesh is also indelibly marke"
        "d with The Brand, an unholy symbol that draws the forces of darkness to him an"
        "d dooms him as their sacrifice. But Guts won't take his fate lying down; he'll"
        " cut a crimson swath of carnage through the ranks of the damned—and anyone els"
        "e foolish enough to oppose him! Accompanied by Puck the Elf, more an annoyance"
        " than a companion, Guts relentlessly follows a dark, bloodstained path that le"
        "ads only to death...or vengeance."
    )
    assert al_data["publisher"] == "Dark Horse"
    assert al_data["status"] == "RELEASING"


def test_get_cv_data():
    # Case with "normal" publisher
    cv_data = get_cv_data(
        "Assassination Classroom",
        {
            "title": "",
            "publisher": "Viz Media",
            "year": 0,
            "number of volumes": 0,
            "cover image": "",
            "url": "",
        },
    )

    assert cv_data["title"] == "Assassination Classroom"
    assert cv_data["year"] == "2014"
    assert cv_data["number of volumes"] == 21
    assert (
        cv_data["cover image"]
        == "https://comicvine.gamespot.com/a/uploads/original/6/67663/4253038-01.jpg"
    )
    assert (
        cv_data["url"]
        == "https://comicvine.gamespot.com/assassination-classroom/4050-78567/"
    )

    # Case with publisher with "comics" in the name
    cv_data = get_cv_data(
        "Berserk Deluxe Edition",
        {
            "title": "",
            "publisher": "Dark Horse",
            "year": 0,
            "number of volumes": 0,
            "cover image": "",
            "url": "",
        },
    )

    assert cv_data["title"] == "Berserk Deluxe Edition"
    assert cv_data["year"] == "2019"
    assert (
        cv_data["cover image"]
        == "https://comicvine.gamespot.com/a/uploads/original/6/67663/6818216-01.jpg"
    )
    assert (
        cv_data["url"]
        == "https://comicvine.gamespot.com/berserk-deluxe-edition/4050-117309/"
    )


def test_get_manga_data():
    manga_data = get_manga_data("The Promised Neverland")

    assert manga_data["title"] == "The Promised Neverland"
    assert manga_data["author"] == "Posuka Demizu"
    assert manga_data["publisher"] == "Viz Media"
    assert manga_data["year"] == "2017"
    assert (
        manga_data["description"] == "Emma, Norman and Ray are the brightest kids at th"
        "e Grace Field House orphanage. And under the care of the woman they refer to a"
        "s “Mom,” all the kids have enjoyed a comfortable life. Good food, clean clothe"
        "s and the perfect environment to learn—what more could an orphan ask for? One "
        "day, though, Emma and Norman uncover the dark truth of the outside world they "
        "are forbidden from seeing."
    )
    assert manga_data["status"] == "FINISHED"
    assert manga_data["number of volumes"] == 20
    assert (
        manga_data["cover image"]
        == "https://comicvine.gamespot.com/a/uploads/original/6/67663/6164855-01.jpg"
    )
    assert (
        manga_data["url"]
        == "https://comicvine.gamespot.com/the-promised-neverland/4050-106538/"
    )
