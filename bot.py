# -*- coding: utf-8 -*-
# Python program to solve JSONDecodeError: Expecting value: line 1 column 1 (char 0)
#подключение библиотек, модулей и функций
import discord
from discord import role, utils
from discord.ext import commands, tasks
from discord.utils import get
from asyncio import sleep
from random import randint, uniform
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from time import *
import json
import os
import requests
import io
import sys
import asyncio

print('Code successfully started.')
print('Bot starting now.')

allowed_mentions = discord.AllowedMentions(everyone = True)
with open('prefix.txt') as prefix:
    prefix_cr = str(prefix.read())
client = commands.Bot(command_prefix=prefix_cr, help_command=None, intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)  

moderation = [880424360400269394, 891413249801748510, 888356594251890708, 895782543553605662, 856608768090439710]

english_commands = ['8ball', 'prefix', 'ping', 'bot', 'clear', 'kick', 'ban', 'unban', 'new_year_congrats', 'random', 'help', 'mute', 'user', 'server', 'xp']
russian_comands = ['пинг', 'префикс', 'бот', 'чистка', 'кик', 'бан', 'разбан', 'пнг', 'рандом', 'хелп', 'мут', 'юзер', 'сервер']
other_commands = ['pref', 'преф', 'ранд', 'rand', 'bot-info', 'бот-инфо', 'мьют', 'скрыть', 'серв', 'serv', 'юз']

linf = {'8ball':None, 'ping':'пинг', 'prefix':'префикс, pref, преф', 'bot':'бот, bot-info, бот-инфо', 'clear':'чистка', 'kick':'кик', 'ban':'бан', 'unban':'разбан', 'new_year_congrats':'пнг', 'random':'рандом, rand, ранд', 'help':'хелп', 'mute':'мут, мьют, скрыть', 'user':'юзер, юз', 'server':'сервер, serv, серв', 'xp':None}
largs = {'8ball':'<вопрос>', 'ping':None, 'prefix':'<new_pref>', 'bot':None, 'clear':'<total>', 'kick':'<member>, <reason>', 'ban':'<member>, <reason>', 'unban':'<member>', 'new_year_congrats':None, 'random':'<type_>, <arg1>, <arg2>', 'help':'<команда>', 'mute':'<member>, <time_mute>, <reason>', 'user':'<user_m>, <background>', 'server':None, 'xp':'<member>, <type_do>, <amount>'}
lreq_args = {'8ball':'<вопрос>', 'ping':None, 'prefix':'<new_pref>', 'bot':None, 'clear':None, 'kick':'<member>', 'ban':'<member>', 'unban':'<member>', 'new_year_congrats':None, 'random':'<type_> (в некоторых случаях: <arg1>, <arg2>)', 'help':None, 'mute':'<member>', 'user':None, 'server':None, 'xp':'<member>, <type_do>, <amount>'}
largs_info = {'8ball':'<вопрос> - ваш вопрос волшебному шару', 'ping':None, 'prefix':'<new_pref> - новый префикс', 'bot':None, 'clear':'<total> - количество сообщений на чистку', 'kick':'<member> - участник на кик\n<reason> - причина кика', 'ban':'<member> - участник на бан\n<reason> - причина бана', 'unban':'<member> - участник на разбан', 'new_year_congrats':None, 'random':'<type_> - тип рандома (число, дробь, монетка, кость, гранник)\n<arg1> (обязателен, если <type_> = число, гранник или дробь) - 1-й аргумент\n<arg2> (обязателен, если <type_> = число или дробь) - 2-й аргумент', 'help':'<команда> - команда из списка команд', 'mute':'<member> - участник на скрытие\n<time_mute> - время скрытия в минутах\n<reason> - причина скрытия', 'user':'<user_m> - владелец карточки\n<backgroung> - фон карточки', 'server':None, 'xp':'<member> - участник, чьё xp измениться\n<type_do> - тип действия (a - добавить, r - удалить, s - установить)\n<amount> - на сколько изменить xp'}
ldo = {'8ball':'Отвечает на ваш вопрос', 'ping':'Узнаёт задержку бота в мс', 'prefix':'Изменяет префикс бота', 'bot':'Печатает информацию о <@888478321657139220>', 'clear':'Нет аргументов - очищает канал на 10 сообщений.\nЕсть аргумент <total> - очищает канал на указанное количество сообщений', 'kick':'Выгоняет участника с сервера', 'ban':'Банит участника на сервере', 'unban':'Разбанивает участника на сервере', 'new_year_congrats':'Поздравляет с новым годом', 'random':'Использует команду рандома, указанную в <type_>', 'help':'Нет аргументов - печатает список всех команд и их краткое описание.\nЕсть аргумент <command> - печатает полную информацию о конкретной команде', 'mute':'Мутит (мьютит) участника мааксимум на 3 суток', 'user':'Печатает карточку указанного участника или вас', 'server':'Печатает информацию о сервере', 'xp':'Добавляет, удаляет, устанавливает участнику xp'}
lcan_run = {'8ball':None, 'ping':None, 'prefix':'owner', 'bot':None, 'clear':'owner', 'kick':'owner', 'ban':'owner', 'unban':'owner', 'new_year_congrats':'owner', 'random':None, 'help':None, 'mute':'moder', 'user':None, 'server':None, 'xp':'owner'}

