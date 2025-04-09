import re
import discord

def replacing_mentions(message: discord.Message):
    """
    This function replaces mentions in the message with their names.
    :param message: The message to process
    :return: The processed message
    """
    content = message.content

    # Replacing mentions with their names
    for mention in message.mentions:
        content = content.replace(f'<@{mention.id}>', mention.name)

    return content


def extract_mentions(message: discord.Message):
    """
    This function extracts mentions from the message.
    :param message: The message to process
    :return: A list of mentions
    """
    result = []

    mentions = message.mentions
    for mention in mentions:
        result.append({
            "name": mention.name,
            "id": mention.id,
            "avatar": mention.display_avatar.url
        })

    return result


def remove_mentions(message: discord.Message):
    """
    This function removes mentions from the message.
    :param message: The message to process
    :return: The processed message
    """
    content = message.content

    # Removing mentions
    for mention in message.mentions:
        content = content.replace(f'<@{mention.id}>', '')

    # Removing last "-" and all ","
    content = re.sub(r'-(\s*,?)*$', '', content, 1)

    return content.strip()


def get_random_color_seeded(seed: str):
    """
    This function generates a random color based on a seed.
    :param seed: The seed to generate the color
    :return: The generated color
    """
    # Hashing the seed to get a number
    hash_value = hash(seed)

    # Generating a color from the hash value
    color = discord.Color.from_rgb((hash_value & 0xFF0000) >> 16, (hash_value & 0x00FF00) >> 8, hash_value & 0x0000FF)

    return color