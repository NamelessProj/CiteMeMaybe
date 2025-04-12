# CiteMeMaybe - 🎤 Save the legendary moments.
CiteMeMaybe automatically logs every message from a designated channel and stores it as a citation. Whether it’s hilarious, out of pocket, or pure gold—you’ll never lose a quote again.

* [CiteMeMaybe - 🎤 Save the legendary moments.](#citememaybe----save-the-legendary-moments)
  * [🛠️ Features](#-features)
  * [🤝 Perfect for](#-perfect-for)
  * [📊 .env](#-env)
  * [🤖 How to run the bot](#-how-to-run-the-bot)
  * [🚗 Automations](#-automations)
  * [❌ How to prevent messages from being saved](#-how-to-prevent-messages-from-being-saved)
  * [🎮 Commands](#-commands)
    * [`/example`](#example)
    * [`/help`](#help)
    * [`/setup_server`](#setup_server)
    * [`/update_database`](#update_database)
    * [`/random_citation`](#random_citation)
    * [`/get_a_citation`](#get_a_citation)
    * [`/how_many`](#how_many)
    * [`/how_many_written_by`](#how_many_written_by)

## 🛠️ Features
__Auto-log messages__ from a specified channel as citations.

__Random citation__ generator (from anyone or specific users).

__Stats commands__ – total citations, user-specific counts, and more.

__Citation lookup__ by ID, in case someone really wants to deny it.

## 🤝 Perfect for
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

PYTHON_ENV=dev

MONGO_URI=mongodb+srv://<username>:<password>@cluster0.3xq4j.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=your_database_name
```
The `BOT_TOKEN` will be used to connect the bot to your server.

The `GUILD_ID` will be used to get the server where the bot is connected and to get the channel where the citations are.

The `PYTHON_ENV` will be used to set the environment of the bot. It can be `dev` or `prod`. If you set it to `dev`, the bot will be only available for you. If you set it to `prod`, the bot will be available for everyone.

The `MONGO_URI` will be used to connect to your mongoDB database.

The `MONGO_DB_NAME` will be used to get the database name where the citations will be saved.

> [!note]
> ### How to get your Bot token ?
> To get your bot token, you'll need to go to the [Discord Developer Portal](https://discord.com/developers/applications).
> You'll have to create a `New Application` and in the `Bot` page, you'll have to:
> - Turn on `Presence Intent`
> - Turn on `Server Members Intent`
> - Turn on `Message Content Intent`
> - Check `Administartor` in the `Bot Permissions` that way the bot can do anything. _(Make sure to trust the code)_
> 
> Then on the `OAuth2` page, in the `OAuth2 URL Generator` part, check `bot`, copy the url and pasted it in your browser.
> 
> Once your bot on the server you wanted it to be, back on the `Discrod Developer Portal`, in the `Bot` page, you'll find a button `Reset Token`. Click on it and then your token will be displayed. __Make sure to save it, it'll be showed one time only__.

> [!note]
> ### How to get the ID of your Server ?
> On Discord, you'll have to go to your `user settings` and in the `Advanced` tab. In there, you'll have to turn on the `Developer Mode`.
>
> Then make a right click on the server you want the bot in and at the bottom of the context menu, you'll find the possibility to copy the ID of the server.

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
5. Create a `.env` file in the root of the project and add everything from the [`.env.exemple`](/.env.exemple) file. You can also check the [📊 .env](#-env) section for more information.
6. Run the bot
```bash
python main.py
```

Everytime you want to run the bot, you have to activate the virtual environment and run the bot _(step 3 and 6)_.

## 🚗 Automations
Every time a message is sent in the channel, the bot will check if the message is a citation and if it is, it will save it in the database.

When a message is deleted, the bot will check if the message is a citation and if it is, it will delete it from the database.

When a message is edited, the bot will check if the message is a citation and if it is, it will update it in the database.

## ❌ How to prevent messages from being saved
Before sending a message in the channel, add at the beginning of the message `no-saving`. It has to be in a code block.

## 🎮 Commands
### `/example`
This command give you an example of how to write a citation.

### `/help`
This command will give you a list of all the commands available.

### `/setup_server`
__This command is only available to the administrators.__

This command will set up the server and the channel where it'll find the citations.

### `/update_database`
__This command is only available to the administrators.__

This command will update the database with the citations from the channel.

### `/random_citation`
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

### `/how_many_written_by`
This command let you get the number of citations written by a specific user. By default, it will get the number of citations written by you.
#### Parameters:
- `user`: _optional_