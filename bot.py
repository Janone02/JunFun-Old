# -*- coding: utf-8 -*-
#подключение библиотек, модулей и функций
import discord
from discord import role, utils
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle
from asyncio import sleep
from random import randint, uniform
from PIL import Image, ImageFont, ImageDraw
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import time
import json
import os
import requests
import io
import sys
#подготовка переменных и функций
print('Code successfully started.')
print('Bot starting now.')

allowed_mentions = discord.AllowedMentions(everyone = True)
with open('prefix.txt') as prefix:
    prefix_cr = str(prefix.read())
client = commands.Bot(command_prefix=prefix_cr, help_command=None, intents=discord.Intents.all())
client1 = discord.Client()
slash = SlashCommand(client, sync_commands=True)  

moderation = [880424360400269394, 891413249801748510, 888356594251890708, 895782543553605662, 856608768090439710]

english_commands = ['8ball', 'prefix', 'ping', 'bot', 'clear', 'kick', 'ban', 'unban', 'new_year_congrats', 'random', 'help', 'mute', 'user', 'server', 'xp', 'avatar', 'gamble', 'system', 'poll', 'default']
russian_comands = ['пинг', 'префикс', 'бот', 'чистка', 'кик', 'бан', 'разбан', 'пнг', 'рандом', 'хелп', 'мут', 'юзер', 'сервер', 'аватар', 'азарт', 'опрос', 'стандарт']
other_commands = ['pref', 'преф', 'ранд', 'rand', 'bot-info', 'бот-инфо', 'мьют', 'скрыть', 'серв', 'serv', 'юз', 'ава']

linf = {'8ball':None, 'ping':'пинг', 'prefix':'префикс, pref, преф', 'bot':'бот, bot-info, бот-инфо', 'clear':'чистка', 'kick':'кик', 'ban':'бан', 'unban':'разбан', 'new_year_congrats':'пнг', 'random':'рандом, rand, ранд', 'help':'хелп', 'mute':'мут, мьют, скрыть', 'user':'юзер, юз', 'server':'сервер, serv, серв', 'xp':None, 'avatar':'аватар, ава', 'gamble':'азарт', 'system':None, 'poll':'опрос', 'default':'стандарт'}
largs = {'8ball':'<вопрос>', 'ping':None, 'prefix':'<new_pref>', 'bot':None, 'clear':'<total>', 'kick':'<member>, <reason>', 'ban':'<member>, <reason>', 'unban':'<member>', 'new_year_congrats':None, 'random':'<type_>, <arg1>, <arg2>', 'help':'<команда>', 'mute':'<member>, <time_mute>, <reason>', 'user':'<user_m>, <background>', 'server':None, 'xp':'<member>, <type_do>, <amount>', 'avatar':'<avatar_own>', 'gamble':'<type_>, <arg1>, <arg2>', 'system':None, 'poll':'<type_>, <question>, <variants>', 'default':'<background>'}
lreq_args = {'8ball':'<вопрос>', 'ping':None, 'prefix':'<new_pref>', 'bot':None, 'clear':None, 'kick':'<member>', 'ban':'<member>', 'unban':'<member>', 'new_year_congrats':None, 'random':'<type_> (в некоторых случаях: <arg1>, <arg2>)', 'help':None, 'mute':'<member>', 'user':None, 'server':None, 'xp':'<member>, <type_do>, <amount>', 'avatar':None, 'gamble':'<type_>, <arg1>, <arg2>', 'system':None, 'poll':'<type_>, <question>', 'default':'<background>'}
largs_info = {'8ball':'<вопрос> - ваш вопрос волшебному шару', 'ping':None, 'prefix':'<new_pref> - новый префикс', 'bot':None, 'clear':'<total> - количество сообщений на чистку', 'kick':'<member> - участник на кик\n<reason> - причина кика', 'ban':'<member> - участник на бан\n<reason> - причина бана', 'unban':'<member> - участник на разбан', 'new_year_congrats':None, 'random':'<type_> - тип рандома (число, дробь, монетка, кость, гранник)\n<arg1> (обязателен, если <type_> = число, гранник или дробь) - 1-й аргумент\n<arg2> (обязателен, если <type_> = число или дробь) - 2-й аргумент', 'help':'<команда> - команда из списка команд', 'mute':'<member> - участник на скрытие\n<time_mute> - время скрытия в минутах\n<reason> - причина скрытия', 'user':'<user_m> - владелец карточки\n<backgroung> - фон карточки', 'server':None, 'xp':'<member> - участник, чьё xp измениться\n<type_do> - тип действия (a - добавить, r - удалить, s - установить)\n<amount> - на сколько изменить xp', 'avatar':'<avatar_own> - владелец аватарки', 'gamble':'<type_> - тип азарта\n<arg1> - 1-й аргумент\n<arg2> - 2-й аргумент', 'system':None, 'poll':'<type_> - тип опроса\n<question> - вопрос\n<variants> - варианты ответа', 'default':'<background> - фон карточки'}
ldo = {'8ball':'Отвечает на ваш вопрос', 'ping':'Узнаёт задержку бота в мс', 'prefix':'Изменяет префикс бота', 'bot':'Печатает информацию о <@888478321657139220>', 'clear':'Нет аргументов - очищает канал на 10 сообщений.\nЕсть аргумент <total> - очищает канал на указанное количество сообщений', 'kick':'Выгоняет участника с сервера', 'ban':'Банит участника на сервере', 'unban':'Разбанивает участника на сервере', 'new_year_congrats':'Поздравляет с новым годом', 'random':'Использует команду рандома, указанную в <type_>', 'help':'Нет аргументов - печатает список всех команд и их краткое описание.\nЕсть аргумент <command> - печатает полную информацию о конкретной команде', 'mute':'Мутит (мьютит) участника максимум на 3 суток', 'user':'Печатает карточку указанного участника или вас', 'server':'Печатает информацию о сервере', 'xp':'Добавляет, удаляет, устанавливает участнику xp', 'avatar':'Печатает аватарку вас или указанного участника', 'gamble':'Азартные игры на xp', 'system':'Команда используется в целях тестирования функций этого бота. Обычно, она вызывает команду help, но иногда она печатает что-то другое', 'poll':'Создаёт опросы разных типов', 'default':'Устанавливает стандартный фон вашей карточки пользователя'}
lcan_run = {'8ball':None, 'ping':None, 'prefix':'owner', 'bot':None, 'clear':'owner', 'kick':'owner', 'ban':'owner', 'unban':'owner', 'new_year_congrats':'owner', 'random':None, 'help':None, 'mute':'moder', 'user':None, 'server':None, 'xp':'owner', 'avatar':None, 'gamble':None, 'system':None, 'poll':'owner', 'default':None}

