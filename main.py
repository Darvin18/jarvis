# made by n3nsy
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import config
from functions import *


q = queue.Queue()
model = Model("vosk_model-small")

device = sd.default.device # int, out [0,0]
samplerate = int(sd.query_devices(device[0], "input")["default_samplerate"])


# прогон команд для fuzzy wuzzy
prepared_commands = []
command_map = {}

for cmd, variants in config.data_set.items():
    for variant in variants:
        prepared_commands.append(variant)
        command_map[variant] = cmd


def callback(indata, frames, time, status):
    q.put(bytes(indata))


def recognize(data):
    trg = config.TRIGGERS.intersection(data.split())
    if not trg:
        return

    formated_data = "".join(data.split(list(trg)[0])[1:]).strip()

    # print(formated_data)
    result = process.extractOne(formated_data, prepared_commands, scorer=fuzz.ratio)

    if result and result[1] >= 40:
        matched_variant = result[0]
        best_match = command_map.get(matched_variant)
        # print(best_match)
        if best_match:
            try:
                exec(f"{best_match}()")

            except Exception as e:
                print(f"Error executing {best_match}: {e}")


def main():
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device,
                           dtype="int16", channels=1, callback=callback):

        rec = KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())["text"]
                recognize(data)
            # else:
            #     print(rec.PartialResult()) # Вывод промежуточного результата

if __name__ == "__main__":
    main()