import discord
import asyncio
import calendar
import time
from tinydb import TinyDB, Query
from datetime import datetime, timedelta

class Bot(object):
    prefix = ""
    client = None
    repost_deleted = None
    stop = "NO"
    lastID = ""
    messageDB = None
    permsDB = None
    dqDB = None

    def __init__(self,  prefix, repost_deleted, messageDB, permsDB, dqDB):
        self.prefix = prefix
        self.client = discord.Client()
        self.repost_deleted = repost_deleted
        self.messageDB = TinyDB(messageDB)
        self.permsDB = TinyDB(permsDB)
        self.dqDB = TinyDB(dqDB)

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

    def ship(self, message, args):
        vowels = 0
        count = 0
        vowel2 = 0
        name1 = args[0]
        name2 = args[1]

        for character in name1:
            if character != name1[0]: count = count + 1
            if character in "aeiouAEIOU": vowels += 1
            if vowels == 2:
                vowel2 = count
                break

        shipPart1 = name1[0:vowel2 + 1]

        consonant = 0
        count = 0
        consonant2 = 0
        consonants = 0

        for consonant in name2:
            if consonant != name2[0]: count = count + 1
            if consonant not in "aeiouAEIOU":
                consonants += 1
            if consonants == 2:
                consonant2 = count
                break

        shipPart2 = name2[consonant2:len(name2)]
        return shipPart1 + shipPart2

    def count(self, message, args):
        key = args[0]
        for arg in range(1, len(args)):
            key += " " + args[arg]
        Message = Query()
        result = self.messageDB.search(Message["content"].search("[^\\&].*(" + key + ").*"))
        end = 0
        for i in range(len(result)):
            if result[i]["server"] == message.server.id:
                end += 1
        return end

    def find(self, message, args):
        key = args[1]
        for arg in range(2, len(args)):
            key += " " + args[arg]
        limit = 0
        try:
            limit = int(args[0])
        except TypeError:
            limit = 1
        Message = Query()
        result = self.messageDB.search(Message.content.search("[^\\&].*(" + key + ").*"))
        for i in range(len(result)):
            if result[i]["server"] == message.server.id:
                end += 1
        if len(result) > limit:
            result = result[1:(limit + 1)]
        while len(str(result)) >= 2000:
            result = result[0:-1]
        return str(result)

    def regex(self, message, args):
        key = args[0]
        for arg in range(1, len(args)):
            key += " " + args[arg]
        Message = Query()
        result = self.messageDB.search(Message.content.search(key))
        for i in range(len(result)):
            if result[i]["server"] != message.server.id:
                result[i].pop()
        return str(result)[:2000]

    def parseTime(self, time, length):
        return {
            'year' : time[0:3],
            'month' : time[5:6],
            'day' : time[8:9],
            'hour' : time[11:12],
            'minute' : time[14:15],
            'second' : time[17:18],
        }[length]

    def dq(self, userID, serverID, hours):
        endtime = (hours * 3600) + calendar.timegm(time.gmtime())
        print("food")
        self.dqDB.insert({'server' : serverID, 'user' : userID, 'ends' : str(endtime)})
        print("bard")

    def getdq(self, serverID):
        Key = Query
        result1 = self.dqDB.search(Key["server"] == serverID)
        print(result1)
        result2 = []
        for i in range(len(result1)):
            print(result2)
            if int(result1[i][ends]) >= calendar.timegm(time.gmtime()):
                result2.append(result1[i][user])
                print("foo")
        #self.dqDB.remove((int(Key["ends"]) >= calendar.timegm(time.gmtime()) and Key["server"] == serverID))
        return result2

    def help(self, message, args):
        return self.prefix + """ is the prefix for any commands in use with `;Maze`\n
                `help`  |  displays this message about usable commands\n
                `say <message>`  |  causes me to say the message\n
                `ping`  |  pong\n
                `pong`  |  ping\n
                `repost`  |  toggle reposting of deleted messages\n
                `ex <statement>`  |  execute a statement\n
                `getx <satatement>`  |  execute a statement and get the result\n
                `time`  |  get the current EST time\n
                `count <key>`  |  count the number of times the key has appeared in` ;Maze's` history\n
        """

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
