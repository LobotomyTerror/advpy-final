import unittest
from pymongo import MongoClient, errors
from program.main import check_genre_title
from program.main import find_movie_genre_id
from program.main import find_tv_genre_id
from program.database import create_mongo_client
from program.database import get_uri


class test_main(unittest.TestCase):
    def test_check_genre_title(self) -> None:
        self.assertEqual(check_genre_title("horror"), "Horror")
        self.assertEqual(check_genre_title("Horror"), "Horror")
        self.assertEqual(
            check_genre_title("Action"),
            "Action")
        self.assertEqual(
            check_genre_title("comedy adventure"),
            "Comedy Adventure")
        self.assertEqual(
            check_genre_title("Comedy adventure"),
            "Comedy Adventure")
        self.assertEqual(
            check_genre_title("comedy Adventure"),
            "Comedy Adventure")

    def test_find_movie_genre_id(self) -> None:
        self.assertEqual(find_movie_genre_id("Action"), 28)
        self.assertEqual(find_movie_genre_id("Comedy"), 35)
        self.assertEqual(find_movie_genre_id("Horror"), 27)
        self.assertEqual(find_movie_genre_id("Adventure"), 12)

    def test_find_tv_genre_id(self) -> None:
        self.assertEqual(find_tv_genre_id("Drama"), 18)
        self.assertEqual(find_tv_genre_id("Comedy"), 35)

    def test_mongodb_response1(self) -> None:
        uri = get_uri()
        result = create_mongo_client(uri)
        self.assertIsInstance(result, MongoClient)

    def test_mongodb_response2(self) -> None:
        try:
            uri = ''
            # Purposely not using result just for testing purposes
            create_mongo_client(uri)

        except errors.ConfigurationError:
            self.assertRaises(errors.ConfigurationError)


if __name__ == "__main__":
    unittest.main()
