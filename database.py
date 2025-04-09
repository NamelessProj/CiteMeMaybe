import os
import discord
from pymongo import MongoClient

from utils import replacing_mentions, remove_mentions, extract_mentions

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

def insert_citation_to_db(message: discord.Message):
    """
    This function inserts the citation to the database.
    :param message: The message to process
    :return: None
    """
    # Getting the citation ID
    citation_id = message.id

    # Getting the database and collection
    db = get_database()
    collection = db["citation"]

    # Checking if the citation already exists in the database
    if collection.find_one({"citation_id": citation_id}):
        print(f"Message with ID {citation_id} already exists in the database.")
        return

    # Replacing mentions in the message with their names
    content = replacing_mentions(message)

    # Removing mentions from the message
    content_without_mentions = remove_mentions(message)

    # Extracting mentions from the message
    all_mentions = extract_mentions(message)

    # Preparing the citation data
    citation_data = {
        "guild_id": message.guild.id,
        "citation_id": citation_id,
        "author": {
            "name": message.author.name,
            "id": message.author.id,
            "avatar": message.author.display_avatar.url
        },
        "content": content,
        "content_without_mentions": content_without_mentions,
        "mentions": all_mentions,
        "timestamp": message.created_at
    }

    # Inserting the citation data into the database
    collection.insert_one(citation_data)