command_choices = []
for command in english_commands:
    choice = create_choice(name=command, value=command)
    command_choices.append(choice)

member_roles_vocabluary = {}
member_time_voc = {}
channel_mute = None
mute_message = None
mute_text = None

def to_dict(string: dict):
    return string

with open('mutes_time.txt') as time_memb:
    if time_memb != '':
        member_time_voc = time_memb.read()
        member_time_voc = to_dict(member_time_voc)

with open('mutes_roles.txt') as roles_memb:
    if roles_memb != '':
        member_roles_vocabluary = roles_memb.read()
        member_roles_vocabluary = to_dict(member_roles_vocabluary)

with open('bot_version.txt') as version_last:
    bot_version_last = int(version_last.read())
with open('bot_version.txt', 'w') as version_last:
    version_last.write(str(bot_version_last + 1))
    version_last.close()
bot_version = 'Alpha 1.3.' + str(bot_version_last) + '.'

def slash_context(string: SlashContext):
    return string
def discord_member(string: discord.Member):
    return string

async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}'] = 0

async def add_experience(users, user, exp):
    users[f'{user.id}'] += exp

@client.event
async def on_ready():
    global channel_mute
    channel_mute = client.get_channel(888561763182845962)
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.streaming, name='-help, -bot', url='https://www.twitch.tv/janone02'))
    print('Bot successfully started.')

@client.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)
    await update_data(users, member)
    with open('users.json', 'w') as f:
        json.dump(users, f)

@client.event
async def on_message(message):
    if message.author.bot == False:
        if message.content[0] != '-':
            if len(message.content) != 100:
                with open('users.json', 'r') as f:
                    users = json.load(f)
                await update_data(users, message.author)
                await add_experience(users, message.author, 5)
                with open('users.json', 'w') as f:
                    json.dump(users, f)
    await client.process_commands(message)

@tasks.loop(seconds=1)
async def is_time_over():
    for time in member_time_voc:
        print(time)

@slash.slash(name='help', description='Cписок команд сервера или подробная информация об 1 команде', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='command', description='Команда, о которой будет напечатана информация', required=False, option_type=3, choices=command_choices)])
@client.command(aliases=['help', 'хелп'])
async def help_(ctx, command=None):
    try:
        profile_picture = ctx.message.author.avatar_url
    except:
        command = slash_context(command)
    if command != None:
        if str(command) in english_commands or str(command) in russian_comands or str(command) in other_commands:
            if lcan_run[command] == None:
                can_now_info = True
            elif lcan_run[command] == 'moder':
                for role in ctx.author.roles:
                    if role.id in moderation:
                        can_now_info = True
                        break
                    else:
                        can_now_info = False
            elif lcan_run[command] == 'owner':
                for role in ctx.author.roles:
                    if role.id == 880424360400269394:
                        can_now_info = True
                        break
                    else:
                        can_now_info = False
            if can_now_info == True:
                if ldo[command] != '':
                    inf = linf[command]
                    args = largs[command]
                    req_args = lreq_args[command]
                    args_info = largs_info[command]
                    do = ldo[command]
                else:
                    embed_help = discord.Embed(title='Команда help\nИнформация о команде: не найдено', description='Команда найдена в базе данных команд, но информация о ней не найдена.\nОбычно это значит, что информацию об этой команде ещё не заполнили.', colour=0x0000ff)
                    await ctx.reply(embed=embed_help)
                    return
                embed_help = discord.Embed(title='Команда help\nИнформация о команде: ' + command, colour=0x0000ff)
                if largs[command] != None:
                    embed_help.add_field(name='Аргументы', value=args)
                if lreq_args[command] != None:
                    embed_help.add_field(name='Обязательные аргументы', value=req_args)
                if largs_info[command] != None:
                    embed_help.add_field(name='Информация об аргументах', value=args_info) 
                if linf[command] != None:
                    embed_help.add_field(name='Другие формы команды', value=inf)
                embed_help.add_field(name='Что делает', value=do)
            else:
                embed_help = discord.Embed(title='Команда help\nОшибка', description='Вы не имеете право на информацию об этой команде!', colour=0xff0000)
        else:
            embed_help = discord.Embed(title='Команда help\nОшибка', description='Команда не найдена!', colour=0xff0000)
    else:
        embed_help = discord.Embed(title='Команда help', colour=0x0000ff)
        embed_help.add_field(name='Общие команды', value='```1. help (хелп) <command> - список команд сервера или подробная информация об 1 команде.\n2. bot (бот, bot-info, bot_info) - узнать о боте.\n3. ping (пинг) - узнать пинг бота.\n4. 8ball <question>* - спросить волшебный шар вопрос.\n5. random (рандом, ранд, rand) <type_>* <1 аргумент> <2 аргумент> - рандомайзеры: монетка, многогранник, число, дробь...\n6. user (юзер) <user>* - отправка карточки пользователя\n7. server (сервер, serv, серв) - печатает информацию о сервере```\n* - обязательный аргумент.')
        member = ctx.author
        for role in member.roles:
            if role.id in moderation:
                embed_help.add_field(name='Модеративные команды', value='Если вы видите эту категорию, вы являетесь модератором или администратором.\n```1. mute (мут, мьют) <member>* <time_mute> <reason> - налог скрытия на указанного участника.```', inline=False)
    embed_help.set_footer(text='Все команды используются с префиксом ' + prefix_cr + '.')
    await ctx.reply(embed=embed_help)

