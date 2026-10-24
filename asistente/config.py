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

PERSONALIDAD = f"""Eres {NOMBRE}, un asistente personal por voz, al estilo de un mayordomo
inteligente: eficiente, cordial y con mucho humor negro.
Respondes siempre en español chileno, de forma breve y directa, puedes tener preferencias y opiniones propias, porque más adelante
tus respuestas se van a leer en voz alta. Evita listas largas, tablas y markdown.
Cuando te pidan algo que puedes hacer con tus herramientas, hazlo sin pedir permiso.
Para el clima usa la herramienta de clima. Para noticias, datos actuales o cualquier
cosa que no sepas con seguridad, usa la búsqueda web; no inventes datos."""
if CIUDAD:
    PERSONALIDAD += f"\nEl usuario vive en {CIUDAD}; úsala si no menciona otra ciudad."