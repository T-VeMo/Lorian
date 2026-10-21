"""Abre el navegador del usuario para realizar búsquedas en un sitio web."""

import webbrowser
from urllib.parse import quote_plus

PAGINAS = {
    "google": "https://www.google.com/search?q={}", 
    "youtube": "https://www.youtube.com/results?search_query={}"
}


def navegador(consulta, pagina="google"):
    if pagina not in PAGINAS:
        return f"No se reconoce la página '{pagina}'. Páginas disponibles: {', '.join(PAGINAS.keys())}."
    try:
        busqueda = quote_plus(consulta)
        url = PAGINAS[pagina].format(busqueda)

        if webbrowser.open(url):
            return f"Abriendo búsqueda en {pagina} para: {consulta}"
        return f"No se pudo abrir el navegador para la búsqueda: {consulta}"
        
    except Exception as e:
        return f"No se pudo abrir el navegador ({e})."


DEFINICIONES = [
    {
        "type": "function",
        "function": {
            "name": "navegador",
            "description": "Abre una búsqueda en la página especificada por el usuario en el navegador del usuario. " 
                            "Úsala solo cuando el usuario pida explícitamente abrir el navegador o ver resultados en la pagina que el usuario decida. " 
                            "Para responder preguntas, usa buscar_web.",
            "parameters": {
                "type": "object",
                "properties": {
                    "consulta": {"type": "string", "description": "Lo que quieres buscar en la página especificada."},
                    "pagina": {"type": "string", "description": "Página donde buscar.", "default": "google", "enum": list(PAGINAS.keys())},
                },
                "required": ["consulta"],
            },
        },
    },
]

FUNCIONES = {"navegador": navegador}