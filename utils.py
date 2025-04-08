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