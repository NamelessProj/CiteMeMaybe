import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

from utils import replacing_mentions, extract_mentions, remove_mentions

# Load environment variables
load_dotenv()

# Getting the guild ID from the environment variable
GUILD_ID = discord.Object(id=os.getenv("GUILD_ID"))

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
    # Getting the channel using an ID from the environment variable
    channel = client.get_channel(int(os.getenv("CHANNEL_ID")))
    if channel is None:
        error_embed = discord.Embed(title="Channel not found", description="Sorry, I couldn't find the channel.", color=discord.Color.red())
        await interaction.response.send_message(embed=error_embed)
        return

    # Fetching messages from the channel history
    msgs = [message async for message in channel.history(limit=1000)]
    for message in msgs:
        # Replacing mentions in the message with their names
        content = replacing_mentions(message)

        # Removing mentions from the message
        content_without_mentions = remove_mentions(message)

        # Extracting mentions from the message
        all_mentions = extract_mentions(message)

        print(f'{message.author.name}: {content}')
        print(f'Content without mentions: {content_without_mentions}')
        if all_mentions:
            print(f'Mentions: {", ".join([f"{mention["name"]} ({mention["id"]})" for mention in all_mentions])}')

        print('')

    # Sending a response to the interaction at the end of the command
    success_embed = discord.Embed(title="All the messages were found", description="I have fetched all the messages from the channel.", color=discord.Color.green())
    await interaction.response.send_message(embed=success_embed)

# Run the bot
client.run(os.getenv('BOT_TOKEN'))