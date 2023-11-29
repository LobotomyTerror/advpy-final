import sys
import os
from typing import Any
from dotenv import load_dotenv
import requests  # type: ignore
from tmdbv3api import TMDb
from tmdbv3api import Genre
from . import database as db

load_dotenv()
tmdb_api_key = os.getenv('TMDB_API_KEY')
tmdb = TMDb()
tmdb.api_key = tmdb_api_key
tmdb.language = 'en'
tmdb.debug = True


def check_genre_title(genre: str) -> str:
    genre_title = genre.title()
    return genre_title


def find_genre_id(genre: str) -> int:
    genre_id = 0
    genre_list = Genre()
    genre_list = genre_list.movie_list()
    for gl in genre_list:
        if genre == gl['name']:
            genre_id = gl['id']
            return genre_id
    return 0


def remove_from_db() -> Any:
    db.delete_db()


def get_movies_by_genre(genre: str) -> Any:
    genre = check_genre_title(genre)
    genre_id = find_genre_id(genre)
    if genre_id != 0:
        movie_list = []
        tmdb_auth_key = os.getenv('TMDB_AUTH_KEY')
        url = "https://api.themoviedb.org/3/discover/movie?"
        params = {
            "include_adult": "false",
            "include_video": "false",
            "language": "en-US",
            "page": "1",
            "sort_by": "popularity.desc",
            "with_genres": str(genre_id)
        }
        headers = {
            "accept": "application/json",
            "Authorization": tmdb_auth_key
        }
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=1000
            )
        movies = response.json()
        for m in movies['results']:
            movie_list.append(m)
        ids = db.insert_to_mongo(movie_list)
        return ids
    return genre_id


def return_movie_data(movie_ids: list) -> Any:  # type: ignore
    movie_collection = db.get_documents(movie_ids)
    return movie_collection


def get_input() -> str:
    sys.stdout.write("Enter a genre to search for: ")
    line = sys.stdin.readline()
    genre = line.strip()
    return genre


def getMovies() -> None:
    genre_in = get_input()
    genre = check_genre_title(genre_in)
    get_movies_by_genre(genre)


def main() -> None:
    getMovies()


if __name__ == "__main__":
    main()
