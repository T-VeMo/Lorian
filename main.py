"""Punto de entrada: interfaz de texto en la terminal."""

import sys
import time

import openai

from asistente import config
from asistente.cerebro import Cerebro
from asistente.herramientas import alarmas
from asistente.voz import hablar


def sonar_alarma(mensaje, hora):
    print(f"\n\n⏰  ¡ALARMA! {mensaje}  ({hora:%H:%M})\n")
    for _ in range(5):
        sys.stdout.write("\a")  # Pitido del sistema
        sys.stdout.flush()
        time.sleep(0.4)
    print("Tú: ", end="", flush=True)


def main():
    if not config.API_KEY:
        print(f"Falta {config.VARIABLE_KEY}. Copia .env.example como .env y pon tu key ahí.")
        sys.exit(1)

    cerebro = Cerebro(al_usar_herramienta=lambda nombre: print(f"   [usando {nombre}...]"))
    alarmas.iniciar_vigilancia(sonar_alarma)

    nombre = config.NOMBRE
    print(f"{nombre} en línea \n")

    while True:
        try:
            texto = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not texto:
            continue
        if texto.lower() in ("salir", "exit", "chao"):
            break
        #if texto.lower() == "nuevo":
        #    cerebro.reiniciar()
        #    print("(Conversación reiniciada)\n")
        #    continue

        try:
            respuesta = cerebro.pensar(texto)
            print(f"{nombre}: {respuesta}\n")
            hablar(respuesta)
        except openai.RateLimitError:
            print("(Llegaste al límite gratuito por ahora. Espera un momento y vuelve a intentar.)\n")
        except openai.APITimeoutError as e:
            #print(type(e).__name__, e)
            print(f"(Tiempo de espera agotado: {e})\n")
        except openai.APIConnectionError:
            print("(No hay conexión con el servicio de IA. Revisa tu internet.)\n")
        except openai.APIError as e:
            print(f"(Error de la API: {e})\n")

    print(f"{nombre}: Hasta luego.")


if __name__ == "__main__":
    main()