command_choices = []
for command in english_commands:
    choice = create_choice(name=command, value=command)
    command_choices.append(choice)

guild = None
channel_mute = None
mute_message = None
mute_text = None
mute_role = None

with open('mutes.json') as mute:
    mutes = json.load(mute)

with open('bot_version.txt') as version_last:
    bot_version_last = int(version_last.read())
with open('bot_version.txt', 'w') as version_last:
    version_last.write(str(bot_version_last + 1))
    version_last.close()
bot_version = 'Release 1.3.'

def slash_context(string: SlashContext):
    return string
def discord_member(string: discord.Member):
    return string

async def update_data(users, user_):
    if not f'{user_.id}' in users:
        users[f'{user_.id}'] = 0

async def add_experience(users, user_, exp):
    users[f'{user_.id}'] += exp

async def unmute_time():
    while True:
        global mutes
        for member in mutes:
            cr_time = time.time()
            end_mute = float(mutes[member]['time']) - mutes[member]['minus_time']
            if cr_time >= end_mute:
                global guild
                global mute_role
                member_roles = mutes[member]['roles']
                member_u = discord.utils.get(guild.members, id=int(member))
                await member_u.remove_roles(mute_role)
                for role in member_roles:
                    if role != '@everyone':
                        role = discord.utils.get(guild.roles, name=role)
                        await member_u.add_roles(role)
                del mutes[member]
                with open('mutes.json', 'w') as mute:
                    json.dump(mutes, mute)
                await log_reg('Run command: unmute_time', 'Bot')
        await sleep(1)

async def log_reg(log_text, type_log):
    local_time_ = time.localtime()
    time_string = time.strftime("%m.%d.%Y / %H:%M:%S", local_time_)
    log_content = f'[{time_string}][{type_log}] {log_text}\n'
    with open('logs.txt', 'a') as file:
        file.write(log_content)

@client.event
async def on_ready():
    global channel_mute
    global guild
    global mute_role
    channel_mute = client.get_channel(888561763182845962)
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.streaming, name='-help | -bot', url='https://www.twitch.tv/janone02'))
    print('Bot successfully started.')
    guild = discord.utils.get(client.guilds, name="JunFun")
    mute_role = discord.utils.get(guild.roles, name="Скрытый")
    client1.loop.create_task(unmute_time())
    await log_reg('Bot succesfully started', 'Bot')

@client.event
async def on_member_join(member):
    if member.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)
        await update_data(users, member)
        with open('users.json', 'w') as f:
            json.dump(users, f)

@client.event
async def on_message(message):
    if message.author.bot == False:
        if message.content[0] != '-':
            if len(message.content) <= 100 and len(message.content) >= 2:
                is_plus = randint(0, 3)
                if is_plus >= 0:
                    with open('users.json', 'r') as f:
                        users = json.load(f)
                    await update_data(users, message.author)
                    xp_ = randint(5, 10)
                    await add_experience(users, message.author, int(xp_))
                    with open('users.json', 'w') as f:
                        json.dump(users, f)
    await client.process_commands(message)
#команды
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
        embed_help.add_field(name='Общие команды', value='```1. help (хелп) <command> - список команд сервера или подробная информация об 1 команде.\n2. bot (бот, bot-info, bot_info) - узнать о боте.\n3. ping (пинг) - узнать пинг бота.\n4. 8ball <question>* - спросить волшебный шар вопрос.\n5. random (рандом, ранд, rand) <type_>* <1 аргумент> <2 аргумент> - рандомайзеры: монетка, многогранник, число, дробь...\n6. user (юзер) <user_m> <background> - отправка карточки пользователя\n7. server (сервер, serv, серв) - печатает информацию о сервере\n8. avatar (аватар, ава) <member> - показывает аватарку вас или участника\n9. gamble (азарт) <type_>* <arg1>* <arg2>* - азартные игры\n10. default (стандарт) <background>* - устанавливает стандартный фон для вашей карточки пользователя```\n***** - обязательный аргумент')
        member = ctx.author
        for role in member.roles:
            if role.id in moderation:
                embed_help.add_field(name='Модеративные команды', value='Если вы видите эту категорию, вы являетесь модератором или администратором.\n```1. mute (мут, мьют) <member>* <time_mute> <reason> - налог скрытия на указанного участника.```\n***** - обязательный аргумент.', inline=False)
    embed_help.set_footer(text='help <command> - подробная информация о команде. Все команды используются с префиксом ' + prefix_cr + ' и /.')
    await ctx.reply(embed=embed_help)
    await log_reg('Run command: help', ctx.author.name)

