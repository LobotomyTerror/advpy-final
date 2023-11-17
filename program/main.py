import sys
import random
from tmdbv3api import TMDb
from tmdbv3api import Movie
from tmdbv3api import Discover
from tmdbv3api import Genre
import requests

tmdb = TMDb()
tmdb.api_key = 'ddc68a76526100939a2f7c62b4f6b061'
tmdb.language = 'en'
tmdb.debug = True

def get_movies_by_genre(genre: str, numOfMovies: int):
    discover = Discover()
    movie_list = []
    movies = discover.discover_movies({
        'with_genres': f'{genre}',
        'sort_by': 'popularity.desc'
    })
    movie_list.append(movies)
    print(f"{len(movie_list)}")


def getMovies():
    get_movies_by_genre(27, 50)


def main():
    getMovies()


if __name__ == "__main__":
    main()
