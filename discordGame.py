import discord
import asyncio
import pickle
from game import *
from game import data as game
from tinydb import TinyDB, Query
from datetime import datetime, timedelta

with open('../discord_token.txt', 'r') as discord_file:
    DISCORD_TOKEN = discord_file.read()[:-1]
prefix = ";"
client = discord.Client()
db = TinyDB("db/messageDB.json")
game.load()

def record(message, form):
    db.insert({'type': form, 'id': message.id, 'server': message.server.id, 'channel': message.channel.id, 'author: ': message.author.id, 'content': message.content, 'time': str(datetime.now())})
    servername = message.server.name
    channelname = message.channel.name
    authorname = message.author.name
    print(servername.ljust(15) + " | " + channelname.ljust(15) + "  | " + authorname.ljust(10) + " | " + message.content)

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------\n')

@client.event
@asyncio.coroutine
def on_message(message):
    record(message, "create")
    content = message.content[1:]
    if message.content[0] == prefix:
        result = ""
        if content.startswith("attack "):
            newc = content[7:].split(" ")
            content = "attack(" + message.author.id + ", '" + newc[0] + "', '" + newc[2] + "')"
            result = eval(content)
        elif content.startswith("user "):
            newc = content[5:].split(" ")
            username = newc[0]
            key = newc[1]
            value = ""
            for i in range(2,len(newc)):
                value += " " + newc[i]
            final = "game.users" + "['" + username + "']." + key
            if value != "":
                final += "=" + value
                result = exec(final)
                if result == None or result == "":
                    result = eval(value)
            else:
                result = eval(final)
        elif content.startswith("inventory"):
            response = ""
            if len(content) > 9:
                result = game.users[content[10:]].inventory()
            else:
                result = game.users[getUserById(message.author.id)].inventory()
        else:
            result = eval(content)
        if result != None and result != "":
            yield from client.send_message(message.channel, result)

@client.event
@asyncio.coroutine
def on_message_delete(message):
    record(message, "delete")

@client.event
@asyncio.coroutine
def on_message_edit(message):
    record(message, "edit")

client.run(DISCORD_TOKEN)
