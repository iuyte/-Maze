import discord
import asyncio
import re
from tools import Maze

client = discord.Client()

DISCORD_TOKEN = open('../discord_tokens.txt', 'r').read()

counts = ["kek", "lol", "rekt"]
maze = Maze("&", counts)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    maze.countP(message.content)
    if message.content.startswith(maze.prefix):
        cont = message.content.split(maze.prefix)[1].split(" ")
        command = cont[0]
        args = cont[1:len(cont)]
        response =  maze.respond(command, args)
        await client.send_message(message.channel, response)

client.run(DISCORD_TOKEN)
