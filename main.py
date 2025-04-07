import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object(id=os.getenv("GUILD_ID"))
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')

        except Exception as e:
            print(f'Error syncing commands: {e}')

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=os.getenv("GUILD_ID"))

@client.tree.command(name="get_messages", description="Getting all messages", guild=GUILD_ID)
async def get_messages(interaction: discord.Interaction):
    channel = discord.utils.get(interaction.guild.channels, name=os.getenv("CHANNEL_NAME"))
    if channel is None:
        await interaction.message.channel.send('Channel not found')
        return

    msgs = [message async for message in channel.history(limit=1000)]
    for message in msgs:
        print(f'${message.author.name}: {message.content}')

    await interaction.message.channel.send('All messages found')

client.run(os.getenv('BOT_TOKEN'))