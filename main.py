import telebot
import sqlite3
# Scary!
import re
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
        bot.send_message(message.chat.id, f'Привет! Я бот для регулировки групп S8. \n'
                                          f'Чтобы получить полный функционал, добавьте бота в свою группу.\n'
                                          f'Что я могу:\n'
                                          f'🔹 Удалять сообщения с ключевыми словами\n'
                                          f'🔹 Посылать в мут* пользователей группы\n'
                                          f'🔹 Решать споры с монеткой или костью\n'
                                          f'🔹 Запустить одну из 3 игр для всей группы\n'
                                          f'Список всех команд: /menu')
    else:
        bot.send_message(message.chat.id, f'Всем привет! Я бот для регулировки групп S8. \n'
                                          f'Что я могу:\n'
                                          f'🔹 Удалять сообщения с ключевыми словами\n'
                                          f'🔹 Посылать в мут* пользователей группы\n'
                                          f'🔹 Решать споры с монеткой или костью\n'
                                          f'🔹 Запустить одну из 3 игр для всей группы\n'
                                          f'Список всех команд: /menu')

        group_db_name = 'DB' + str(message.chat.id) + 'S8.db'

        con = sqlite3.connect(group_db_name)
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS 
                        Admins(admin TEXT UNIQUE)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS 
                        Banned_words(phrase TEXT UNIQUE, punishment_type TEXT)""")

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
                                      '/blacklisted_words - ❗ - Управление запрещенными словами\n'
                                      '/coin_flip - Подбрасывает монетку\n'
                                      '/rtd - Кидает кость\n'
                                      '/play_game - ❗ - Запускает игру\n'
                                      '/anecdote - Печатает случайный анекдот')


# ------------------------------------------------------------------------------------

# -- QUICK_MENU -- Список всех быстрых команд, начинающиеся с //, все 3 вида

@bot.message_handler(commands=['quick_menu'])
def menu(message):
    bot.send_message(message.chat.id, 'Список быстрых команд - они вводятся как сообщения.\n'
                                      '(❗ - доступно только администраторам)\n'
                                      '-- Только команда:\n'
                                      '//mdata - ❗ - присылает сырые данные сообщения\n'
                                      '//get_to_admin_list - ❗ - добавляет в список админов группы\n'
                                      '//get_group_id - ❗ - присылает код группы\n'
                                      '//members - присылает список участников группы\n\n'
                                      '-- Команда с параметрами\n'
                                      '//mute \n//unmute \n//remove_from_admin_list')


# ------------------------------------------------------------------------------------


# -- BLACKLISTED_WORDS -- Работа с нелегальными словами


@bot.message_handler(commands=['blacklisted_words'])
def blacklisted_words_main(message):
    if message.chat.type in ['group', 'supergroup']:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        btn1 = types.KeyboardButton('✅ Добавить слова')
        btn2 = types.KeyboardButton('❌ Удалить слова')
        btn3 = types.KeyboardButton('➡ Просмотреть список')
        btn4 = types.KeyboardButton('💥 Удалить список')
        btn5 = types.KeyboardButton('🔙 Вернуться')

        markup.add(btn1, btn2, btn3, btn4, btn5)

        bot.reply_to(message, 'Сейчас вы изменяете список запрещенных слов в группе.\n'
                              'Выберите один из варинатов чтобы продолжить.', reply_markup=markup)
    elif message.chat.type == 'private':
        bot.send_message(message.chat.id, f'Если вы являетесь админом группы, ответьте на ваше предыдущее сообщение '
                                          f'с командой и напишите код вашей группы.\nДля этого нужно прописать в '
                                          f'группе -\n //get_group_id - получить код группы\n//add_to_admin_list - '
                                          f'Чтобы мне знать, что вы являетесь админом')

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
    bot.reply_to(message, 'Наберите значение сторон кости (4-100) и <em>перешлите сообщение,'
                          ' где вы вводили команду</em>', parse_mode='html')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Провкрка сообщений на ключевые слова с обычных сообщений:


@bot.message_handler(func=lambda message: True)
def commands_in_text(message):
    # Основные кнопки:

    if message.text == '🔙 Вернуться':
        bot.send_message(message.chat.id, 'Список команд: /menu', reply_markup=types.ReplyKeyboardRemove())

    # -----------------------------------------------------------------

    # Проверка ключевых слов с команды BLACKLISTED_WORDS:
    if message.text == '✅ Добавить слова':
        bot.send_message(message.chat.id, 'Харош! 1', reply_markup=types.ReplyKeyboardRemove())

    elif message.text == '❌ Удалить слова':
        bot.send_message(message.chat.id, 'Харош! 2', reply_markup=types.ReplyKeyboardRemove())

    elif message.text == '➡ Просмотреть список':
        bot.send_message(message.chat.id, 'Харош! 3', reply_markup=types.ReplyKeyboardRemove())

    elif message.text == '💥 Удалить список':
        bot.send_message(message.chat.id, 'Харош! 4', reply_markup=types.ReplyKeyboardRemove())

    # -----------------------------------------------------------------

    # Проверка ключевых слов с команды DICE_ROLL:
    if message.text.isnumeric():
        if message.reply_to_message is not None:
            if message.reply_to_message.from_user.id == message.from_user.id:
                if 4 <= int(message.text) <= 100:
                    dice_rolled = randint(1, int(message.text))
                    bot.reply_to(message, f'Кость была брошена, и на ней выпало число...'
                                          f'\n\n<b>{dice_rolled}!</b>', parse_mode='html')
                else:
                    bot.reply_to(message, 'Неправильное значение кости! Попробуйте снова')

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
                con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                cur = con.cursor()
                done = cur.execute("SELECT username FROM User_ids").fetchall()
                con.close()

                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, '\n'.join([''.join(n) for n in done])[:4047])

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
                                             until_date=message.date + int(mt[0]) * 3600 * 24 + int(mt[1]) * 3600
                                                        + int(mt[2]) * 60,
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

                splitt = message.text.split(' ')
                username = splitt[1].strip('@')

                con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
                cur = con.cursor()

                user_id = cur.execute("SELECT username, id FROM User_ids").fetchall()
                user_id = user_id[[n[0] for n in user_id].index(username)][1]

                if str(bot.get_chat_member(message.chat.id, user_id).status) not in ('creator', 'administrator'):
                    cur.execute("DELETE FROM Admins WHERE admin LIKE '%{user_id}%'")
                    con.commit()
                    con.close()
                else:
                    log = 'Ползователь всё ещё админ'

                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, log)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Быстрые команды (На замену)

    if '//rtd' in message.text:
        replaced_message = re.sub(r'//rtd', str(randint(4, 100)), message.text)

        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, f'@{message.from_user.username}:\n{replaced_message}')

    # -----------------------------------------------------------------

    elif '//coin_flip' in message.text:
        coin = ['орёл', 'решка'][randint(0, 1)]
        replaced_message = re.sub(r'//coin_flip', coin, message.text)

        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, f'@{message.from_user.username}:\n{replaced_message}')

    # -----------------------------------------------------------------

    elif '//pick_user' in message.text:
        if message.chat.type in ['group', 'supergroup']:
            con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
            cur = con.cursor()
            done = cur.execute("SELECT username FROM User_ids").fetchall()
            con.close()

            user = choice([''.join(n) for n in done])

            replaced_message = re.sub(r'//pick_user', '@' + str(user), message.text)

            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, f'@{message.from_user.username}:\n{replaced_message}')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Заполнение базы User_ids

    if message.chat.type in ['group', 'supergroup']:
        con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
        cur = con.cursor()

        cur.execute("INSERT OR IGNORE INTO User_ids VALUES(?, ?) ",
                    tuple([str(message.from_user.username).strip('@'), str(message.from_user.id)]))
        con.commit()
        con.close()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


bot.polling(none_stop=True)
