import telebot, json
import requests as req
from geopy import geocoders
from telebot import types

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

def geo_pos(city: str):
    global latitude, longitude

    geolocator = geocoders.Nominatim(user_agent="telebot")
    latitude = str(geolocator.geocode(city).latitude)
    longitude = str(geolocator.geocode(city).longitude)
    
def code_location(latitude: str, longitude: str, token_accu: str):
    url_location_key = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=' \
                       f'{token_accu}&q={latitude},{longitude}&language=en'
    resp_loc = req.get(url_location_key, headers={"APIKey": token_accu})
    json_data = json.loads(resp_loc.text)
    code = json_data['Key']
    
    return code

def weather(code_loc: str, token_accu: str):
    url_weather = f'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{code_loc}?' \
                  f'apikey={token_accu}&language=en&metric=True'
    response = req.get(url_weather, headers={"APIKey": token_accu})
    json_data = json.loads(response.text)
    dict_weather = dict()
    dict_weather['link'] = json_data[0]['MobileLink']
    
    time = 'now'
    dict_weather[time] = {'temp': json_data[0]['Temperature']['Value'], 'sky': json_data[0]['IconPhrase']}
    
    for i in range(1, len(json_data)):
        time = '+' + str(i) + 'h'
        dict_weather[time] = {'temp': json_data[i]['Temperature']['Value'], 'sky': json_data[i]['IconPhrase']}
    
    return dict_weather

def print_weather(dict_weather):
    bot.send_message(userId, 
                     f'Current temp. is {dict_weather["now"]["temp"]} {dict_weather["now"]["sky"]}\n'
                     f'+3h. temp. is {dict_weather["+3h"]["temp"]} {dict_weather["+3h"]["sky"]}\n'
                     f'+6h. temp. is {dict_weather["+6h"]["temp"]} {dict_weather["+6h"]["sky"]}\n'
                     f'+9h. temp. is {dict_weather["+9h"]["temp"]} {dict_weather["+9h"]["sky"]}'
    )

    bot.send_message(userId, f' Verbosely about current weather \n {dict_weather["link"]}')

def get_weather():
    global latitude, longitude

    code_loc = code_location(latitude, longitude, tokens["token_accu"])
    you_weather = weather(code_loc, tokens["token_accu"])
    print_weather(you_weather)

# ###############################################################

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global userId, firstName

    userId = message.from_user.id
    firstName = message.from_user.first_name

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text= "Show current weather!", request_location= True))

    bot.send_message(message.from_user.id, f"👋 Hi, {message.from_user.first_name}. I'm a weather bot. \nPlease push <b>\"Show current weather!\"</b> button or just type your city", parse_mode= "HTML", reply_markup=markup)

@bot.message_handler(content_types=["location"])
def location(message):
    global latitude, longitude, userId, firstName

    userId = message.from_user.id
    firstName = message.from_user.first_name

    if message.location is not None:
        latitude = message.location.latitude
        longitude =  message.location.longitude
        
        get_weather()

@bot.message_handler(content_types=["text"])
def get_text(message):
    try:
        geo_pos(message.text)
        get_weather()

    except AttributeError as err:
        bot.send_message(message.from_user.id, f'Sorry! I don\'t know that city')

# ###############################################################

bot.infinity_polling()