@slash.slash(name='ping', description='Узнаёт задержку бота в мс', guild_ids=[847106317356630049, 934526675373420654], options=[])
@client.command(aliases=['пинг'])
async def ping(ctx):
    embed_ping = discord.Embed(title='Команда ping', description=f'Понг! Время полёта мячика {client.latency * 1000} мс.', colour=0x0000ff)
    await ctx.reply(embed=embed_ping)
    await log_reg('Run command: ping', ctx.author.name)

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
    await log_reg('Run command: 8ball', ctx.author.name)

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
                    embed_random = discord.Embed(description = f'Вам выпало число\n```{str(num)}```', color = 0x0000ff, title = 'Команда random')
                else:
                    embed_random = discord.Embed(description = 'В аргументах могут быть только числа!', color = 0xff0000, title = 'Команда random\nОшибка')
            else:
                embed_random = discord.Embed(description = 'Вы не указали обязательный(-ые) аргумент(-ы)!', color = 0xff0000, title = 'Команда random\nОшибка')
            await log_reg('Run command: random (number)', ctx.author.name)
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
                    embed_random = discord.Embed(description = f'Вы подкинули гранник с {str(arg1) + message_coin} и он показал число\n```{str(num)}```', color = 0x0000ff, title = 'Команда random')
                else:
                    embed_random = discord.Embed(description = 'Вы должны указать количество граней числом!', color = 0xff0000, title = 'Команда random\nОшибка')
            else:
                embed_random = discord.Embed(description = 'Вы не указали обязательный(-ые) аргумент(-ы)!', color = 0xff0000, title = 'Команда random\nОшибка')
            await log_reg('Run command: random (hedron)', ctx.author.name)
        elif type_ == 'coin' or type_ == 'монетка':
            num = randint(0, 2000)
            if num >= 1 and num <= 1000:
                coin = 'Решку'
                coin_name = 'Решка'
            elif num >= 1001 and num <= 2000:
                coin = 'Орла'
                coin_name = 'Орёл'
            elif num == 0:
                coin = 'Ребро'
                coin_name = 'Ребро' 
            if arg1 == None:
                embed_random = discord.Embed(description = f'Вы подкинули монетку и она приземлилась показав\n```{coin}```', title = 'Команда random', colour=0x0000ff)
            else:
                if arg1 == 'Решка' or arg1 == 'Орёл' or arg1 == 'Ребро':
                    if coin_name == arg1:
                        game_end = f'Вы выиграли'
                    else:
                        game_end = f'Вы проиграли'
                    embed_random = discord.Embed(color = 0x0000ff, title = 'Команда random')
                    embed_random.add_field(name='Ваши ставки:', value=f'```{arg1}```')
                    embed_random.add_field(name='Что выпало:', value=f'```{coin_name}```')
                    embed_random.add_field(name='Итог:', value=f'```{game_end}```')
                else:
                    embed_random = discord.Embed(description = 'Вы можете выбрать только "Орёл", "Решка" или "Ребро" в качестве ставки!', color = 0xff0000, title = 'Команда random\nОшибка')
            await log_reg('Run command: random (coin)', ctx.author.name)
        elif type_ == 'дробь' or type_ == 'float':
            if arg1 != None and arg2 != None:
                try:
                    num = uniform(float(arg1), float(arg2))
                    embed_random = discord.Embed(description = f'Вам выпала дробь ```{str(num)}```', title = 'Команда random', colour=0x0000ff)
                except:
                    embed_random = discord.Embed(description = 'В аргументах могут быть только числа и дроби!', color = 0xff0000, title = 'Команда random\nОшибка')
            else:
                embed_random = discord.Embed(description = 'Вы не указали обязательный(-ые) аргумент(-ы)!', color = 0xff0000, title = 'Команда random\nОшибка')
            await log_reg('Run command: random (float)', ctx.author.name)
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
                    random_text = f'Вы подбросили {str(arg1)}{total_dice}'
                    for i in range(arg1):
                        num = randint(1, 6)
                        if arg1 == 1:
                            random_text = random_text + '\n```' + str(num) + '```'
                            embed_random = discord.Embed(description = random_text, title = 'Команда random', colour=0x0000ff)
                        else:
                            if i == 0:
                                random_text = random_text + '\n```' + str(num)
                                embed_random = discord.Embed(description = random_text, title = 'Команда random', colour=0x0000ff)
                            elif i == arg1-1:
                                random_text = random_text + ', ' + str(num) + '```'
                                embed_random = discord.Embed(description = random_text, title = 'Команда random', colour=0x0000ff)
                            else:
                                random_text = random_text + ', ' + str(num)
                else:
                    embed_random = discord.Embed(description = 'Вы можете подбросить от 1 до 10 игральных костей!', colour = 0xff0000, title = 'Команда random\nОшибка')
            else:
                embed_random = discord.Embed(desription = 'Укажите количество игральных костей числом!', colour = 0xff0000, title = 'Команда random\nОшибка')
            await log_reg('Run command: random (dice)', ctx.author.name)
        else:
            embed_random = discord.Embed(description = 'Вы указали несуществующий тип рандома!', colour = 0xff0000, title = 'Команда random\nОшибка')
    else:
        embed_random = discord.Embed(description = 'Вы не указали обязательный(-ые) аргумент(-ы)!', colour = 0xff0000, title = 'Команда random\nОшибка')
        await log_reg('Run command: random', ctx.author.name)
    await ctx.reply(embed=embed_random)

