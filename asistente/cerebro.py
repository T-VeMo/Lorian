"""El cerebro: conversa con el modelo de IA y ejecuta herramientas hasta tener una respuesta.

No sabe nada de terminales, voz ni pantallas: recibe texto y devuelve texto.
Funciona con cualquier proveedor compatible con el formato de OpenAI (Groq, Gemini, Ollama...).
"""
import os

import json

from datetime import datetime

from openai import OpenAI

from asistente import config, herramientas


DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MAX_MENSAJES = 30          # Historial máximo, para no gastar la cuota gratuita
MAX_PASOS_HERRAMIENTAS = 6  # Evita bucles infinitos si el modelo se confunde



class Cerebro:
    def __init__(self, al_usar_herramienta=None):
        self.cliente = OpenAI(base_url=config.URL_API, api_key=config.API_KEY, timeout=20, max_retries=1)
        self.historial = self._cargar_historial()
        self.al_usar_herramienta = al_usar_herramienta  # Aviso opcional, ej: mostrar "[buscando...]"

    def _cargar_historial(self):
        try:
            with open("datos/historial.json", "r", encoding="utf-8") as f:
                historial = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            historial = []
        return historial

    def _guardar_historial(self):
        try:
            os.makedirs("datos", exist_ok=True)
            with open("datos/historial.json", "w", encoding="utf-8") as f:
                json.dump(self.historial, f, indent=2, ensure_ascii=False)
        except PermissionError:
            print(f"No se pudo guardar el historial")
        except OSError as o:
            print(f"No se pudo crear el directorio de historial: {o}")
        else:
            return True
        
    #def reiniciar(self):
       # self._cargar_historial()

    def _instrucciones(self):
        ahora = datetime.now()
        return f"{config.PERSONALIDAD}\n\nAhora es {DIAS[ahora.weekday()]} {ahora:%d/%m/%Y, %H:%M}."

    def _recortar_historial(self):
        """Olvida lo más antiguo, cortando siempre al inicio de un mensaje del usuario."""
        while len(self.historial) > MAX_MENSAJES:
            self.historial.pop(0)
            while self.historial and self.historial[0]["role"] != "user":
                self.historial.pop(0)

    def pensar(self, texto):
        largo_previo = len(self.historial)
        self.historial.append({"role": "user", "content": texto})
        try:
            respuesta = self._bucle()
        except Exception:
            del self.historial[largo_previo:]  # Deshace el turno fallido
            raise
        self._recortar_historial()
        self._guardar_historial()
        return respuesta

    def _bucle(self):
        for _ in range(MAX_PASOS_HERRAMIENTAS):
            respuesta = self.cliente.chat.completions.create(
                model=config.MODELO,
                messages=[{"role": "system", "content": self._instrucciones()}] + self.historial,
                tools=herramientas.DEFINICIONES,
                tool_choice="auto",
                max_tokens=1024,
            )
            mensaje = respuesta.choices[0].message

            if not mensaje.tool_calls:
                texto = (mensaje.content or "").strip()
                self.historial.append({"role": "assistant", "content": texto})
                return texto

            # El modelo pidió usar herramientas: las ejecutamos y le devolvemos los resultados
            self.historial.append(mensaje.model_dump(exclude_none=True))
            for llamada in mensaje.tool_calls:
                nombre = llamada.function.name
                if self.al_usar_herramienta:
                    self.al_usar_herramienta(nombre)
                try:
                    argumentos = json.loads(llamada.function.arguments or "{}")
                except json.JSONDecodeError:
                    argumentos = {}
                self.historial.append({
                    "role": "tool",
                    "tool_call_id": llamada.id,
                    "content": herramientas.ejecutar(nombre, argumentos),
                })

        texto = "Perdón, me enredé intentando resolver eso. ¿Me lo pides de otra forma?"
        self.historial.append({"role": "assistant", "content": texto})
        return texto