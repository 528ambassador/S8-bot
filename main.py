import telebot
import sqlite3
from random import randint
from telebot import types


# Ссылка на бота С8:
bot = telebot.TeleBot('7066300352:AAHoKT8LAaZd4pdnkbU3vlzBijI25bM7Xqo')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Основные команды:


# --  START -- Начало общения с ботом, выводит на экран приветствие и несколько комманд

@bot.message_handler(commands=['start'])
def start(message):

    if message.chat.type == 'private':
        bot.send_message(message.chat.id, f'Привет! Я бот для регулировки групп S8. \n'
                                          f'Чтобы получить полный функционал, добавьте бота в свою группу.\n'
                                          f'Что я могу:\n'
                                          f'◻ Удалять сообщения с ключевыми словами\n'
                                          f'◻ Посылать в мут* пользователей группы\n'
                                          f'◻ Решать споры с монеткой или костью\n'
                                          f'◻ Запустить одну из 3 игр для всей группы\n'
                                          f'Список всех команд: /menu\n'
                                          f'Список разрешений: /permissions')
    else:
        bot.send_message(message.chat.id, f'Всем привет! Я бот для регулировки групп S8. \n'
                                          f'Что я могу:\n'
                                          f'🔹 Удалять сообщения с ключевыми словами\n'
                                          f'🔹 Посылать в мут* пользователей группы\n'
                                          f'🔹 Решать споры с монеткой или костью\n'
                                          f'🔹 Запустить одну из 3 игр для всей группы\n'
                                          f'Список всех команд: /menu\n'
                                          f'Список разрешений: /permissions')

        group_db_name = 'DB' + str(message.chat.id) + 'S8'
        con = sqlite3.connect(group_db_name)
        cur = con.cursor()
        
        # НЕ РАБОТАЕТ
        cur.execute("""CREATE TABLE IF NOT EXISTS 
                        admins_ids(admin TEXT UNIQUE)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS 
                        banned_words_list(phrase, punishment_type)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS 
                        mute_list(muted_user, date_start, date_finish)""")
        con.commit()


# ------------------------------------------------------------------------------------

# -- MENU -- Список всех команд, выводит одним сообщением.


@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(message.chat.id, 'Список команд:\n'
                                      '/start - Начало разговора\n'
                                      '/menu - Меню со всеми командами\n'
                                      '/permissions - Разрешения для бота и участников группы\n'
                                      '/blacklisted_words - Управление запрещенными словами\n'
                                      '/mute_list - Список участников в муте\n'
                                      '/coin_flip - Подбрасывает монетку\n'
                                      '/dice_roll - Кидает кость\n'
                                      '/play_game - Запускает игру\n'
                                      '/anecdote - Печатает случайный анекдот')


# ------------------------------------------------------------------------------------


# -- BLACKLISTED_WORDS -- Работа с нелегальными словами


@bot.message_handler(commands=['blacklisted_words'])
def blacklisted_words_main(message):
    if message.chat.type != 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        btn1 = types.KeyboardButton('✅ Добавить слова')
        btn2 = types.KeyboardButton('❌ Удалить слова')
        btn3 = types.KeyboardButton('➡ Просмотреть список')
        btn4 = types.KeyboardButton('💥 Удалить список')
        btn5 = types.KeyboardButton('🔙 Вернуться')

        markup.add(btn1, btn2, btn3, btn4, btn5)

        bot.reply_to(message, 'Сейчас вы изменяете список запрещенных слов в группе.\n'
                              'Выберите один из варинатов чтобы продолжить.', reply_markup=markup)

    else:
        bot.reply_to(message, 'Изменить список запрещенных слов можно только в группе')


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


@bot.message_handler(commands=['dice_roll'])
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
        # bot.delete_message(message.chat.id, message.reply_to_message.message_id)
        bot.send_message(message.chat.id, 'Список команд: /menu')

    # -----------------------------------------------------------------

    # Проверка ключевых слов с команды BLACKLISTED_WORDS:

    # Первая ветка после BLACKLISTED_WORDS:
    if message.text == '✅ Добавить слова':
        # bot.delete_message(message.chat.id, message.reply_to_message.message_id)
        bot.send_message(message.chat.id, 'Харош! 1', reply_markup=None)

    elif message.text == '❌ Удалить слова':
        # bot.delete_message(message.chat.id, message.reply_to_message.message_id)
        bot.send_message(message.chat.id, 'Харош! 2')

    elif message.text == '➡ Просмотреть список':
        # bot.delete_message(message.chat.id, message.reply_to_message.message_id)
        bot.send_message(message.chat.id, 'Харош! 3')

    elif message.text == '💥 Удалить список':
        # bot.delete_message(message.chat.id, message.reply_to_message.message_id)
        bot.send_message(message.chat.id, 'Харош! 4')

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

    # -----------------------------------------------------------------

    # Тестирование
    if message.text == '//rofls':
        bot.send_message(message.chat.id, str(message)[:4047])
    elif message.text == '//add_to_admin_list':
        if message.chat.type != 'private':
            bot.send_message(message.chat.id, "Ваш статус - " +
                             str(bot.get_chat_member(message.chat.id, message.from_user.id).status))
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):

                # НЕ РАБОТАЕТ

                con = sqlite3.connect('DB' + str(message.chat.id) + 'S8')
                cur = con.cursor()

                try:
                    cur.execute("INSERT INTO admins_ids VALUES (?) ", str(message.from_user.id))
                    con.commit()

                except sqlite3.IntegrityError:
                    pass

                res = cur.execute("SELECT admin FROM admins_ids").fetchall()

                bot.send_message(message.chat.id, str([n for n in res]))
                con.close()
                cur.close()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


bot.polling(none_stop=True)
