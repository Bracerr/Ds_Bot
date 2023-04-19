import discord
import datetime
import random
import os
from dotenv import load_dotenv
from discord.ext import commands


class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        emb = discord.Embed(title='Help', colour=discord.Colour.dark_red())
        admin_command = "**/listen** - Позволяет изменить статус сервера.\n" \
                    "**/global_text** - Позволяет вывести сообщение в глобальный чат.\n" \
                        "**/adminOnline** - Позволяет узнать колличество админов онлайн."
        player_command = "**/status** - Позволяет узнать текущий статус сервера.\n" \
                        "**/checkTime** - Позволяет узнать время на сервере.\n" \
                        "**/playersOnline** - Позволяет узнать колличество игроков на сервере."
        emb.add_field(name="Команды для админов :man_detective:", value=admin_command)
        emb.add_field(name='Команды для игроков :construction_worker:', value=player_command)
        await channel.send(embed=emb)


load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=os.getenv('PREFIX'), intents=intents, help_command=MyHelp())

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


async def Permission(ctx):
    emb = discord.Embed(title='Error', colour=discord.Colour.red())
    emb.add_field(name='', value='У вас нет прав на данную команду :rage:')
    await ctx.send(embed=emb)


@bot.command()
async def status(ctx):
    if not ServerData['status']:
        emb = discord.Embed(title="Статус сервера", colour=discord.Colour.red())
        emb.add_field(name='', value=f"{ServerData['status']} :low_battery:")
    else:
        emb = discord.Embed(title="Статус сервера", colour=discord.Colour.green())
        emb.add_field(name='', value=f"{ServerData['status']} :battery:")
    await ctx.send(embed=emb)


@bot.command()
async def checkTime(ctx):
    DataObj = f"{ServerData['time']['hours']}:{ServerData['time']['minutes']}:{ServerData['time']['seconds']}"
    emb = discord.Embed(title="Время на сервере :watch:", colour=discord.Colour.green())
    emb.add_field(name='', value=DataObj)
    await ctx.send(embed=emb)


# Это я реализую потом нормально, как работа с данными будет нормальная
@bot.command()
async def time(ctx, hours, minutes, seconds):
    ServerData['time']['hours'] = int(hours)
    ServerData['time']['minutes'] = int(minutes)
    ServerData['time']['seconds'] = int(seconds)


@bot.command()
async def playersOnline(ctx):
    emb = discord.Embed(title="Игроки онлайн :construction_worker:", colour=discord.Colour.green())
    emb.add_field(name='Игроков:', value=ServerData['online'])
    await ctx.send(embed=emb)


@bot.command()
async def adminOnline(ctx):
    if any(str(roll) == 'Admin' for roll in ctx.author.roles):
        emb = discord.Embed(title="Админы онлайн :man_detective:", colour=discord.Colour.green())
        emb.add_field(name='Админов:', value=ServerData['AdminOnline'])
        await ctx.send(embed=emb)
    else:
        await Permission(ctx)


@bot.command()
async def listen(ctx, *, message: str):
    emb_done = discord.Embed(title="Готово :white_check_mark:", colour=discord.Colour.green())
    if any(str(roll) == 'Admin' for roll in ctx.author.roles):
        if (message != "True") and (message != "False"):
            emb_error = discord.Embed(title="Error", colour=discord.Colour.red())
            emb_error.add_field(name='', value="Сообщение не соответсвует True/False")
            await ctx.send(embed=emb_error)
        elif message == str(ServerData['status']):
            await ctx.send(f"Server already {message}")
        elif message == "True":
            ServerData['status'] = True
            emb_done.add_field(name='', value=f"Статус сервера **{message}**")
            await ctx.send(embed=emb_done)
        elif message == "False":
            ServerData['status'] = False
            emb_done.add_field(name='', value=f"Статус сервера **{message}**")
            await ctx.send(embed=emb_done)
    else:
        await Permission(ctx)


@bot.command()
async def global_text(ctx, *, message: str):
    if any(str(roll) == 'Admin' for roll in ctx.author.roles):
        emb_done = discord.Embed(title="Готово :white_check_mark:", colour=discord.Colour.green())
        emb_done.add_field(name='', value=f"Сообщение **{message}** было отправлено в глобальный чат.")
        await ctx.send(embed=emb_done)
    else:
        await Permission(ctx)


bot.run(os.getenv('TOKEN'))

