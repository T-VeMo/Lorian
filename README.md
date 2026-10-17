# Jarvis — asistente personal con IA

Asistente personal que conversa, pone alarmas y temporizadores, y busca información en internet. Usa Claude como cerebro.

Por ahora funciona por texto en la terminal. La voz y la interfaz vienen en próximas versiones.

## Estructura

```
jarvis/
├── main.py                  # Punto de entrada (interfaz de terminal)
├── requirements.txt         # Dependencias
├── .env.example             # Plantilla de configuración
└── asistente/
    ├── config.py            # Nombre, modelo, personalidad
    ├── cerebro.py           # Conversa con Claude y usa las herramientas
    └── herramientas/
        ├── __init__.py      # Registro de herramientas
        ├── alarmas.py       # Alarmas y temporizadores
        └── web.py           # Búsqueda web
```

El cerebro no depende de la terminal: recibe texto y devuelve texto. Así, más adelante se le puede poner voz o una pantalla encima sin tocarlo.

## Instalación

1. Instala Python 3.9 o superior.
2. Consigue una API key en [platform.claude.com](https://platform.claude.com) (sección API Keys).
3. En la carpeta del proyecto:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate

pip install -r requirements.txt
```

4. Copia `.env.example` como `.env` y pon tu API key ahí.

## Uso

```bash
python main.py
```

Ejemplos:

- `pon una alarma a las 7:30 para ir al gimnasio`
- `avísame en 10 minutos que saque la pizza`
- `qué alarmas tengo?` / `cancela la de la pizza`
- `cómo va a estar el clima mañana?`

Comandos: `nuevo` reinicia la conversación, `salir` cierra el programa.

## Agregar una herramienta

1. Crea un archivo en `asistente/herramientas/` con sus funciones, `DEFINICIONES` y `FUNCIONES` (usa `alarmas.py` de ejemplo).
2. Regístrala en `asistente/herramientas/__init__.py`.

## Hoja de ruta

- [x] Cerebro con Claude y búsqueda web
- [x] Alarmas y temporizadores
- [ ] Guardar alarmas al cerrar el programa
- [ ] Voz (escuchar y hablar)
- [ ] Palabra de activación
- [ ] Interfaz en pantalla
- [ ] Correr en un Android
