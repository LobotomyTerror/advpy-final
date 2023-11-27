from typing import Any
from pymongo.mongo_client import MongoClient
import certifi
import config


def get_uri() -> Any:
    uri = (
        "mongodb+srv://" + config.MONGODB_USRNM +
        ":" + config.MONGODB_PASS +
        "@cluster0.zybp0x4.mongodb.net/?"
        "retryWrites=true&w=majority"
    )
    return uri


def create_mongo_client(uri: str) -> MongoClient:  # type: ignore
    return MongoClient(uri, tlsCAFile=certifi.where())


def insert_to_mongo(movie_list: list) -> Any:  # type: ignore
    uri = get_uri()
    client: MongoClient = create_mongo_client(uri)  # type: ignore

    db = client.movie_data
    movie = db.movie
    for movie_data in movie_list:
        movie_data['_id'] = movie_data.pop('id')
    return_ids = movie.insert_many(movie_list)
    return return_ids.inserted_ids


def delete_db() -> Any:
    uri = get_uri()
    client: MongoClient = create_mongo_client(uri)  # type: ignore
    db = client.movie_data
    movie = db.movie
    movie.delete_many({})


def get_documents(movie_ids: list) -> Any:
    uri = get_uri()
    client: MongoClient = create_mongo_client(uri)
    db = client.movie_data
    movie_collection = db.movie

    result = movie_collection.find({'_id': {'$in': movie_ids}})
    movies = list(result)
    return movies