@slash.slash(name='ping', description='Узнаёт задержку бота в мс', guild_ids=[847106317356630049, 934526675373420654], options=[])
@client.command(aliases=['пинг'])
async def ping(ctx):
    embed_ping = discord.Embed(title='Команда ping', description=f'Понг! Время полёта мячика {client.latency * 1000} мс.', colour=0x0000ff)
    await ctx.reply(embed=embed_ping)

@slash.slash(name='8ball', description='"Спрашивает" у волшебного шара вопрос', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='question', description='Вопрос, который будет задан', option_type=3, required=True)])
@client.command(aliases=['8ball'])
async def ball(ctx, *, question=None):
    if question != None:
        if len(question) <= 50:
            try:
                profile_picture = ctx.message.author.avatar_url
            except:
                question = slash_context(question)
            ball_answers = ['```"Предрешено".```', '```"Никаких сомнений".```', '```"Определённо да".```', '```"Можешь быть уверен в этом".```', '```"Бесспорно".```',
                            '```"Мне кажется — «да»".```', '```"Вероятнее всего".```', '```"Хорошие перспективы".```', '```"Знаки говорят — «да»".```', '```"Да".```',
                            '```"Пока не ясно, попробуй снова".```', '```"Спроси позже".```', '```"Лучше не рассказывать".```', '```"Сейчас нельзя предсказать".```', '```"Сконцентрируйся и спроси опять".```',
                            '```"Даже не думай".```', '```"Мои ответ — «нет»".```', '```"По моим данным — «нет»".```', '```"Весьма сомнительно".```', '```"Перспективы не очень хорошие".```']
            random_num = randint(0, 19)
            word_from_ball = ball_answers[random_num]
            ball_text = 'Вы задали вопрос: "' + question + '".\n'
            if random_num >= 0 and random_num <= 4:
                ball_text = ball_text + 'Шар **утвердительно** ответил: ' + word_from_ball
            elif random_num >= 5 and random_num <= 9:
                ball_text = ball_text + 'Шар **нерешительно** ответил: ' + word_from_ball
            elif random_num >= 10 and random_num <= 14:
                ball_text = ball_text + 'Шар **нейтрально** ответил: ' + word_from_ball
            elif random_num >= 15 and random_num <= 19:
                ball_text = ball_text + 'Шар **отрицательно** ответил: ' + word_from_ball
            color = 0x0000ff
            title = 'Команда 8ball'
        else:
            ball_text = 'Ваш вопрос не должен содержать больше 50 символов!' 
            await ctx.channel.purge(limit=1)
            color = 0xff0000
            title = 'Команда 8ball\nОшибка'
    elif question == None:
        ball_text = 'Вы не задали вопрос!'
        color = 0xff0000
        title = 'Команда 8ball\nОшибка'
    embed_8ball = discord.Embed(title=title, description=ball_text, colour=color)
    if ball_text != 'Ваш вопрос не должен содержать больше 50 символов!':
        await ctx.reply(embed=embed_8ball)
    else:
        await ctx.send(embed=embed_8ball)