@slash.slash(name='bot', description='Печатает информацию о боте', guild_ids=[847106317356630049, 934526675373420654], options=[])
@client.command(aliases=['bot-info', 'бот', 'бот-инфо'])
async def bot(ctx):
    global prefix
    embed_bot = discord.Embed(title='Команда bot', description='Бот: JunFun Bot.\nЯзык программирования: python.\nИспользуемая библиотека: discord.py.\nПрефикс бота: ' + prefix_cr + '.\nАвтор и кодер бота: Janone#2404.\nДата начала разработки и выпуска первой версии: <t:1636322933>\nДата регистрации: <t:1631900139>\nДата релиза: <t:1643574600>\nДата поставки на хостинг Heroku: <t:1644701087>\nТекущая версия: ' + bot_version + '\nБот был сделан специально и исключительно для сервера JunFun. Использование бота на других серверах запрещено без разрешения владельца проекта! Исходный код закрыт!', colour = 0x0000ff)
    embed_bot.set_footer(text='<@840232854066954271> (Janone©) | 2022 Все права защищены | JunFun Bot©')
    await ctx.reply(embed=embed_bot)
    await log_reg('Run command: bot', ctx.author.name)

@slash.slash(name='user', description='Печатает карточку вас или выбранного участника', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='user_m', description='Пользователь, чью карточку вы хотите видеть', option_type=6, required=False), create_option(name='background', description='Фон карточки', option_type=3, required=False, choices=[create_choice(name='Красный', value='r'), create_choice(name='Синий', value='b'), create_choice(name='Зелёный', value='g'), create_choice(name='Жёлтый', value='y'), create_choice(name='Фиолетовый', value='p'), create_choice(name='Абстракция 1', value='a1'), create_choice(name='Абстракция 2', value='a2'), create_choice(name='Кибергород 1', value='c1'), create_choice(name='Кибергород 2', value='c2'), create_choice(name='Кибергород 3', value='c3'), create_choice(name='Кибергород 4', value='c4'), create_choice(name='Космос 1', value='g1'), create_choice(name='Космос 2', value='g2'), create_choice(name='Космос 3', value='g3'), create_choice(name='Космос 4', value='g4'), create_choice(name='Стандартный', value='d')])])
@client.command(aliases=['юзер', 'юз'])
async def user(ctx, user_m: discord.Member=None, background=None):
    try:
        profile_picture = ctx.message.author.avatar_url
    except:
        if background != None:
            background = slash_context(background)
        if user_m != None:
            user_m = slash_context(user_m)
    error = 0
    card_colors = {'g': 'green', 'b': 'blue', 'r': 'red', 'y': 'yellow', 'c1': 'cybercity1', 'c2': 'cybercity2', 'c3': 'cybercity3', 'c4': 'cybercity4', 'a1': 'abstraction1', 'a2': 'bstraction2', 'd': 'old', 'p': 'purple', 'g1':'galactic1', 'g2':'galactic2', 'g3':'galactic3', 'g4':'galactic4', 'default':'old'}
    if background != None:
        if not background in card_colors:
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
        with open('users_backs.json') as needb:
            needback = json.load(needb)
        if background == None:
            if str(user_id) in needback:
                user_image = Image.open(f'card_backgrounds/profile_card_background_{needback[str(user_id)]}.png')
            else:
                user_image = Image.open('card_backgrounds/profile_card_background_old.png')
        else:
            if background in card_colors:
                user_image = Image.open(f'card_backgrounds/profile_card_background_{card_colors[background]}.png')
            else:
                user_image = Image.open(f'card_backgrounds/profile_card_background_error.png')
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
            try:
                user_xp = users[str(user_id)]
                progress = 463 + (int(user_xp) % 100) * 6.1
            except:
                progress = 463
                user_xp = 0
            idraw.rounded_rectangle(xy=(460, 300, 1076, 336), fill='gray', width=8, radius=15)
            if progress > 463 and progress <= 1073:
                idraw.rounded_rectangle(xy=(463, 303, progress, 333), fill='blue', width=8, radius=15)
            else:
                if progress != 463:
                    idraw.text((480, 304), f'Ошибка Ошибка Ошибка', font = ImageFont.truetype('arial.ttf', size=28), fill='#ffffff')
        card_headline = ImageFont.truetype('Leto Text Sans Defect.ttf', size=user_nickname_size)
        card_under = ImageFont.truetype('Leto Text Sans Defect.ttf', size=50)
        if user_m.bot == False:
            idraw.text((460, 250), f'100th: {user_xp//100}', font=card_under, fill=text_color)
            idraw.text((980-30*len(str(user_xp)), 250), f'XP: {user_xp}', font=card_under, fill=text_color)
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
    await log_reg('Run command: user', ctx.author.name)

@slash.slash(name='avatar', description='Печатает аватарку вас или выбранного участника', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='avatar_own', description='Пользователь, чью аватарку вы хотите видеть', option_type=6, required=False)])
@client.command(aliases=['ава', 'аватар'])
async def avatar(ctx, avatar_own: discord.Member=None):
    try:
        profile_picture = ctx.message.author.avatar_url
    except:
        if avatar_own != None:
            avatar_own = slash_context(avatar_own)
    if avatar_own == None:
        avatar_own = ctx.author
        ava = ctx.author.avatar_url
    else:
        ava = avatar_own.avatar_url
    embed_avatar = discord.Embed(title=f'Команда avatar\nПользователь: {avatar_own.name}', color=0x0000ff)
    embed_avatar.set_image(url=ava)
    await ctx.reply(embed=embed_avatar)
    await log_reg('Run command: avatar', ctx.author.name)

