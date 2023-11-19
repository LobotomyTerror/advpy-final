import sys
import requests
import config
from tmdbv3api import TMDb
from tmdbv3api import Genre
import database as db


tmdb = TMDb()
tmdb.api_key = config.TMDB_API_KEY
tmdb.language = 'en'
tmdb.debug = True


def check_genre_name(genre: str) -> str:
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


def get_movies_by_genre(genre: str) -> None:
    genre_id = find_genre_id(genre)
    if genre_id != 0:
        movie_list = []
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
            "Authorization": config.TMDB_AUTH_KEY
        }
        response = requests.get(url, headers=headers, params=params, timeout=1000)
        movies = response.json()
        for m in movies['results']:
            movie_list.append(m)
        db.insert_to_mongo(movie_list)


def get_input() -> str:
    sys.stdout.write("Enter a genre to search for: ")
    line = sys.stdin.readline()
    genre = line.strip()
    return genre


def getMovies() -> None:
    genre_in = get_input()
    genre = check_genre_name(genre_in)
    get_movies_by_genre(genre)


def main() -> None:
    getMovies()


if __name__ == "__main__":
    main()
