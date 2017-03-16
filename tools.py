import discord
import asyncio
import time
from datetime import datetime

class Bot(object):
    prefix = ""
    counters = []
    client = None
    repost_deleted = None
    stop = "NO"
    lastID = ""

    def __init__(self,  prefix, counters, repost_deleted):
        self.prefix = prefix
        self.counters = counters
        self.client = discord.Client()
        self.repost_deleted = repost_deleted

    def ping(self, message, args):
        return "pong"

    def pong(self, message, args):
        return "ping"

    def yes(self, message):
        return True

    def countP(self, message):
        for i in range(len(self.counters)):
            key = self.counters[i]
            if message[0] != self.prefix:
                counted = message.count(key)
                writePath = 'db/' + key + '.pydb'
                prevFile = open(writePath, 'r')
                prevData = prevFile.read()
                prevFile.close()
                if prevData != '':
                    newData = int(prevData) + counted
                    if newData != prevData:
                        writeTo = open(writePath, 'w')
                        writeTo.write(str(newData))
                        writeTo.close()

    def count(self, message, args):
        readPath = 'db/' + args[0] + '.pydb'
        readFile = open(readPath, 'r')
        readData = readFile.read()
        readFile.close()
        if readData == '':
            return "That has not been recorded."
        else:
            if readData[-1] == "\n":
                readData = readData[0:-1]
            return "That has been recorded " + readData + " times."

    def say(self, message, args):
        response = ""
        for arg in range(len(args)):
            response += " " + args[arg]
        return response

    def repostDel(self, message):
        if self.repost_deleted:
            return message.author.name + " said " + message.content
        else:
            return ""

    def repost(self, message, args):
        if args[0] == "deleted":
            if self.repost_deleted:
                self.repost_deleted = False
                return "Reposting of deleted messages is now OFF"
            else:
                self.repost_deleted = True
                return "Reposting of deleted messages is now ON"
        else:
            return "Command not found.\nDid you mean: `&repost deleted`"

    def ex(self, message, args):
        s = ""
        for arg in range(len(args)):
            s += " " + args[arg]
        if s != "exit()":
            eval(s)
            return "Done."
        else:
            return "No."

    def getx(self, message, args):
        s = ""
        for arg in range(len(args)):
            s += " " + args[arg]
        if s != "exit()":
            return eval(s)
        else:
            return "No."

    def time(self, message, args):
         return str(datetime.now())

    def respond(self, message, command, args):
        response = ""
        try:
            response = eval("self." + command + "(message, args)")
        except AttributeError:
            response = "Please use a valid command."
        except IndexError:
            response = "Please use a valid argument."
        except TypeError:
            response = eval("self." + command)
        except SyntaxError:
            response = "Please use a valid command."
        return response