@slash.slash(name='server', description='Печатает информацию о сервере', guild_ids=[847106317356630049, 934526675373420654], options=[])
@client.command(aliases=['serv', 'сервер', 'серв'])
async def server(ctx):
    embed_server = discord.Embed(title='Команда server', description='Сервер: JunFun\nВладелец: Janone#2404\nКоличество участников: ' + str(ctx.guild.member_count) + '\nДата создания: <t:1622047084>', colour=0x0000ff)
    await ctx.reply(embed=embed_server)
    await log_reg('Run command: server', ctx.author.name)

@slash.slash(name='gamble', description='Азартные игры на xp (не больше 25 xp)', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='type_', description='Тип игры', option_type=3, required=True, choices=[create_choice(name='Монетка', value='coin'), create_choice(name='Число', value='number')]), create_option(name='arg1', description='Аргумент 1', option_type=3, required=True), create_option(name='arg2', description='Аргумент 2', option_type=4, required=True)])
@client.command(aliases=['азарт'])
async def gamble(ctx, type_=None, arg1=None, arg2=None):
    if type_ != None:
        with open('users.json', 'r') as f:
            users = json.load(f)
        if type_ == 'монетка' or type_ == 'coin':
            num = randint(0, 2000)
            if num >= 1 and num <= 1000:
                coin = 'Решка'
            elif num >= 1001 and num <= 2000:
                coin = 'Орёл'
            elif num == 0:
                coin = 'Ребро'
            if arg1 != None:
                if arg1 == 'Решка' or arg1 == 'Орёл' or arg1 == 'Ребро':
                    if arg2 != None:
                        if str(arg2).isdigit() == True:
                            arg2 = int(arg2)
                            if arg2 >= 1 and arg2 <= 25:
                                arg2 = int(arg2)
                                await update_data(users, ctx.author)
                                if coin == arg1:
                                    await add_experience(users, ctx.author, arg2)
                                    game_end = f'Вы выиграли и получили {arg2} xp'
                                else:
                                    users[f'{str(ctx.author.id)}'] -= arg2
                                    game_end = f'Вы проиграли и потеряли {arg2} xp'
                                embed_gamble = discord.Embed(color = 0x0000ff, title = 'Команда gamble')
                                embed_gamble.add_field(name='Ваши ставки:', value=f'```{arg1}```')
                                embed_gamble.add_field(name='Что выпало:', value=f'```{coin}```')
                                embed_gamble.add_field(name='Итог:', value=f'```{game_end}```')
                                if coin == 'Ребро':
                                    embed_gamble.add_field(name='Бонус', value='Вам выпал бонус в виде 125 xp за "Ребро". Шанс того, что монетка приземлиться на ребро в этой команде = 1 к 2001', inline=False)
                                    await add_experience(users, ctx.author, 125)
                            else:
                                embed_gamble = discord.Embed(description = 'Ваша ставка не может быть больше 25 xp или меньше 1 xp!', color = 0xff0000, title = 'Команда gamble\nОшибка')
                        else:
                            embed_gamble = discord.Embed(description = 'В аргументе может быть только число!', color = 0xff0000, title = 'Команда gamble\nОшибка')
                    else:
                        embed_gamble = discord.Embed(description = 'Вы не указали обязательный(-ые) аргумент(-ы)!', color = 0xff0000, title = 'Команда gamble\nОшибка')
                else:
                    embed_gamble = discord.Embed(description = 'Вы можете выбрать только "Орёл", "Решка" или "Ребро"!', color = 0xff0000, title = 'Команда gamble\nОшибка')
            else:
                embed_gamble = discord.Embed(description = 'Вы не указали обязательный(-ые) аргумент(-ы)!', color = 0xff0000, title = 'Команда gamble\nОшибка')
            await log_reg('Run command: gamble (coin)', ctx.author.name)
        elif type_ == 'num' or type_ == 'number' or type_ == 'число':
            if arg1 != None:
                if str(arg1).isdigit() == True:
                    arg1 = int(arg1)
                    if arg1 >= 1 and arg1 <= 5:
                        if arg2 != None:
                            if str(arg2).isdigit() == True:
                                arg2 = int(arg2)
                                if arg2 >= 2 and arg2 <= 5:
                                    gam_num = randint(1, arg2)
                                    if gam_num == 1:
                                        await add_experience(users, ctx.author, (arg1 * arg2))
                                        game_end = f'Вы выиграли и получили {arg1 * arg2} xp'
                                    else:
                                        users[str(ctx.author.id)] -= (arg1 * arg2)
                                        game_end = f'Вы проиграли и потеряли {arg1 * arg2} xp'
                                    embed_gamble = discord.Embed(color = 0x0000ff, title = 'Команда gamble')
                                    embed_gamble.add_field(name='Ваши ставки:', value=f'```{arg1} xp с риском {100 // arg2}% ```')
                                    embed_gamble.add_field(name='Итог:', value=f'```{game_end}```')
                                else:
                                    embed_gamble = discord.Embed(description = 'Риск не может быть меньше 2 или больше 5!', color = 0xff0000, title = 'Команда gamble\nОшибка')
                            else:
                                embed_gamble = discord.Embed(description = 'В агрументах могут быть только числа!', color = 0xff0000, title = 'Команда gamble\nОшибка')
                        else:
                            embed_gamble = discord.Embed(description = 'Вы не указали обязательный(-ые) аргумент(-ы)!', color = 0xff0000, title = 'Команда gamble\nОшибка')
                    else:
                        embed_gamble = discord.Embed(description = 'Ваша ставка не может быть меньше 1 xp или больше 5 xp!', color = 0xff0000, title = 'Команда gamble\nОшибка')
                else:
                    embed_gamble = discord.Embed(description = 'В агрументах могут быть только числа!', color = 0xff0000, title = 'Команда gamble\nОшибка')
            else:
                embed_gamble = discord.Embed(description = 'Вы не указали обязательный(-ые) аргумент(-ы)!', color = 0xff0000, title = 'Команда gamble\nОшибка')
            await log_reg('Run command: gamble (number)', ctx.author.name)
        else:
            embed_gamble = discord.Embed(description = 'Вы указали несуществующий тип азарта!', color = 0xff0000, title = 'Команда gamble\nОшибка')
            await log_reg('Run command: gamble', ctx.author.name)
    else:
        embed_gamble = discord.Embed(description = 'Вы не указали обязательный(-ые) аргумент(-ы)!', color = 0xff0000, title = 'Команда gamble\nОшибка')
        await log_reg('Run command: gamble', ctx.author.name)
    with open('users.json', 'w') as f:
        json.dump(users, f)
    await ctx.reply(embed=embed_gamble)

