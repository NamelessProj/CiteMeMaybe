import discord

from constants import CONSTANTS
from database import get_database
from utils import replacing_mentions, remove_mentions, extract_mentions, extract_mentions_string


def insert_citation_to_db(message: discord.Message):
    """
    This function inserts the citation to the database.
    :param message: The message to process
    :return: None
    """
    # Checking if the message start with the string "`no-saving`"
    # This is used to prevent saving messages that are not citations
    if message.content.startswith(CONSTANTS["no_saving"]):
        return

    # Getting the citation ID
    citation_id = message.id

    # Getting the database and collection
    db = get_database()
    collection = db["citation"]

    # Checking if the citation already exists in the database
    if collection.find_one({"citation_id": citation_id}):
        return

    # Replacing mentions in the message with their names
    content = replacing_mentions(message)

    # Removing mentions from the message
    content_without_mentions = remove_mentions(message)

    # Extracting mentions from the message
    all_mentions = extract_mentions(message)

    all_mentions_string = extract_mentions_string(message) if len(all_mentions) == 0 else []

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
        "mentions_string": all_mentions_string,
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
    if message.content.startswith(CONSTANTS["no_saving"]):
        # If the message starts with "`no-saving`", we delete the citation from the database
        delete_citation_from_db(message.id)
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

    all_mentions_string = extract_mentions_string(message) if len(all_mentions) == 0 else []

    # Preparing the citation data
    citation_data = {
        "content": content,
        "content_without_mentions": content_without_mentions,
        "mentions": all_mentions,
        "mentions_string": all_mentions_string,
        "timestamp": message.created_at
    }

    print(citation_data)

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


def get_random_citation_from_user(guild_id: int, user_id: int):
    """
    This function gets a random citation from the database for a specific user.
    :param guild_id: The ID of the guild
    :param user_id: The ID of the user
    :return: The citation data
    """
    # Getting the database and collection
    db = get_database()
    collection = db["citation"]

    # Checking if the user has any citations
    if not collection.count_documents({"guild_id": guild_id, "mentions.id": user_id}):
        return None

    # Getting a random citation from the database for the user
    citation = collection.aggregate([
        {"$match": {"guild_id": guild_id, "mentions.id": user_id}},
        {"$sample": {"size": 1}}
    ]).next()

    return citation


def get_citation_from_db(guild_id: int, citation_id: int):
    """
    This function gets a citation from the database.
    :param guild_id: The ID of the guild
    :param citation_id: The ID of the citation
    :return: The citation data
    """
    # Getting the database and collection
    db = get_database()
    collection = db["citation"]

    # Getting the citation from the database
    citation = collection.find_one({"guild_id": guild_id, "citation_id": citation_id})

    return citation


def get_citation_count(guild_id: int, user_id: int = None):
    """
    This function gets the count of citations in the database or for a specific user (in mentions).
    :param guild_id: The ID of the guild
    :param user_id: The ID of the user (optional)
    :return: The count of citations
    """
    # Getting the database and collection
    db = get_database()
    collection = db["citation"]

    # Checking if the user ID is provided
    if user_id:
        # Getting the count of citations for the user
        count = collection.count_documents({"guild_id": guild_id, "mentions.id": user_id})
    else:
        # Getting the count of all citations
        count = collection.count_documents({"guild_id": guild_id})

    return count