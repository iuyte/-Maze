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
