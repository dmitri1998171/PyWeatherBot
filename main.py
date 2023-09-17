from telebot import types
from weather import *

def parseJSON():
    tokens = {}

    with open("tokens.json", 'r') as f:
        tokens = json.load(f)

    return tokens

tokens = parseJSON()
bot = telebot.TeleBot(tokens['token'])

def print_weather(dict_weather, message):
    bot.send_message(message.from_user.id, f'Разрешите доложить, Ваше сиятельство!'
                                           f' Температура сейчас {dict_weather["сейчас"]["temp"]}!'
                                           f' А на небе {dict_weather["сейчас"]["sky"]}.'
                                           f' Температура через три часа {dict_weather["через3ч"]["temp"]}!'
                                           f' А на небе {dict_weather["через3ч"]["sky"]}.'
                                           f' Температура через шесть часов {dict_weather["через6ч"]["temp"]}!'
                                           f' А на небе {dict_weather["через6ч"]["sky"]}.'
                                           f' Температура через девять часов {dict_weather["через9ч"]["temp"]}!'
                                           f' А на небе {dict_weather["через9ч"]["sky"]}.')
    bot.send_message(message.from_user.id, f' А здесь ссылка на подробности '
                                           f'{dict_weather["link"]}')

def print_yandex_weather(dict_weather_yandex, message):
    day = {'night': 'ночью', 'morning': 'утром', 'day': 'днем', 'evening': 'вечером', 'fact': 'сейчас'}
    bot.send_message(message.from_user.id, f'А яндекс говорит:')
    for i in dict_weather_yandex.keys():
        if i != 'link':
            time_day = day[i]
            bot.send_message(message.from_user.id, f'Температура {time_day} {dict_weather_yandex[i]["temp"]}'
                                                   f', на небе {dict_weather_yandex[i]["condition"]}')

    bot.send_message(message.from_user.id, f' А здесь ссылка на подробности '
                                           f'{dict_weather_yandex["link"]}')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Show current weather!"))

    bot.send_message(message.from_user.id, f"👋 Hi, {message.from_user.first_name}. I'm weather bot", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text(message):
    global cities

    if(message.text == "Show current weather!"):
        city = "Shymkent"
        bot.send_message(message.from_user.id, f'О великий и могучий {message.from_user.first_name}!'
                                                f' Твой город {city}')
        latitude, longitude = geo_pos(city)
        code_loc = code_location(latitude, longitude, tokens["token_accu"])
        you_weather = weather(code_loc, tokens["token_accu"])
        print_weather(you_weather, message)
        yandex_weather_x = yandex_weather(latitude, longitude, tokens["token_yandex"])
        print_yandex_weather(yandex_weather_x, message)
    

bot.infinity_polling()

# Reference
# https://habr.com/ru/articles/584134/