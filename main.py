import telebot

import sqlite3
import time
# Scary!
import re
import os
import requests
from random import randint, choice
from telebot import types

# Ссылка на бота С8:
bot = telebot.TeleBot('7066300352:AAHoKT8LAaZd4pdnkbU3vlzBijI25bM7Xqo')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Основные команды:


# --  START -- Начало общения с ботом, выводит на экран приветствие и несколько комманд

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, f'<b>Привет! Я чат бот S8.</b>\n'
                                          f'Я буду помогать вам регулировать группы, а также предоставлять полезные '
                                          f'и развлекательные функции\n'
                                          f'<b>Чтобы я корректно работал, добавьте меня в свою группу как '
                                          f'администратор</b>\n'
                                          f'Вот список полезных команд - /menu\n'
                                          f'<b>Если вы хотите изменить некоторые параметры группы через лс</b>:\n'
                                          f'Впишите в свою группу команды:\n'
                                          f'<b>//add_to_admin_list</b> - я буду знать, что вы являетесь админом\n'
                                          f'<b>//get_group_id</b> - код, которые будут просить функции\n'
                                          f'Давайте начнём!', parse_mode='html')

    elif message.chat.type in ['group', 'supergroup']:
        bot.send_message(message.chat.id, f'<b>Всем привет! Я чат бот S8.</b>\n'
                                          f'Я буду помогать вам регулировать группы, а также предоставлять полезные '
                                          f'и развлекательные функции\n'
                                          f'<b>Чтобы я корректно работал, добавьте меня в свою группу как '
                                          f'администратор</b>\n'
                                          f'Вот список полезных команд - /menu\n'
                                          f'<b>Некоторые параметры группы я могу изменять в лс</b>\n'
                                          f'Давайте начнём!', parse_mode='html')

        group_db_name = 'DB' + str(message.chat.id) + 'S8.db'

        con = sqlite3.connect(group_db_name)
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS 
                        Admins(admin TEXT UNIQUE)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS 
                        Banned_words(phrase TEXT UNIQUE, punishment_type TEXT)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS 
                        Banned_types(ttype TEXT UNIQUE)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS 
                        User_ids(username TEXT UNIQUE, id TEXT UNIQUE)""")

        con.commit()
        con.close()


# ------------------------------------------------------------------------------------

# -- MENU -- Список всех команд, выводит одним сообщением.


@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(message.chat.id, 'Список команд:\n'
                                      '(❗ - доступно только администраторам)\n'
                                      '/start - Начало разговора\n'
                                      '/menu - Меню со всеми командами\n'
                                      '/quick_menu - Меню с быстрыми командами\n'
                                      '/blacklisted_words -❗- Управление запрещенными словами\n'
                                      '/blacklisted_types -❗- Управление запрещенными типами сообщений\n'
                                      '/coin_flip - Подбрасывает монетку\n'
                                      '/rtd - Кидает кость d100\n'
                                      '/8ball - Пишет случайный результат волшебного шара восьмерки\n'
                                      '/quote - Пишет случайную цитату на английском\n'
                                      '/cat - Посылает случайную картинку с котиком\n'
                                      'Больше комманд для админимтраторов в /blacklisted_words')


# ------------------------------------------------------------------------------------

# -- QUICK_MENU -- Список всех быстрых команд, начинающиеся с //, все 3 вида

@bot.message_handler(commands=['quick_menu'])
def menu(message):
    bot.send_message(message.chat.id, 'Список быстрых команд - они вводятся как сообщения.\n'
                                      '(❗ - доступно только администраторам)\n\n'
                                      '--- Только команды:\n'
                                      '//mdata -❗- присылает сырые данные сообщения\n'
                                      '//add_to_admin_list -❗- добавляет в список админов группы\n'
                                      '//get_group_id -❗- присылает код группы\n'
                                      '//members - присылает список участников группы\n\n'
                                      '--- Команды с параметрами\n'
                                      '//mute {@-} {d:h:m} -❗- заглушает полльзователя на d, h, m дней, '
                                      'часов, минут соответственно\n'
                                      '//unmute {@-} -❗- убрать заглушение с пользователя\n'
                                      '//kick {@-} -❗- кикает участника группы с шансом вернутся в неё\n'
                                      '//ban {@-} -❗- банит участника группы без шанса на возвращение\n'
                                      '//unban {@-} -❗- разбан пользователя (юзернейм нужно помнить, '
                                      'не возвращает обратно в группу)\n'
                                      '//remove_from_admin_list {@-} -❗- убрать из списка админов\n'
                                      '//bwl_add {фраза: последствие}-❗- добавляет в список запрещенных слов список,'
                                      'каждую фразу с последствием писать с новой строки, последствия: m, k, a - '
                                      'заглушить на час, кикнуть, предупредить соответственно\n'
                                      '//bwl_remove {фраза} -❗- вводятся с новой строки, удаляет из списка'
                                      'выбранные фразы если есть\n'
                                      '//bwl_delete -❗- удаляет весь список\n'
                                      '//bwl_show_list -❗- показывает весь список\n'
                                      '//btl_set {тип} -❗- удаляет сообщения с данными типами, '
                                      'писать на отдельных строках, список в самой команде\n'
                                      '//btl_show_list -❗- показывает список запрещенных типов сообщений\n\n'
                                      '--- Заменяющие команды (бот заменяет команду и пересылает ваше сообщение)\n'
                                      '//coin_flip - заменяется на орёла / решку\n'
                                      '//rtd - заменяется на число 1 - 100\n'
                                      '//pick_user - заменяется случайным пользователем')


# ------------------------------------------------------------------------------------


# -- BLACKLISTED_WORDS -- Работа с нелегальными словами


@bot.message_handler(commands=['blacklisted_words'])
def blacklisted_words_main(message):
    if message.chat.type in ['group', 'supergroup']:
        if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
            btn1 = types.KeyboardButton('✅ Добавить слова')
            btn2 = types.KeyboardButton('❌ Удалить слова')
            btn3 = types.KeyboardButton('➡ Просмотреть список')
            btn4 = types.KeyboardButton('💥 Удалить список')
            btn5 = types.KeyboardButton('🔙 Вернуться')

            markup.add(btn1, btn2, btn3, btn4, btn5)

            bot.reply_to(message, 'Сейчас вы изменяете список запрещенных слов в группе. \n'
                                  'При использовании запрещенного слова от не администратора следуют последствия.\n'
                                  ' Выберите один из варинатов чтобы продолжить.', reply_markup=markup)

    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        btn1 = types.KeyboardButton('✅ Добавить слова')
        btn2 = types.KeyboardButton('❌ Удалить слова')
        btn3 = types.KeyboardButton('➡ Просмотреть список')
        btn4 = types.KeyboardButton('💥 Удалить список')
        btn5 = types.KeyboardButton('🔙 Вернуться')

        markup.add(btn1, btn2, btn3, btn4, btn5)

        bot.reply_to(message, 'Сейчас вы изменяете список запрещенных слов в группе. \n'
                              'При использовании запрещенного слова от не администратора следуют последствия.\n'
                              ' Для этого вам понадобится код вашей группы (инструкция в /start). \n'
                              'Выберите один из варинатов чтобы продолжить.\n', reply_markup=markup)


# ------------------------------------------------------------------------------------


# -- BLACKLISTED_TYPES -- Работа с нелегальными типами сообщений


@bot.message_handler(commands=['blacklisted_types'])
def blacklisted_types_main(message):
    if message.chat.type in ['group', 'supergroup']:
        if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
            btn1 = types.KeyboardButton('✅ Изменить список типов')
            btn2 = types.KeyboardButton('➡ Просмотреть список типов')

            markup.add(btn1)
            markup.add(btn2)

            bot.reply_to(message, 'Сейчас вы изменяете список запрещенных типов слов в группе. \n'
                                  'Все сообщения от не администраторов с данным типом будут сразу удалены. \n'
                                  'Выберите один из варинатов чтобы продолжить.', reply_markup=markup)

    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        btn1 = types.KeyboardButton('✅ Изменить список типов')
        btn2 = types.KeyboardButton('➡ Просмотреть список типов')

        markup.add(btn1)
        markup.add(btn2)

        bot.reply_to(message, 'Сейчас вы изменяете список запрещенных слов в группе. \n'
                              'Все сообщения от не администраторов с данными типами будут сразу удалены. \n'
                              'Для этого вам понадобится код вашей группы (инструкция в /start). \n'
                              'Выберите один из варинатов чтобы продолжить.\n', reply_markup=markup)


# ------------------------------------------------------------------------------------

# -- COIN_FLIP -- Подбрасывает монетку и случайным обрзаом выбирает орла или решку.


@bot.message_handler(commands=['coin_flip'])
def coin_flip(message):
    coin_random = randint(0, 1)
    coin = ['ОРЁЛ', 'РЕШКА'][coin_random]
    word = ['оказался', 'оказалась'][coin_random]
    bot.reply_to(message, f'Монетка была подброшена в воздух, и когда она приземлилась, на ней {word}...'
                          f' \n \n<b>{coin}!</b>', parse_mode='html')


# ------------------------------------------------------------------------------------

# -- DICE_ROLL -- Кидает n-гранную кость по числу, введенное пользователем.


@bot.message_handler(commands=['rtd'])
def dice_roll(message):
    dice_rolled = randint(1, 100)
    bot.reply_to(message, f'Кость была брошена, и на ней выпало число...'
                          f'\n\n<b>{dice_rolled}!</b>', parse_mode='html')


# ------------------------------------------------------------------------------------

# -- QUOTE -- Пишет случайную цитату и его автора, с помощью QUOTABLE API, пишет на английском

@bot.message_handler(commands=['quote'])
def quote(message):
    quotable_get_text = requests.get('https://api.quotable.io/random')
    quote_get = quotable_get_text.json()

    bot.send_message(message.chat.id, f'{quote_get["content"]} - {quote_get["author"]}')


# ------------------------------------------------------------------------------------

# -- 8BALL -- Выводит случайный результат шара восьмерки

@bot.message_handler(commands=['8ball'])
def eightball(message):
    variants = ["Бесспорно", "Предрешено", "Без сомнения", "Да, определенно", "Можешь на это рассчитывать",
                "Как я вижу, да", "Самое вероятное", "Вероятно", "Знаки указывают на да", "Да", "Ответ положительный",
                "Не могу сейчас сказать, попробуй снова", "Спроси позже", "Лучше не говорить тебе сейчас",
                "Сейчас нельзя предсказать", "Сосредоточься и спроси опять", "Не надейся", "Мой ответ - нет",
                "Мои источники говорят - нет", "По моим данным - нет", "Перспективы не очень хорошие",
                "Весьма сомнительно", "Нет", "Ответ отрицательный"]

    bot.send_message(message.chat.id, variants[randint(0, len(variants) - 1)])


# ------------------------------------------------------------------------------------

# -- CAT -- Выводит фото случайного котика с помощью THECATAPI

@bot.message_handler(commands=['cat'])
def cat(message):
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    if response.status_code == 200:
        data = response.json()
        image_url = data[0]['url']
        bot.send_photo(message.chat.id, image_url)
    else:
        bot.send_message(message.chat.id, 'Возникла ошибка при выполнении команды')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Провкрка сообщений на ключевые слова с обычных сообщений:


@bot.message_handler(func=lambda message: message.content_type == 'text')
def commands_in_text(message):
    # Основные кнопки:

    if message.text == '🔙 Вернуться':
        bot.send_message(message.chat.id, 'Список команд: /menu', reply_markup=types.ReplyKeyboardRemove())

    # -----------------------------------------------------------------

    # Проверка ключевых слов с команды BLACKLISTED_WORDS:
    if message.text == '✅ Добавить слова':
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
                bot.send_message(message.chat.id, 'Сейчас вы будете добавлять фразы в список.\n'
                                                  '🔹 <b>Формат:</b> \n'
                                                  'Первая строка - команда <b>//bwl_add</b>,\n'
                                                  'Последующие - слово, <i>пробел</i>, последствие.\n'
                                                  '🔸 <b>Типы последствий: </b>\n'
                                                  '<b>a</b> - предупредить,\n'
                                                  '<b>m</b> - заглушить на час, \n'
                                                  '<b>k</b> - кикнуть\n'
                                                  'Каждая фраза на отдельных строках',
                                 reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')

        elif message.chat.type == 'private':
            bot.send_message(message.chat.id, 'Сейчас вы будете добавлять фразы в список.\n'
                                              '🔹 <b>Формат: </b>\n'
                                              'Первая строка - команда <b>//bwl_add</b>,\n'
                                              'Вторая строка - <i>Код группы</i>\n'
                                              'Последующие - слово, <i>пробел</i>, последствие.\n'
                                              '🔸 <b>Типы последствий: </b>\n'
                                              '<b>a</b> - предупредить,\n'
                                              '<b>m</b> - заглушить на час, \n'
                                              '<b>k</b> - кикнуть\n'
                                              'Каждая фраза на отдельных строках',
                             reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')

    # -----------------------------------------------------------------

    elif message.text == '❌ Удалить слова':
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
                bot.send_message(message.chat.id, 'Сейчас вы будете удалять фразы из списка.\n'
                                                  '🔹 <b>Формат:</b> \n'
                                                  'Первая строка - команда <b>//bwl_remove</b>\n'
                                                  'Последующие - слово.\n'
                                                  'Каждая фраза на отдельных строках!',
                                 reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')

        elif message.chat.type == 'private':
            bot.send_message(message.chat.id, 'Сейчас вы будете удалять фразы из списка.\n'
                                              '🔹 <b>Формат:</b> \n'
                                              'Первая строка - команда <b>//bwl_remove</b>\n'
                                              'Вторая строка - <i>Код группы</i>\n'
                                              'Последующие - слово.\n'
                                              'Каждая фраза на отдельных строках!',
                             reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')

    # -----------------------------------------------------------------

    elif message.text == '➡ Просмотреть список' and message.chat.type == 'private':
        bot.send_message(message.chat.id, 'Введите команду <b>//bwl_show_list {Код группы}</b>',
                         reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
    # -----------------------------------------------------------------

    elif message.text == '💥 Удалить список':
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
                bot.send_message(message.chat.id, 'Сейчас вы будете удалять список. \n'
                                                  'Для этого введите команду <b>//bwl_delete</b>',
                                 reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')

        elif message.chat.type == 'private':
            bot.send_message(message.chat.id, 'Сейчас вы будете удалять список. \n'
                                              'Для этого введите команду <b>//bwl_delete {Код группы}</b>',
                             reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')

    # -----------------------------------------------------------------
    # -----------------------------------------------------------------

    # Проверка ключевых слов с команды BLACKLISTED_TYPES:
    elif message.text == '✅ Изменить список типов':
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
                bot.send_message(message.chat.id, 'Сейчас вы будете добавлять новый список запрещенных типов.\n'
                                                  'Возможные запрещенные типы:\n'
                                                  'audio, photo, voice, video, document, \n'
                                                  'location, contact, sticker\n'
                                                  '🔹 <b>Формат:</b> \n'
                                                  'Первая строка - команда <b>//btl_set</b>,\n'
                                                  'Последующие - тип из списка.\n'
                                                  'Каждая фраза на отдельных строках\n'
                                                  'Чтобы очистить список, напишите что-либо не являющимся типом',
                                 reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
        elif message.chat.type == 'private':
            bot.send_message(message.chat.id, 'Сейчас вы будете добавлять новый список запрещенных типов.\n'
                                              'Возможные запрещенные типы:\n'
                                              'audio, photo, voice, video, document, \n'
                                              'location, contact, sticker\n'
                                              '🔹 <b>Формат:</b> \n'
                                              'Первая строка - команда <b>//btl_set</b>,\n'
                                              'Вторая строка - <i>Код группы</i>\n'
                                              'Последующие - тип из списка.\n'
                                              'Каждая фраза на отдельных строках\n'
                                              'Чтобы очистить список, напишите что-либо не являющимся типом',
                             reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')

    # -----------------------------------------------------------------

    elif message.text == '➡ Просмотреть список типов' and message.chat.type == 'private':

        bot.send_message(message.chat.id, 'Введите команду <b>//btl_show_list {Код группы}</b>',
                         reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Быстрые команды BLACKLISTED_WORDS:

    if '//bwl_add' in message.text:

        # ДЛЯ ГРУПП - ДОБАВЛЕНИЕ ФРАЗ - СЛОВА
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
                log = 'Изменения сохранены'
                try:
                    wrd_list = [[m.lower() for m in n.split(' ')] for n in message.text.split('\n')[1:]
                                if n.split(' ')[1].lower() in 'mka']

                    con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                    cur = con.cursor()

                    cur.executemany("INSERT OR IGNORE INTO Banned_words VALUES (?, ?) ",
                                    wrd_list)
                    con.commit()
                    con.close()
                except Exception:
                    log = 'Некорректный ввод'

                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, log)

        # ДЛЯ ЛС БОТА - ДОБАВЛЕНИЕ ФРАЗ - СЛОВА
        elif message.chat.type == 'private':
            log = 'Изменения сохранены'
            try:
                wrd_list = [[m.lower() for m in n.split(' ')] for n in message.text.split('\n')[2:]
                            if n.split(' ')[1].lower() in 'mka']
                chat_id = message.text.split('\n')[1]
                db_name = 'DB' + chat_id + 'S8.db'

                if os.path.exists(db_name):
                    con = sqlite3.connect(db_name)
                else:
                    raise Exception

                cur = con.cursor()

                check = (cur.execute("SELECT admin FROM Admins WHERE admin = ?",
                                     (message.from_user.username,)).fetchone())

                if check:
                    cur.executemany("INSERT OR IGNORE INTO Banned_words VALUES (?, ?) ",
                                    wrd_list)
                    con.commit()
                    con.close()
                else:
                    log = 'Вы не являетесь админом группы'

            except Exception:
                log = 'Некорректный ввод'

            bot.send_message(message.chat.id, log)

    # -----------------------------------------------------------------

    if '//bwl_remove' in message.text:

        # ДЛЯ ГРУПП - УДАЛЕНИЕ ФРАЗ - СЛОВА
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
                log = 'Изменения сохранены'
                try:
                    wrd_list = [n.strip(' ') for n in message.text.split('\n')[1:]]

                    con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                    cur = con.cursor()

                    for word in wrd_list:
                        try:
                            cur.execute("DELETE FROM Banned_words WHERE phrase = ?", (word,))
                        except Exception:
                            pass
                        con.commit()

                    con.close()
                except Exception:
                    log = 'Некорректный ввод'

                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, log)

        # ДЛЯ ЛС БОТА - УДАЛЕНИЕ ФРАЗ - СЛОВА
        elif message.chat.type == 'private':
            log = 'Изменения сохранены'
            try:
                wrd_list = [n.strip(' ') for n in message.text.split('\n')[2:]]
                chat_id = message.text.split('\n')[1]
                db_name = 'DB' + chat_id + 'S8.db'

                if os.path.exists(db_name):
                    con = sqlite3.connect(db_name)
                else:
                    raise Exception

                cur = con.cursor()

                check = (cur.execute("SELECT admin FROM Admins WHERE admin = ?",
                                     (message.from_user.username,)).fetchone())

                if check:
                    for word in wrd_list:
                        try:
                            cur.execute("DELETE FROM Banned_words WHERE phrase = ?", (word,))
                        except Exception:
                            pass
                        con.commit()
                    con.close()

                else:
                    log = 'Вы не являетесь админом группы'

            except Exception:
                log = 'Некорректный ввод'

            bot.send_message(message.chat.id, log)

    # -----------------------------------------------------------------

    if '//bwl_show_list' in message.text or message.text == '➡ Просмотреть список':

        # ДЛЯ ГРУПП - ПОКАЗАТЬ СПИСОК - СЛОВА
        if message.chat.type in ['group', 'supergroup'] and message.text == '➡ Просмотреть список':
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):

                log = 'Неожиданная ошибка'

                try:
                    con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                    cur = con.cursor()

                    raw_list = cur.execute("SELECT * FROM Banned_words").fetchall()
                    con.close()

                    full_list = '\n'.join([' : '.join(n) for n in raw_list])
                    if full_list:
                        log = 'Список запрещенных слов:\n' + full_list
                    else:
                        log = 'В списке нет запрещенных слов'

                except Exception:
                    pass

                if message.text != '➡ Просмотреть список':
                    bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, log, reply_markup=types.ReplyKeyboardRemove())

        # ДЛЯ ЛС БОТА - ПОКАЗАТЬ СПИСОК - СЛОВА
        elif message.chat.type == 'private' and message.text != '➡ Просмотреть список':
            try:
                chat_id = message.text.split(' ')[1].strip(' ')
                db_name = 'DB' + chat_id + 'S8.db'

                if os.path.exists(db_name):
                    con = sqlite3.connect(db_name)
                else:
                    raise Exception

                cur = con.cursor()

                check = (cur.execute("SELECT admin FROM Admins WHERE admin = ?",
                                     (message.from_user.username,)).fetchone())

                if check:
                    raw_list = cur.execute("SELECT * FROM Banned_words").fetchall()
                    con.close()

                    full_list = '\n'.join([' : '.join(n) for n in raw_list])
                    if full_list:
                        log = 'Список запрещенных слов:\n' + full_list
                    else:
                        log = 'В списке нет запрещенных слов'

                else:
                    log = 'Вы не являетесь админом группы'

            except Exception:
                log = 'Некорректный ввод'

            bot.send_message(message.chat.id, log)

    # -----------------------------------------------------------------

    if '//bwl_delete' in message.text:

        # ДЛЯ ГРУПП - УДАЛИТЬ СПИСОК - СЛОВА
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):

                log = 'Неожиданная ошибка'

                try:
                    con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                    cur = con.cursor()

                    cur.execute("DELETE FROM Banned_words")
                    con.commit()
                    con.close()

                    log = 'Список успешно удален'

                except Exception:
                    pass

                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, log)

        # ДЛЯ ЛС БОТА - УДАЛИТЬ СПИСОК - СЛОВА
        elif message.chat.type == 'private':
            try:

                chat_id = message.text.split(' ')[1].strip(' ')
                db_name = 'DB' + chat_id + 'S8.db'

                if os.path.exists(db_name):
                    con = sqlite3.connect(db_name)
                else:
                    raise Exception

                cur = con.cursor()

                check = (cur.execute("SELECT admin FROM Admins WHERE admin = ?",
                                     (message.from_user.username,)).fetchone())

                if check:
                    cur.execute("DELETE FROM Banned_words")
                    con.commit()
                    con.close()
                    log = 'Список успешно удален'

                else:
                    log = 'Вы не являетесь админом группы'

            except Exception:
                log = 'Некорректный ввод'

            bot.send_message(message.chat.id, log)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Быстрые команды BLACKLISTED_TYPES:
    if '//btl_set' in message.text:

        # ДЛЯ ГРУПП - ДОБАВИТЬ СПИСОК - ТИПЫ
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):

                log = 'Изменения сохранены'
                try:
                    allowed = ['audio', 'photo', 'voice', 'video', 'document', 'location', 'contact', 'sticker']
                    written_types = message.text.split('\n')[1:]

                    con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                    cur = con.cursor()

                    cur.execute("DELETE FROM Banned_types")
                    con.commit()

                    for ttype in written_types:
                        if ttype.strip(' ').lower() in allowed:
                            try:
                                cur.execute("INSERT OR IGNORE INTO Banned_types VALUES (?) ",
                                            (ttype.strip(' ').lower(),))
                            except Exception:
                                pass

                    con.commit()
                    con.close()

                except Exception:
                    log = 'Некорректный ввод'

                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, log)

        # ДЛЯ ЛС БОТА - ДОБАВИТЬ СПИСОК - ТИПЫ
        if message.chat.type == 'private':
            log = 'Изменения сохранены'
            try:
                allowed = ['audio', 'photo', 'voice', 'video', 'document', 'location', 'contact', 'sticker']
                written_types = message.text.split('\n')[2:]

                chat_id = message.text.split('\n')[1].strip(' ')
                db_name = 'DB' + chat_id + 'S8.db'

                if os.path.exists(db_name):
                    con = sqlite3.connect(db_name)
                else:
                    raise Exception

                cur = con.cursor()

                check = (cur.execute("SELECT admin FROM Admins WHERE admin = ?",
                                     (message.from_user.username,)).fetchone())

                if check:
                    cur.execute("DELETE FROM Banned_types")
                    con.commit()
                    for ttype in written_types:
                        if ttype.strip(' ').lower() in allowed:
                            try:
                                cur.execute("INSERT OR IGNORE INTO Banned_types VALUES (?) ",
                                            (ttype.strip(' ').lower(),))
                            except Exception:
                                pass

                else:
                    log = 'Вы не являетесь админом группы'

                con.commit()
                con.close()

            except Exception:
                log = 'Некорректный ввод'

            bot.send_message(message.chat.id, log)

        # -----------------------------------------------------------------

    # ДЛЯ ГРУПП - ПОКАЗАТЬ СПИСОК - ТИПЫ
    if message.text == '//btl_show_list' or message.text == '➡ Просмотреть список типов':
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):

                log = 'Неожиданная ошибка'

                try:
                    con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                    cur = con.cursor()

                    raw_list = cur.execute("SELECT * FROM Banned_types").fetchall()
                    con.close()

                    full_list = '\n'.join([''.join(n) for n in raw_list])
                    if full_list:
                        log = 'Список запрещенных типов:\n' + full_list
                    else:
                        log = 'В списке нет запрещенных типов'

                except Exception:
                    pass

                if message.text != '➡ Просмотреть список типов':
                    bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, log, reply_markup=types.ReplyKeyboardRemove())

        # ДЛЯ ЛС БОТА - ПОКАЗАТЬ СПИСОК - ТИПЫ

        if message.chat.type == 'private' and message.text != '➡ Просмотреть список типов':
            log = 'Неожиданная ошибка'

            try:
                chat_id = message.text.split(' ')[1].strip(' ')
                db_name = 'DB' + chat_id + 'S8.db'

                if os.path.exists(db_name):
                    con = sqlite3.connect(db_name)
                else:
                    raise Exception

                cur = con.cursor()

                check = (cur.execute("SELECT admin FROM Admins WHERE admin = ?",
                                     (message.from_user.username,)).fetchone())

                if check:
                    raw_list = cur.execute("SELECT * FROM Banned_types").fetchall()
                    con.close()

                    full_list = '\n'.join([''.join(n) for n in raw_list])
                    if full_list:
                        log = 'Список запрещенных типов:\n' + full_list
                    else:
                        log = 'В списке нет запрещенных типов'
                else:
                    log = 'Вы не являетесь админом группы'

            except Exception:
                pass

            bot.send_message(message.chat.id, log, reply_markup=types.ReplyKeyboardRemove())

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Быстрые команды (Только команда):
    if message.text == '//mdata':
        if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, str(message)[:4047])

    # -----------------------------------------------------------------

    elif message.text == '//get_group_id':
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, message.chat.id)

    # -----------------------------------------------------------------

    elif message.text == '//add_to_admin_list':
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
                con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                cur = con.cursor()

                cur.execute("INSERT OR IGNORE INTO Admins VALUES (?) ", tuple([str(message.from_user.username)]))
                con.commit()
                con.close()

                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, 'Список успешно изменен')

    # -----------------------------------------------------------------

    elif message.text == '//members':
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
                try:
                    con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                    cur = con.cursor()
                    done = cur.execute("SELECT username FROM User_ids").fetchall()
                    con.close()
                    bot.send_message(message.chat.id, '\n'.join([''.join(n) for n in done])[:4047])
                except Exception:
                    print('Ошибка с подкючением к БД')

                bot.delete_message(message.chat.id, message.message_id)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Быстрые команды (С параметрами)
    if '//mute' in message.text:
        log = 'Неверный ввод'
        if message.chat.type in ['group', 'supergroup']:
            try:
                splitt = message.text.split(' ')
                username = splitt[1].strip('@')

                con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                cur = con.cursor()
                user_id = cur.execute("SELECT username, id FROM User_ids").fetchall()
                con.close()

                user_id = user_id[[n[0] for n in user_id].index(username)][1]

                mt = splitt[2].split(':')

                try:
                    bot.restrict_chat_member(message.chat.id, user_id,
                                             until_date=(message.date + int(mt[0]) * 3600 * 24 + int(mt[1]) * 3600 +
                                                         int(mt[2]) * 60),
                                             can_send_messages=False)
                except Exception:
                    log = 'Неверный пользователь'
                    raise Exception

                bot_mute_message = []
                if int(mt[2]) != 0:
                    bot_mute_message.append(str(mt[2]) + ' минут')
                if int(mt[1]) != 0:
                    bot_mute_message.append(str(mt[1]) + ' часов')
                if int(mt[0]) != 0:
                    bot_mute_message.append(str(mt[0]) + ' дней')
                bot_mute_message = ', '.join(bot_mute_message)

                bot.send_message(message.chat.id, f'@{username} теперь в муте на: {bot_mute_message}')
            except Exception:
                bot.send_message(message.chat.id, log)

            bot.delete_message(message.chat.id, message.message_id)

        else:
            bot.send_message(message.chat.id, 'Команда работает только в группах')

    # -----------------------------------------------------------------
    elif '//unmute' in message.text:
        if message.chat.type in ['group', 'supergroup']:

            log = 'Неверный ввод'

            try:
                splitt = message.text.split(' ')
                username = splitt[1].strip('@')

                con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                cur = con.cursor()
                user_id = cur.execute("SELECT username, id FROM User_ids").fetchall()
                con.close()

                user_id = user_id[[n[0] for n in user_id].index(username)][1]

                try:
                    bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=True)
                except Exception:
                    log = 'Неверный пользователь'
                    raise Exception

                bot.send_message(message.chat.id, f'@{username} может продолжать общение')
            except Exception:
                bot.send_message(message.chat.id, log)

            bot.delete_message(message.chat.id, message.message_id)

        else:
            bot.send_message(message.chat.id, 'Команда работает только в группах')

    # -----------------------------------------------------------------

    elif '//remove_from_admin_list' in message.text:
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
                log = 'Список успешно изменен'

                try:

                    splitt = message.text.split(' ')
                    username = splitt[1].strip('@').strip(' ')

                    con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                    cur = con.cursor()

                    user_id = cur.execute("SELECT username, id FROM User_ids").fetchall()
                    user_id = user_id[[n[0] for n in user_id].index(username)][1]

                    if str(bot.get_chat_member(message.chat.id, user_id).status) not in ('creator', 'administrator'):
                        cur.execute("DELETE FROM Admins WHERE admin = ?", (username,))
                        con.commit()
                        con.close()
                    else:
                        log = 'Ползователь всё ещё админ'

                except Exception:
                    print('Неверный ввод')

                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, log)

        else:
            bot.send_message(message.chat.id, 'Команда работает только в группах')

    # -----------------------------------------------------------------

    elif '//kick' in message.text:
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
                splitt = message.text.split(' ')
                username = splitt[1].strip('@').strip(' ')
                user_id = ''

                log = f'Пользователь @{username} был кикнут из группы'

                con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                cur = con.cursor()

                try:
                    user_id = cur.execute("SELECT username, id FROM User_ids").fetchall()
                    user_id = user_id[[n[0] for n in user_id].index(username)][1]
                except Exception:
                    log = 'Некорректный ввод'

                try:
                    bot.kick_chat_member(message.chat.id, user_id)
                    time.sleep(0.1)
                    bot.unban_chat_member(message.chat.id, user_id)
                except Exception:
                    log = 'Пользователь админ'

                bot.send_message(message.chat.id, log)

    # -----------------------------------------------------------------

    elif '//ban' in message.text:
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
                splitt = message.text.split(' ')
                username = splitt[1].strip('@').strip(' ')
                user_id = ''

                log = f'Пользователь @{username} был забанен'

                con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                cur = con.cursor()

                try:
                    user_id = cur.execute("SELECT username, id FROM User_ids").fetchall()
                    user_id = user_id[[n[0] for n in user_id].index(username)][1]
                except Exception:
                    log = 'Некорректный ввод'

                try:
                    bot.kick_chat_member(message.chat.id, user_id)
                except Exception:
                    log = 'Возникла ошибка'

                bot.send_message(message.chat.id, log)

    # -----------------------------------------------------------------

    elif '//unban' in message.text:
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
                splitt = message.text.split(' ')
                username = splitt[1].strip('@').strip(' ')
                user_id = ''

                log = f'Пользователь @{username} был разбанен'

                con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                cur = con.cursor()

                try:
                    user_id = cur.execute("SELECT username, id FROM User_ids").fetchall()
                    user_id = user_id[[n[0] for n in user_id].index(username)][1]
                except Exception:
                    log = 'Некорректный ввод'

                try:
                    bot.unban_chat_member(message.chat.id, user_id)
                except Exception:
                    log = 'Возникла ошибка'

                bot.send_message(message.chat.id, log)

    # -----------------------------------------------------------------

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Быстрые команды (На замену)

    if '//rtd' in message.text:
        try:
            replaced_message = re.sub(r'//rtd', str(randint(4, 100)), message.text)

            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, f'@{message.from_user.username}:\n{replaced_message}')
        except Exception:
            bot.send_message(message.chat.id, 'Возникла неожиданная ошибка')

    # -----------------------------------------------------------------

    elif '//coin_flip' in message.text:
        try:
            coin = ['орёл', 'решка'][randint(0, 1)]
            replaced_message = re.sub(r'//coin_flip', coin, message.text)

            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, f'@{message.from_user.username}:\n{replaced_message}')
        except Exception:
            bot.send_message(message.chat.id, 'Возникла неожиданная ошибка')

    # -----------------------------------------------------------------

    elif '//pick_user' in message.text:
        if message.chat.type in ['group', 'supergroup']:
            try:
                con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                cur = con.cursor()
                done = cur.execute("SELECT username FROM User_ids").fetchall()
                con.close()

                user = choice([''.join(n) for n in done])

                replaced_message = re.sub(r'//pick_user', '@' + str(user), message.text)

                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, f'@{message.from_user.username}:\n{replaced_message}')
            except Exception:
                bot.send_message(message.chat.id, 'Возникла неожиданная ошибка')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    if message.chat.type in ['group', 'supergroup']:
        # Заполнение базы User_ids
        con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
        cur = con.cursor()

        cur.execute("INSERT OR IGNORE INTO User_ids VALUES(?, ?) ",
                    tuple([str(message.from_user.username).strip('@'), str(message.from_user.id)]))
        con.commit()

        # Проверка на нелегальные ключевые слова

        bwlist = cur.execute("SELECT * FROM Banned_words").fetchall()
        result = 'n'

        con.close()

        for bw in bwlist:
            if bw[0] in message.text.lower():
                if bw[1] == 'k':
                    result = 'k'

                if bw[1] == 'm' and result != 'k':
                    result = 'm'

                if bw[1] == 'a' and result != 'm' and result != 'k':
                    result = 'a'

        if result == 'k':
            try:
                bot.kick_chat_member(message.chat.id, message.from_user.id)
                time.sleep(0.1)
                bot.unban_chat_member(message.chat.id, message.from_user.id)

                bot.send_message(message.chat.id, f'Ползователь @{message.from_user.username} был кикнут '
                                                  f'из группы за использование запрещенных слов')
            except Exception:
                pass

        elif result == 'm':
            try:
                bot.restrict_chat_member(message.chat.id, message.from_user.id,
                                         until_date=(message.date + 3600))
                bot.send_message(message.chat.id, f'Ползователь @{message.from_user.username} был заглушен '
                                                  f'на час за использование запрещенных слов')
            except Exception:
                pass

        elif result == 'a':
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) not in (
                    'creator', 'administrator'):
                bot.reply_to(message, f'@{message.from_user.username}, вы использовали слово, '
                                      f'входящее в список запрещенных.\n'
                                      f'Администраторы группы могут принять меры \n[bwl_alert]')


# Допуск сообщений
@bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
                                                               'location', 'contact', 'sticker'])
def parse_message(message):
    if message.chat.type in ['group', 'supergroup']:

        con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
        cur = con.cursor()

        btlist = cur.execute("SELECT * FROM Banned_types").fetchall()

        con.close()

        types_list = [''.join(n) for n in btlist]

        # Проверка на легальный тип сообщения
        if message.content_type in types_list:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) not in (
                    'creator', 'administrator'):
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                except Exception:
                    pass


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

bot.polling(none_stop=True)
