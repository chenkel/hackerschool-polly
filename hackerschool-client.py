import simpleaudio as sa
import json
import base64
import requests
import time

# Die API liefert Audio und Viseme base64 kodiert zurück.
POLLY_API = 'https://hackerschool.christopher.cloud/viseme'

# Verfuegbare Stimmen: Marlene (Default), Vicki, Hans
stimme = 'Hans'

# Text der an Polly geschickt wird
text = 'Hallo Tobias. Wie geht es dir?'

# URL zusammensetzen
get_url = POLLY_API + '?text=' + text
if stimme:
    get_url = get_url + '&voice=' + stimme

# Anfrage abschicken
print("The API Call: '" , get_url, "'")
r = requests.get(get_url)

# Audio und Viseme einlesen
data = json.loads(r.text)
wav = base64.b64decode(data['audio'])
viseme = json.loads(base64.b64decode(data['viseme']).decode('utf-8'))

# Audio ausgeben
with open("speech.wav", "wb") as f:
    f.write(wav)
    wave_obj = sa.WaveObject.from_wave_file('speech.wav')
    play_obj = wave_obj.play()

# Viseme parallel ausgeben
prev_time = 0.0
visem_time_diff = 0.0
for visem in viseme:
    if 'viseme' in visem['type']:
        visem_time = float(visem['time'])
        visem_time_diff = visem_time - prev_time
        print(visem)
        time.sleep(visem_time_diff / 1000.0)
        prev_time = visem_time

# Das Programm wird nicht beendet, bevor nicht alles vollständig vorgelesen wurde.
play_obj.wait_done()
