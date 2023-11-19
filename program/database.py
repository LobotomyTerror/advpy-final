from pymongo.mongo_client import MongoClient
import certifi
import config

def insert_to_mongo(movie_list) -> None:
    uri = (
        "mongodb+srv://" + config.MONGODB_USRNM + 
        ":" + config.MONGODB_PASS + "@cluster0.zybp0x4.mongodb.net/?retryWrites=true&w=majority")
    client = MongoClient(uri, tlsCAFile=certifi.where())

    db = client.movie_data
    movie = db.movie
    movie.insert_many(movie_list)
    movie.delete_many({})
