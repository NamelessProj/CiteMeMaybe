# CiteMeMaybe - 🎤 Save the legendary moments.
CiteMeMaybe automatically logs every message from a designated channel and stores it as a citation. Whether it’s hilarious, out of pocket, or pure gold—you’ll never lose a quote again.

## 🛠️ Features:
__Auto-log messages__ from a specified channel as citations.

__Random citation__ generator (from anyone or specific users).

__Stats commands__ – total citations, user-specific counts, and more.

__Citation lookup__ by ID, in case someone really wants to deny it.

## 🤝 Perfect for:
Friend groups who say way too much.

Servers that run on inside jokes.

Anyone who needs proof that “yes, you did say that.”

> 💬 __Save it. Quote it. Laugh at it later.__
> 
> 📚 __Powered by friendship and bad takes.__

## 📊 .env
To be able to use this exemple bot, you'll need a `.env` file.
```env
BOT_TOKEN=Your_Bot_Token
GUILD_ID=Your_Server_Id

MONGO_URI=mongodb+srv://<username>:<password>@cluster0.3xq4j.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=your_database_name
```
The `BOT_TOKEN` will be used to connect the bot to your server.

The `GUILD_ID` will be used to get the server where the bot is connected and to get the channel where the citations are.

The `MONGO_URI` will be used to connect to your mongoDB database.

The `MONGO_DB_NAME` will be used to get the database name where the citations will be saved.

## 🤖 How to run the bot
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

## 🚗 Automations
Every time a message is sent in the channel, the bot will check if the message is a citation and if it is, it will save it in the database.

When a message is deleted, the bot will check if the message is a citation and if it is, it will delete it from the database.

When a message is edited, the bot will check if the message is a citation and if it is, it will update it in the database.

## ❌ How to prevent messages from being saved
Before sending a message in the channel, add at the beginning of the message `no-saving`. It has to be in a code block.

## 🎮 Commands
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