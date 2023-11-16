import sys
import random
from tmdbv3api import TMDb
from tmdbv3api import Movie
from tmdbv3api import Discover

tmdb = TMDb()
tmdb.api_key = 'ddc68a76526100939a2f7c62b4f6b061'
tmdb.language = 'en'
tmdb.debug = True

def get_movies_by_genre(genre: str, numOfMovies: int):
    discover = Discover()
    movies = discover.discover_movies({
        'with_genres': f'{genre}',
        'sort_by': 'popularity.desc'
    })
    print(f"{movies[0]}")


def getMovies():
    get_movies_by_genre('horror', 50)


def main():
    getMovies()


if __name__ == "__main__":
    main()