@slash.slash(name='random', description='Рандомайзер разных типов', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='type_', description='Тип рандомайзера', option_type=3, required=True, choices=[create_choice(name='Число', value='number'), create_choice(name='Дробь', value='float'), create_choice(name='Гранник', value='hedron'), create_choice(name='Монетка', value='coin'), create_choice(name='Игральный кубик', value='dice')]), create_option(name='arg1', description='1 аргумент (обязателен при <type_> = Число, Дробь или Гранник)', option_type=3, required=False), create_option(name='arg2', description='2 аргумент (обязателен при <type_> = Число или Дробь)', option_type=3, required=False)])
@client.command(aliases=['rand', 'ранд', 'рандом'])
async def random(ctx, type_=None, arg1=None, arg2=None):
    if type_ != None:
        try:
            profile_picture = ctx.message.author.avatar_url
        except:
            type_ = slash_context(type_)
            if arg1 != None:
                arg1 = slash_context(arg1)
            if arg2 != None:
                arg2 = slash_context(arg2)
        if type_ == 'число' or type_ == 'number' or type_ == 'num':
            if arg1 != None and arg2 != None:
                if arg1.isdigit() == True and arg2.isdigit() == True:
                    num = randint(int(arg1), int(arg2))
                    random_text = 'Вам выпало число ```' + str(num) + '```'
                    color = 0x0000ff
                    title = 'Команда random'
                else:
                    random_text = 'В аргументах могут быть только числа!'
                    color = 0xff0000
                    title = 'Команда random\nОшибка'
            else:
                random_text = 'Вы не указали обязательный(-ые) аргумент(-ы)!'
                color = 0xff0000
                title = 'Команда random\nОшибка'
        elif type_ == 'гранник' or type_ == 'hedron' or type_ == 'гран':
            if arg1 != None:
                if arg1.isdigit() == True:
                    num = randint(1, int(arg1))
                    arg1 = int(arg1)
                    if arg1 % 10 == 1:
                        message_coin = '(-ой) стороной '
                    elif arg1 % 10 == 2 or arg1 % 10 == 3 or arg1 % 10 == 4:
                        message_coin = '(-я) стороной '
                    else:
                        message_coin = '(-ю) сторонами '
                    random_text = 'Вы подкинули гранник с ' + str(arg1) + message_coin + 'и он показал число\n```' + str(num) + '```'
                    color = 0x0000ff
                    title = 'Команда random'
                else:
                    random_text = 'Вы должны указать количество граней числом!'
                    color = 0xff0000
                    title = 'Команда random\nОшибка'
            else:
                random_text = 'Вы не указали обязательный(-ые) аргумент(-ы)!'
                color = 0xff0000
                title = 'Команда random\nОшибка'
        elif type_ == 'coin' or type_ == 'монетка':
            num = randint(0, 100)
            if num >= 1 and num <= 50:
                coin = 'Решку'
            elif num >= 51 and num <= 100:
                coin = 'Орла'
            elif num == 0:
                coin = 'Ребро'
            random_text = 'Вы подкинули монетку и она приземлилась показав ```' + coin + '```'
            color = 0x0000ff
            title = 'Команда random'
        elif type_ == 'дробь' or type_ == 'float':
            if arg1 != None and arg2 != None:
                num = uniform(float(arg1), float(arg2))
                random_text = 'Вам выпала дробь ```' + str(num) + '```'
                color = 0x0000ff
                title = 'Команда random'
            else:
                random_text = 'Вы не указали обязательный(-ые) аргумент(-ы)!'
                color = 0xff0000
                title = 'Команда random\nОшибка'
        elif type_ == 'кость' or type_ == 'dice':
            if arg1 == None:
                arg1 = 1
            if str(arg1).isdigit() == True:
                arg1 = int(arg1)
                if arg1 >= 1 and arg1 <= 10:
                    if arg1 % 10 == 1:
                        total_dice = ' игральную кость и получили на верхушке число'
                    elif arg1 % 10 == 2 or arg1 % 10 == 3 or arg1 % 10 == 4:
                        total_dice = ' игральные кости и получили на верхушках числа'
                    elif arg1 % 10 == 5 or arg1 % 10 == 6 or arg1 % 10 == 7 or arg1 % 10 == 8 or arg1 % 10 == 9 or arg1 % 10 == 0:
                        total_dice = ' игральных костей и получили на верхушках числа'
                    random_text = 'Вы подбросили ' + str(arg1) + total_dice
                    for i in range(arg1):
                        num = randint(1, 6)
                        if arg1 == 1:
                            random_text = random_text + '\n```' + str(num) + '```'
                            color = 0x0000ff
                            title = 'Команда random'
                        else:
                            if i == 0:
                                random_text = random_text + '\n```' + str(num)
                                color = 0x0000ff
                                title = 'Команда random'
                            elif i == arg1-1:
                                random_text = random_text + ', ' + str(num) + '```'
                                color = 0x0000ff
                                title = 'Команда random'
                            else:
                                random_text = random_text + ', ' + str(num)
                else:
                    random_text = 'Вы можете подбросить от 1 до 10 игральных костей!'
                    color = 0xff0000
                    title = 'Команда random\nОшибка'
            else:
                random_text = 'Укажите количество игральных костей числом!'
                color = 0xff0000
                title = 'Команда random\nОшибка'
    else:
        random_text = 'Вы не указали обязательный(-ые) аргумент(-ы)!'
        color = 0xff0000
        title = 'Команда random\nОшибка'
    embed_random = discord.Embed(title=title, description=random_text, colour=color)
    await ctx.reply(embed=embed_random)

@slash.slash(name='bot', description='Печатает информацию о боте', guild_ids=[847106317356630049, 934526675373420654], options=[])
@client.command(aliases=['bot-info', 'бот', 'бот-инфо'])
async def bot(ctx):
    global prefix
    embed_info = discord.Embed(title='Команда bot', description='Бот: JunFun Bot.\nЯзык программирования: python.\nИспользуемая библиотека: discord.py.\nПрефикс бота: ' + prefix_cr + '.\nАвтор и кодер бота: Janone#2404.\nДата выпуска первой версии: <t:1636322933>\nТекущая версия: ' + bot_version + '\nБот был сделан специально и исключительно для сервера JunFun, использование бота на других серверах запрещено!', colour = 0x0000ff)
    await ctx.reply(embed=embed_info)

