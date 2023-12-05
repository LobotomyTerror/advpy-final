""" Main file that operates as the "middle-man" form the
f_app file and the database file. Where the API connection
happens and gathers data from the TMDB and then stores
the JSON data into Mongodb.

    Returns:
        _type_: Any, Lists, Dicts, Str, Ints
    """
import sys
import os
import re
from typing import Any
from dotenv import load_dotenv
import requests  # type: ignore
from tmdbv3api import TMDb
from tmdbv3api import Genre
from . import database as db
# import database as db

# This section just connects my api key that I
# created for the movie database. I changed the
# config file to environment variables so that
# I can push this to a public repo and not give
# away sensitive information.

load_dotenv()
tmdb_api_key = os.getenv('TMDB_API_KEY')
tmdb = TMDb()
tmdb.api_key = tmdb_api_key
tmdb.language = 'en'
tmdb.debug = True


def check_genre_title(genre: str) -> str:
    """Capitalize first character of each word

    Args:
        genre (str): The genre (str) that is passed
        in is just capitilized for the first char
        so is matches TMDB's setup
    Returns:
        str: New string with first char capitilized
    """
    genre_title = genre.title()
    return genre_title


def find_movie_genre_id(genre: str) -> int:
    """Once the genre has been capitilized this
    function sets the genre_list to class Genre
    which in turn allows us to get the movie genre
    list. Allowing us to find the corresponding id
    value that TMDB uses.

    Args:
        genre (str): Compares genre against the genre_list
        to find if a they are identical then setting the id
        value (int) to the genre_id

    Returns:
        int: genre_id equals the integer value and returns said
        value for discovering movies with that genre
    """
    genre_id = 0
    genre_list = Genre()
    genre_list = genre_list.movie_list()
    for gl in genre_list:
        if genre == gl['name']:
            genre_id = gl['id']
            return genre_id
    return 0


def find_tv_genre_id(genre: str) -> int:
    genre_id = 0
    genre_list = Genre()
    genre_list = genre_list.tv_list()
    for gl in genre_list:
        if genre == gl['name']:
            genre_id = gl['id']
            return genre_id
    return 0


def remove_from_db() -> Any:
    """Goes to the database module where the insertion
    into the Mongodb database is conducted

    Returns:
        Any: No return
    """
    db.delete_db()


def search_by_genre(genre: str, type_of_search: str) -> Any:
    """Checks if genre_id is an actual valid id from the
    TMDB. If so it sets the url beginning for discovering
    movies from the website. Then sets specific parameters and
    headers for structuring the entire url -
    (https://api.themoviedb.org/3/discover/
    movie?...paramstuff...headers...). Then sends a request and
    stores in the response var then making it a json structure.
    Then stores as a list of dicts to be inserted into Mongodb.

    Args:
        genre (str): The genre that we are searching for

    Returns:
        Any: Returns either a list of id's from mongodb or
        a 0 to indicate there was no matching id for that genre
    """
    genre = check_genre_title(genre)
    tmdb_auth_key = os.getenv('TMDB_AUTH_KEY')
    if type_of_search == 'movie_search':
        genre_id = find_movie_genre_id(genre)
        if genre_id != 0:
            movie_list = []
            num_of_pages = 5
            for page_num in range(1, num_of_pages + 1):
                url = "https://api.themoviedb.org/3/discover/movie?"
                params = {
                    "include_adult": "false",
                    "include_video": "false",
                    "language": "en-US",
                    "page": f"{page_num}",
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
    if type_of_search == 'tv_search':
        genre_id = find_tv_genre_id(genre)
        if genre_id != 0:
            tv_list = []
            num_of_pages = 5
            for page_num in range(1, num_of_pages + 1):
                url = "https://api.themoviedb.org/3/discover/tv?"
                params = {
                    "include_adult": "false",
                    "include_video": "false",
                    "language": "en-US",
                    "page": f"{page_num}",
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
                tv_shows = response.json()
                for tv_show in tv_shows['results']:
                    tv_list.append(tv_show)
            ids = db.insert_to_mongo(tv_list)
            return ids

    return genre_id


def return_movie_data(discovered_ids: list) -> Any:  # type: ignore
    """Movie collection variable gets the data from the mongodb
    collection in the cluster.

    Args:
        movie_ids (list): Passing in the list of movie ids,
        so mongodb can return the movie data stored in the
        cluster

    Returns:
        Any: Returns a list of dicts with all the JSON data
        that was stored in the mongodb database
    """
    discovery_collection = db.get_documents(discovered_ids)
    return discovery_collection


def return_movie_data_from_api_id(discovered_ids: list) -> Any:  # type: ignore
    """Movie collection variable gets the data from the mongodb
    collection in the cluster.

    Args:
        movie_ids (list): Passing in the list of movie ids,
        so mongodb can return the movie data stored in the
        cluster

    Returns:
        Any: Returns a list of dicts with all the JSON data
        that was stored in the mongodb database
    """
    discovery_collection = db.get_documents_API_ID(discovered_ids)
    return discovery_collection


def get_trailer_data(
        title_id: int,
        search_type: str,
        genre_ids: list) -> Any:  # type: ignore

    tmdb_auth_key = os.getenv('TMDB_AUTH_KEY')
    genre_list = Genre()
    headers = {
            "accept": "application/json",
            "Authorization": tmdb_auth_key
    }

    if search_type == "movie_trailers":
        url = (
            f"https://api.themoviedb.org/3/movie"
            f"/{title_id}/videos?language=en-US"
        )

        response = requests.get(url, headers=headers, timeout=1000)
        video = response.json()
        trailer_variations = re.compile(
            "Official Trailer|Trailer|original trailer",
            re.I)

        # genre_list = Genre()
        genre_list = genre_list.movie_list()
        genre_names = []

        for genre_name in genre_list:
            if genre_name.get('id', '') in genre_ids:
                genre_names.append(genre_name.get('name', ''))

        for trailer in video['results']:
            trailer_name = trailer.get('name', '')
            if trailer_variations.search(trailer_name) \
                    and trailer.get('type', '') == "Trailer":
                return trailer.get("key", None), genre_names
    else:
        url = (
            f"https://api.themoviedb.org/3/tv/"
            f"{title_id}/videos?language=en-US"
        )

        response = requests.get(url, headers=headers, timeout=1000)
        video = response.json()
        trailer_variations = re.compile(
            "Official Trailer|Trailer|original trailer",
            re.I)

        genre_list = genre_list.tv_list()
        genre_names = []

        for genre_name in genre_list:
            if genre_name.get('id', '') in genre_ids:
                genre_names.append(genre_name.get('name', ''))

        for trailers in video['results']:
            trailers_name = trailers.get('name', '')
            if trailer_variations.search(trailers_name) \
                    or trailers.get('official', '') is True \
                    and trailers.get('type', '') == "Trailer":
                official_trailer = trailers.get('key', None)
                return official_trailer, genre_names
    return None, genre_names

# These functions below are not used, only for testing
# purposes for when I was setting up the api and the
# the connection to Mongodb.


def get_input() -> str:
    sys.stdout.write("Enter a genre to search for: ")
    line = sys.stdin.readline()
    genre = line.strip()
    return genre


def getMovies() -> None:
    # get_trailer_data(741592, "movie_trailers")
    # get_trailer_data(2025, "tv_trailers", [])
    genre_in = get_input()
    genre = check_genre_title(genre_in)
    search_by_genre(genre, 'movie_search')


def main() -> None:
    getMovies()


if __name__ == "__main__":
    main()
