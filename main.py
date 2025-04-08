import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Getting the guild ID from the environment variable
GUILD_ID = discord.Object(id=os.getenv("GUILD_ID"))

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

# Define the bot client
class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        # Syncing the commands with the guild
        try:
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f'Synced {len(synced)} commands to guild {GUILD_ID.id}')

        except Exception as e:
            print(f'Error syncing commands: {e}')

# Define the intents
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

# Command to get all messages from a specific channel
@client.tree.command(name="get_messages", description="Getting all messages", guild=GUILD_ID)
async def get_messages(interaction: discord.Interaction):
    # Getting the channel from the environment variable
    channel = discord.utils.get(interaction.guild.channels, name=os.getenv("CHANNEL_NAME"))
    if channel is None:
        await interaction.response.send_message('Channel not found')
        return

    # Fetching messages from the channel history
    msgs = [message async for message in channel.history(limit=1000)]
    for message in msgs:
        content = replacing_mentions(message)

        print(f'{message.author.name}: {content}')

    # Sending a response to the interaction at the end of the command
    await interaction.response.send_message('All messages found')

# Run the bot
client.run(os.getenv('BOT_TOKEN'))