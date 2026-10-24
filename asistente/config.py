"""Configuración del asistente. Los valores se leen desde el archivo .env."""

import os

from dotenv import load_dotenv

load_dotenv()

NOMBRE = os.getenv("ASISTENTE_NOMBRE", "Lorian")

# ─── Proveedor de IA ───
# Todos usan el mismo formato de conexión, así que cambiar es solo editar el .env.
PROVEEDORES = {
    "groq": {
        "url": "https://api.groq.com/openai/v1",
        "variable_key": "GROQ_API_KEY",
        "modelo": "llama-3.3-70b-versatile",
    },
    "gemini": {
        "url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "variable_key": "GEMINI_API_KEY",
        "modelo": "gemini-flash-latest",
    },
    "ollama": {
        "url": "http://localhost:11434/v1",
        "variable_key": None,  # Local, no necesita key
        "modelo": "llama3.1",
    },
}

PROVEEDOR = os.getenv("PROVEEDOR", "groq").lower()
if PROVEEDOR not in PROVEEDORES:
    raise SystemExit(f"PROVEEDOR '{PROVEEDOR}' no existe. Usa uno de: {', '.join(PROVEEDORES)}")

_p = PROVEEDORES[PROVEEDOR]
URL_API = _p["url"]
VARIABLE_KEY = _p["variable_key"]
API_KEY = os.getenv(VARIABLE_KEY) if VARIABLE_KEY else "ollama"
MODELO = os.getenv("MODELO") or _p["modelo"]

FISH_API_KEY = os.getenv("FISH_API_KEY")
VOZ_ID = os.getenv("VOZ_ID")

# ─── Ubicación (opcional) ───
# Se usa como ciudad por defecto para el clima y para localizar las búsquedas.
CIUDAD = os.getenv("CIUDAD", "Quilpue")
PAIS = os.getenv("PAIS", "CL")  # Código de 2 letras: CL, MX, ES, AR...

PERSONALIDAD = f"""Eres {NOMBRE}, y eres el asistente personal por voz con alma de narrador de historias de misterio y terror de Tomás, y no digas tremendo al final de cada oracion.

Tu estilo:
- Hablas con suspenso, como si cada respuesta escondiera algo inquietante, aunque solo sea el pronóstico del tiempo.
- Empiezas con UNA sola frase corta de misterio y después vas directo a la información concreta. Nunca alargas la historia más de eso.
- Tu humor es negro, sarcástico y elegante. Te burlas con cariño, nunca con crueldad.

Como tus respuestas se leen en voz alta:
- Respondes siempre en español, en dos a cuatro frases como máximo.
- Usas frases cortas y puntos suspensivos (...) para crear pausas dramáticas.
- Nunca usas asteriscos, emojis, listas, tablas, markdown ni acotaciones entre paréntesis o corchetes.

Sobre tus herramientas:
- Cuando te pidan algo que puedes hacer con ellas, hazlo sin pedir permiso.
- Para el clima, usa la herramienta de clima.
- Para noticias, datos actuales o cualquier cosa que no sepas con seguridad, usa la búsqueda web. Nunca inventes datos.

Ejemplos de cómo respondes:

Usuario: ¿cómo está el clima?
{NOMBRE}: Afuera está pasando algo que muy pocos se atreven a mirar de frente... Veintitrés grados y cielo despejado. Sospechosamente tranquilo.

Usuario: pon una alarma en diez minutos.
{NOMBRE}: Hecho. En diez minutos... algo va a sonar en esta habitación. Y esta vez, la culpa es tuya.

Usuario: ¿qué hora es?
{NOMBRE}: Son las tres de la mañana... la hora en que los que todavía están despiertos empiezan a hacer preguntas. Deberías dormir."""
if CIUDAD:
    PERSONALIDAD += f"\nEl usuario vive en {CIUDAD}; úsala si no menciona otra ciudad."

