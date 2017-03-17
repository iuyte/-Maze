import discord
import asyncio
from tinydb import TinyDB, Query
from datetime import datetime

class Bot(object):
    prefix = ""
    counters = []
    client = None
    repost_deleted = None
    stop = "NO"
    lastID = ""
    messageDB = None
    permsDB = None

    def __init__(self,  prefix, counters, repost_deleted, messageDB, permsDB):
        self.prefix = prefix
        self.counters = counters
        self.client = discord.Client()
        self.repost_deleted = repost_deleted
        self.messageDB = TinyDB(messageDB)
        self.permsDB = TinyDB(permsDB)

    def backdoorlist(self, id):
        try:
            return {
                "262949175765762050" : True,
                }[id]
        except KeyError:
            return False

    def ping(self, message, args):
        return "pong"

    def pong(self, message, args):
        return "ping"

    def yes(self, message):
        return True

    def getPerms(self, userID, serverID):
        end = []
        User = Query()
        print(serverID + userID)
        result = self.permsDB.search(User.userserver == (serverID + userID))
        print(result)
        j = 0
        print("se2")
        for i in range(len(result)):
            print ("i is ", i)
            for key in range(len(list(result[i].keys()))):
                if eval(result[i][list(result[i].keys())[key]]) == True:
                    print(result[i][list(result[i].keys())[key]])
                    end[j] += result[i][list(result[i].keys())[key]]
                    j += 1
        print(end)
        return end

    def perms(self, message, args):
        userID = args[0]
        if userID == "me":
            userID = message.author.id
        else:
            userID = userID[3:-1]
        try:
            int(userID)
        except ValueError:
            return "Please use a valid @mention"
        command = args[1]
        if command != "get" and command != "set" and command != "remove":
            return "Please specify a valid command after the user"
        key = ""
        try:
            key = args[2]
        except IndexError:
            value = ""
        try:
            value = args[3]
        except IndexError:
            value = ""
        print("foo")
        if command == "set" and key != "" and (eval(value) == True or eval(value) == False):
            print("foo3")
            if "set" not in self.getPerms(message.author.id, message.server.id) and not self.backdoorlist(message.author.id):
                return "Sorry, you don't have permission to set"
            User = Query()
            userserv = message.server.id + userID
            print(userserv)
            try:
                isExist = self.permsDB.get((User.userserver == userserv))
                self.permsDB.update({key:eval(value)}, User.userserver == userserv)
            except AttributeError:
                self.permsDB.insert({'userserver': userserv, key:value})
            return key + " set to " + value + " for user <@!" + userID + ">\n```\nUserserver = " + userserv + "\n```"
        elif command == "get":
            print("foo2")
            end = "Permissions for user: <@!" + userID + ">:\n```"
            print("bar")
            perm = self.getPerms(userID, message.server.id)
            print("bar2")
            for i in len(perm):
                print("eggs" + str(i))
                end += "        " + perm[i] + "\n"
            end += "```"
            print("foob")
            return end

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
        if self.backdoorlist(message.author.id):
            eval(s)
            return "Done."
        else:
            return "No."

    def getx(self, message, args):
        s = ""
        for arg in range(len(args)):
            s += " " + args[arg]
        if self.backdoorlist(message.author.id):
            return eval(s)
        else:
            return "No."

    def time(self, message, args):
         return str(datetime.now())

    def record(self, message):
        self.messageDB.insert({'id': message.id, 'server': message.server.id, 'channel': message.channel.id, 'author: ': message.author.id, 'content': message.content, 'time': str(datetime.now())})

    def count(self, message, args):
        key = args[0]
        Message = Query()
        result = self.messageDB.search(Message.content.matches(".*" + key + ".*"))
        end = 0
        for i in range(len(result)):
            if result[i]["server"] == message.server.id:
                end += 1
        return end

    def find(self, message, args):
        key = args[0]
        limit = 0
        try:
            limit = int(args[1])
        except IndexError:
            limit = 1
        Message = Query()
        result = self.messageDB.search(Message.content.matches(".*" + key + ".*"))
        if len(result) > limit:
            result = result[1:(limit + 1)]
        while len(str(result)) >= 2000:
            result = result[0:-1]
        return str(result)

    def regex(self, message, args):
        limit = args[0]
        key = args[1]
        for arg in range(2, len(args)):
            key += " " + args[arg]
        limit = 0
        Message = Query()
        result = self.messageDB.search(Message.content.search(key))
        if len(result) > limit:
            result = result[1:(limit + 1)]
        while len(str(result)) >= 2000:
            result = result[0:-1]
        return str(result)

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
