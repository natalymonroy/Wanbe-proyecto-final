# Wanbe proyecto final

Aplicacion visual sencilla creada en Python con `tkinter`.

La idea es conservar la base de la app Wanbe original, pero en una version mas simple:

- Pantalla de inicio con buscador.
- Categorias SAT y RENAP.
- Checklist de requisitos antes de iniciar cada trámite.
- Guía paso a paso con barra de progreso.
- Enlaces a portales oficiales o de referencia.

El proyecto se centra solo en tres guías:

- NIT
- DPI
- Calcomanía

## Temas de Python usados

- Listas para requisitos y pasos.
- Matrices para rutas de navegación.
- Diccionarios para guardar la información de trámites.
- Recursión en el buscador y en la búsqueda de categorías.
- Interfaz gráfica con `tkinter`.

## Ejecutar

Aplicacion de escritorio:

```bash
python3 proyecto.py
```

Vista web local:

```bash
python3 vista_web.py
```

Luego abrir:

```text
http://127.0.0.1:8000
```

## Instalación y dependencias

Instala las dependencias mínimas (solo necesarias si vas a extraer PDFs u otras tareas):

```bash
python3 -m pip install -r requirements.txt
```

## Persistencia de estado

La aplicación guarda un archivo JSON en `data/state.json` con el estado de la sesión (paso actual, checklist, configuración e historial). Si el archivo no existe, se crea automáticamente.

Si quieres reiniciar el estado, borra `data/state.json` y vuelve a arrancar la app.

## Mapeo rápido a la rúbrica

- POO: clase `WanbeApp` en `app.py`.
- Funciones: utilidades en `utils.py` (`normalizar`, `buscar_recursivo`, `encontrar_categoria`) y persistencia en `data.py` (`cargar_estado`, `guardar_estado`).
- Estructuras de datos: `TRAMITES` y `MENU` en `data.py` (diccionarios y listas).
- Manejo de archivos: lectura/escritura JSON en `data/state.json` (con try/except).
- Recursión: `buscar_recursivo` y `encontrar_categoria`.
- Tests: pendientes (se recomienda `pytest` para funciones puras y persistencia).

## Sugerencia de commit

Commit propuesto para estos cambios:

```
git add .
git commit -m "Refactor: separar en módulos (data, utils, app), añadir persistencia JSON y vista web ajustada"
```

