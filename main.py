import discord
import asyncio

client = discord.Client()

DISCORD_TOKEN = "MjkxNjU4Nzc0MTM2MDk0NzMy.C6ssDw.j14MlwY7IsQOiOud-77IPbaclF8"

prefix = "\\"

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith(prefix):
        cont = message.content.split(prefix)[1].split(" ")
        command = cont[0]
        args = cont[1:len(cont)]
        response =  "command: ```\n"+command+ "```\nargs: ```\n"
        for arg in range(len(args)):
            response += args[arg] + "\n"
        response += "```"
        await client.send_message(message.channel, response)

client.run(DISCORD_TOKEN)
