import discord
from discord.ext import commands
from discord.ext.commands import Bot
import datetime
import os 
PREFIX = '.'
client = commands.Bot(command_prefix = PREFIX)
client.remove_command('help')

@client.event
async def on_ready(*args):
    type = discord.ActivityType.listening
    activity = discord.Activity(name = "тебя", type = type)
    status = discord.Status.dnd
    await client.change_presence(activity = activity, status = status)

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


#Connect
token = os.environ.get('BOT_TOKEN')

client.run(token)
