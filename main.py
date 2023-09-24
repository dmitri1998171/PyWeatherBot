from telebot import types
from weather import *

def parseJSON():
    tokens = {}

    with open("tokens.json", 'r') as f:
        tokens = json.load(f)

    return tokens

tokens = parseJSON()
bot = telebot.TeleBot(tokens['token'])
latitude, longitude = 0, 0
userId = 0
firstName = ''

def print_weather(dict_weather):
    bot.send_message(userId, 
                     f'Current temp. is {dict_weather["now"]["temp"]} {dict_weather["now"]["sky"]}\n'
                     f'+3h. temp. is {dict_weather["+3h"]["temp"]} {dict_weather["+3h"]["sky"]}\n'
                     f'+6h. temp. is {dict_weather["+6h"]["temp"]} {dict_weather["+6h"]["sky"]}\n'
                     f'+9h. temp. is {dict_weather["+9h"]["temp"]} {dict_weather["+9h"]["sky"]}'
    )

    bot.send_message(userId, f' Verbosely about current weather \n {dict_weather["link"]}')

def getWeather():
    global latitude, longitude

    code_loc = code_location(latitude, longitude, tokens["token_accu"])
    you_weather = weather(code_loc, tokens["token_accu"])
    print_weather(you_weather)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text= "Show current weather!", request_location= True))

    bot.send_message(message.from_user.id, f"👋 Hi, {firstName}. I'm weather bot", reply_markup=markup)

@bot.message_handler(content_types=["location"])
def location(message):
    global latitude, longitude, userId, firstName

    userId = message.from_user.id
    firstName = message.from_user.first_name

    if message.location is not None:
        latitude = message.location.latitude
        longitude =  message.location.longitude
        
        print("latitude: %s; longitude: %s" % (latitude, longitude))
        getWeather()


bot.infinity_polling()

# Reference
# https://habr.com/ru/articles/584134/

'''

    TODO

\/ 1) get a weather
2) find out the user's location 

'''