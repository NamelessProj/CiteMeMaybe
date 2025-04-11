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

    # Extracting mentions from the message
    mentions = message.mentions
    for mention in mentions:
        result.append({
            "name": mention.name,
            "id": mention.id,
            "avatar": mention.display_avatar.url
        })

    # Reversing the list to keep the order of mentions
    result = result[::-1]

    return result


def extract_mentions_string(message: discord.Message):
    """
    This function extracts mentions from the message and returns them as a string.
    :param message: The message to process
    :return: A list of mentions as strings
    """
    result = []

    # Extracting mentions from the message
    pattern = r"-(\s*@?\w+)+$"
    mentions = re.findall(pattern, message.content)
    for mention in mentions:
        mention = mention.replace("-", "").strip()
        result.append(mention)

    return result


def remove_mentions(message: discord.Message):
    """
    This function removes mentions from the message.
    :param message: The message to process
    :return: The processed message
    """
    content = message.content

    # Extracting mentions from the message
    if len(message.mentions) == 0:
        pattern = r"-(\s*@?\w+)+$"
        mentions = re.findall(pattern, content)
        for mention in mentions:
            mention = mention.replace("-", "").strip()
            content = content.replace(mention, '')
    else:
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


def setup_citation_embed(citation):
    """
    This function sets up the citation embed.
    :param citation: The citation data
    :return: The citation embed and the mentions string
    """
    # Preparing the mentions string
    all_mentions_string = ""

    if len(citation["mentions"]) == 0:
        for mention in citation["mentions_string"]:
            all_mentions_string += f"{mention}, "
    else:
        for mention in citation["mentions"]:
            mention_id = mention["id"]
            all_mentions_string += f"<@{mention_id}>, "

    # Removing the last comma and space
    all_mentions_string = all_mentions_string[:-2]

    # Generating a random color based on the citation ID
    color = get_random_color_seeded(citation["citation_id"])

    author_id = citation["author"]["id"]
    citation_id = citation["citation_id"]

    # Creating an embed with the citation data
    embed = discord.Embed(title="Citation", description=citation["content_without_mentions"], color=color)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="Who said it?", value=all_mentions_string, inline=True)
    embed.add_field(name="Who write it?", value=f"<@{author_id}>", inline=True)
    embed.set_footer(text=f"Citation ID: {citation_id}")
    embed.timestamp = citation["timestamp"]

    return {
        "embed": embed,
        "all_mentions_string": all_mentions_string
    }