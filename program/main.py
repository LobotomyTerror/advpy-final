import sys
# import random
from tmdbv3api import TMDb
# from tmdbv3api import Movie
from tmdbv3api import Discover
from tmdbv3api import Genre


# Movie genres:

# [ { id: 28, name: 'Action' },
# { id: 12, name: 'Adventure' },
# { id: 16, name: 'Animation' },
# { id: 35, name: 'Comedy' },
# { id: 80, name: 'Crime' },
# { id: 99, name: 'Documentary' },
# { id: 18, name: 'Drama' },
# { id: 10751, name: 'Family' },
# { id: 14, name: 'Fantasy' },
# { id: 36, name: 'History' },
# { id: 27, name: 'Horror' },
# { id: 10402, name: 'Music' },
# { id: 9648, name: 'Mystery' },
# { id: 10749, name: 'Romance' },
# { id: 878, name: 'Science Fiction' },
# { id: 10770, name: 'TV Movie' },
# { id: 53, name: 'Thriller' },
# { id: 10752, name: 'War' },
# { id: 37, name: 'Western' }, ]


tmdb = TMDb()
tmdb.api_key = 'ddc68a76526100939a2f7c62b4f6b061'
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
    discover = Discover()
    genre_id = find_genre_id(genre)

    if genre_id != 0:
        movies = discover.discover_movies({
                'with_genres': f"{genre_id}",
                'sort_by': 'popularity.desc'
            })
        for m in movies:
            print(m)


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
