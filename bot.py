import discord
from discord.ext import commands
from discord.ext.commands import Bot
from random import choice
import datetime
import os
import random
import asyncio
PREFIX = '.'
client = commands.Bot(command_prefix = PREFIX)
client.remove_command('help')


#clear
@client.command(pass_context = True)

async def clear( ctx, amount = 10000):        
    await ctx.channel.purge(limit = amount)
    

#Kick
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def kick( ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge (limit = 1)

    await member.kick(reason = reason)
    await ctx.send( f'kick user {member.mention}' )

#Ban
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def ban(ctx, member: discord.Member, *, reason= None):
    await ctx.channel.purge(limit = 1)

    await member.ban(reason=reason)
    await ctx.send(f'ban user{member.mention}')

@client.command()
@commands.has_permissions( administrator = True) 
async def send(ctx, member: discord.Member = None, *, arg): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif arg is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: сообщение!**'))

    else:
        
        await member.send(embed = discord.Embed(description = f'{arg}', color=0x0c0c0c))

@client.command(pass_context = True)
@commands.has_permissions(administrator = True)

#help
async def help(ctx):
    await ctx.channel.purge(limit = 1)

    emb = discord.Embed(title = 'Навигация по командам')

    emb.add_field(name = '{}clear'.format(PREFIX), value = 'Очистка чата' )
    emb.add_field(name = '{}kick'.format(PREFIX), value = 'Удаление участника с сервера' )
    emb.add_field(name = '{}ban'.format(PREFIX), value = 'Ограничение доступа к серверу' )
    emb.add_field(name = '{}time'.format(PREFIX), value = 'Показывает время' )
    emb.add_field(name = '{}inv'.format(PREFIX), value = 'Создаёт приглашение на сервер' )
    
    await ctx.send(embed = emb)

#time
@client.command()
async def time(ctx):
    emb = discord.Embed(colour= discord.Color.green(), url= 'https://www.timeserver.ru')
    
    emb.set_author(name= client.user.name, icon_url=client.user.avatar_url)
    emb.set_footer(text= 'Если у вас время по МСК, то к этому добавляйте +1 час', icon_url=ctx.author.avatar_url)
    emb.set_thumbnail(url='https://www.worldtimeserver.com/img/dst/dst-2-3.png')

    now_date = datetime.datetime.now()
    emb.add_field(name='Time', value='{}'.format(now_date))

    await ctx.send( embed = emb )
 
@client.command()
async def inv(ctx):
    channel = client.get_channel(532486664363442180) #id канала, который увидит приглашённый пользователь впервые при входе на сервер
    log = client.get_channel(693181465336217680) #id канала с логами приглашений
    await ctx.message.delete()
    invitelink = await channel.create_invite(max_uses=1, max_age=21600, unique=True) #Настраиваем само приглашение - количество использований и длительность действия. Именно тут - одно использование и 6 часов. Подроблее: API Ref.
    await ctx.author.send(f'Вы запросили ссылку-приглашение на сервер. Здорово! Теперь отправь eё другу:\n{invitelink}') #приглашение в ЛС пользователю
    emb = discord.Embed(title= 'Создано приглашение на сервер', color=discord.Color.orange())
    emb.add_field(name= 'Приглашение создано участником:', value = ctx.author.mention)
    await log.send(embed=emb) #отправка лога.
    
@client.command()
@commands.has_permissions( administrator = True)
async def say(ctx, *, arg):

    await ctx.message.delete()
    await ctx.send(embed = discord.Embed(description = f'{arg}', color=0x0c0c0c))
    
@client.command()
@commands.has_permissions(administrator = True)
async def pidor(ctx, arg: discord.Member):
    colors = (0xFF0000,0xFF7F00,0xFFFF00,0x00FF00,0x0000FF,0x4B0082,0x9400D3)
    role = discord.utils.get(ctx.guild.roles, id = '693209339158200452')
    await arg.add_roles(role)
    emb1 = discord.Embed(description=f"Теперь ты пидор, {arg.mention}", colour= 0xffffff)
    emb1.set_thumbnail(url= arg.avatar_url)
    emb1.set_footer(text= f'Вызвал: {ctx.author}', icon_url= ctx.author.avatar_url)
    await ctx.send(embed = emb1)
    while True:
        await asyncio.sleep(2)
        col = random.choice(colors)
        role = discord.utils.get(ctx.guild.roles, id = '693209339158200452')
        await role.edit(colour = discord.Colour(col))

 while True:
    moves = ['Камень','Ножницы','Бумага']
    a = input("Выбери ход Камень, Ножницы или Бумага: ")
    b = random.choice(moves)

    if (a == "Бумага") and (b == "Ножницы"):
        print("Бот победил!")
    
    if (a == "Ножницы") and (b == "Бумага"):
        print("Ты победил!")

    if (a == "Бумагаь") and (b == "Камень"):
        print("Ты победил!")
    
    if (a == "Камень") and (b == "Бумага"):
        print("Бот победил!")
    
    if (a == "Камень") and (b == "Ножницы"):
        print("Ты победил!")
    
    if (a == "Ножницы") and (b == "Камень"):
        print("Бот победил!")
    
    if (a == "Бумага") and (b == "Бумага"):
        print("Ничья!")
    
    if (a == "Ножницы") and (b == "Ножницы"):
        print("Ничья!")

    if (a == "Камень") and (b == "Камень"):
        print("Ничья!")
       
       
 
#Connect
token = os.environ.get('BOT_TOKEN')

client.run(token)
