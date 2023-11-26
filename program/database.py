from typing import Any
from pymongo.mongo_client import MongoClient
import certifi
import config


def create_mongo_client(uri: str) -> MongoClient:  # type: ignore
    return MongoClient(uri, tlsCAFile=certifi.where())


def insert_to_mongo(movie_list: list) -> Any:  # type: ignore
    uri = (
        "mongodb+srv://" + config.MONGODB_USRNM +
        ":" + config.MONGODB_PASS +
        "@cluster0.zybp0x4.mongodb.net/?"
        "retryWrites=true&w=majority"
        )
    client: MongoClient = create_mongo_client(uri)  # type: ignore

    db = client.movie_data
    movie = db.movie
    return_ids = movie.insert_many(movie_list)
    return return_ids.inserted_ids
    # movie.delete_many({})
