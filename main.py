# made by n3nsy
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import pvporcupine
import struct
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

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
  keywords=['computer'],
)

q = queue.Queue()
model = Model("vosk_model-small")

# sounddevice microphone choice
device = sd.default.device # int, out [0,0]
samplerate = int(sd.query_devices(device[0], "input")["default_samplerate"])


def callback(indata, frames, time, status):
    q.put(bytes(indata))

def recognize(data):
    # ('fgrgre', 0-100)
    result = process.extractOne(data, prepared_commands, scorer=fuzz.ratio)

    if result and result[1] >= 50:
        matched_variant = result[0]

        # Переменная, выводящая функцию, которую лучше всего вызвать
        best_match = command_map.get(matched_variant)
        # Переменная, показывающая, какую фразу должен сказать ассистент
        voice_match = voice_commands.get(matched_variant)
        if best_match:
            try:
                exec(f"{best_match}()")
                speaker(voice_match)
            except Exception as e:
                print(f"Error executing {best_match}: {e}")

def listen_for_commands(timeout=4):
    last_command_time = time.time()

    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device,
                           dtype="int16", channels=1, callback=callback):
        rec = KaldiRecognizer(model, samplerate)

        while True:
            if time.time() - last_command_time > timeout:
                return

            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())["text"]
                if data.strip():
                    print(f"Command recognized: {data}")
                    recognize(data)
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