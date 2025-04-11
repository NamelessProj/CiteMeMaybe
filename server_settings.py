from collections.abc import Mapping
from pymongo.synchronous.database import Database


def setup_server_settings(db: Database[Mapping], guild_id: int, citation_channel_id: int):
    """
    This function sets up the server settings in the database.
    :param db: The database
    :param guild_id: The ID of the guild
    :param citation_channel_id: The ID of the channel
    :return: The server settings
    """
    # Getting the collection
    collection = db.get_collection('server_settings')

    # Checking if the server settings already exist
    if collection.find_one({"guild_id": guild_id}):
        return update_server_settings(db, guild_id, citation_channel_id)

    # Setting up the server settings
    server_settings = {
        "guild_id": guild_id, # The ID of the guild
        "citation_channel_id": citation_channel_id, # The ID of the channel in which the bot will gather citations
        "history_limit": 100, # Default history limit
    }

    # Inserting the server settings into the database
    collection.insert_one(server_settings)

    # Returning the server settings
    return server_settings


def update_server_settings(db: Database[Mapping], guild_id: int, citation_channel_id: int = None):
    """
    This function updates the server settings in the database.
    :param db: The database
    :param guild_id: The ID of the guild
    :param citation_channel_id: The ID of the channel
    :return: The server settings
    """
    # Checking if we received parameters
    if citation_channel_id is None:
        return None

    # Getting the collection
    collection = db.get_collection('server_settings')

    # Preparing the update data
    update_data = {}

    # Checking if the citation channel ID is provided and updating it
    if citation_channel_id is not None:
        update_data["citation_channel_id"] = citation_channel_id

    # Updating the server settings
    collection.update_one({"guild_id": guild_id}, {"$set": update_data})

    # Getting the updated server settings
    server_settings = collection.find_one({"guild_id": guild_id})

    return server_settings


def get_server_settings(db: Database[Mapping], guild_id: int):
    """
    This function gets the server settings from the database.
    :param db: The database
    :param guild_id: The ID of the guild
    :return: The server settings
    """
    # Getting the collection
    collection = db.get_collection('server_settings')

    # Getting the server settings
    server_settings = collection.find_one({"guild_id": guild_id})

    return server_settings