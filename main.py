import discord
import asyncio
import time
from datetime import datetime
from tools import Bot

clent = discord.Client()

DISCORD_TOKEN = open('../discord_tokens.txt', 'r').read()

counts = ["kek", "lol", "rekt", "lel", "log"]
maze = Bot( "&", counts, False)

@maze.client.event
async def on_ready():
    print('Logged in as')
    print(maze.client.user.name)
    print(maze.client.user.id)
    print('------')

@maze.client.event
async def on_message(message):
    if message.author.id != "291658774136094732":
        maze.countP(message.content)
        if message.content.startswith(maze.prefix):
            cont = message.content.split(maze.prefix)[1].split(" ")
            command = cont[0]
            args = cont[1:len(cont)]
            if command != "delete":
                if command == "say":
                    await maze.client.delete_message(message)
                response =  maze.respond(message, command, args)
                await maze.client.send_message(message.channel, response)
            else:
                if args[0] != '':
                    await maze.client.purge_from(channel=message.channel, limit=int(args[0]), check = maze.yes)
                else:
                    await maze.client.send_message(message.channel, "Please specify a valid number of messages")

@maze.client.event
async def on_message_delete(message):
    response = maze.repostDel(message)
    if maze.repost_deleted:
        await maze.client.send_message(message.channel, response)

maze.client.run(DISCORD_TOKEN)
