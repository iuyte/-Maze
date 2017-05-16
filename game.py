import pickle
import random

class GameData(object):
    def __init__(self):
        self.users = {}
        self.items = {}
        self.rooms = {}

    def save_object(self, obj, filename):
        with open(filename, 'wb') as output:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

    def save(self):
        self.save_object(self.users, "db/game/users.p")
        self.save_object(self.items, "db/game/items.p")
        self.save_object(self.rooms, "db/game/rooms.p")
        return "Game saved."

    def load(self):
        with open("db/game/users.p", "rb") as userfile:
            self.users = pickle.load(userfile)
        with open("db/game/items.p", "rb") as itemfile:
            self.items = pickle.load(itemfile)
        with open("db/game/rooms.p", "rb") as roomfile:
            self.rooms = pickle.load(roomfile)

data = GameData()

class Pos(object):
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

class Item(object):
    class Misc(object):
        def __init__(self, name, description):
            self.name = name
            self.description = description

    class Ability(object):
        def __init__(self, name, description, script):
            self.name = name
            self.description = description
            self.script = script

    class Weapon(object):
        def __init__(self, name, description, form, damage, accuracy):
            self.name = name
            self.description = description
            self.form = form
            self.damage = damage
            self.accuracy = accuracy

def item(key):
    return data.items[key]

def newItem(name, item):
    data.items[name] = item
    return "Item created."

def getItemByName(iname):
    for item in data.items:
        if str(data.items[item].name) == str(iname):
            return item
    return None

class User(object):
    uid = None
    items = None
    health = None
    attributes = None
    pos = None

    def __init__(self, uid):
        self.uid = uid
        self.items = []
        self.health = 100
        self.attributes = []
        self.pos = Pos()

    def add(self, item):
        self.items.append(data.items[item])
        return str(self) + " now has a/an " + item

    def move(self, direction):
        if direction == "f":
            self.pos.y += 1
        elif direction == "b":
            self.pos.y -= 1
        elif direction == "r":
            self.pos.x += 1
        elif direction == "l":
            self.pos.x -= 1
        else:
            return "Didn't move."
        return "Now at (" + str(self.pos.x) + ", " + str(self.pos.y) + ")"

    def inventory(self):
        if len(self.items) < 1:
            return "You have nothing"
        out = "You have the following:\n```\n"
        for i in range(len(self.items)):
            out += str(i + 1) + ") " + self.items[i].name + "\n"
        out += '```'
        return out

    def use(self, ability):
        ability = None
        where = 0
        for item in self.items:
            if item.name == ability0:
                ability = item
                break
            where += 1
        if ability == None:
            return "You don't have that item"
        exec(ability.script)
        self.items.pop(where)
        return "You used " + ability.name

def user(key):
    return data.users[key]

def newUser(name, uid):
    data.users[name] = User(uid)
    return "User created."

def getUserById(uid):
    for user in data.users:
        if str(data.users[user].uid) == str(uid):
            return user
    return None

def attack(attacker, attackee, weapon):
    attacker = getUserById(attacker)
    for item in data.users[attacker].items:
        if item.name == weapon:
            weapon = item
            break
    if type(weapon) is str:
        return "You do not have that weapon."
    acc = weapon.accuracy
    if acc == None:
        acc = 55
    dam = weapon.damage
    if dam == None:
        dam = 2.5
    if random.randint(1, 100) > int(acc):
        return "You missed!"
    try:
        data.users[attackee].health = float(data.users[attackee].health) - float(dam)
    except:
        data.users[attackee].health = data.users[attackee].health
    return attacker + " hit " + attackee + "!\n" + attackee + " health now at " + str(user(attackee).health)

class Room(object):
    def __init__(self, pos, contains=[]):
        self.contains = contains
        self.pos = Pos()

def newRoom(name, pos, contains=[]):
    data.rooms[name] = Room(pos, contains)
    return "Room created."

def getRoomByPos(pos):
    for room in data.rooms:
        if data.rooms[room].pos.x == pos.x and data.rooms[room].pos.y == pos.y:
            return rooms
    return None

def gimput():
    eval(input(">"))
