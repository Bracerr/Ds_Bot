import discord
import datetime
import random
import json
from discord.ext import commands

config_file = open('config.json', 'r')
config = json.load(config_file)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

DataObj = datetime.datetime.now()

ServerData = {
    'status': False,
    'time': {
        'hours': DataObj.hour,
        'minutes': DataObj.minute,
        'seconds': DataObj.second
    },
    'online': random.randint(0, 100),
    'AdminOnline': random.randint(0, 5)
}


@bot.command()
async def status(ctx):
    await ctx.send(ServerData['status'])


@bot.command()
async def checkTime(ctx):
    DataObj = f"{ServerData['time']['hours']}:{ServerData['time']['minutes']}:{ServerData['time']['seconds']}"
    await ctx.send(DataObj)
#Это я реализую потом нормально, как работа с данными будет нормальная
@bot.command()
async def time(ctx, hours, minutes, seconds):
    ServerData['time']['hours'] = int(hours)
    ServerData['time']['minutes'] = int(minutes)
    ServerData['time']['seconds'] = int(seconds)


@bot.command()
async def playersOnline(ctx):
    await ctx.send(ServerData['online'])


@bot.command()
async def adminOnline(ctx):
    await ctx.send(ServerData['AdminOnline'])


@bot.command()
async def listen(ctx, *, message: str):
    if any(str(roll) == 'Admin' for roll in ctx.author.roles):
        if (message != "True") and (message != "False"):
            await ctx.send("Error")
        elif message == str(ServerData['status']):
            await ctx.send(f"Server already {message}")
        elif message == "True":
            ServerData['status'] = True
        elif message == "False":
            ServerData['status'] = False
    else:
        await ctx.send("You are not admin")


@bot.command()
async def global_text(ctx, *, message: str):
    if any(str(roll) == 'Admin' for roll in ctx.author.roles):
        await ctx.send(f"Сообщение {message} было отправлено в глобальный чат.")
    else:
        await ctx.send(f"У вас нет прав к данной команде.")



bot.run(config['token'])