@slash.slash(name='user', description='Печатает карточку вас или выбранного участника', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='user_m', description='Пользователь, чью карточку вы хотите видеть', option_type=6, required=False), create_option(name='background', description='Фон карточки', option_type=3, required=False, choices=[create_choice(name='Красный', value='r'), create_choice(name='Синий', value='b'), create_choice(name='Зелёный', value='g'), create_choice(name='Жёлтый', value='y'), create_choice(name='Фиолетовый', value='p'), create_choice(name='Абстракция 1', value='a1'), create_choice(name='Абстракция 2', value='a2'), create_choice(name='Кибергород 1', value='c1'), create_choice(name='Кибергород 2', value='c2'), create_choice(name='Кибергород 3', value='c3'), create_choice(name='Кибергород 4', value='c4'), create_choice(name='Космос 1', value='g1'), create_choice(name='Космос 2', value='g2'), create_choice(name='Космос 3', value='g3'), create_choice(name='Космос 4', value='g4'), create_choice(name='Стандартный', value='d')])])
@client.command(aliases=['юзер', 'юз'])
async def user(ctx, user_m: discord.Member=None, background='default'):
    try:
        profile_picture = ctx.message.author.avatar_url
    except:
        if background != None:
            background = slash_context(background)
        if user_m != None:
            user_m = slash_context(user_m)
    error = 0
    card_colors = {'g': 'green', 'b': 'blue', 'r': 'red', 'y': 'yellow', 'c1': 'cybercity1', 'c2': 'cybercity2', 'c3': 'cybercity3', 'c4': 'cybercity4', 'a1': 'abstraction1', 'a2': 'bstraction2', 'd': 'old', 'p': 'purple', 'g1':'galactic1', 'g2':'galactic2', 'g3':'galactic3', 'g4':'galactic4', 'default':'old'}
    if background in card_colors.keys():
        user_image = Image.open(f'card_backgrounds/profile_card_background_{card_colors[background]}.png')
    else:
        user_image = Image.open('card_backgrounds/profile_card_background_error.png')
        error = 1
    if error != 1: 
        if user_m == None:
            profile_picture = str(ctx.author.avatar_url)
            user_name = ctx.author.name
            user_tag = ctx.author.discriminator
            user_id = ctx.author.id
            user_m = ctx.author
        else:
            profile_picture = str(user_m.avatar_url)
            user_name = user_m.name
            user_tag = user_m.discriminator
            user_id = user_m.id
        response = requests.get(profile_picture, stream = True)
        response = Image.open(io.BytesIO(response.content))
        response = response.convert('RGBA')
        response = response.resize((400, 400), Image.ANTIALIAS)
        user_image.paste(response, (30, 30, 430, 430))
        idraw = ImageDraw.Draw(user_image)
        if user_m == None or user_m == ctx.author:
            user_tag = user_tag + '\n(Вы)'
        elif user_id == 888478321657139220:
            user_tag = user_tag + '\n(Я)'
        user_nickname_size = 0
        if len(str(user_name + '#' + user_tag)) <= 14.714285714285714:
            user_nickname_size = 70
        if len(str(user_name + '#' + user_tag)) >= 14.714285714285714 and len(str(user_name + '#' + user_tag)) < 18.42857142857143:
            user_nickname_size = 60
        if len(str(user_name + '#' + user_tag)) >= 18.42857142857143 and len(str(user_name + '#' + user_tag)) < 22.14285714285714:
            user_nickname_size = 50
        if len(str(user_name + '#' + user_tag)) >= 22.14285714285714 and len(str(user_name + '#' + user_tag)) < 25.85714285714286:
            user_nickname_size = 40
        if len(str(user_name + '#' + user_tag)) >= 25.85714285714286 and len(str(user_name + '#' + user_tag)) < 29.57142857142857:
            user_nickname_size = 30
        if len(str(user_name + '#' + user_tag)) >= 29.57142857142857 and len(str(user_name + '#' + user_tag)) < 33.28571428571428:
            user_nickname_size = 30
        if len(str(user_name + '#' + user_tag)) >= 33.28571428571428 and len(str(user_name + '#' + user_tag)) <= 37:
            user_nickname_size = 30
        if background == 'y':
            text_color = '#000000'
        else:
            text_color = '#ffffff'
        with open('users.json', 'r') as f:
            users = json.load(f)
        if user_m.bot == False:
            if users[str(user_id)] == None:
                progress = 463
            else:
                progress = 463 + (int(users[str(user_id)]) % 100) * 6.1
            idraw.rounded_rectangle(xy=(460, 300, 1076, 336), fill='gray', width=8, radius=15)
            if progress > 463 and progress <= 1073:
                idraw.rounded_rectangle(xy=(463, 303, progress, 333), fill='blue', width=8, radius=15)
            else:
                if progress != 463:
                    idraw.text((480, 304), f'Ошибка Ошибка Ошибка', font = ImageFont.truetype('arial.ttf', size=28), fill='#ffffff')
        card_headline = ImageFont.truetype('Leto Text Sans Defect.ttf', size=user_nickname_size)
        card_under = ImageFont.truetype('Leto Text Sans Defect.ttf', size=50)
        if user_m.bot == False:
            idraw.text((460, 250), f'100th: {users[str(user_id)]//100}', font=card_under, fill=text_color)
            idraw.text((980-30*len(str(users[str(user_id)])), 250), f'XP: {users[str(user_id)]}', font=card_under, fill=text_color)
        idraw.text((460, 75), f'{user_name}#{user_tag}', font=card_headline, fill=text_color)
        idraw.text((460, 400), f'ID: {user_id}', font=card_under, fill=text_color)
        user_image.save('user_card.png')
        user_embed_image = discord.File('user_card.png')
        embed_user = discord.Embed(title='Команда user', colour=0x0000ff)
        embed_user.set_image(url="attachment://user_card.png")
    else:
        user_image.save('user_card.png')
        user_embed_image = discord.File('user_card.png')
        embed_user = discord.Embed(title='Команда user\nОшибка', colour=0xff0000)
        embed_user.set_image(url="attachment://user_card.png")
    await ctx.reply(embed=embed_user, file=user_embed_image)

