import webbrowser, subprocess
import pyttsx3


engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speaker(text):
    engine.say(text)
    engine.runAndWait()


def open_browser():
    webbrowser.open("https://conceptix.ru")




def passive():
    pass