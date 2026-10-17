"""Búsqueda web. La ejecuta directamente la API de Claude, así que solo hay que declararla."""

from asistente import config


def definicion():
    herramienta = {"type": "web_search_20250305", "name": "web_search", "max_uses": 3}
    ubicacion = {}
    if config.CIUDAD:
        ubicacion["city"] = config.CIUDAD
    if config.PAIS:
        ubicacion["country"] = config.PAIS
    if ubicacion:
        herramienta["user_location"] = {"type": "approximate", **ubicacion}
    return herramienta
