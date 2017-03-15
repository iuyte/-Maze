import discord
import asyncio

client = discord.Client()

DISCORD_TOKEN = "MjkxNjU4Nzc0MTM2MDk0NzMy.C6ssDw.j14MlwY7IsQOiOud-77IPbaclF8"

class Commands(object):
    prefix = ""

    def __init__(self, prefix):
        self.prefix = prefix

    def ping(self, args):
        return "pong"

    def pong(self, args):
        return "ping"

    def respond(self, command, args):
        return eval("self." + command + "(args)")

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
