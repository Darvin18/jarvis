# made by n3nsy
import pyttsx3

def speaker(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
