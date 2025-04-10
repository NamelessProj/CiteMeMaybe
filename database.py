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
    # Checking if the message start with the string "`no-saving`"
    # This is used to prevent saving messages that are not citations
    if message.content.startswith("`no-saving`"):
        return

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


def edit_citation_in_db(message: discord.Message):
    """
    This function edits the citation in the database.
    :param message: The message to process
    :return: None
    """
    # Checking if the message start with the string "`no-saving`"
    # This is used to prevent saving messages that are not citations
    if message.content.startswith("`no-saving`"):
        return

    # Getting the citation ID
    citation_id = message.id

    # Getting the database and collection
    db = get_database()
    collection = db["citation"]

    # Replacing mentions in the message with their names
    content = replacing_mentions(message)

    # Removing mentions from the message
    content_without_mentions = remove_mentions(message)

    # Extracting mentions from the message
    all_mentions = extract_mentions(message)

    # Preparing the citation data
    citation_data = {
        "content": content,
        "content_without_mentions": content_without_mentions,
        "mentions": all_mentions,
        "timestamp": message.created_at
    }

    # Updating the citation data in the database
    collection.update_one({"citation_id": citation_id}, {"$set": citation_data})


def delete_citation_from_db(citation_id: int):
    """
    This function deletes a citation from the database.
    :param citation_id: The ID of the citation to delete
    :return: None
    """
    # Getting the database and collection
    db = get_database()
    collection = db["citation"]

    # Deleting the citation from the database
    collection.delete_one({"citation_id": citation_id})


def get_random_citation_from_db(guild_id: int):
    """
    This function gets a random citation from the database.
    :return: The citation data
    """
    # Getting the database and collection
    db = get_database()
    collection = db["citation"]

    # Getting a random citation from the database
    citation = collection.aggregate([
        {"$match": {"guild_id": guild_id}},
        {"$sample": {"size": 1}}
    ]).next()

    return citation