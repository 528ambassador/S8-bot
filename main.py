import telebot
from telebot import types

bot = telebot.TeleBot('7066300352:AAHoKT8LAaZd4pdnkbU3vlzBijI25bM7Xqo')


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Арбузы')


@bot.message_handler(commands=['pashalko'])
def main(message):
    bot.send_message(message.chat.id, '<b>Врубаем винтилядоры!!!!!!!!!!!!!!!!!!!!!</b>', parse_mode='html')


@bot.message_handler(commands=['rofls'])
def main(message):
    bot.send_message(message.chat.id, message)


@bot.message_handler(commands=['hello'])
def main(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.username}')


@bot.message_handler(commands=['banned_words'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Пасхалко медный бык', callback_data='useless')
    btn2 = types.InlineKeyboardButton('ещкереее сгма сгма сгма', callback_data='cool')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, f'Что ты выберешшшш па?', reply_markup=markup)
    print('ksko')


@bot.message_handler(func=lambda message: True)
def main(message):
    if 'balls' in message.text:
        bot.send_message(message.chat.id, f'опачки, ваши данный мои лмао олух {message.from_user.id}')
    elif [1 for n in ['пасхалко', '1488', 'вентилятор'] if n in message.text]:
        bot.reply_to(message, f'уффффхпр посхалочка')
    else:
        bot.send_message(message.chat.id, f'Вы сказали "{message.text}"')


@bot.callback_query_handler(func=lambda callback: True)
def magic(callback):
    if callback.data == 'cool':
        print('эммм')
        bot.send_message(callback.message.chat.id, f'1488%!!!!!!!')
    elif callback.data == 'useless':
        bot.send_message(callback.message.chat.id, f'харош??????')
        # with open('ban.txt', 'w', encoding='utf-8') as ban_file:
        #     for word in message.text.split('\n'):
        #         ban_file.write(word)
        # ban_file.close()
        #
        # test = open('ban.txt', 'r', encoding='utf-8')
        # bot.send_message(message.chat.id, f'вот это вы надристали: {test.readlines()}')


bot.polling(none_stop=True)

