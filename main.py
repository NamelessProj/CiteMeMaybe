import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

from database import insert_citation_to_db, get_random_citation_from_db, delete_citation_from_db, edit_citation_in_db, \
    get_citation_count, get_random_citation_from_user, get_citation_from_db
from server_settings import setup_server_settings, get_server_settings
from utils import get_random_color_seeded, setup_citation_embed

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

    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        # Getting the server settings from the database
        server_settings = get_server_settings(message.guild.id)

        if server_settings is None:
            error_embed = discord.Embed(title="Server settings not found", description="Sorry, I couldn't find the server settings. Please set them up using the /setup_server command.", color=discord.Color.red())
            await message.channel.send(embed=error_embed)
            return

        # Checking if the message is in the channel specified in the environment variable
        if message.channel.id == server_settings["citation_channel_id"]:
            # Inserting the citation to the database
            insert_citation_to_db(message)

    async def on_message_edit(self, before, after):
        # Ignore messages from the bot itself
        if before.author == self.user:
            return

        # Getting the server settings from the database
        server_settings = get_server_settings(after.guild.id)

        if server_settings is None:
            error_embed = discord.Embed(title="Server settings not found",description="Sorry, I couldn't find the server settings. Please set them up using the /setup_server command.",color=discord.Color.red())
            await after.channel.send(embed=error_embed)
            return

        # Checking if the message is in the channel specified in the environment variable
        if before.channel.id == server_settings["citation_channel_id"]:
            # Inserting the citation to the database
            edit_citation_in_db(after)

    async def on_message_delete(self, message):
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        # Getting the server settings from the database
        server_settings = get_server_settings(message.guild.id)

        if server_settings is None:
            error_embed = discord.Embed(title="Server settings not found",description="Sorry, I couldn't find the server settings. Please set them up using the /setup_server command.",color=discord.Color.red())
            await message.channel.send(embed=error_embed)
            return

        # Checking if the message is in the channel specified in the environment variable
        if message.channel.id == server_settings["citation_channel_id"]:
            # Deleting the citation from the database
            delete_citation_from_db(message.id)


# Define the intents
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)


# Command to get all messages from a specific channel
@client.tree.command(name="updating_database", description="Updating the database with all the messages from the channel", guild=GUILD_ID)
@app_commands.checks.has_permissions(administrator=True)
async def updating_database(interaction: discord.Interaction):
    # Getting the server settings from the database
    server_settings = get_server_settings(interaction.guild.id)

    if server_settings is None:
        error_embed = discord.Embed(title="Server settings not found", description="Sorry, I couldn't find the server settings. Please set them up using the /setup_server command.", color=discord.Color.red())
        await interaction.response.send_message(embed=error_embed)
        return

    # Getting the channel using an ID from the environment variable
    channel = client.get_channel(server_settings["citation_channel_id"])
    if channel is None:
        error_embed = discord.Embed(title="Channel not found", description="Sorry, I couldn't find the channel.", color=discord.Color.red())
        await interaction.response.send_message(embed=error_embed)
        return

    # Fetching messages from the channel history
    msgs = [message async for message in channel.history(limit=server_settings["history_limit"])]
    for message in msgs:
        insert_citation_to_db(message)

    # Sending a response to the interaction at the end of the command
    success_embed = discord.Embed(title="All the messages were found", description="I have fetched all the messages from the channel.", color=discord.Color.green())
    await interaction.response.send_message(embed=success_embed)


@client.tree.command(name="random_citation", description="Getting a random citation", guild=GUILD_ID)
@app_commands.describe(user="The user to get the citation for")
async def get_random_citation(interaction: discord.Interaction, user: discord.User = None):
    # Getting the guild ID from the interaction
    guild_id = interaction.guild.id

    # Getting a random citation from the database
    if user is None:
        citation = get_random_citation_from_db(guild_id)
    else:
        citation = get_random_citation_from_user(guild_id, user.id)

    # Checking if there are a citation
    if citation is None and user is not None:
        error_embed = discord.Embed(title="The user has no citations", description=f"Sorry, I couldn't find any citations for {user.mention}", color=discord.Color.red())
        await interaction.response.send_message(embed=error_embed)
        return
    elif citation is None:
        error_embed = discord.Embed(title="No citations found", description="Sorry, I couldn't find any citations.", color=discord.Color.red())
        await interaction.response.send_message(embed=error_embed)
        return

    embed = setup_citation_embed(citation)

    # Sending the embed as a response to the interaction
    await interaction.response.send_message("- "+embed["all_mentions_string"]+"\n", embed=embed["embed"])


