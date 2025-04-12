import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

from citations import insert_citation_to_db, get_random_citation_from_db, delete_citation_from_db, edit_citation_in_db, \
    get_citation_count, get_random_citation_from_user, get_citation_from_db, get_all_citations_from_db
from constants import CONSTANTS
from database import get_database
from server_settings import setup_server_settings, get_server_settings
from utils import setup_citation_embed, get_top_user_citations_said, get_top_user_citations_written

# Load environment variables
load_dotenv()

# Getting the guild ID from the environment variable
GUILD_ID = discord.Object(id=os.getenv("GUILD_ID")) if os.getenv("PYTHON_ENV") == "dev" else None

# Define the bot client
class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        # Syncing the commands with the guild
        try:
            synced = await self.tree.sync(guild=GUILD_ID)
            display_id = GUILD_ID.id if GUILD_ID else "global"
            print(f'Synced {len(synced)} commands to guild {display_id}')

        except Exception as e:
            print(f'Error syncing commands: {e}')

    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        db = get_database()

        # Getting the server settings from the database
        server_settings = get_server_settings(db, message.guild.id)

        if server_settings is None:
            return

        # Checking if the message is in the channel specified in the environment variable
        if message.channel.id == server_settings["citation_channel_id"]:
            # Inserting the citation to the database
            insert_citation_to_db(db, message)

    @commands.Cog.listener(name="on_message_edit")
    async def on_message_edit(self, before, after):
        # Ignore messages from the bot itself
        if before.author == self.user:
            return

        db = get_database()

        # Getting the server settings from the database
        server_settings = get_server_settings(db, after.guild.id)

        if server_settings is None:
            return

        # Checking if the message is in the channel specified in database
        if before.channel.id == server_settings["citation_channel_id"]:
            # Inserting the citation to the database
            edit_citation_in_db(db, after)

    @commands.Cog.listener(name="on_message_delete")
    async def on_message_delete(self, message):
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        db = get_database()

        # Getting the server settings from the database
        server_settings = get_server_settings(db, message.guild.id)

        if server_settings is None:
            return

        # Checking if the message is in the channel specified in the environment variable
        if message.channel.id == server_settings["citation_channel_id"]:
            # Deleting the citation from the database
            delete_citation_from_db(db, message.id)


# Define the intents
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)


@client.tree.command(name="save_new_citations", description="Updating the database with all the messages from the channel", guild=GUILD_ID)
@app_commands.checks.has_permissions(administrator=True)
async def update_database(interaction: discord.Interaction):
    # Letting Discord know that we are processing the command
    await interaction.response.defer()

    db = get_database()

    # Getting the server settings from the database
    server_settings = get_server_settings(db, interaction.guild.id)

    if server_settings is None:
        error_embed = discord.Embed(title="Server settings not found", description="Sorry, I couldn't find the server settings. Please set them up using the /setup_server command.", color=discord.Color.red())
        await interaction.followup.send(embed=error_embed)
        return

    # Getting the channel using an ID from the environment variable
    channel = interaction.client.get_channel(server_settings["citation_channel_id"])
    if channel is None:
        error_embed = discord.Embed(title="Channel not found", description="Sorry, I couldn't find the channel.", color=discord.Color.red())
        await interaction.followup.send(embed=error_embed)
        return

    # Fetching messages from the channel history
    msgs = [message async for message in channel.history(limit=server_settings["history_limit"])]
    for message in msgs:
        insert_citation_to_db(db, message)

    # Sending a response to the interaction at the end of the command
    success_embed = discord.Embed(title="All the messages were found", description="I have fetched all the messages from the channel.", color=discord.Color.green())
    await interaction.followup.send(embed=success_embed)