@slash.slash(name='default', description='Устанавливает стандартную карточку пользователя', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name = 'background', description = 'Фон карточки', option_type=3, required=True, choices=[create_choice(name='Красный', value='r'), create_choice(name='Синий', value='b'), create_choice(name='Зелёный', value='g'), create_choice(name='Жёлтый', value='y'), create_choice(name='Фиолетовый', value='p'), create_choice(name='Абстракция 1', value='a1'), create_choice(name='Абстракция 2', value='a2'), create_choice(name='Кибергород 1', value='c1'), create_choice(name='Кибергород 2', value='c2'), create_choice(name='Кибергород 3', value='c3'), create_choice(name='Кибергород 4', value='c4'), create_choice(name='Космос 1', value='g1'), create_choice(name='Космос 2', value='g2'), create_choice(name='Космос 3', value='g3'), create_choice(name='Космос 4', value='g4'), create_choice(name='Стандартный', value='d')])])
@client.command(aliases=['стандарт'])
async def default(ctx, background=None):
    if background != None:
        card_colors = {'g': 'green', 'b': 'blue', 'r': 'red', 'y': 'yellow', 'c1': 'cybercity1', 'c2': 'cybercity2', 'c3': 'cybercity3', 'c4': 'cybercity4', 'a1': 'abstraction1', 'a2': 'bstraction2', 'd': 'old', 'p': 'purple', 'g1':'galactic1', 'g2':'galactic2', 'g3':'galactic3', 'g4':'galactic4', 'default':'old'}
        if background in card_colors.keys():
            with open('users_backs.json') as file:
                backs = json.load(file)
            if str(ctx.author.id) in backs.keys():
                del backs[str(ctx.author.id)]
            backs[str(ctx.author.id)] = card_colors[background]
            with open('users_backs.json', 'w') as file:
                json.dump(backs, file)
            embed_default = discord.Embed(title='Команда default', description=f'Ваш фон карточки был успешно изменён на **{card_colors[background]}**.', colour=0x0000ff)
        else:
            embed_default = discord.Embed(title='Команда default\nОшибка', description='Указанный фон не найден в библиотеке фонов!', colour=0xff0000)
    else:
        embed_default = discord.Embed(title='Команда default\nОшибка', description='Вы не указали обязательный аргумент!', colour=0xff0000)
    await ctx.reply(embed=embed_default)
    await log_reg('Run command: default', ctx.author.name)
#команды владельца
@slash.slash(name='poll', description='Опрос', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='type_', description='Тип опроса', option_type=3, required=True, choices=[create_choice(name='✅ и ❌', value='check'), create_choice(name='Варианты', value='variants')]), create_option(name='question', description='Вопрос (в кавычках если не через /)', option_type=3, required=True), create_option(name='variants', description='Варианты (обязателен при <type_> = Варианты)', option_type=3, required=False)])
@client.command(aliases=['опрос'])
async def poll(ctx, type_=None, question=None, *, variants=None):
    for role in ctx.author.roles:
        if role.id == 880424360400269394:
            if type_ != None:
                if question != None:
                    if type_ == 'variants':
                        if variants != None:
                            answers = variants.split('|')
                            if len(answers) <= 10 and len(answers) >= 2:
                                numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
                                for i in range(len(answers)):
                                    if i == 0:
                                        answers_text = f'{numbers[0]} {answers[0]}'
                                    else:
                                        answers_text = f'{answers_text}\n{numbers[i]} {answers[i]}'
                                embed_poll = discord.Embed(title = 'Команда poll', color=0x0000ff)
                                embed_poll.add_field(name = question, value = answers_text)
                                message = await ctx.reply(embed=embed_poll)
                                for i in range(len(answers)):
                                    await message.add_reaction(numbers[i])
                                return
                            else:
                                embed_poll = discord.Embed(description = 'Вы можете добавить только от 2 до 10 вариантов ответа!', title = 'Команда poll\nОшибка', color=0xff0000)
                        else:
                            embed_poll = discord.Embed(description = 'Вы не указали обязательный аргумент!', title = 'Команда poll\nОшибка', color=0xff0000)
                    elif type_ == 'check':
                        numbers = ['✅', '❌']
                        embed_poll = discord.Embed(title = 'Команда poll', description = f'**{question}**', color=0x0000ff)
                        message = await ctx.reply(embed=embed_poll)
                        for i in range(2):
                            await message.add_reaction(numbers[i])
                        return
                    else:
                        embed_poll = discord.Embed(description = 'Вы можете выбрать только "variants" иил "check"!', title = 'Команда poll\nОшибка', color=0xff0000)
                else:
                    embed_poll = discord.Embed(description = 'Вы не указали обязательный(-ые) аргумент(-ы)!', title = 'Команда poll\nОшибка', color=0xff0000)
            else:
                embed_poll = discord.Embed(description = 'Вы не указали обязательный(-ые) аргумент(-ы)!', title = 'Команда poll\nОшибка', color=0xff0000)
            break
        else:
            embed_poll = discord.Embed(description = 'Вы не имеете право на выполнение этой команды!', title = 'Команда poll\nОшибка', color=0xff0000)
    await ctx.reply(embed=embed_poll)
    await log_reg('Run command: poll', ctx.author.name)

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
    await log_reg('Run command: prefix', ctx.author.name)

