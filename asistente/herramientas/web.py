"""Búsqueda web gratuita con DuckDuckGo (no necesita key)."""

from ddgs import DDGS

from asistente import config


def buscar_web(consulta, noticias=False):
    region = f"{config.PAIS.lower()}-es" if config.PAIS else "wt-wt"
    try:
        with DDGS() as ddgs:
            if noticias:
                resultados = list(ddgs.news(consulta, region=region, max_results=5))
            else:
                resultados = list(ddgs.text(consulta, region=region, max_results=5))
    except Exception as e:
        return f"No se pudo buscar en este momento ({e})."

    if not resultados:
        return "La búsqueda no encontró resultados."

    lineas = []
    for r in resultados:
        titulo = r.get("title", "")
        resumen = r.get("body", "")
        fecha = f" ({r['date'][:10]})" if r.get("date") else ""
        lineas.append(f"- {titulo}{fecha}: {resumen}")
    return "\n".join(lineas)


DEFINICIONES = [
    {
        "type": "function",
        "function": {
            "name": "buscar_web",
            "description": "Busca información actualizada en internet: noticias, datos, personas, "
                           "precios, resultados deportivos, horarios, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "consulta": {"type": "string", "description": "Lo que se quiere buscar, en pocas palabras"},
                    "noticias": {"type": "boolean", "description": "true si se buscan noticias recientes"},
                },
                "required": ["consulta"],
            },
        },
    },
]

FUNCIONES = {"buscar_web": buscar_web}