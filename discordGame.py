import discord
import asyncio
import pickle
from gpiozero import LED
from time import sleep
from game import *
from game import data as game
from datetime import datetime, timedelta
led = LED(17)

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
        elif content.startswith("on"):
            led.on()
            result = "LED ON"
        elif content.startswith("off"):
            led.off()
            result = "LED OFF"
        elif content.startswith("blink"):
            led.blink()
            result = "LED BLINKING"
        else:
            result = eval(content)
        if result != None and result != "":
            yield from client.send_message(message.channel, result)

client.run(DISCORD_TOKEN)