@client.tree.command(name="random_citation", description="Getting a random citation", guild=GUILD_ID)
@app_commands.describe(user="The user to get the citation for")
async def get_random_citation(interaction: discord.Interaction, user: discord.User = None):
    # Getting the guild ID from the interaction
    guild_id = interaction.guild.id

    db = get_database()

    # Getting a random citation from the database
    if user is None:
        citation = get_random_citation_from_db(db, guild_id)
    else:
        citation = get_random_citation_from_user(db, guild_id, user.id)

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

    text_mention = embed["all_mentions_string"] if len(embed["all_mentions_string"]) > 0 else "no mentions found"

    # Sending the embed as a response to the interaction
    await interaction.response.send_message(f"- {text_mention}\n", embed=embed["embed"])


@client.tree.command(name="how_many", description="Getting the number of citations total or for a specific user", guild=GUILD_ID)
@app_commands.describe(user="The user to get the number of citations for")
async def how_many(interaction: discord.Interaction, user: discord.User = None):
    # Getting the guild ID from the interaction
    guild_id = interaction.guild.id

    db = get_database()

    # Getting the server settings from the database
    server_settings = get_server_settings(db, guild_id)

    if server_settings is None:
        error_embed = discord.Embed(title="Server settings not found", description="Sorry, I couldn't find the server settings. Please set them up using the /setup_server command.", color=discord.Color.red())
        await interaction.response.send_message(embed=error_embed)
        return

    # Getting the number of citations from the database
    citation_count = get_citation_count(db, guild_id, user.id if user else None)

    # Determining the correct form of the word "citation" based on the count
    citation_str = "citations" if citation_count["number"] > 1 else "citation"

    formated_number = citation_count["formated_number"]

    # Getting the number of citations from the database
    if user is None:
        response_message = f"There are **{formated_number}** {citation_str} in total."
    else:
        response_message = f"There are **{formated_number}** {citation_str} for {user.mention}."

    # Sending a response to the interaction at the end of the command
    await interaction.response.send_message(response_message)


@client.tree.command(name="how_many_written_by", description="Getting the number of citations written by a specific user", guild=GUILD_ID)
@app_commands.describe(user="The user to get the number of citations for. By default, it's the user who wrote the command")
async def how_many_written_by(interaction: discord.Interaction, user: discord.User = None):
    # Getting the guild ID from the interaction
    guild_id = interaction.guild.id

    db = get_database()

    # Getting the server settings from the database
    server_settings = get_server_settings(db, guild_id)

    if server_settings is None:
        error_embed = discord.Embed(title="Server settings not found", description="Sorry, I couldn't find the server settings. Please set them up using the /setup_server command.", color=discord.Color.red())
        await interaction.response.send_message(embed=error_embed)
        return

    # Getting the number of citations from the database
    citation_count = get_citation_count(db, guild_id, user.id if user else interaction.user.id, True)

    # Determining the correct form of the word "citation" based on the count
    citation_str = "citations" if citation_count["number"] > 1 else "citation"

    formated_number = citation_count["formated_number"]

    # Getting the number of citations from the database
    response_message = f"There are **{formated_number}** {citation_str} written by you." if user else f"There are **{formated_number}** {citation_str} written by {user.mention}."

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

    db = get_database()

    # Converting the citation ID to an integer
    citation_id = int(citation_id)

    # Getting a citation from the database
    citation = get_citation_from_db(db, guild_id, citation_id)

    # Checking if there are a citation
    if citation is None:
        error_embed = discord.Embed(title="Citation not found", description="Sorry, I couldn't find any citations.", color=discord.Color.red())
        await interaction.response.send_message(embed=error_embed)
        return

    embed = setup_citation_embed(citation)

    # Sending the embed as a response to the interaction
    await interaction.response.send_message("- "+embed["all_mentions_string"]+"\n", embed=embed["embed"])


