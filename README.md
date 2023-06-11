# MangaLibrary
A manga library for organizing and recording physical manga for multiple users.

Uses the Comic Vine and Anilist APIs to retrieve manga info.

## Environment Variables
1. Create `.env` file in root directory
2. Add the following variables (replace `<api key>` with your api key):
```
CV_API_KEY=<api key>
```

## Installing Poetry and Requirements
1. `pip install poetry`
2. `poetry install`

## Running the Program
`poetry run MangaLibrary`

## Testing with pytest
`poetry run pytest --cov` (add `--cov-report=html:coverage_re` flag if you want an HTML report)
