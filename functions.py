# made by n3nsy
from tts import speaker
import KEY
import os
import webbrowser
import subprocess
from PIL import ImageGrab
from datetime import datetime
#Для установки потребовалось: comtypes, pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from randfacts import get_fact
from googletrans import Translator
from pyjokes import get_joke



def open_browser():
    webbrowser.open("https://dzen.ru")

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
    translator = Translator()
    fact = translator.translate(get_fact(), src='en', dest="ru")
    speaker(fact.text)

def tell_joke():
    joke = get_joke("ru")
    speaker(joke)

def daily_report():

    time = datetime.now()
    night_word = "часа" if 1 <= time.hour <= 4 else "часов"
    time_of_day = {"timeofday": ("Прекрасная ночь, сэр", "ночи")}
    if 6 <= time.hour < 12:
        time_of_day = {"timeofday": ("Доброе утро", "утра")}
    elif 12 <= time.hour < 18:
        time_of_day = {"timeofday": ("Добрый день, сэр", "дня")}
    elif 18 <= time.hour < 24:
        time_of_day = {"timeofday": ("Добрый вечер", "вечера")}
    speaker(f"{time_of_day['timeofday'][0]}. Сейчас: {time.hour} {night_word} {time_of_day['timeofday'][1]}")
daily_report()



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