# CiteMeMaybe
CiteMeMaybe is a Discord bot written in python that will gather all your citations from your citations channel and save them in a database.

You'll have to set up your mongoDB database as the project only doesn't give you one.

I used `Python 3.12.6`.

## .env
To be able to use this exemple bot, you'll need a `.env` file.
```env
BOT_TOKEN=Your_Bot_Token
GUILD_ID=Your_Server_Id
CHANNEL_ID=The_Id_Of_Your_Citation_Channel
```
The `BOT_TOKEN` will be used to connect the bot to your server.

The `GUILD_ID` will be used to get the server where the bot is connected and to get the channel where the citations are.

The `CHANNEL_ID` will be used to gather the citations from the channel and save them in the database.

## Dependencies
- discord.py
- python-dotenv

## Commands
### `/get_messages`
This command let you update the database with all the messages that might not have been saved.