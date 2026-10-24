import os
import requests

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame

from asistente import config

RUTA_AUDIO = "datos/voz.mp3"


def _generar_audio(texto):
    try:
        response = requests.post(
            "https://api.fish.audio/v1/tts", 
            headers={
            "Authorization": f"Bearer {config.FISH_API_KEY}",
            "Content-Type": "application/json",
            "model": "s2.1-pro-free",
        },
            json={"text": texto, "reference_id": config.VOZ_ID, "format": "mp3"},
            timeout=30
        )
        response.raise_for_status()
        os.makedirs("datos", exist_ok=True)
        with open(RUTA_AUDIO, "wb") as f: 
            f.write(response.content)

            return RUTA_AUDIO
    except requests.RequestException as e:
        print(f"Error al llamar a la API de voz: {e}")
        return None

def _reproducir(ruta):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"Error al reproducir el audio: {e}")

def hablar(texto):
    ruta = _generar_audio(texto)
    if ruta is None:
        return
    _reproducir(ruta)

