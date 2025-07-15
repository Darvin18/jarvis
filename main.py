# made by n3nsy
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import pvporcupine
import struct
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import winsound

# мои модули
import json
import config
from functions import *
from tts import speaker
import KEY


# прогон команд для fuzzywuzzy
prepared_commands = []
command_map = {}
voice_commands = {}

for cmd, variants in config.data_set.items():
    for variant in variants.items():
        prepared_commands.append(variant[0])
        command_map[variant[0]] = cmd
        voice_commands[variant[0]] = variant[1]


# picovoice connection
porcupine = pvporcupine.create(
  access_key=KEY.pvporcupine_key,
  keywords=['jarvis'],
)

q = queue.Queue()
model = Model("vosk_model-small")

# sounddevice microphone choice
device = sd.default.device # int, out [0,0]
samplerate = int(sd.query_devices(device[0], "input")["default_samplerate"])

hello()


def callback(indata, frames, time, status):
    q.put(bytes(indata))

def recognize(data):
    trg = config.TRIGGERS.intersection(data.split())
    # ('fgrgre', 0-100)
    result = process.extractOne(data, prepared_commands, scorer=fuzz.ratio)

    # Когда до сих пор вызвана функция listen_for_commands, юзер может говорить в микро всё что угодно
    # И когда он говорит что-то большое и после этого сразу команду, она не может не обработаться, т.к
    # обрабатываться будет гигантское предложение, которое тупо не пройдёт по fuzzywuzzy
    # поэтому я исправил эту вещь, сделав так, чтобы человек мог говорить всё что угодно
    # но сказав --ДЖАРВИС-- И --КОМАНДУ--, splitом предложение разделится и fuzzywuzzy сработает корректно
    if trg:
        result_list = list(result)
        result_list[0] = "".join(data.split(list(trg)[0])[1:]).strip()
        result = process.extractOne(result_list[0], prepared_commands, scorer=fuzz.ratio)

    if result and result[1] >= 60:
        matched_variant = result[0]
        # Переменная, выводящая функцию, которую лучше всего вызвать
        best_match = command_map.get(matched_variant)
        # Переменная, показывающая, какую фразу должен сказать ассистент
        voice_match = voice_commands.get(matched_variant)
        if best_match:
            try:
                exec(f"{best_match}()")
                speaker(voice_match)
                return True
            except Exception as e:
                print(f"Error executing {best_match}: {e}")
                return False
    return False

def listen_for_commands(timeout=10):
    last_command_time = time.time()

    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device,
                           dtype="int16", channels=1, callback=callback):
        rec = KaldiRecognizer(model, samplerate)

        while True:
            if time.time() - last_command_time > timeout:
                winsound.Beep(200, 200)
                return

            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())["text"]
                if data.strip():
                    print(f"Command recognized: {data}")
                    if recognize(data):
                    # Если user что-то сказал, переменная обнуляется
                        last_command_time = time.time()

def listen_for_wake_word():
    print("Listening for wake word...")
    with sd.RawInputStream(samplerate=16000, blocksize=porcupine.frame_length,
                           device=device, dtype="int16", channels=1) as stream:
        while True:
            data, _ = stream.read(porcupine.frame_length)
            data = struct.unpack_from("h" * porcupine.frame_length, data)

            keyword_index = porcupine.process(data)
            if keyword_index == 0:
                speaker("Да")
                print(f"Detected wake word with index: {keyword_index}")
                return True

def main():
    while True:
        listen_for_wake_word()  # Ждём wake word
        listen_for_commands()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        porcupine.delete()