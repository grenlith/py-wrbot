import srcomapi, srcomapi.datatypes as dt
import asynctwitch

api = srcomapi.SpeedrunCom()

twitch = asynctwitch.Bot(
    user = "username",
    oauth = "oauth:",
    channel = "channel",
    prefix = "!",
)

thegame = None
thecategory = None

@twitch.override
async def event_message(message):
    await parse_message(message, message)

async def parse_message(message, passto):
    if len(message.content) > 0:
        msg = message.content.split(' ')
        options = {
            '!game' : game,
            '!category' : category,
            '!wr' : wr
        }
        if msg[0] in options:
            await options[msg[0]](passto)

#get or set the current game
async def game(message):
    global thegame
    if len(message.content[6:]) > 0 and (message.author.mod or message.author.name == message.channel):
        thegame = await findGame(message.content[6:])
        await twitch.say(message.channel, "Game set to: " + thegame.name)
    else:
        if thegame != None:
            await twitch.say(message.channel, "Current game is: " + thegame.name)
        else:
            await twitch.say(message.channel, "No game is currently set.")

#get or set the current category
async def category(message):
    global thegame
    global thecategory
    if len(message.content[10:]) > 0 and (message.author.mod or message.author.name == message.channel):
        thecategory = await findCategory(thegame, message.content[10:])
        await twitch.say(message.channel, "Category set to: " + thecategory.name)
    else:
        if thecategory != None:
            await twitch.say(message.channel, "Current category is: " + thecategory.name)
        else:
            await twitch.say(message.channel, "No category is currently set.")

#display the current world record
async def wr(message):
    if thecategory != None:
        wr = await findWR(thecategory)
        await twitch.say(message.channel, "WR for " + thegame.name + ": " + thecategory.name + " is " + wr)
    else:
        await twitch.say(message.channel, "No game or category currently set.")

async def findGame(name):
    games = api.search(dt.Game, {"name": name})
    for game in games:
        if game.name.lower() == name.lower():
            print ("Found game: " + game.name)
            return game
    return {name: "Game not found"}

async def findCategory(game, name):
    categories = game.categories
    for category in categories:
        if category.name.lower() == name.lower():
            print("Found category: " + category.name)
            return category
    return {name: "Category not found"}

async def findWR(category):
    fullrun = category.records[0].runs[0]["run"]
    time = fullrun.times["primary"][2:].lower()
    player = fullrun.players[0].name
    return time + " by " + player

twitch.start()