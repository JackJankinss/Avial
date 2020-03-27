import discord
from discord.ext import commands
from discord.ext.commands import Bot
import datetime
import os 
PREFIX = '.'
client = commands.Bot(command_prefix = PREFIX)
client.remove_command('help')
@client.event

async def on_ready():
    print('Ya rodilsya')

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
    emb.add_field(name = '{}kick'.format(PREFIX), value = 'удаление участника с сервера' )
    emb.add_field(name = '{}ban'.format(PREFIX), value = 'Ограничение доступа к серверу' )
    
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
#Connect
token = os.environ.get('BOT_TOKEN')

client.run(token)