import discord
from discord import role
from discord.ext import commands, tasks
from random import randint, uniform
from time import *
from itertools import cycle
import json
import os

prefix = '-'
client = commands.Bot(command_prefix = prefix, help_command=None)
'''os.chdir(r'C:\Users\Asus\Desktop\Дискорд Бот')'''
statuses = cycle(['-help - список комманд.', 'JunFun Bot сделан Janone2404', 'На языке Python', 'Специально для JunFun'])
token = 'ODg4NDc4MzIxNjU3MTM5MjIw.YUTR6w.PuOnMe2BZGnFvTek2aJPA7IkNH8'

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle)
    print('Bot protocol now working.')

'''@client.event
async def on_member_join(member):
    with open('users.json', 'r') as file:
        users = json.load(file)
        
    await update_data(users, member)

    with open('users.json', 'w') as file:
        json.dump(users, file)

@client.event
async def on_message(message):
    with open('users.json', 'r') as file:
        users = json.load(file)
    
    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)

    with open('users.json', 'w') as file:
        json.dump(users, file)

async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 0

async def add_experience(users, user, amount):
    users[user.id]['experience'] += amount

async def level_up(users, user, channel):
    experience = users[user.id]['experience']
    lvl1 = users[user.id]['level']
    lvl2 = int(experience ** (1/4))

    if lvl1 < lvl2:
        await client.send_message(channel, '{}, ты толко что **достиг уровня {}!!!**\n***Спасибо за твою активность на JuFun🎊!!!***'.format(user.mention, lvl2))
        users[user.id]['level'] = lvl2'''

@client.command(aliases=['help', 'хелп'])
async def help_(ctx):
    await ctx.send('Список доступных команд JunFun Bot:\n```1. info - узнать о боте.```\n```2. ping - узнать пинг бота.```\n```3. 8ball <вопрос> - спросить волшебный шар.```')

@client.command(aliases=['пинг'])
async def ping(ctx):
    await ctx.send(f'Pong! {client.latency * 1000} ms.')

@client.command(aliases=['8ball'])
async def ball(ctx, *, question):
    ball_answers = ['```"Предрешено".```', '```"Никаких сомнений".```', '```"Определённо да".```', '```"Можешь быть уверен в этом".```', '```"Бесспорно".```',
                    '```"Мне кажется — «да»".```', '```"Вероятнее всего".```', '```"Хорошие перспективы".```', '```"Знаки говорят — «да»".```', '```"Да".```',
                    '```"Пока не ясно, попробуй снова".```', '```"Спроси позже".```', '```"Лучше не рассказывать".```', '```"Сейчас нельзя предсказать".```', '```"Сконцентрируйся и спроси опять".```',
                    '```"Даже не думай".```', '```"Мои ответ — «нет»".```', '```"По моим данным — «нет»".```', '```"Весьма сомнительно".```', '```"Перспективы не очень хорошие".```']
    random_num = randint(0, 19)
    word_from_ball = ball_answers[random_num]
    try:
        question = str(question)
    except discord.ext.commands.errors.MissingRequiredArgument:
        await ctx.send('Задайте вопрос!')
    await ctx.send('Вопрос: ' + question)
    if random_num >= 0 and random_num <= 4:
        await ctx.send('Шар утвердительно говорит: ' + word_from_ball)
    elif random_num >= 5 and random_num <= 9:
        await ctx.send('Шар нерешительно говорит: ' + word_from_ball)
    elif random_num >= 10 and random_num <= 14:
        await ctx.send('Шар нейтрально говорит: ' + word_from_ball)
    elif random_num >= 15 and random_num <= 19:
        await ctx.send('Шар отрицательно говорит: ' + word_from_ball)

@client.command(aliases=['rand', 'ранд', 'рандом'])
async def random(ctx, type_, arg1, arg2):
    if type_ == 'число' or type_ == 'number' or type_ == 'num':
        num = randint(arg1, arg2)
        num = str(num)
        await ctx.send('Вам выпало число ```'+num+'```')
        
    

@client.command(aliases=['bot-info', 'info'])
async def bot_info(ctx):
    await ctx.send('Бот: "JunFun Bot".\nЯзык программирования: "python".\nИспользуемая библиотека: "discord.py".\nПрефикс бота: "' + prefix + '".\nАвтор и кодер бота: "Janone#2404".\nГод выпуска: "2021".\nБот был сделан специально и исключительно для сервера JunFun, использование бота на других серверах запрещено!')

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(statuses)))

@client.command()
@commands.has_role(880424360400269394)
async def clear(ctx, total=10):
    await ctx.channel.purge(limit=total+1)

@client.command()
@commands.has_role(880424360400269394)
async def kick(ctx, member:discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} был успешно изгнан по причине: "' + reason + '".')

@client.command()
@commands.has_role(880424360400269394)
async def ban(ctx, member:discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} был успешно забанен по причине: "' + reason + '".')

@client.command()
@commands.has_role(880424360400269394)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} был успешно разбанен.')

@client.command()
@commands.has_role(880424360400269394 or 856608768090439710 or 895782543553605662 or 888356594251890708 or 891413249801748510)
async def mute(ctx, member: discord.Member):
    getrole = discord.utils.get(ctx.guild.roles, id = 884014537525846096)
    await member.add_roles(getrole)

client.run(token)