@slash.slash(name='server', description='Печатает информацию о сервере', guild_ids=[847106317356630049, 934526675373420654], options=[])
@client.command(aliases=['serv', 'сервер', 'серв'])
async def server(ctx):
    embed_server = discord.Embed(title='Команда server', description='Сервер: JunFun\nВладелец: Janone#2404\nКоличество участников: ' + str(ctx.guild.member_count) + '\nДата создания: <t:1622047084>', colour=0x0000ff)
    await ctx.reply(embed=embed_server)

@slash.slash(name='prefix', description='Меняет префикс сервера', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='new_pref', description='Новый префикс', option_type=3, required=True)])
@client.command(aliases=['pref', 'префикс', 'преф'])#----------------------------------------------только владелец
async def prefix(ctx, new_pref=None):
    for role in ctx.author.roles:
        if role.id == 880424360400269394:
            if new_pref != None:
                try:
                    profile_picture = ctx.message.author.avatar_url
                except:
                    new_pref = slash_context(new_pref)
                global prefix_cr
                global client
                print(client)
                with open('prefix.txt', 'w') as prefix:
                    prefix.write(new_pref)
                    prefix.close()
                embed_prefix = discord.Embed(title='Команда prefix', description='Префикс бота успешно изменён с **' + str(prefix_cr) + '** на **' + new_pref + '**.', colour=0x0000ff)
                prefix_cr = new_pref
                client = commands.Bot(command_prefix=prefix_cr, help_command=None, intents=discord.Intents.all())
            else:
                embed_prefix = discord.Embed(title='Команда prefix\nОшибка', description='Вы не указали новый префикс!', colour=0xff0000)
            break
        else:
            embed_prefix = discord.Embed(title='Команда prefix\nОшибка', description='Вы не имеете право на выполнение этой команды!', colour=0xff0000)
    await ctx.reply(embed=embed_prefix)

@client.command(aliases=['пнг'])#------------------------------------------------------------------только владелец
@commands.has_role(880424360400269394)
async def new_year_congrats(ctx):
    await ctx.channel.purge(limit=1)
    embed_new_year_congrats = discord.Embed(title='Поздравление с новым годом от JunFun', description='Ну что-же, наступил очередной 365 день года. А это значит, что сегодня 31 декабря (но иногда и 30), совсем скоро наступит **новый 2022 год**. Это также значит, что сегодня вечерком почти все сядут за стол со своими любимыми людьми и начнут кушать мандаринки, оливье и какую-нибудь ещё прикольную еду. Кто-то уже поставил ёлку, а кому-то было лень ставить. Кто-то красивенько нарядил, а кто-то оставил голую. В любом случае, большинство людей сядут за телевизоры и начнут слушать поздравление от своих президентов.\nНу а что я, я хочу поздравить вас с наступающим завтра в 00:00 **новым годом**. Пожелать всего наилучшего того, что вам там желают.\n***СПАСИБО ЗА ВСЁ ХОРОШЕЕ СДЕЛАННОЕ ВАМИ ЗА ГОД НА JUNFUN, УДАЧИ В НОВОМ ГОДУ!!!***', colour=0x0000ff)
    profile_picture = ctx.message.author.avatar_url
    embed_new_year_congrats.set_footer(text='Текст написал и вас поздравил ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(content='<@everyone>', embed=embed_new_year_congrats, allowed_mentions = allowed_mentions)

@client.command()
async def system(ctx):
    await ctx.send('Команда сейчас пуста.')

@slash.slash(name='clear', description='Чистит текстовый канал', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='total', description='Количество сообщений на чистку', option_type=4, required=False)])
@client.command(aliases=['чистка'])#---------------------------------------------------------------только владелец
async def clear(ctx, total=10):
    try:
        profile_picture = ctx.message.author.avatar_url
    except:
        if total != None:
            total = slash_context(total)
    for role in ctx.author.roles:
        if role.id == 880424360400269394:
            await ctx.channel.purge(limit=total+1)
            clear_text = 'Успешно было очищено несколько сообщений. Сообщение призывающее команду сюда не входит.'
            title = 'Команда clear'
            color = 0x0000ff
            break
        else:
            kick_text = 'Вы не имеете право на выполнение этой команды!'
            title = 'Команда ban\nОшибка'
            color = 0xff0000
    embed_clear = discord.Embed(title=title, description=clear_text, colour=color)
    await ctx.reply(embed=embed_clear)

