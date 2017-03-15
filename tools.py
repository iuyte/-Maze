class Maze(object):
    prefix = ""
    counters = []

    def __init__(self, prefix, counters):
        self.prefix = prefix
        self.counters = counters

    def ping(self, args):
        return "pong"

    def pong(self, args):
        return "ping"

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

    def count(self, args):
        readPath = 'db/' + args[0] + '.pydb'
        readFile = open(readPath, 'r')
        readData = readFile.read()
        readFile.close()
        if readData == '':
            return "That has not been recorded."
        else:
            return "That has been recorded " + readData + " times."

    def respond(self, command, args):
        response = ""
        try:
            response = eval("self." + command + "(args)")
        except AttributeError:
            response = "Please use a valid command."
        except IndexError:
            response = "Please use a valid argument."
        except TypeError:
            response = self.prefix
        except SyntaxError:
            response = "Please use a valid command."
        return response
