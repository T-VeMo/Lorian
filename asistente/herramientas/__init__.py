"""Registro de herramientas.

Para agregar una herramienta nueva:
  1. Crea un archivo en esta carpeta con sus funciones, DEFINICIONES y FUNCIONES
     (usa clima.py como ejemplo).
  2. Agrégala a la lista MODULOS de abajo.
"""

from . import alarmas, clima, web

MODULOS = [alarmas, clima, web]

DEFINICIONES = [d for m in MODULOS for d in m.DEFINICIONES]
FUNCIONES = {nombre: f for m in MODULOS for nombre, f in m.FUNCIONES.items()}


def ejecutar(nombre, argumentos):
    funcion = FUNCIONES.get(nombre)
    if not funcion:
        return f"Herramienta desconocida: {nombre}"
    try:
        return str(funcion(**argumentos))
    except Exception as e:
        return f"Error al ejecutar {nombre}: {e}"