@client.tree.command(name="how_many", description="Getting the number of citations total or for a specific user", guild=GUILD_ID)
@app_commands.describe(user="The user to get the number of citations for")
async def how_many(interaction: discord.Interaction, user: discord.User = None):
    # Getting the guild ID from the interaction
    guild_id = interaction.guild.id

    # Getting the server settings from the database
    server_settings = get_server_settings(guild_id)

    if server_settings is None:
        error_embed = discord.Embed(title="Server settings not found", description="Sorry, I couldn't find the server settings. Please set them up using the /setup_server command.", color=discord.Color.red())
        await interaction.response.send_message(embed=error_embed)
        return

    # Getting the number of citations from the database
    citation_count = get_citation_count(guild_id, user.id if user else None)
    "{: }".format(citation_count)

    # Getting the number of citations from the database
    if user is None:
        response_message = f"There are {citation_count} citation{"s" if citation_count > 1 else ""} in total."
    else:
        response_message = f"There are {citation_count} citation{"s" if citation_count > 1 else ""} for {user.mention}."

    # Sending a response to the interaction at the end of the command
    await interaction.response.send_message(response_message)


@client.tree.command(name="get_a_citation", description="Getting a citation by an ID", guild=GUILD_ID)
@app_commands.describe(citation_id="The ID (integer) of the citation to get")
async def get_a_citation(interaction: discord.Interaction, citation_id: str):
    # Getting the guild ID from the interaction
    guild_id = interaction.guild.id

    # Checking if the citation ID is valid
    if not citation_id.isdigit():
        error_embed = discord.Embed(title="Invalid citation ID", description="Sorry, the citation ID must be a number.", color=discord.Color.red())
        await interaction.response.send_message(embed=error_embed)
        return

    # Converting the citation ID to an integer
    citation_id = int(citation_id)

    # Getting a citation from the database
    citation = get_citation_from_db(guild_id, citation_id)

    # Checking if there are a citation
    if citation is None:
        error_embed = discord.Embed(title="Citation not found", description="Sorry, I couldn't find any citations.", color=discord.Color.red())
        await interaction.response.send_message(embed=error_embed)
        return

    embed = setup_citation_embed(citation)

    # Sending the embed as a response to the interaction
    await interaction.response.send_message("- "+embed["all_mentions_string"]+"\n", embed=embed["embed"])


@client.tree.command(name="setup_server", description="Setting up the server settings. Only for administrators", guild=GUILD_ID)
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(citation_channel="The channel in which the bot will gather citations")
async def setup_server(interaction: discord.Interaction, citation_channel: discord.TextChannel):
    # Getting the guild ID from the interaction
    guild_id = interaction.guild.id

    # Setting up the server settings in the database
    server_settings = setup_server_settings(guild_id, citation_channel.id)

    # Checking if the server settings were set up successfully
    if server_settings is None:
        error_embed = discord.Embed(title="An error occur", description="Sorry, I couldn't set up the server settings. Something unexpected happened.", color=discord.Color.red())
        await interaction.response.send_message(embed=error_embed)
        return

    # Sending a response to the interaction at the end of the command
    success_embed = discord.Embed(title="Server settings set up", description="I have set up the server settings.", color=discord.Color.green())
    await interaction.response.send_message(embed=success_embed)


@client.tree.command(name="help", description="Getting help", guild=GUILD_ID)
async def help_command(interaction: discord.Interaction):
    # Creating an embed with the help information
    embed = discord.Embed(title="Help", description="Here are the commands you can use:", color=discord.Color.blue())
    embed.add_field(name="/random_citation", value="Get a random citation from the database or for a specific user.", inline=False)
    embed.add_field(name="/how_many", value="Get the number of citations total or for a specific user.", inline=False)
    embed.add_field(name="/get_a_citation", value="Get a citation by an ID.", inline=False)
    embed.add_field(name="/setup_server", value="Set up the server settings. Only available for administrators.", inline=False)
    embed.add_field(name="/updating_database", value="Update the database with all the messages from the channel. Only available for administrators.", inline=False)
    embed.add_field(name="/help", value="Get help with the bot commands.", inline=False)
    embed.add_field(name="How not to save a message?", value="To not save a message, start the message with `no-saving`. You have to put it in a code block.", inline=False)

    # Sending the embed as a response to the interaction
    await interaction.response.send_message(embed=embed)


@setup_server.error
async def setup_server_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    # Checking if the error is a MissingPermissions error
    if isinstance(error, app_commands.MissingPermissions):
        error_embed = discord.Embed(title="Missing permissions", description="Sorry, you don't have permission to use this command.", color=discord.Color.red())
        await interaction.response.send_message(embed=error_embed)
    else:
        # Sending a generic error message
        error_embed = discord.Embed(title="An error occur", description="Sorry, I couldn't set up the server settings. Something unexpected happened.", color=discord.Color.red())
        await interaction.response.send_message(embed=error_embed)


# Run the bot
client.run(os.getenv('BOT_TOKEN'))