@slash.slash(name='kick', description='Кикает участника', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='member', description='Участник на кик', option_type=6, required=True), create_option(name='reason', description='Причина кика', option_type=3, required=False)])
@client.command(aliases=['кик'])#------------------------------------------------------------------только владелец
async def kick(ctx, member:discord.Member=None, *, reason=None):
    for role in ctx.author.roles:
        if role.id == 880424360400269394:
            if member != None:
                try:
                    profile_picture = ctx.message.author.avatar_url
                except:
                    member = slash_context(member)
                    if reason != None:
                        reason = slash_context(reason)
                await member.kick(reason=reason)
                if reason != None:
                    kick_text = f'{member.mention} был успешно изгнан по причине: "' + reason + '".'
                else:
                    kick_text = f'{member.mention} был успешно изгнан без причины.'
                title = 'Команда kick'
                color = 0x0000ff
            else:
                kick_text = 'Не указан участник на кик!'
                title = 'Команда kick\nОшибка'
                color = 0xff0000
            break
        else:
            kick_text = 'Вы не имеете право на выполнение этой команды!'
            title = 'Команда ban\nОшибка'
            color = 0xff0000
    embed_kick = discord.Embed(title = title, description = kick_text, colour = color)
    await ctx.reply(embed=embed_kick)

@slash.slash(name='ban', description='Банит участника', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='member', description='Участник на бан', option_type=6, required=True), create_option(name='reason', description='Причина бана', option_type=3, required=False)])
@client.command(aliases=['бан'])#------------------------------------------------------------------только владелец
async def ban(ctx, member:discord.Member=None, *, reason=None):
    for role in ctx.author.roles:
        if role.id == 880424360400269394:
            if member != None:
                try:
                    profile_picture = ctx.message.author.avatar_url
                except:
                    member = slash_context(member)
                    if reason != None:
                        reason = slash_context(reason)
                await member.ban(reason=reason)
                if reason != None:
                    ban_text = f'{member.mention} был успешно забанен по причине: "' + reason + '".'
                else:
                    ban_text = f'{member.mention} был успешно забанен без причины.'
                title = 'Команда ban'
                color = 0x0000ff
            else:
                ban_text = 'Не указан участник на бан!'
                title = 'Команда ban\nОшибка'
                color = 0xff0000
            break
        else:
            ban_text = 'Вы не имеете право на выполнение этой команды!'
            title = 'Команда ban\nОшибка'
            color = 0xff0000
    embed_ban = discord.Embed(title = title, description = ban_text, colour = color)
    await ctx.reply(embed=embed_ban)

@slash.slash(name='unban', description='Разбанивает участника', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='member', description='Участник на разбан в формате nick#0000', option_type=3, required=True)])
@client.command(aliases=['разбан'])#---------------------------------------------------------------только владелец
async def unban(ctx, *, member=None):
    for role in ctx.author.roles:
        if role.id == 880424360400269394:
            if member != None:
                try:
                    profile_picture = ctx.message.author.avatar_url
                except:
                    member = slash_context(member)
                banned_users = await ctx.guild.bans()
                member_name, member_discriminator = member.split('#')
                for ban_entry in banned_users:
                    user = ban_entry.user
                    if (user.name, user.discriminator) == (member_name, member_discriminator):
                        await ctx.guild.unban(user)
                        unban_text = f'{user.mention} был успешно разбанен.'
                        title = 'Команда unban'
                        color = 0x0000ff
            else:
                unban_text = 'Вы не указали участника на разбан!'
                title = 'Команда unban\nОшибка'
                color = 0xff0000
            break
        else:
            unban_text = 'Вы не имеете право на выполнение этой команды!'
            title = 'Команда unban\nОшибка'
            color = 0xff0000
    embed_unban = discord.Embed(title = title, description = unban_text, colour = color)
    await ctx.reply(embed=embed_unban)

@slash.slash(name='xp', description='Добавляет, удаляет или устанавливает участнику xp', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='member', description='Участник, чьё xp измениться', option_type=6, required=True), create_option(name='type_do', description='Действие (добавить, удалить, установить)', option_type=3, required=True, choices=[create_choice(name='Добавить', value='a'), create_choice(name='Удалить', value='r'), create_choice(name='Установить', value='s')]), create_option(name='amount', description='Сколько xp добавить, удалить, установить', option_type=4, required=True)])
@client.command()#---------------------------------------------------------------только владелец
async def xp(ctx, member:discord.Member=None, type_do=None, amount=None):
    for role in ctx.author.roles:
        if role.id == 880424360400269394:
            if member != None:
                if type_do != None:
                    if amount != None:
                        if amount.isdigit() == True:
                            with open('users.json', 'r') as f:
                                users = json.load(f)
                            await update_data(users, member)
                            if type_do == 'a':
                                await add_experience(users, member, amount)
                                type_do_rus = 'добавлено участнику'
                            elif type_do == 's':
                                del users[str(member.id)]
                                users[str(member.id)] = amount
                                type_do_rus = 'установлено участнику'
                            elif type_do == 'r':
                                users[str(member.id)] -= amount
                                type_do_rus = 'удалено у участникуа'
                            else:
                                embed_xp = discord.Embed(title = 'Команда xp\nОшибка', description = 'Тип действия не найден!', colour = 0xff0000)
                                await ctx.reply(embed=embed_xp)
                                return
                            with open('users.json', 'w') as f:
                                json.dump(users, f)
                            embed_xp = discord.Embed(title = 'Команда xp', description = f'Успешно было {type_do_rus} {amount} xp.', colour = 0x0000ff)
                        else:
                            embed_xp = discord.Embed(title = 'Команда xp\nОшибка', description = 'Вы должны указать аргумент числом!', colour = 0xff0000)
                    else:
                        embed_xp = discord.Embed(title = 'Команда xp\nОшибка', description = 'Вы не указали обязательный(-ые) агрумент(-ы)!', colour = 0xff0000)
                else:
                    embed_xp = discord.Embed(title = 'Команда xp\nОшибка', description = 'Вы не указали обязательный(-ые) агрумент(-ы)!', colour = 0xff0000)
            else:
                embed_xp = discord.Embed(title = 'Команда xp\nОшибка', description = 'Вы не указали обязательный(-ые) агрумент(-ы)!', colour = 0xff0000)
            break
        else:
            embed_xp = discord.Embed(title = 'Команда xp\nОшибка', description = 'Вы не имеете право на выполнение этой команды!', colour = 0xff0000)
    await ctx.reply(embed=embed_xp)


