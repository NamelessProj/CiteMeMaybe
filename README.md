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

MONGO_URI=mongodb+srv://<username>:<password>@cluster0.3xq4j.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=your_database_name
```
The `BOT_TOKEN` will be used to connect the bot to your server.

The `GUILD_ID` will be used to get the server where the bot is connected and to get the channel where the citations are.

The `CHANNEL_ID` will be used to gather the citations from the channel and save them in the database.

The `MONGO_URI` will be used to connect to your mongoDB database.

The `MONGO_DB_NAME` will be used to get the database name where the citations will be saved.

## How to run the bot
1. Clone the repository
```bash
git clone https://github.com/NamelessProj/CiteMeMaybe.git
```
2. Create a virtual environment
```bash
python -m venv venv
```
3. Activate the virtual environment
```bash
# Windows
venv\Scripts\activate
# Linux
source venv/bin/activate
```
4. Install the dependencies
```bash
pip install -r requirements.txt
```

## Automations
Every time a message is sent in the channel, the bot will check if the message is a citation and if it is, it will save it in the database.

When a message is deleted, the bot will check if the message is a citation and if it is, it will delete it from the database.

When a message is edited, the bot will check if the message is a citation and if it is, it will update it in the database.

## How to prevent messages from being saved
Before sending a message in the channel, add at the beginning of the message `no-saving`. It has to be in a code block.

## Commands
### `/help`
This command will give you a list of all the commands available.

### `/setup_server`
__This command is only available to the administrators.__

This command will set up the server and the channel where it'll find the citations.

### `/update_database`
__This command is only available to the administrators.__

This command will update the database with the citations from the channel.

### `/get_random_citation`
This command let you get a random citation from the database or from a specific user.
#### Parameters:
- `user`: _optional_

### `/get_a_citation`
This command let you get a specific citation from the database using an id.
#### Parameters:
- `citation_id`: int

### `/how_many`
This command let you get the number of citations in the database or the number of citations from a specific user.
#### Parameters:
- `user`: _optional_