import discord
import asyncio
import calendar
import time
from tinydb import TinyDB, Query
from datetime import datetime
from tools import Bot

clent = discord.Client()
prefix = "&"

DISCORD_TOKEN = open('../discord_tokens.txt', 'r').read()

maze = Bot(prefix, False, "db/messageDB.json", "db/permsDB.json", "db/dq.json")

@maze.client.event
async def on_ready():
    print('Logged in as')
    print(maze.client.user.name)
    print(maze.client.user.id)
    print('------')

@maze.client.event
async def on_message(message):
    if not message.content.startswith(maze.prefix + "count"):
        maze.record(message)
    if message.author.id != "291658774136094732":
        if message.content.startswith(maze.prefix):
            cont = message.content.split(maze.prefix)[1].split(" ")
            command = cont[0]
            args = cont[1:len(cont)]
            if command == "delete":
                if args[0] != '':
                    await maze.client.purge_from(channel=message.channel, limit=int(args[0]), check = maze.yes)
                else:
                    await maze.client.send_message(message.channel, "Please specify a valid number of messages")

            elif command == "kick" and maze.backdoorlist(message.author.id):
                userID = args[0]
                try:
                    await maze.client.kick(message.server.get_member_named(userID))
                    await maze.client.send_message(message.channel, "Kicked.")
                except ValueError:
                    await maze.client.send_message(message.channel, "Please use a valid @mention.")

            elif command == "dq" and maze.backdoorlist(message.author.id):
                userID = args[0]
                try:
                    print(1)
                    userID = message.server.get_member_named(userID)
                    print(2)
                    time = int(args[1])
                    print(3)
                    maze.dq(userID, message.server.id, time)
                    print(4)
                    await maze.client.ban(userID, 0)
                    await maze.client.send_message(message.channel, "<@!" + userID + "> dqed.")
                except:
                    await maze.client.send_message(message.channel, "Please use valid arguments.")

            else:
                if command == "say":
                    await maze.client.delete_message(message)
                response =  maze.respond(message, command, args)
                await maze.client.send_message(message.channel, response)

@maze.client.event
async def on_message_delete(message):
    response = maze.repostDel(message)
    if maze.repost_deleted:
        await maze.client.send_message(message.channel, response)

maze.client.run(DISCORD_TOKEN)
