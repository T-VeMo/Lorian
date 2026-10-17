"""El cerebro: conversa con Claude y ejecuta herramientas hasta tener una respuesta.

No sabe nada de terminales, voz ni pantallas: recibe texto y devuelve texto.
Así se puede reutilizar igual desde la terminal, la voz o una interfaz gráfica.
"""

from datetime import datetime

import anthropic

from asistente import config, herramientas

DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


class Cerebro:
    def __init__(self, al_usar_herramienta=None):
        self.cliente = anthropic.Anthropic()
        self.historial = []
        self.al_usar_herramienta = al_usar_herramienta  # Aviso opcional, ej: mostrar "[buscando...]"

    def reiniciar(self):
        self.historial.clear()

    def _instrucciones(self):
        ahora = datetime.now()
        return f"{config.PERSONALIDAD}\n\nAhora es {DIAS[ahora.weekday()]} {ahora:%d/%m/%Y, %H:%M}."

    def pensar(self, texto):
        largo_previo = len(self.historial)
        self.historial.append({"role": "user", "content": texto})
        try:
            return self._bucle()
        except Exception:
            del self.historial[largo_previo:]  # Deshace el turno fallido
            raise

    def _bucle(self):
        while True:
            respuesta = self.cliente.messages.create(
                model=config.MODELO,
                max_tokens=1024,
                system=self._instrucciones(),
                tools=herramientas.DEFINICIONES,
                messages=self.historial,
            )
            self.historial.append({"role": "assistant", "content": respuesta.content})

            if respuesta.stop_reason == "tool_use":
                resultados = []
                for bloque in respuesta.content:
                    if bloque.type == "tool_use":
                        if self.al_usar_herramienta:
                            self.al_usar_herramienta(bloque.name)
                        resultados.append({
                            "type": "tool_result",
                            "tool_use_id": bloque.id,
                            "content": herramientas.ejecutar(bloque.name, bloque.input),
                        })
                self.historial.append({"role": "user", "content": resultados})
                continue

            if respuesta.stop_reason == "pause_turn":
                continue  # Búsqueda larga: se reenvía tal cual para que siga

            return "".join(b.text for b in respuesta.content if b.type == "text").strip()
