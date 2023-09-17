import telebot, json
from telebot import types

def parseJSON():
    tokens = {}

    with open("tokens.json", 'r') as f:
        tokens = json.load(f)

    return tokens

tokens = parseJSON()
bot = telebot.TeleBot(tokens['token'])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Show current weather!"))

    bot.send_message(message.from_user.id, f"👋 Hi, {message.from_user.first_name}. I'm weather bot", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text(message):
    if(message.text == "Show current weather!"):
        bot.send_message(message.from_user.id, "Show current weather!")
    

bot.infinity_polling()

# Reference
# https://habr.com/ru/articles/584134/