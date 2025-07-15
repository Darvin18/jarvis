# made by n3nsy
import KEY
from tts import speaker
import os
import webbrowser
import subprocess
from PIL import ImageGrab
from datetime import datetime
#Для установки потребовалось: comtypes, pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from googletrans import Translator
import requests
import http.client
from pymorphy3 import MorphAnalyzer
import json
import pyperclip


# googletrans
translator = Translator()
def googletranslator(text: str) -> str:
    translation = translator.translate(text, src='en', dest="ru")
    return translation.text

# pymorphy2
morph = MorphAnalyzer()
def get_city_in_prepositional(city_name):
    parsed = morph.parse(city_name)[0]
    return parsed.inflect({"loct"}).word

def open_browser():
    try:
        webbrowser.open("https://dzen.ru")
    except Exception as e:
        speaker(f"Ошибка: {str(e)}")

def make_screenshot():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    screenshot = ImageGrab.grab()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    try:
        screenshot.save(f"{desktop}\screenshot_{timestamp}.png")
    except FileNotFoundError:
        oneDrive = os.path.join(os.path.join(os.environ['USERPROFILE']), 'OneDrive')
        screenshot.save(f"{oneDrive}\Desktop\screenshot_{timestamp}.png")


devices = AudioUtilities.GetSpeakers()
inteface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(inteface, POINTER(IAudioEndpointVolume))
def off_volume():
    speaker("тихий режим активирован")
    volume.SetMute(1, None)

def on_volume():
    volume.SetMute(0, None)
    speaker("тихий режим отключён")

def random_fact():
    from randfacts import get_fact
    speaker(googletranslator(get_fact()))

def tell_joke():
    from pyjokes import get_joke
    speaker(get_joke("ru"))

def translate_words():
    text = pyperclip.paste()
    translation = translator.translate(text, dest="ru")
    pyperclip.copy(translation.text)
    if len(translation.text) < 100:
        speaker(translation.text)
    else:
        speaker("Перевод уже в буфере обмена")



# def get_degree_form(number: int) -> str:
#     if number % 10 == 1 and number != 11:
#         return "градус"
#     elif number % 10 in (2, 3, 4) and number not in (12, 13, 14):
#         return "градуса"
#     return "градусов"

# def get_weather(city):
#     response = requests.get(
#         f"https://api.openweathermap.org/data/2.5/weather?q={city}"
#         f"&appid={KEY.openweaher_key}&units=metric&lang=ru"
#     )
#     data = response.json()
#     temperature = data['main']['temp']
#     description: str = data['weather'][0]['description']
#     wind_speed: str = data['wind']['speed']
#     weather = {
#         "temperature": temperature,
#         "description": description,
#         "wind_speed": wind_speed,
#     }
#     print(weather)
# get_weather("Москва")

# def daily_report():
#     user_city = ""
#     city_morph = ""
#     conn = http.client.HTTPConnection("ifconfig.me")
#     conn.request("GET", "/ip")
#     user_ip = conn.getresponse().read()
#     try:
#         response = requests.get(url=f"http://ip-api.com/json/{user_ip.decode('utf-8')}").json()
#         user_city = googletranslator(response.get("city")).text
#         city_morph = get_city_in_prepositional(user_city)
#     except requests.exceptions.ConnectionError:
#         print("please, check your connection to the internet")
#
#     weather = get_weather(user_city)
#
#     time = datetime.now()
#     night_word = "часа" if 1 <= time.hour <= 4 else "часов"
#     time_of_day = {"timeofday": ("Прекрасная ночь, сэр", "ночи")}
#     if 6 <= time.hour < 12:
#         time_of_day = {"timeofday": ("Доброе утро", "утра")}
#     elif 12 <= time.hour < 18:
#         time_of_day = {"timeofday": ("Добрый день, сэр", "дня")}
#     elif 18 <= time.hour < 24:
#         time_of_day = {"timeofday": ("Добрый вечер", "вечера")}
#
#     speaker(f"{time_of_day['timeofday'][0]}. Сейчас: {time.hour} {night_word} "
#             f"{time_of_day['timeofday'][1]}. В {city_morph} сейчас {weather['temperature']} "
#             f"{get_degree_form(int(weather['temperature']))}, {weather['description']}, "
#             f"скорость ветра {weather['wind_speed']} километров в час")



def passive():
    pass

def hello():
    time = datetime.now()
    if 6 <= time.hour < 12:
        speaker("доброе утро")
    elif 12 <= time.hour < 18:
        speaker("добрый день")
    elif 18 <= time.hour < 24:
        speaker("добрый вечер")
    else:
        speaker("Прекрасная ночь, сэр")