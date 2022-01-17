<<<<<<< HEAD
# -*- coding: utf-8 -*-
#подключение библиотек, модулей и функций
import discord
from discord import role
from discord.ext import commands, tasks
from discord.utils import get
from asyncio import sleep
from random import randint, uniform
from PIL import Image, ImageFont, ImageDraw
import json
import os
import requests
import io

print('Code successfully started.')
print('Bot starting now.')

allowed_mentions = discord.AllowedMentions(everyone = True)
with open('prefix.txt') as prefix:
    prefix_start = prefix.read()
client = commands.Bot(command_prefix = prefix_start, help_command=None, intents = discord.Intents.all())
#os.chdir(r'C:\Users\Asus\Desktop\Дискорд Бот')

moderation = [880424360400269394, 891413249801748510, 888356594251890708, 895782543553605662, 856608768090439710]

english_commands = ['8ball', 'ping', 'prefix', 'info', 'clear', 'kick', 'ban', 'unban', 'new_year_congrats', 'random', 'help', 'mute', 'user']
russian_comands = ['пинг', 'префикс', 'инфо', 'чистка', 'кик', 'бан', 'разбан', 'пнг', 'рандом', 'хелп', 'мут', 'юзер']
other_commands = ['pref', 'преф', 'ранд', 'rand', 'bot-info', 'бот-инфо', 'мьют', 'скрыть']

prefix_count = 1
channel_mute = None

@client.event
async def on_ready():
    global channel_mute
    channel_mute = client.get_channel(888561763182845962)
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.streaming, name='-help, -info', url='https://www.twitch.tv/janone02'))
    print('Bot successfully started.')
