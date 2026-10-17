"""Configuración del asistente. Los valores se leen desde el archivo .env."""

import os

from dotenv import load_dotenv

load_dotenv()

NOMBRE = os.getenv("ASISTENTE_NOMBRE", "Jarvis")
MODELO = os.getenv("MODELO", "claude-haiku-5-5")

# Ubicación para que las búsquedas (clima, noticias) sean locales. Opcional.
CIUDAD = os.getenv("CIUDAD", "")
PAIS = os.getenv("PAIS", "")  # Código de 2 letras: CL, MX, ES, AR...

PERSONALIDAD = f"""Eres {NOMBRE}, un asistente personal por voz, al estilo de un mayordomo
inteligente: eficiente, cordial y con un toque de humor sutil.
Respondes siempre en español, de forma breve y directa, porque más adelante
tus respuestas se van a leer en voz alta. Evita listas largas, tablas y markdown.
Cuando te pidan algo que puedes hacer con tus herramientas, hazlo sin pedir permiso.
Si te piden información actual (clima, noticias, precios, resultados), búscala en la web."""
