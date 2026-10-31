# Lorian — asistente personal con IA

Asistente personal que conversa, pone alarmas y temporizadores, da el clima y busca información en internet. **Funciona gratis** usando la capa gratuita de Groq.

Por ahora funciona por texto en la terminal. La voz y la interfaz vienen en próximas versiones.

## Estructura

```
Lorian/
├── main.py                  # Punto de entrada (interfaz de terminal)
├── datos
    └──historial.json        # Donde se guardan las conversaciones 
├── requirements.txt         # Dependencias
├── .env.example             # Plantilla de configuración
└── asistente/
    ├── config.py            # Nombre, proveedor de IA, personalidad
    ├── cerebro.py           # Conversa con la IA y usa las herramientas
    └── herramientas/
        ├── __init__.py      # Registro de herramientas
        ├── alarmas.py       # Alarmas y temporizadores
        ├── clima.py         # Clima con Open-Meteo (gratis)
        ├── navegador.py     # Abre el navegador para realizar busquedas
        └── web.py           # Búsqueda con DuckDuckGo (gratis)
```

El cerebro no depende de la terminal: recibe texto y devuelve texto. Así, más adelante se le puede poner voz o una pantalla encima sin tocarlo.

## Instalación

1. Instala Python 3.9 o superior.
2. Crea una cuenta gratis en [console.groq.com](https://console.groq.com) y genera una API key en la sección API Keys.
3. En la carpeta del proyecto:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate

pip install -r requirements.txt
```

4. Copia `.env.example` como `.env` y pega tu key en `GROQ_API_KEY`. Opcionalmente, pon tu ciudad y país para el clima.

## Uso

```bash
python main.py
```

Ejemplos:

- `pon una alarma a las 7:30 para ir al gimnasio`
- `avísame en 10 minutos que saque la pizza`
- `qué alarmas tengo?` / `cancela la de la pizza`
- `va a llover mañana?`
- `qué noticias hay hoy de tecnología?`

Comandos: `salir` cierra el programa.

## Cambiar de proveedor de IA

En el `.env`, cambia `PROVEEDOR`:

| Proveedor | Costo | Key |
|-----------|-------|-----|
| `groq` | Gratis con límites diarios | [console.groq.com](https://console.groq.com) |
| `gemini` | Gratis con límites (usa tus datos para entrenar) | [aistudio.google.com](https://aistudio.google.com) |
| `ollama` | Gratis, corre en tu PC | No necesita, pero sí [Ollama](https://ollama.com) instalado |

Con `MODELO` puedes elegir otro modelo del proveedor.

## Agregar una herramienta

1. Crea un archivo en `asistente/herramientas/` con sus funciones, `DEFINICIONES` y `FUNCIONES` (usa `clima.py` de ejemplo).
2. Agrégala a `MODULOS` en `asistente/herramientas/__init__.py`.

## Hoja de ruta

- [x] Cerebro con IA gratuita
- [x] Alarmas y temporizadores
- [x] Clima y búsqueda web
- [x] Guardar conversaciones al cerrar el programa
- [ ] Guardar alarmas al cerrar el programa
- [ ] Voz (escuchar y hablar)
- [ ] Palabra de activación
- [ ] Interfaz en pantalla
- [ ] Correr en un Android

---

## 🇬🇧 English summary

**Lorian** is a personal AI assistant written in Python. It chats in natural language and uses **tool calling** to act on requests: it sets alarms and timers, reports the weather (Open-Meteo), searches the web (DuckDuckGo), opens the browser and can answer out loud (text-to-speech).

**Highlights**

- Provider-agnostic AI layer: switch between **Groq**, **Google Gemini** or a local **Ollama** model from the `.env` file
- Modular tools: each tool declares its JSON schema and handler, and is registered in one place
- The "brain" is decoupled from the interface (text in, text out), so voice or a GUI can be added without touching it
- Runs entirely on free tiers

**Stack:** Python · OpenAI-compatible SDK · Groq / Gemini / Ollama · DuckDuckGo search · Open-Meteo · pygame (audio)

**Quick start:** `pip install -r requirements.txt`, copy `.env.example` to `.env`, add a free Groq API key and run `python main.py`.

**Author:** Tomás Vega · [github.com/T-VeMo](https://github.com/T-VeMo)
