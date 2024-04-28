import time

import telebot
import sqlite3
# Scary!
import re
from random import randint, choice
from telebot import types
import os

# Ссылка на бота С8:
bot = telebot.TeleBot('7066300352:AAHoKT8LAaZd4pdnkbU3vlzBijI25bM7Xqo')

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class SnakeGame:
    def __init__(self, group_id):
        self.score = None
        self.apple_position = None
        self.snake_segments = None
        self.db_connection = sqlite3.connect(f'DBGAMES' + str(group_id) + 'S8.db')
        self.db_cursor = self.db_connection.cursor()
        self.setup_game()

    def setup_game(self):
        # Создаем таблицу, если она не существует
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS Snake_S8 (
                                    snake_segments TEXT,
                                    apple_position TEXT
                                  )''')
        self.db_connection.commit()

        # Устанавливаем начальное состояние игры
        self.snake_segments = [(3, 3)]  # Сегменты змеи (начинаем в центре)
        self.apple_position = self.generate_new_apple()
        self.score = 0

        # Сохраняем начальное состояние в базу данных
        self.save_game_state()

    def save_game_state(self):
        # Сохраняем текущее состояние игры в базу данных
        self.db_cursor.execute('''INSERT INTO Snake_S8 (snake_segments, apple_position)
                                   VALUES (?, ?)''', (str(self.snake_segments), str(self.apple_position)))
        self.db_connection.commit()

    def generate_new_apple(self):
        # Генерируем новое случайное положение для яблока
        apple_x = randint(0, 6)
        apple_y = randint(0, 6)
        return apple_x, apple_y

    def move_snake(self, direction):
        head_x, head_y = self.snake_segments[0]

        if direction == 'up':
            new_head = (head_x, head_y - 1)
        elif direction == 'down':
            new_head = (head_x, head_y + 1)
        elif direction == 'left':
            new_head = (head_x - 1, head_y)
        elif direction == 'right':
            new_head = (head_x + 1, head_y)
        else:
            return False  # Некорректное направление

        # Проверяем столкновение с телом змеи
        if new_head in self.snake_segments[1:]:
            self.end_game()
            return False

        # Проверяем столкновение с границами карты
        if not (0 <= new_head[0] <= 6 and 0 <= new_head[1] <= 6):
            self.end_game()
            return False

        # Добавляем новую голову к змее
        self.snake_segments.insert(0, new_head)

        # Проверяем, съела ли змея яблоко
        if new_head == self.apple_position:
            self.apple_position = self.generate_new_apple()
            self.score += 1
        else:
            # Удаляем последний сегмент змеи
            self.snake_segments.pop()

        # Сохраняем новое состояние игры
        self.save_game_state()

        return True

    def display_game(self):
        # Выводим игровое поле с использованием эмодзи
        for y in range(7):
            for x in range(7):
                if (x, y) in self.snake_segments:
                    if (x, y) == self.snake_segments[0]:
                        print('🅾️', end=' ')
                    else:
                        print('🟥', end=' ')
                elif (x, y) == self.apple_position:
                    print('🍎', end=' ')
                else:
                    print('🟦', end=' ')
            print()  # Новая строка для следующей строки поля

    def end_game(self):
        print(f"Игра окончена! Ваш счёт: {self.score}")
        self.db_connection.close()
        exit()

# Пример использования
# game = SnakeGame()
# game.display_game()
#
# while True:
#     direction = input("Введите направление (up/down/left/right): ")
#     if game.move_snake(direction):
#         game.display_game()
#     else:
#         print("Некорректное направление. Используйте 'up', 'down', 'left', или 'right'.")


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
                                          f'<b>Некоторые параметры группы я могу изменять в лс</b>'
                                          f'Давайте начнём!', parse_mode='html')

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
                                      '/blacklisted_words -❗- Управление запрещенными словами\n'
                                      '/coin_flip - Подбрасывает монетку\n'
                                      '/rtd - Кидает кость d100\n'
                                      '/play_game -❗- Запускает игру\n'
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
                                      '//game_stop -❗- останавливает идущаю игру\n'
                                      '//members - присылает список участников группы\n\n'
                                      '--- Команды с параметрами\n'
                                      '//mute {@-} {d:h:m} -❗- заглушает полльзователя на d, h, m дней, '
                                      'часов, минут соответственно\n'
                                      '//unmute {@-} -❗- убрать заглушение с пользователя\n'
                                      '//remove_from_admin_list {@-} -❗- убрать из списка админов\n'
                                      '//bwl_add {фраза: последствие}-❗- добавляет в список запрещенных слов список,'
                                      'каждую фразу с последствие писать с новой строки, последствия: m, k, a - '
                                      'заглушить на час, кикнуть, предупредить соответственно\n'
                                      '//bwl_remove {фраза} -❗- вводятся с новой строки, удаляет из списка'
                                      'выбранные фразы если есть\n'
                                      '//bwl_delete -❗- удаляет весь список\n'
                                      '//bwl_show_list -❗- показывает весь список\n'
                                      '//game_start {игра} -❗- запускает выбранную игру (змейка / )\n'
                                      '//poll {выборы} -❗- создает опрос с выборами в виде введеных аргументов,'
                                      'каждый с новой строки \n\n'
                                      '--- Заменяющие команды (бот заменяет команду и пересылает ваше сообщение)\n'
                                      '//coin_flip - заменяется на орёла / решку\n'
                                      '//rtd - заменяется на число 1 - 100\n'
                                      '//pick_user - заменяется случайным пользователем')


# ------------------------------------------------------------------------------------


# -- BLACKLISTED_WORDS -- Работа с нелегальными словами


@bot.message_handler(commands=['blacklisted_words'])
def blacklisted_words_main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
    btn1 = types.KeyboardButton('✅ Добавить слова')
    btn2 = types.KeyboardButton('❌ Удалить слова')
    btn3 = types.KeyboardButton('➡ Просмотреть список')
    btn4 = types.KeyboardButton('💥 Удалить список')
    btn5 = types.KeyboardButton('🔙 Вернуться')

    markup.add(btn1, btn2, btn3, btn4, btn5)

    if message.chat.type in ['group', 'supergroup']:
        bot.reply_to(message, 'Сейчас вы изменяете список запрещенных слов в группе.\n'
                              'Выберите один из варинатов чтобы продолжить.', reply_markup=markup)
    elif message.chat.type == 'private':
        bot.reply_to(message, 'Сейчас вы изменяете список запрещенных слов в группе.\n'
                              'Для этого вам понадобится код вашей группы (инструкция в /start)\n'
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

# -- COIN_FLIP -- Подбрасывает монетку и случайным обрзаом выбирает орла или решку.


@bot.message_handler(commands=['game'])
def snake_start(message):
    g = SnakeGame(message.chat.id)
    g.display_game()

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

    elif message.text == '➡ Просмотреть список':
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
                bot.send_message(message.chat.id, 'Введите команду <b>//bwl_show_list</b>',
                                 reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')

        elif message.chat.type == 'private':
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

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Быстрые команды BLACKLISTED_WORDS:

    if '//bwl_add' in message.text:

        # ДЛЯ ГРУПП - ДОБАВЛЕНИЕ ФРАЗ
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

        # ДЛЯ ЛС БОТА - ДОБАВЛЕНИЕ ФРАЗ
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

        # ДЛЯ ГРУПП - УДАЛЕНИЕ ФРАЗ
        if message.chat.type in ['group', 'supergroup']:
            if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) in ('creator', 'administrator'):
                log = 'Изменения сохранены'
                try:
                    wrd_list = [[m.lower() for m in n.strip(' ')] for n in message.text.split('\n')[1:]]

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

        # ДЛЯ ЛС БОТА - УДАЛЕНИЕ ФРАЗ
        elif message.chat.type == 'private':
            log = 'Изменения сохранены'
            try:
                wrd_list = [[m.lower() for m in n.strip(' ')] for n in message.text.split('\n')[2:]]
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

    if '//bwl_show_list' in message.text:

        # ДЛЯ ГРУПП - ПОКАЗАТЬ СПИСОК
        if message.chat.type in ['group', 'supergroup']:
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

                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, log)

        # ДЛЯ ЛС БОТА - ПОКАЗАТЬ СПИСОК
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

        # ДЛЯ ГРУПП - УДАЛИТЬ СПИСОК
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

        # ДЛЯ ЛС БОТА - УДАЛИТЬ СПИСОК
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

    # Заполнение базы User_ids

    if message.chat.type in ['group', 'supergroup']:
        con = sqlite3.connect('DB' + str(message.chat.id) + 'S8.db')
        cur = con.cursor()

        cur.execute("INSERT OR IGNORE INTO User_ids VALUES(?, ?) ",
                    tuple([str(message.from_user.username).strip('@'), str(message.from_user.id)]))
        con.commit()

        bwlist = cur.execute("SELECT * FROM Banned_words").fetchall()
        con.close()

        result = 'n'

        for bw in bwlist:
            if bw[0] in message.text:
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
                                      f'Администраторы группы могут принять меры [bwl_a]')



# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


bot.polling(none_stop=True)
