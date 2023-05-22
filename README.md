# MangaLibrary
A manga library for organizing and recording physical manga for multiple users.

Uses the Comic Vine and Anilist APIs to retrieve manga info.

## Environment Variables
1. Create `.env` file in root directory
2. Add the following variables (replace `<api key>` with your api key):
```
CV_API_KEY=<api key>
```

## Run with Poetry

1. `pip install poetry`
2. `poetry install`
3. `poetry run MangaLibrary`
