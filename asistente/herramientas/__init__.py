"""Registro de herramientas.

Para agregar una herramienta nueva:
  1. Crea un archivo en esta carpeta con sus funciones, DEFINICIONES y FUNCIONES
     (usa alarmas.py como ejemplo).
  2. Impórtala aquí y súmala a las dos listas de abajo.
"""

from . import alarmas, web

DEFINICIONES = alarmas.DEFINICIONES + [web.definicion()]

FUNCIONES = {
    **alarmas.FUNCIONES,
}


def ejecutar(nombre, argumentos):
    funcion = FUNCIONES.get(nombre)
    if not funcion:
        return f"Herramienta desconocida: {nombre}"
    try:
        return str(funcion(**argumentos))
    except Exception as e:
        return f"Error al ejecutar {nombre}: {e}"
