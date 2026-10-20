"""Abre el navegador del usuario para realizar búsquedas en Google."""

import webbrowser
from urllib.parse import quote_plus


def buscar_en_google(consulta):
    try:
        busqueda = quote_plus(consulta)
        url = f"https://www.google.com/search?q={busqueda}"

        if webbrowser.open(url):
            return f"Abriendo búsqueda en Google para: {consulta}"
        else:
            return f"No se pudo abrir el navegador para la búsqueda: {consulta}"
        
    except Exception as e:
        return f"No se pudo abrir el navegador ({e})."


DEFINICIONES = [
    {
        "type": "function",
        "function": {
            "name": "buscar_en_google",
            "description": "Abre una búsqueda en Google en el navegador del usuario. Úsala solo cuando el usuario pida explícitamente abrir el navegador o ver resultados en Google."
                           "Para responder preguntas, usa buscar_web.",
            "parameters": {
                "type": "object",
                "properties": {
                    "consulta": {"type": "string", "description": "Lo que quieres buscar en Google."},
                },
                "required": ["consulta"],
            },
        },
    },
]

FUNCIONES = {"buscar_en_google": buscar_en_google}