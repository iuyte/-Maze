import discord
import asyncio
from command import Commands

client = discord.Client()

DISCORD_TOKEN = open('../discord_tokens.txt', 'r').read()

commands = Commands("&")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith(commands.prefix):
        cont = message.content.split(commands.prefix)[1].split(" ")
        command = cont[0]
        args = cont[1:len(cont)]
        response =  commands.respond(command, args)
        await client.send_message(message.channel, response)

client.run(DISCORD_TOKEN)