@client.command(aliases=['пнг'])#------------------------------------------------------------------только владелец
@commands.has_role(880424360400269394)
async def new_year_congrats(ctx):
    await ctx.channel.purge(limit=1)
    embed_new_year_congrats = discord.Embed(title='Поздравление с новым годом от JunFun', description='Ну что-же, наступил очередной 365 день года. А это значит, что сегодня 31 декабря (но иногда и 30), совсем скоро наступит **новый 2022 год**. Это также значит, что сегодня вечерком почти все сядут за стол со своими любимыми людьми и начнут кушать мандаринки, оливье и какую-нибудь ещё прикольную еду. Кто-то уже поставил ёлку, а кому-то было лень ставить. Кто-то красивенько нарядил, а кто-то оставил голую. В любом случае, большинство людей сядут за телевизоры и начнут слушать поздравление от своих президентов.\nНу а что я, я хочу поздравить вас с наступающим завтра в 00:00 **новым годом**. Пожелать всего наилучшего того, что вам там желают.\n***СПАСИБО ЗА ВСЁ ХОРОШЕЕ СДЕЛАННОЕ ВАМИ ЗА ГОД НА JUNFUN, УДАЧИ В НОВОМ ГОДУ!!!***', colour=0x0000ff)
    profile_picture = ctx.message.author.avatar_url
    embed_new_year_congrats.set_footer(text='Текст написал и вас поздравил ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(content='<@everyone>', embed=embed_new_year_congrats, allowed_mentions = allowed_mentions)
    await log_reg('Run command: new_year_congrats', ctx.author.name)

@client.command()
async def system(ctx):
    embed_system = discord.Embed(title='Команда help\nИнформация о команде: system', color=0x0000ff)
    embed_system.add_field(name='Что делает', value='Команда используется в целях тестирования функций этого бота. Обычно, она вызывает команду help, но иногда она печатает что-то другое')
    await ctx.send(embed=embed_system)
    await log_reg('Run command: system', ctx.author.name)

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
            clear_text = 'Вы не имеете право на выполнение этой команды!'
            title = 'Команда clear\nОшибка'
            color = 0xff0000
    embed_clear = discord.Embed(title=title, description=clear_text, colour=color)
    await ctx.send(embed=embed_clear)
    await log_reg('Run command: clear', ctx.author.name)

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
    await channel_mute.send(embed=embed_kick)
    await log_reg('Run command: kick', ctx.author.name)

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
    await channel_mute.send(embed=embed_ban)
    await log_reg('Run command: ban', ctx.author.name)

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
    await log_reg('Run command: unban', ctx.author.name)

@slash.slash(name='xp', description='Добавляет, удаляет или устанавливает участнику xp', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='member', description='Участник, чьё xp измениться', option_type=6, required=True), create_option(name='type_do', description='Действие (добавить, удалить, установить)', option_type=3, required=True, choices=[create_choice(name='Добавить', value='a'), create_choice(name='Удалить', value='r'), create_choice(name='Установить', value='s')]), create_option(name='amount', description='Сколько xp добавить, удалить, установить', option_type=4, required=True)])
@client.command()#---------------------------------------------------------------только владелец
async def xp(ctx, member:discord.Member=None, type_do=None, amount=None):
    for role in ctx.author.roles:
        if role.id == 880424360400269394:
            if member != None:
                if member.bot == False:
                    if type_do != None:
                        if amount != None:
                            if str(amount).isdigit() == True:
                                try:
                                    profile_picture = ctx.message.author.avatar_url
                                except:
                                    member = slash_context(member)
                                    type_do = slash_context(type_do)
                                    amount = slash_context(amount)
                                with open('users.json', 'r') as f:
                                    users = json.load(f)
                                await update_data(users, member)
                                if type_do == 'a':
                                    await add_experience(users, member, amount)
                                    type_do_rus = 'добавлено участнику'
                                    await log_reg('Run command: xp (add)', ctx.author.name)
                                elif type_do == 's':
                                    del users[str(member.id)]
                                    users[str(member.id)] = int(amount)
                                    type_do_rus = 'установлено участнику'
                                    await log_reg('Run command: xp (set)', ctx.author.name)
                                elif type_do == 'r':
                                    users[str(member.id)] -= amount
                                    type_do_rus = 'удалено у участника'
                                    await log_reg('Run command: xp (remove)', ctx.author.name)
                                else:
                                    embed_xp = discord.Embed(title = 'Команда xp\nОшибка', description = 'Тип действия не найден!', colour = 0xff0000)
                                    await ctx.reply(embed=embed_xp)
                                    await log_reg('Run command: xp (xp)', ctx.author.name)
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
                    embed_xp = discord.Embed(title = 'Команда xp\nОшибка', description = 'Невозможно выполнить команду с ботом!', colour = 0xff0000)
            else:
                embed_xp = discord.Embed(title = 'Команда xp\nОшибка', description = 'Вы не указали обязательный(-ые) агрумент(-ы)!', colour = 0xff0000)
            break
        else:
            embed_xp = discord.Embed(title = 'Команда xp\nОшибка', description = 'Вы не имеете право на выполнение этой команды!', colour = 0xff0000)
    await ctx.reply(embed=embed_xp)
