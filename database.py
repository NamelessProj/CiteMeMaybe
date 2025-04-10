import os
from pymongo import MongoClient


def get_database():
    """
    This function gets the database from the MongoDB client.
    :return: The database
    """
    # Getting the client using the MongoDB URI from the environment variable
    client = MongoClient(os.getenv('MONGO_URI'))

    # Getting the database and collection
    db = client[os.getenv('MONGO_DB_NAME')]
    return db