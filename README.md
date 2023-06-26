# MangaLibrary
A manga library for organizing and recording physical manga for multiple users.

Uses the Comic Vine and Anilist APIs to retrieve manga info.

## Environment Variables
1. Rename the `.env.template` file in the root directory to `.env`
2. Add your Comic Vine API key to the `.env` file:
```shell
CV_API_KEY=
```

## Installing Poetry and Requirements
1. Make sure poetry is installed:
    ```shell
    pip install poetry
    ```

2. Install the requirements:
    ```shell
    poetry install
    ```

## Running the Program
```shell
poetry run MangaLibrary
```

## Testing with pytest
```shell
poetry run pytest
```
add `--cov` to see coverage or `--cov --cov-report html:cov_html` for a full HTML report