'''
@client.event
async def on_member_join(member):
    with open('users.json', 'r') as file:
        users = json.load(file)
    await update_data(users, member)
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=0)

@client.event
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as file:
            users = json.load(file)
        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)
        with open('users.json', 'w') as file:
            json.dump(users, file, indent=4)
    await client.process_commands(message)

async def update_data(users, user):
    if user.id in users.keys() == False:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 0

async def add_experience(users, user, amount):
    users[user.id]['experience'] += amount

async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[user.id]['experience']
    lvl1 = users[user.id]['level']
    lvl2 = int(experience ** (1/4))
    if lvl1 < lvl2:
        await message.channel.send(f'{user.mention}, ты толко что **достиг уровня {lvl2}!!!**\n***Спасибо за твою активность на JuFun🎊!!!***')
        users[user.id]['level'] = lvl2
'''
@client.command(aliases=['help', 'хелп'])
async def help_(ctx, command=None):
    embed_help_ex = None
    profile_picture = ctx.message.author.avatar_url
    if command != None:
        if str(command) in english_commands or str(command) in russian_comands or str(command) in other_commands:
            title_field = None
            if command == 'help' or command == 'хелп':
                name_help = 'help'
                inf = 'хелп.'
                args = '<команда>'
                req_args = 'Нет обязательных аргументов'
                args_info = '<команда> - любая команда из списка команд'
                do = 'Нет аргументов - печатает список всех команд и их краткое описание.\nЕсть аргумент <команда> - печатает полную информацию о конкретной команде.'
                title_field = 'Информация о команде help\nОбщие команды'
                description_field = '```1. help (хелп) <команда> - список команд сервера или подробная информация об 1 команде.\n2. info (инфо, bot-info, bot_info) - узнать о боте.```\n```...```'
            elif command == 'info' or command == 'bot-info' or command == 'инфо' or command == 'бот-инфо':
                name_help = 'info'
                inf = 'bot-info, инфо, бот-инфо.'
                args = 'Нет аргументов'
                req_args = 'Нет обязательных аргументов'
                args_info = 'Нет информации об аргументах'
                do = 'Печатает информацию о <@888478321657139220>'
                title_field = 'Информация о команде info'
                description_field = 'Бот: "JunFun Bot".\nЯзык программирования: "python".\n```...```'
            else:
                embed_help = discord.Embed(title='Команда help\nИнформация о команде: не найдено', description='Команда найдена в базе данных команд, но информация о ней не найдена.\nОбычно это значит, что информацию об этой команде ещё не заполнили.', colour=0x0000ff)
                await ctx.send(embed=embed_help)
                return
            embed_help = discord.Embed(title='Команда help\nИнформация о команде: ' + name_help, colour=0x0000ff)
            embed_help.add_field(name='Другие формы команды', value=inf)
            embed_help.add_field(name='Есть аргументы', value=args)
            embed_help.add_field(name='Есть обязательные аргументы', value=req_args)
            embed_help.add_field(name='Информация об аргументах:', value=args_info)
            embed_help.add_field(name='Что делает:', value=do)
            embed_help_ex = discord.Embed(title='Команда help', colour=0x0000ff)
            embed_help_ex.add_field(name=title_field, value=description_field)
            embed_help_ex.set_footer(text='"..." - продолжение оригинальной команды.\nЗапросил ' + str(ctx.message.author), icon_url=profile_picture)
        else:
            embed_help = discord.Embed(title='Команда help\nОшибка', description='Команда не найдена!', colour=0xff0000)
    else:
        embed_help = discord.Embed(title='Команда help', colour=0x0000ff)
        embed_help.add_field(name='Общие команды', value='```1. help (хелп) <команда> - список команд сервера или подробная информация об 1 команде.\n2. info (инфо, bot-info, bot_info) - узнать о боте.\n3. ping (пинг) - узнать пинг бота.\n4. 8ball <вопрос>* - спросить волшебный шар вопрос.\n5. random (рандом, ранд, rand) <тип рандома>* <1 аргумент> <2 аргумент> - рандомайзеры: монетка, многогранник, число, дробь...```\n* - обязательный аргумент.')
        member = ctx.author
        for role in member.roles:
            if role.id in moderation:
                embed_help.add_field(name='Модеративные команды', value='Если вы видите эту категорию, вы являетесь модератором или администратором.\n```1. mute (мут, мьют) <пинг участника> - налог скрытия на указанного участника.```', inline=False)
    embed_help.set_footer(text='Все команды используются с префиксом ' + prefix_start + '.\nЗапросил ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_help)
    if embed_help_ex != None:
        await ctx.send(embed=embed_help_ex)
    
@client.command(aliases=['пинг'])
async def ping(ctx):
    embed_ping = discord.Embed(title='Команда ping', description=f'Понг! Время полёта мячика {client.latency * 1000} мс.', colour=0x0000ff)
    profile_picture = ctx.message.author.avatar_url
    embed_ping.set_footer(text='Запросил ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_ping)

@client.command(aliases=['8ball'])
async def ball(ctx, *, question=None):
    if question != None:
        if len(question) <= 50:
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
    profile_picture = ctx.message.author.avatar_url
    embed_8ball.set_footer(text='Использовал ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_8ball)
    
@client.command(aliases=['rand', 'ранд', 'рандом'])
async def random(ctx, type_=None, arg1=None, arg2=None):
    if type_ != None:
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
            if arg1.isdigit() == True:
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
    profile_picture = ctx.message.author.avatar_url
    embed_random.set_footer(text='Использовал ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_random)

@client.command(aliases=['bot-info', 'инфо', 'бот-инфо'])
async def info(ctx):
    embed_info = discord.Embed(title='Команда info', description='Бот: "JunFun Bot".\nЯзык программирования: "python".\nИспользуемая библиотека: "discord.py".\nПрефикс бота: "' + prefix_start + '".\nАвтор и кодер бота: "Janone#2404".\nГод выпуска: "2021".\nБот был сделан специально и исключительно для сервера JunFun, использование бота на других серверах запрещено!', colour = 0x0000ff)
    profile_picture = ctx.message.author.avatar_url
    embed_info.set_footer(text='Запросил ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_info)

@client.command(aliases=['юзер'])
async def user(ctx, user:discord.Member=None):
    user_image = Image.open('profile_card_background.png')
    if user == None:
        profile_picture = str(ctx.message.author.avatar_url)
        user_name = ctx.author.name
        user_tag = ctx.author.discriminator
        user_id = ctx.author.id
    else:
        profile_picture = str(user.avatar_url)
        user_name = user.name
        user_tag = user.discriminator
        user_id = user.id
    response = requests.get(profile_picture, stream = True)
    response = Image.open(io.BytesIO(response.content))
    response = response.convert('RGBA')
    response = response.resize((400, 400), Image.ANTIALIAS)
    user_image.paste(response, (30, 30, 430, 430))
    idraw = ImageDraw.Draw(user_image)
    if user == None or user == ctx.message.author:
        user_tag = user_tag + '\n(Вы)'
    user_nickname_size = 0
    if len(str(user_name + '#' + user_tag)) <= 14.714285714285714:
        user_nickname_size = 70
    if len(str(user_name + '#' + user_tag)) >= 14.714285714285714 and len(str(user_name + '#' + user_tag)) <= 18.42857142857143:
        user_nickname_size = 60
    if len(str(user_name + '#' + user_tag)) >= 18.42857142857143 and len(str(user_name + '#' + user_tag)) <= 22.14285714285714:
        user_nickname_size = 50
    if len(str(user_name + '#' + user_tag)) >= 22.14285714285714 and len(str(user_name + '#' + user_tag)) <= 25.85714285714286:
        user_nickname_size = 40
    if len(str(user_name + '#' + user_tag)) >= 25.85714285714286 and len(str(user_name + '#' + user_tag)) <= 29.57142857142857:
        user_nickname_size = 30
    if len(str(user_name + '#' + user_tag)) >= 29.57142857142857 and len(str(user_name + '#' + user_tag)) <= 33.28571428571428:
        user_nickname_size = 20
    if len(str(user_name + '#' + user_tag)) >= 33.28571428571428 and len(str(user_name + '#' + user_tag)) <= 37:
        user_nickname_size = 10
    card_headline = ImageFont.truetype('arial.ttf', size=user_nickname_size)
    card_under = ImageFont.truetype('arial.ttf', size=50)
    idraw.text((460, 75), f'{user_name}#{user_tag}', font = card_headline)
    idraw.text((460, 400), f'ID: {user_id}', font = card_under)
    user_image.save('user_card.png')
    
    author_profile_picture = ctx.message.author.avatar_url
    user_embed_image = discord.File('user_card.png')
    embed_user = discord.Embed(title='Команда user', colour=0x0000ff)
    embed_user.set_footer(text='Запросил ' + str(ctx.message.author), icon_url=author_profile_picture)
    embed_user.set_image(url="attachment://user_card.png")
    await ctx.send(embed=embed_user, file=user_embed_image)

@client.command(aliases=['pref', 'префикс', 'преф'])#----------------------------------------------только владелец
@commands.has_role(880424360400269394)
async def prefix(ctx, new_pref=None):
    global prefix_count
    global prefix_start
    if new_pref != None:
        if prefix_count == 1:
            with open('prefix.txt', 'w') as prefix:
                prefix.write(new_pref)
                prefix.close()
            prefix_count = 0
            embed_prefix = discord.Embed(title='Команда prefix', description='Префикс бота успешно изменён с **' + prefix_start + '** на **' + new_pref + '**, но для вступления изменений в силу бота придётся перезагрузить.', colour=0x0000ff)
        else:
            embed_prefix = discord.Embed(title='Команда prefix\nОшибка', description='Чтобы изменить префикс ещё раз - перезагрузите бота.', colour=0xff0000)
    else:
        embed_prefix = discord.Embed(title='Команда prefix\nОшибка', description='Вы не указали новый префикс!', colour=0xff0000)
    profile_picture = ctx.message.author.avatar_url
    embed_prefix.set_footer(text='Использовал ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_prefix)

@client.command(aliases=['пнг'])#------------------------------------------------------------------только владелец
@commands.has_role(880424360400269394)
async def new_year_congrats(ctx):
    await ctx.channel.purge(limit=1)
    embed_new_year_congrats = discord.Embed(title='Поздравление с новым годом от JunFun', description='Ну что-же, наступил очередной 365 день года. А это значит, что сегодня 31 декабря (но иногда и 30), совсем скоро наступит **новый 2022 год**. Это также значит, что сегодня вечерком почти все сядут за стол со своими любимыми людьми и начнут кушать мандаринки, оливье и какую-нибудь ещё прикольную еду. Кто-то уже поставил ёлку, а кому-то было лень ставить. Кто-то красивенько нарядил, а кто-то оставил голую. В любом случае, большинство людей сядут за телевизоры и начнут слушать поздравление от своих президентов.\nНу а что я, я хочу поздравить вас с наступающим завтра в 00:00 **новым годом**. Пожелать всего наилучшего того, что вам там желают.\n***СПАСИБО ЗА ВСЁ ХОРОШЕЕ СДЕЛАННОЕ ВАМИ ЗА ГОД НА JUNFUN, УДАЧИ В НОВОМ ГОДУ!!!***', colour=0x0000ff)
    profile_picture = ctx.message.author.avatar_url
    embed_new_year_congrats.set_footer(text='Текст написал и вас поздравил ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(content='<@everyone>', embed=embed_new_year_congrats, allowed_mentions = allowed_mentions)

@client.command()#---------------------------------------------------------------------------------только владелец
async def system(ctx):
    await ctx.send('Команда сейчас пуста.')

@client.command(aliases=['чистка'])#---------------------------------------------------------------только владелец
@commands.has_role(880424360400269394)
async def clear(ctx, total=10):
    await ctx.channel.purge(limit=total+1)
    embed_clear = discord.Embed(title='Команда clear', description='Успешно было очищено несколько сообщений. Сообщение призывающее команду сюда не входит.', colour = 0x0000ff)
    profile_picture = ctx.message.author.avatar_url
    embed_clear.set_footer(text='Использовал ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_clear)

@client.command(aliases=['кик'])#------------------------------------------------------------------только владелец
@commands.has_role(880424360400269394)
async def kick(ctx, member:discord.Member=None, *, reason=None):
    if member != None:
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
    embed_kick = discord.Embed(title = title, description = kick_text, colour = color)
    profile_picture = ctx.message.author.avatar_url
    embed_kick.set_footer(text='Модератор ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_kick)

@client.command(aliases=['бан'])#------------------------------------------------------------------только владелец
@commands.has_role(880424360400269394)
async def ban(ctx, member:discord.Member=None, *, reason=None):
    if member != None:
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
    embed_ban = discord.Embed(title = title, description = ban_text, colour = color)
    profile_picture = ctx.message.author.avatar_url
    embed_ban.set_footer(text='Модератор ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_ban)

@client.command(aliases=['разбан'])#---------------------------------------------------------------только владелец
async def unban(ctx, *, member=None):
    for role in ctx.message.author.roles:
        if role.id == 880424360400269394:
            if member != None:
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
        else:
            unban_text = 'Вы не имеете право на выполнение этой команды!'
            title = 'Команда unban\nОшибка'
            color = 0xff0000
    embed_unban = discord.Embed(title = title, description = unban_text, colour = color)
    profile_picture = ctx.message.author.avatar_url
    embed_unban.set_footer(text='Модератор ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_unban)

@client.command(aliases=['мут', 'скрыть', 'мьют'])#------------------------------------------------только модеративные личности сервера
async def mute(ctx, member:discord.Member=None, time_mute=10, *, reason=None):#команда
    for role in ctx.message.author.roles:#перечисление ролей модератора
        if role.id in moderation:#если роль модеративная...
            if member != None:#если участник указан...
                try:
                    time_mute = str(time_mute)
                    if time_mute.isdigit() == True:
                        time_mute = int(time_mute)
                        if time_mute <= 4320:
                            member_roles_vocabluary = {}
                            member_roles_vocabluary[member.nick] = member.roles
                            member_roles_names = [roles_mute.name for roles_mute in member.roles]
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
                except discord.ext.commands.errors.MemberNotFound:
                    mute_text = 'Вы указали участника в неверном формате!'
                    title = 'Команда mute\nОшибка'
                    color = 0xff0000
                    channel = ctx
            else:
                mute_text = 'Вы не указали участника на скрытие!'
                title = 'Команда mute\nОшибка'
                color = 0xff0000
                channel = ctx
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
        await member.move_to(None)
        await sleep(time_mute * 60)
        await member.edit(roles=member_roles_vocabluary[member.nick])
        del member_roles_vocabluary[member.nick]
        embed_mute3 = discord.Embed(title = title, description = mute_text + '\n**Участник уже расскрыт.**', colour = color)
        await mute_message.edit(embed=embed_mute3)

=======
# -*- coding: utf-8 -*-
#подключение библиотек, модулей и функций
import discord
from discord import role
from discord.ext import commands, tasks
from discord.utils import get
from asyncio import sleep
from random import randint, uniform
from PIL import Image, ImageFont, ImageDraw
import json
import os
import requests
import io

print('Code successfully started.')
print('Bot starting now.')

allowed_mentions = discord.AllowedMentions(everyone = True)
with open('prefix.txt') as prefix:
    prefix_start = prefix.read()
client = commands.Bot(command_prefix = prefix_start, help_command=None, intents = discord.Intents.all())
#os.chdir(r'C:\Users\Asus\Desktop\Дискорд Бот')

moderation = [880424360400269394, 891413249801748510, 888356594251890708, 895782543553605662, 856608768090439710]

english_commands = ['8ball', 'ping', 'prefix', 'info', 'clear', 'kick', 'ban', 'unban', 'new_year_congrats', 'random', 'help', 'mute', 'user']
russian_comands = ['пинг', 'префикс', 'инфо', 'чистка', 'кик', 'бан', 'разбан', 'пнг', 'рандом', 'хелп', 'мут', 'юзер']
other_commands = ['pref', 'преф', 'ранд', 'rand', 'bot-info', 'бот-инфо', 'мьют', 'скрыть']

prefix_count = 1
channel_mute = None

@client.event
async def on_ready():
    global channel_mute
    channel_mute = client.get_channel(888561763182845962)
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.streaming, name='-help, -info', url='https://www.twitch.tv/janone02'))
    print('Bot successfully started.')
'''
@client.event
async def on_member_join(member):
    with open('users.json', 'r') as file:
        users = json.load(file)
    await update_data(users, member)
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=0)

@client.event
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as file:
            users = json.load(file)
        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)
        with open('users.json', 'w') as file:
            json.dump(users, file, indent=4)
    await client.process_commands(message)

async def update_data(users, user):
    if user.id in users.keys() == False:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 0

async def add_experience(users, user, amount):
    users[user.id]['experience'] += amount

async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[user.id]['experience']
    lvl1 = users[user.id]['level']
    lvl2 = int(experience ** (1/4))
    if lvl1 < lvl2:
        await message.channel.send(f'{user.mention}, ты толко что **достиг уровня {lvl2}!!!**\n***Спасибо за твою активность на JuFun🎊!!!***')
        users[user.id]['level'] = lvl2
'''
@client.command(aliases=['help', 'хелп'])
async def help_(ctx, command=None):
    embed_help_ex = None
    profile_picture = ctx.message.author.avatar_url
    if command != None:
        if str(command) in english_commands or str(command) in russian_comands or str(command) in other_commands:
            title_field = None
            if command == 'help' or command == 'хелп':
                name_help = 'help'
                inf = 'хелп.'
                args = '<команда>'
                req_args = 'Нет обязательных аргументов'
                args_info = '<команда> - любая команда из списка команд'
                do = 'Нет аргументов - печатает список всех команд и их краткое описание.\nЕсть аргумент <команда> - печатает полную информацию о конкретной команде.'
                title_field = 'Информация о команде help\nОбщие команды'
                description_field = '```1. help (хелп) <команда> - список команд сервера или подробная информация об 1 команде.\n2. info (инфо, bot-info, bot_info) - узнать о боте.```\n```...```'
            elif command == 'info' or command == 'bot-info' or command == 'инфо' or command == 'бот-инфо':
                name_help = 'info'
                inf = 'bot-info, инфо, бот-инфо.'
                args = 'Нет аргументов'
                req_args = 'Нет обязательных аргументов'
                args_info = 'Нет информации об аргументах'
                do = 'Печатает информацию о <@888478321657139220>'
                title_field = 'Информация о команде info'
                description_field = 'Бот: "JunFun Bot".\nЯзык программирования: "python".\n```...```'
            else:
                embed_help = discord.Embed(title='Команда help\nИнформация о команде: не найдено', description='Команда найдена в базе данных команд, но информация о ней не найдена.\nОбычно это значит, что информацию об этой команде ещё не заполнили.', colour=0x0000ff)
                await ctx.send(embed=embed_help)
                return
            embed_help = discord.Embed(title='Команда help\nИнформация о команде: ' + name_help, colour=0x0000ff)
            embed_help.add_field(name='Другие формы команды', value=inf)
            embed_help.add_field(name='Есть аргументы', value=args)
            embed_help.add_field(name='Есть обязательные аргументы', value=req_args)
            embed_help.add_field(name='Информация об аргументах:', value=args_info)
            embed_help.add_field(name='Что делает:', value=do)
            embed_help_ex = discord.Embed(title='Команда help', colour=0x0000ff)
            embed_help_ex.add_field(name=title_field, value=description_field)
            embed_help_ex.set_footer(text='"..." - продолжение оригинальной команды.\nЗапросил ' + str(ctx.message.author), icon_url=profile_picture)
        else:
            embed_help = discord.Embed(title='Команда help\nОшибка', description='Команда не найдена!', colour=0xff0000)
    else:
        embed_help = discord.Embed(title='Команда help', colour=0x0000ff)
        embed_help.add_field(name='Общие команды', value='```1. help (хелп) <команда> - список команд сервера или подробная информация об 1 команде.\n2. info (инфо, bot-info, bot_info) - узнать о боте.\n3. ping (пинг) - узнать пинг бота.\n4. 8ball <вопрос>* - спросить волшебный шар вопрос.\n5. random (рандом, ранд, rand) <тип рандома>* <1 аргумент> <2 аргумент> - рандомайзеры: монетка, многогранник, число, дробь...```\n* - обязательный аргумент.')
        member = ctx.author
        for role in member.roles:
            if role.id in moderation:
                embed_help.add_field(name='Модеративные команды', value='Если вы видите эту категорию, вы являетесь модератором или администратором.\n```1. mute (мут, мьют) <пинг участника> - налог скрытия на указанного участника.```', inline=False)
    embed_help.set_footer(text='Все команды используются с префиксом ' + prefix_start + '.\nЗапросил ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_help)
    if embed_help_ex != None:
        await ctx.send(embed=embed_help_ex)
    
@client.command(aliases=['пинг'])
async def ping(ctx):
    embed_ping = discord.Embed(title='Команда ping', description=f'Понг! Время полёта мячика {client.latency * 1000} мс.', colour=0x0000ff)
    profile_picture = ctx.message.author.avatar_url
    embed_ping.set_footer(text='Запросил ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_ping)

@client.command(aliases=['8ball'])
async def ball(ctx, *, question=None):
    if question != None:
        if len(question) <= 50:
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
    profile_picture = ctx.message.author.avatar_url
    embed_8ball.set_footer(text='Использовал ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_8ball)
    
@client.command(aliases=['rand', 'ранд', 'рандом'])
async def random(ctx, type_=None, arg1=None, arg2=None):
    if type_ != None:
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
            if arg1.isdigit() == True:
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
    profile_picture = ctx.message.author.avatar_url
    embed_random.set_footer(text='Использовал ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_random)

@client.command(aliases=['bot-info', 'инфо', 'бот-инфо'])
async def info(ctx):
    embed_info = discord.Embed(title='Команда info', description='Бот: "JunFun Bot".\nЯзык программирования: "python".\nИспользуемая библиотека: "discord.py".\nПрефикс бота: "' + prefix_start + '".\nАвтор и кодер бота: "Janone#2404".\nГод выпуска: "2021".\nБот был сделан специально и исключительно для сервера JunFun, использование бота на других серверах запрещено!', colour = 0x0000ff)
    profile_picture = ctx.message.author.avatar_url
    embed_info.set_footer(text='Запросил ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_info)

@client.command(aliases=['юзер'])
async def user(ctx, user:discord.Member=None):
    user_image = Image.open('profile_card_background.png')
    if user == None:
        profile_picture = str(ctx.message.author.avatar_url)
        user_name = ctx.author.name
        user_tag = ctx.author.discriminator
        user_id = ctx.author.id
    else:
        profile_picture = str(user.avatar_url)
        user_name = user.name
        user_tag = user.discriminator
        user_id = user.id
    response = requests.get(profile_picture, stream = True)
    response = Image.open(io.BytesIO(response.content))
    response = response.convert('RGBA')
    response = response.resize((400, 400), Image.ANTIALIAS)
    user_image.paste(response, (30, 30, 430, 430))
    idraw = ImageDraw.Draw(user_image)
    if user == None or user == ctx.message.author:
        user_tag = user_tag + '\n(Вы)'
    user_nickname_size = 0
    if len(str(user_name + '#' + user_tag)) <= 14.714285714285714:
        user_nickname_size = 70
    if len(str(user_name + '#' + user_tag)) >= 14.714285714285714 and len(str(user_name + '#' + user_tag)) <= 18.42857142857143:
        user_nickname_size = 60
    if len(str(user_name + '#' + user_tag)) >= 18.42857142857143 and len(str(user_name + '#' + user_tag)) <= 22.14285714285714:
        user_nickname_size = 50
    if len(str(user_name + '#' + user_tag)) >= 22.14285714285714 and len(str(user_name + '#' + user_tag)) <= 25.85714285714286:
        user_nickname_size = 40
    if len(str(user_name + '#' + user_tag)) >= 25.85714285714286 and len(str(user_name + '#' + user_tag)) <= 29.57142857142857:
        user_nickname_size = 30
    if len(str(user_name + '#' + user_tag)) >= 29.57142857142857 and len(str(user_name + '#' + user_tag)) <= 33.28571428571428:
        user_nickname_size = 20
    if len(str(user_name + '#' + user_tag)) >= 33.28571428571428 and len(str(user_name + '#' + user_tag)) <= 37:
        user_nickname_size = 10
    card_headline = ImageFont.truetype('arial.ttf', size=user_nickname_size)
    card_under = ImageFont.truetype('arial.ttf', size=50)
    idraw.text((460, 75), f'{user_name}#{user_tag}', font = card_headline)
    idraw.text((460, 400), f'ID: {user_id}', font = card_under)
    user_image.save('user_card.png')
    
    author_profile_picture = ctx.message.author.avatar_url
    user_embed_image = discord.File('user_card.png')
    embed_user = discord.Embed(title='Команда user', colour=0x0000ff)
    embed_user.set_footer(text='Запросил ' + str(ctx.message.author), icon_url=author_profile_picture)
    embed_user.set_image(url="attachment://user_card.png")
    await ctx.send(embed=embed_user, file=user_embed_image)

@client.command(aliases=['pref', 'префикс', 'преф'])#----------------------------------------------только владелец
@commands.has_role(880424360400269394)
async def prefix(ctx, new_pref=None):
    global prefix_count
    global prefix_start
    if new_pref != None:
        if prefix_count == 1:
            with open('prefix.txt', 'w') as prefix:
                prefix.write(new_pref)
                prefix.close()
            prefix_count = 0
            embed_prefix = discord.Embed(title='Команда prefix', description='Префикс бота успешно изменён с **' + prefix_start + '** на **' + new_pref + '**, но для вступления изменений в силу бота придётся перезагрузить.', colour=0x0000ff)
        else:
            embed_prefix = discord.Embed(title='Команда prefix\nОшибка', description='Чтобы изменить префикс ещё раз - перезагрузите бота.', colour=0xff0000)
    else:
        embed_prefix = discord.Embed(title='Команда prefix\nОшибка', description='Вы не указали новый префикс!', colour=0xff0000)
    profile_picture = ctx.message.author.avatar_url
    embed_prefix.set_footer(text='Использовал ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_prefix)

@client.command(aliases=['пнг'])#------------------------------------------------------------------только владелец
@commands.has_role(880424360400269394)
async def new_year_congrats(ctx):
    await ctx.channel.purge(limit=1)
    embed_new_year_congrats = discord.Embed(title='Поздравление с новым годом от JunFun', description='Ну что-же, наступил очередной 365 день года. А это значит, что сегодня 31 декабря (но иногда и 30), совсем скоро наступит **новый 2022 год**. Это также значит, что сегодня вечерком почти все сядут за стол со своими любимыми людьми и начнут кушать мандаринки, оливье и какую-нибудь ещё прикольную еду. Кто-то уже поставил ёлку, а кому-то было лень ставить. Кто-то красивенько нарядил, а кто-то оставил голую. В любом случае, большинство людей сядут за телевизоры и начнут слушать поздравление от своих президентов.\nНу а что я, я хочу поздравить вас с наступающим завтра в 00:00 **новым годом**. Пожелать всего наилучшего того, что вам там желают.\n***СПАСИБО ЗА ВСЁ ХОРОШЕЕ СДЕЛАННОЕ ВАМИ ЗА ГОД НА JUNFUN, УДАЧИ В НОВОМ ГОДУ!!!***', colour=0x0000ff)
    profile_picture = ctx.message.author.avatar_url
    embed_new_year_congrats.set_footer(text='Текст написал и вас поздравил ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(content='<@everyone>', embed=embed_new_year_congrats, allowed_mentions = allowed_mentions)

@client.command()#---------------------------------------------------------------------------------только владелец
async def system(ctx):
    await ctx.send('Команда сейчас пуста.')

@client.command(aliases=['чистка'])#---------------------------------------------------------------только владелец
@commands.has_role(880424360400269394)
async def clear(ctx, total=10):
    await ctx.channel.purge(limit=total+1)
    embed_clear = discord.Embed(title='Команда clear', description='Успешно было очищено несколько сообщений. Сообщение призывающее команду сюда не входит.', colour = 0x0000ff)
    profile_picture = ctx.message.author.avatar_url
    embed_clear.set_footer(text='Использовал ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_clear)

@client.command(aliases=['кик'])#------------------------------------------------------------------только владелец
@commands.has_role(880424360400269394)
async def kick(ctx, member:discord.Member=None, *, reason=None):
    if member != None:
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
    embed_kick = discord.Embed(title = title, description = kick_text, colour = color)
    profile_picture = ctx.message.author.avatar_url
    embed_kick.set_footer(text='Модератор ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_kick)

@client.command(aliases=['бан'])#------------------------------------------------------------------только владелец
@commands.has_role(880424360400269394)
async def ban(ctx, member:discord.Member=None, *, reason=None):
    if member != None:
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
    embed_ban = discord.Embed(title = title, description = ban_text, colour = color)
    profile_picture = ctx.message.author.avatar_url
    embed_ban.set_footer(text='Модератор ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_ban)

@client.command(aliases=['разбан'])#---------------------------------------------------------------только владелец
async def unban(ctx, *, member=None):
    for role in ctx.message.author.roles:
        if role.id == 880424360400269394:
            if member != None:
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
        else:
            unban_text = 'Вы не имеете право на выполнение этой команды!'
            title = 'Команда unban\nОшибка'
            color = 0xff0000
    embed_unban = discord.Embed(title = title, description = unban_text, colour = color)
    profile_picture = ctx.message.author.avatar_url
    embed_unban.set_footer(text='Модератор ' + str(ctx.message.author), icon_url=profile_picture)
    await ctx.send(embed=embed_unban)

@client.command(aliases=['мут', 'скрыть', 'мьют'])#------------------------------------------------только модеративные личности сервера
async def mute(ctx, member:discord.Member=None, time_mute=10, *, reason=None):#команда
    for role in ctx.message.author.roles:#перечисление ролей модератора
        if role.id in moderation:#если роль модеративная...
            if member != None:#если участник указан...
                try:
                    time_mute = str(time_mute)
                    if time_mute.isdigit() == True:
                        time_mute = int(time_mute)
                        if time_mute <= 4320:
                            member_roles_vocabluary = {}
                            member_roles_vocabluary[member.nick] = member.roles
                            member_roles_names = [roles_mute.name for roles_mute in member.roles]
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
                except discord.ext.commands.errors.MemberNotFound:
                    mute_text = 'Вы указали участника в неверном формате!'
                    title = 'Команда mute\nОшибка'
                    color = 0xff0000
                    channel = ctx
            else:
                mute_text = 'Вы не указали участника на скрытие!'
                title = 'Команда mute\nОшибка'
                color = 0xff0000
                channel = ctx
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
        await member.move_to(None)
        await sleep(time_mute * 60)
        await member.edit(roles=member_roles_vocabluary[member.nick])
        del member_roles_vocabluary[member.nick]
        embed_mute3 = discord.Embed(title = title, description = mute_text + '\n**Участник уже расскрыт.**', colour = color)
        await mute_message.edit(embed=embed_mute3)

>>>>>>> 02b13491b57802263753fa5ed2934545ed790e36
client.run('ODg4NDc4MzIxNjU3MTM5MjIw.YUTR6w.PuOnMe2BZGnFvTek2aJPA7IkNH8')