@slash.slash(name='mute', description='Скрывает участника', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='member', description='Участник на скрытие', option_type=6, required=True), create_option(name='time_mute', description='Время мута', option_type=4, required=False), create_option(name='reason', description='Причина скрытия', option_type=3, required=False)])
@client.command(aliases=['мут', 'скрыть', 'мьют'])#------------------------------------------------только модеративные личности сервера
async def mute(ctx, member:discord.Member=None, time_mute=10, *, reason=None):#команда
    for role in ctx.message.author.roles:#перечисление ролей модератора
        if role.id in moderation:#если роль модеративная...
            if member != None:#если участник указан...
                time_mute = str(time_mute)
                if time_mute.isdigit() == True:
                    time_mute = int(time_mute)
                    if time_mute <= 4320:
                        end_of_mute = int(time()) + int((time_mute * 60))
                        member_time_voc[member] = end_of_mute                                                                                                                                                               
                        member_roles_vocabluary[member] = member.roles
                        member_roles_names = [roles_mute.name for roles_mute in member.roles]
                        with open('mutes_roles.txt', 'w') as roles_memb:
                            roles_memb.write(member_roles_vocabluary)
                        with open('mutes_time.txt', 'w') as time_memb:
                            time_memb.write(member_time_voc)
                        member_roles_text = 'Роли участника на момент скрытия:'
                        for i in range(len(member.roles)):
                            member_roles_text = member_roles_text + '\n' + str(i+1) + '. ' + member_roles_names[i]
                        mute_role = discord.utils.get(ctx.message.guild.roles, name="Скрытый")
                        await member.edit(roles=[mute_role])
                        if time_mute % 10 == 1:
                            time_mute_minutes = ' минуту**.\n'
                        if time_mute % 10 == 2 or time_mute % 10 == 3 or time_mute % 10 == 4:
                            time_mute_minutes = ' минуты**.\n'
                        else:
                            time_mute_minutes = ' минут**.\n'
                        if reason != None:
                            mute_text = member.mention + ' был успешно скрыт по причине **"' + reason + '"** на **' + str(time_mute) + time_mute_minutes + member_roles_text
                        else:
                            mute_text = member.mention + ' был успешно скрыт без причины на **' + str(time_mute) + time_mute_minutes + member_roles_text
                        title = 'Команда mute'
                        color = 0x0000ff
                        global channel_mute
                        channel = channel_mute
                        print(str(member_roles_vocabluary) + '\n' + str(member_time_voc))
                    else:
                        mute_text = 'Время скрытия не должно превышать 3 суток (4320 минут)!'
                        title = 'Команда mute\nОшибка'
                        color = 0xff0000
                        channel = ctx
                else:
                    mute_text = 'Время скрытия должно быть указано числом!'
                    title = 'Команда mute\nОшибка'
                    color = 0xff0000
                    channel = ctx
            else:
                mute_text = 'Вы не указали участника на скрытие!'
                title = 'Команда mute\nОшибка'
                color = 0xff0000
                channel = ctx
            break
        else:
            mute_text = 'Вы не имеете право на выполнение этой команды!'
            title = 'Команда mute\nОшибка'
            color = 0xff0000
            channel = ctx
    embed_mute = discord.Embed(title = title, description = mute_text, colour = color)
    profile_picture = ctx.message.author.avatar_url
    embed_mute.set_footer(text='Модератор ' + str(ctx.message.author), icon_url=profile_picture)
    mute_message = await channel.send(embed=embed_mute)
    if channel == channel_mute:
        embed_mute2 = discord.Embed(title = title, description = mute_text + '\nВ канал <#888561763182845962> написано сообщение.', colour = color)
        profile_picture = ctx.message.author.avatar_url
        embed_mute2.set_footer(text='Модератор ' + str(ctx.message.author), icon_url=profile_picture)
        await ctx.send(embed=embed_mute2)
        await sleep(time_mute * 60)
        await member.edit(roles=member_roles_vocabluary[member.nick])
        del member_roles_vocabluary[member.nick]
        embed_mute3 = discord.Embed(title = title, description = mute_text + '\n**Участник уже расскрыт.**', colour = color)
        await mute_message.edit(embed=embed_mute3)

client.run('ODg4NDc4MzIxNjU3MTM5MjIw.YUTR6w.PuOnMe2BZGnFvTek2aJPA7IkNH8')