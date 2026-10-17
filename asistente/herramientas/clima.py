"""Clima actual y pronóstico con Open-Meteo (gratis, sin key)."""

import requests

from asistente import config

CODIGOS = {
    0: "despejado", 1: "mayormente despejado", 2: "parcialmente nublado", 3: "nublado",
    45: "niebla", 48: "niebla", 51: "llovizna débil", 53: "llovizna", 55: "llovizna intensa",
    61: "lluvia débil", 63: "lluvia", 65: "lluvia intensa", 71: "nieve débil", 73: "nieve",
    75: "nieve intensa", 80: "chubascos", 81: "chubascos", 82: "chubascos fuertes",
    95: "tormenta", 96: "tormenta con granizo", 99: "tormenta con granizo",
}


def _ubicar(ciudad):
    r = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": ciudad, "count": 1, "language": "es"},
        timeout=10,
    )
    r.raise_for_status()
    lugares = r.json().get("results")
    return lugares[0] if lugares else None


def clima(ciudad=None, dias=1):
    ciudad = ciudad or config.CIUDAD
    if not ciudad:
        return "No sé de qué ciudad. Pregúntale al usuario o configura CIUDAD en el .env."
    dias = max(1, min(int(dias), 7))

    try:
        lugar = _ubicar(ciudad)
        if not lugar:
            return f"No encontré la ciudad '{ciudad}'."
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lugar["latitude"],
                "longitude": lugar["longitude"],
                "current": "temperature_2m,apparent_temperature,weather_code,wind_speed_10m",
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
                "timezone": "auto",
                "forecast_days": dias,
            },
            timeout=10,
        )
        r.raise_for_status()
        datos = r.json()
    except requests.RequestException as e:
        return f"No se pudo consultar el clima ({e})."

    actual = datos["current"]
    lineas = [
        f"{lugar['name']}, {lugar.get('country', '')}. Ahora: "
        f"{actual['temperature_2m']:.0f}°C (sensación {actual['apparent_temperature']:.0f}°C), "
        f"{CODIGOS.get(actual['weather_code'], 'condición desconocida')}, "
        f"viento {actual['wind_speed_10m']:.0f} km/h."
    ]
    diario = datos["daily"]
    for i, fecha in enumerate(diario["time"]):
        lineas.append(
            f"{fecha}: {CODIGOS.get(diario['weather_code'][i], '?')}, "
            f"mín {diario['temperature_2m_min'][i]:.0f}°C, máx {diario['temperature_2m_max'][i]:.0f}°C, "
            f"probabilidad de lluvia {diario['precipitation_probability_max'][i]}%."
        )
    return "\n".join(lineas)


DEFINICIONES = [
    {
        "type": "function",
        "function": {
            "name": "clima",
            "description": "Da el clima actual y el pronóstico de una ciudad.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ciudad": {"type": "string", "description": "Ciudad. Omitir para usar la del usuario."},
                    "dias": {"type": "integer", "description": "Días de pronóstico, de 1 a 7. Hoy = 1, mañana = 2."},
                },
            },
        },
    },
]

FUNCIONES = {"clima": clima}