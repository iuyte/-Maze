import discord
import asyncio
import pickle
from subprocess import call as subpcall
from time import sleep
from game import *
from game import data as game
from datetime import datetime, timedelta

with open('../discord_token.txt', 'r') as discord_file:
    DISCORD_TOKEN = discord_file.read()[:-2]
print(DISCORD_TOKEN, end=';')

prefix = ";"
client = discord.Client()
game.load()

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
    content = message.content[1:]
    if message.content[0] == prefix:
        result = ""
        if content.startswith("reg ") and str(message.author.id) == "262949175765762050":
            content = content[4:]
            message.author.id = "999999999999999998"
            message.author.name = "reg"
        if content.startswith("attack "):
            newc = content[7:].split(" ")
            content = "attack(" + message.author.id + ", '" + newc[0] + "', '" + newc[2] + "')"
            result = eval(content)
        elif content.startswith("use "):
            newc = content[4:]
            userr = getUserById(message.author.id)
            content = "game.users['" + userr + "'].use('" + newc + "')"
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
        elif content.startswith("item "):
            newc = content[5:].split(" ")
            username = newc[0]
            key = newc[1]
            value = ""
            for i in range(2,len(newc)):
                value += " " + newc[i]
            final = "game.items" + "['" + username + "']." + key
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
        elif content.startswith("on") and str(message.author.id) == "262949175765762050":
            with open("data.txt", mode="w") as leddata:
                leddata.write("1")
            result = "Lights on."
        elif content.startswith("off") and str(message.author.id) == "262949175765762050":
            with open("data.txt", mode="w") as ledfdata:
                ledfdata.write("0")
            result = "Lights off."
        elif content.startswith("reboot") and str(message.author.id) == "262949175765762050":
            command = "sudo /sbin/reboot"
            subpcall(command, shell = True)
            result = "Rebooting..."
        elif str(message.author.id) == "262949175765762050":
            result = eval(content)
        elif "new" not in content:
            result = eval(content)
        else:
            result = "No"
        if result != None and result != "":
            yield from client.send_message(message.channel, result)
        if message.content.startswith(";reg ") and str(message.author.id) == "999999999999999998":
            message.author.id = "262949175765762050"
            message.author.name = "ethanialw"

client.run(DISCORD_TOKEN)

pause()
