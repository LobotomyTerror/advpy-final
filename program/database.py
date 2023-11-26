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
    return_ids = movie.insert_many(movie_list)
    return return_ids.inserted_ids
    # movie.delete_many({})


def delete_db() -> Any:
    uri = get_uri()
    client: MongoClient = create_mongo_client(uri)  # type: ignore
    db = client.movie_data
    movie = db.movie
    movie.delete_many({})