@client.tree.command(name="top", description="Getting the top users with the most citations", guild=GUILD_ID)
@app_commands.describe(number="The number of users to get max (default 5)")
async def get_top_users(interaction: discord.Interaction, number: int = 5):
    await interaction.response.defer()

    # Getting the guild ID from the interaction
    guild_id = interaction.guild.id

    db = get_database()

    # Getting the server settings from the database
    server_settings = get_server_settings(db, guild_id)

    if server_settings is None:
        error_embed = discord.Embed(title="Server settings not found", description="Sorry, I couldn't find the server settings. Please set them up using the /setup_server command.", color=discord.Color.red())
        await interaction.followup.send(embed=error_embed)
        return

    # Getting all the users that have citations
    all_citations = get_all_citations_from_db(db, guild_id)

    # Getting the top users with the most citations said
    top_users_citations_said = get_top_user_citations_said(number, all_citations)

    # Getting the top users with the most citations written
    top_users_citations_written = get_top_user_citations_written(number, all_citations)

    # Creating an embed to display the top users
    embed = discord.Embed(title="Who's at the top?", description="Top with the most citations...", color=discord.Color.blue())

    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="Said", value=top_users_citations_said, inline=True)
    embed.add_field(name="", value="", inline=True)
    embed.add_field(name="Written", value=top_users_citations_written, inline=True)

    # Sending a response to the interaction at the end of the command
    await interaction.followup.send(embed=embed)


@client.tree.command(name="setup_server", description="Setting up the server settings. Only for administrators", guild=GUILD_ID)
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(citation_channel="The channel in which the bot will gather citations")
async def setup_server(interaction: discord.Interaction, citation_channel: discord.TextChannel):
    # Getting the guild ID from the interaction
    guild_id = interaction.guild.id

    db = get_database()

    # Setting up the server settings in the database
    server_settings = setup_server_settings(db, guild_id, citation_channel.id)

    # Checking if the server settings were set up successfully
    if server_settings is None:
        error_embed = discord.Embed(title="An error occur", description="Sorry, I couldn't set up the server settings. Something unexpected happened.", color=discord.Color.red())
        await interaction.response.send_message(embed=error_embed)
        return

    # Sending a response to the interaction at the end of the command
    success_embed = discord.Embed(title="Server settings set up", description="I have set up the server settings.", color=discord.Color.green())
    await interaction.response.send_message(embed=success_embed)


@client.tree.command(name="example", description="Getting an example on how to write a citation", guild=GUILD_ID)
async def get_example(interaction: discord.Interaction):
    # Getting the string for not saving a message
    no_saving = CONSTANTS["no_saving"]

    # Creating an embed with the example information
    text = "\nIf there's one mention:\n```This is an example of a citation.\n\n- @mention```\n\nIf there's more than one mention:\n```-I'm the first one to talk.\n-And me the second one\n-Don't forget me I'm the third\n\n- @mention1, @mention2, @mention3```"
    embed = discord.Embed(title="How to write a citation", description=text, color=discord.Color.blue())
    embed.add_field(name="", value="")
    embed.add_field(name="Never", value="You should never mention anyone in the text, only in the end of the message.", inline=False)
    embed.add_field(name="", value="")
    embed.set_footer(text=f"To not save a message, start the message with {no_saving}. You have to put it in a code block!")

    # Sending the embed as a response to the interaction
    await interaction.response.send_message(embed=embed)


@client.tree.command(name="help", description="Getting help", guild=GUILD_ID)
async def help_command(interaction: discord.Interaction):
    # Getting the string for not saving a message
    no_saving = CONSTANTS["no_saving"]

    # Creating an embed with the help information
    embed = discord.Embed(title="Help", description="Here are the commands you can use:", color=discord.Color.blue())
    embed.add_field(name="How not to save a message?", value=f"To not save a message, start the message with {no_saving}. You have to put it in a code block!", inline=False)

    for command in CONSTANTS["all_commands"]:
        command_name = command["name"]
        embed.add_field(name="", value="")
        embed.add_field(name=f"`/{command_name}`", value=command["description"], inline=False)

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