#команды модерации
@slash.slash(name='mute', description='Скрывает участника', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='member', description='Участник на скрытие', option_type=6, required=True), create_option(name='time_mute', description='Время мута', option_type=4, required=False), create_option(name='reason', description='Причина скрытия', option_type=3, required=False)])
@client.command(aliases=['мут', 'скрыть', 'мьют'])#------------------------------------------------только модеративные личности сервера
async def mute(ctx, member=None, time_mute=10, *, reason=None):
    for role in ctx.author.roles:
        if role.id in moderation:
            if member != None:
                time_mute = str(time_mute)
                if time_mute.isdigit() == True:
                    time_mute = int(time_mute)
                    if time_mute <= 4320:
                        try:
                            profile_picture = ctx.message.author.avatar_url
                        except:
                            member = slash_context(member)
                            time_mute = slash_context(time_mute)
                            if reason != None:
                                reason = slash_context(reason)
                        global mutes
                        global mute_message
                        end_of_mute = int(time.time()) + int(time_mute * 60)
                        member_roles_names = [roles_mute.name for roles_mute in member.roles]
                        mutes[str(member.id)] = {}
                        mutes[str(member.id)]['roles'] = member_roles_names
                        mutes[str(member.id)]['time'] = end_of_mute
                        mutes[str(member.id)]['reason'] = reason
                        mutes[str(member.id)]['minus_time'] = 0
                        member_roles_text = 'Роли участника на момент скрытия:'
                        for i in range(len(member.roles)):
                            member_roles_text = member_roles_text + '\n' + str(i+1) + '. ' + member_roles_names[i]
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
                        embed_mute = discord.Embed(title = 'Команда mute', description=mute_text, color = 0x0000ff)
                        global channel_mute
                        channel = channel_mute
                        mute_role = discord.utils.get(ctx.guild.roles, name="Скрытый")
                        with open('mutes.json', 'w') as mute:
                            json.dump(mutes, mute)
                        await member.edit(roles=[mute_role])
                        print(mutes)
                    else:
                        embed_mute = discord.Embed(title = 'Команда mute\nОшибка', description = 'Время скрытия не должно превышать 3 суток (4320 минут)!', color = 0xff0000)
                        channel = ctx
                else:
                    embed_mute = discord.Embed(title = 'Команда mute\nОшибка', description = 'Время скрытия должно быть указано числом!', color = 0xff0000)
                    channel = ctx
            else:
                embed_mute = discord.Embed(title = 'Команда mute\nОшибка', description = 'Вы не указали участника на скрытие!', color = 0xff0000)
                channel = ctx
            break
        else:
            embed_mute = discord.Embed(title = 'Команда mute\nОшибка', description = 'Вы не имеете право на выполнение этой команды!', color = 0xff0000)
            channel = ctx
    mute_message = await channel.send(embed=embed_mute)
    await log_reg('Run command: mute', ctx.author.name)
    if channel == channel_mute:
        embed_mute2 = discord.Embed(title = 'Команда mute', description = mute_text + '\nВ канал <#888561763182845962> написано сообщение.', colour = 0x0000ff)
        await ctx.send(embed=embed_mute2)

@slash.slash(name='unmute', description='Расскрывает участника', guild_ids=[847106317356630049, 934526675373420654], options=[create_option(name='member', description='Участник на расскрытие', option_type=6, required=True)])
@client.command(aliases=['размут', 'расскрыть', 'размьют'])#---------------------------------------только модеративные личности сервера
async def unmute(ctx, member:discord.Member=None):
    try:
        profile_picture = ctx.message.author.avatar_url
    except:
        member = slash_context(member)
    for role in ctx.author.roles:
        if role.id in moderation:
            if member != None:
                if member in mutes:
                    embed_unmute = discord.Embed(title = 'Команда unmute', description = member.mention + ' был преждевременно расскрыт.', colour = 0xff0000)
            else:
                embed_unmute = discord.Embed(title = 'Команда mute\nОшибка', description = 'Вы не указали участника на расскрытие!', color = 0xff0000)
            break
        else:
            embed_unmute = discord.Embed(title = 'Команда mute\nОшибка', description = 'Вы не имеете право на выполнение этой команды!', color = 0xff0000)
    await ctx.send(embed=embed_unmute)
    await log_reg('Run command: unmute', ctx.author.name)
#запуск
client.run('ODg4NDc4MzIxNjU3MTM5MjIw.YUTR6w.fzISeaur8zxCy9W4YHeMN2SnzdU')