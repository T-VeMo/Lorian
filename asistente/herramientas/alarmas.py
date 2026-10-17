"""Herramienta de alarmas y temporizadores."""

import threading
import time
from datetime import datetime, timedelta

_alarmas = {}  # id -> {"hora": datetime, "mensaje": str}
_contador = 0
_lock = threading.Lock()


def poner_alarma(hora=None, en_minutos=None, mensaje="Alarma"):
    global _contador
    ahora = datetime.now()

    if en_minutos is not None:
        objetivo = ahora + timedelta(minutes=float(en_minutos))
    elif hora:
        try:
            h, m = map(int, hora.strip().split(":"))
            objetivo = ahora.replace(hour=h, minute=m, second=0, microsecond=0)
        except ValueError:
            return "Error: la hora debe tener formato HH:MM (24 horas)."
        if objetivo <= ahora:
            objetivo += timedelta(days=1)  # Si ya pasó hoy, queda para mañana
    else:
        return "Error: indica 'hora' o 'en_minutos'."

    with _lock:
        _contador += 1
        _alarmas[_contador] = {"hora": objetivo, "mensaje": mensaje}
        id_alarma = _contador

    dia = "hoy" if objetivo.date() == ahora.date() else "mañana"
    return f"Alarma #{id_alarma} lista para {dia} a las {objetivo:%H:%M:%S}: {mensaje}"


def listar_alarmas():
    with _lock:
        if not _alarmas:
            return "No hay alarmas activas."
        return "\n".join(
            f"#{i}: {a['hora']:%d/%m %H:%M:%S} - {a['mensaje']}"
            for i, a in sorted(_alarmas.items(), key=lambda x: x[1]["hora"])
        )


def cancelar_alarma(id_alarma):
    with _lock:
        alarma = _alarmas.pop(int(id_alarma), None)
    if alarma:
        return f"Alarma #{id_alarma} cancelada ({alarma['mensaje']})."
    return f"No existe una alarma #{id_alarma}."


def iniciar_vigilancia(al_sonar):
    """Arranca un hilo en segundo plano que llama a al_sonar(mensaje, hora) cuando vence una alarma.

    Así la alarma no depende de la terminal: más adelante al_sonar puede
    reproducir un sonido, hablar o mostrar algo en pantalla.
    """
    def vigilar():
        while True:
            ahora = datetime.now()
            with _lock:
                vencidas = [(i, a) for i, a in _alarmas.items() if a["hora"] <= ahora]
                for i, _ in vencidas:
                    del _alarmas[i]
            for _, a in vencidas:
                al_sonar(a["mensaje"], a["hora"])
            time.sleep(1)

    threading.Thread(target=vigilar, daemon=True).start()


# ─── Definiciones que ve Claude ───

def _funcion(nombre, descripcion, propiedades=None, requeridos=None):
    parametros = {"type": "object", "properties": propiedades or {}}
    if requeridos:
        parametros["required"] = requeridos
    return {"type": "function", "function": {"name": nombre, "description": descripcion, "parameters": parametros}}


DEFINICIONES = [
    _funcion(
        "poner_alarma",
        "Programa una alarma a una hora exacta o un temporizador dentro de X minutos. "
        "Usa 'hora' para horas del reloj y 'en_minutos' para temporizadores. "
        "Para segundos u horas, conviértelos a minutos (ej: 30 segundos = 0.5).",
        {
            "hora": {"type": "string", "description": "Hora en formato 24h HH:MM, ej: '07:30'"},
            "en_minutos": {"type": "number", "description": "Minutos desde ahora, ej: 15"},
            "mensaje": {"type": "string", "description": "Motivo de la alarma, ej: 'Sacar la pizza'"},
        },
    ),
    _funcion("listar_alarmas", "Muestra todas las alarmas y temporizadores activos."),
    _funcion(
        "cancelar_alarma",
        "Cancela una alarma por su número. Si no sabes el número, primero lista las alarmas.",
        {"id_alarma": {"type": "integer"}},
        ["id_alarma"],
    ),
]

FUNCIONES = {
    "poner_alarma": poner_alarma,
    "listar_alarmas": listar_alarmas,
    "cancelar_alarma": cancelar_alarma,
}