from pymongo.mongo_client import MongoClient
import certifi
import config


def create_mongo_client(uri: str) -> MongoClient:  # type: ignore
    return MongoClient(uri, tlsCAFile=certifi.where())


def insert_to_mongo(movie_list: list) -> None:  # type: ignore
    uri = (
        "mongodb+srv://" + config.MONGODB_USRNM +
        ":" + config.MONGODB_PASS +
        "@cluster0.zybp0x4.mongodb.net/?"
        "retryWrites=true&w=majority"
        )
    client: MongoClient = create_mongo_client(uri)  # type: ignore

    db = client.movie_data
    movie = db.movie
    movie.insert_many(movie_list)
    movie.delete_many({})
