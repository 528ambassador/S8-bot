import telebot

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


@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)


bot.polling(none_stop=True)
