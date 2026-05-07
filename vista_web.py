#!/usr/bin/env python3
"""
Vista web local para Wanbe.

Este archivo permite visualizar la app desde una URL local del navegador.
La lógica y los datos vienen de proyecto.py para mantener Python como base.
"""

from __future__ import annotations

from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse
import sys

from proyecto import COLORS, MENU, TRAMITES, buscar_recursivo, encontrar_categoria

# ========== CONFIGURACIÓN DEL SERVIDOR ==========
# Este archivo convierte la lógica de proyecto.py en una interfaz web accesible desde el navegador
# Se importan las funciones de búsqueda y navegación para reutilizar la misma lógica

BASE_DIR = Path(__file__).resolve().parent  # Directorio del archivo actual
HOST = "127.0.0.1"  # Localhost: solo accesible localmente
DEFAULT_PORT = 8000  # Puerto por defecto para el servidor


# ========== FUNCIONES DE RUTEO ==========
# Generan URLs HTML que corresponden a las rutas del servidor HTTP

def crear_ruta(categoria_id: str) -> str:
    """Crea una URL para abrir una categoria.
    
    Ejemplo: crear_ruta('sat') -> '/categoria/sat'
    Luego el navegador hace GET /categoria/sat y WanbeHandler lo maneja.
    """
    return f"/categoria/{categoria_id}"


def crear_ruta_tramite(tramite_id: str) -> str:
    """Crea una URL para abrir un tramite.
    
    Ejemplo: crear_ruta_tramite('calcomania') -> '/tramite/calcomania'
    """
    return f"/tramite/{tramite_id}"


# ========== FUNCIONES DE RENDERIZADO HTML ==========
# Generan HTML completo que el navegador muestra
# Cada funcion retorna un string con HTML valido

def render_layout(titulo: str, contenido: str) -> str:
    """Plantilla general (master template) de la vista web.
    
    Contiene:
    - Variables CSS con los colores de COLORS (proyecto.py)
    - Header con logo y título
    - Main con el contenido dinámico
    - Estilos responsivos para móviles
    
    Nota: Los colores vienen directamente del diccionario COLORS
    para mantener coherencia entre escritorio y web.
    """
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(titulo)} - Wanbe</title>
  <style>
    @property --glow {{
      syntax: '<color>';
      inherits: false;
      initial-value: transparent;
    }}
    :root {{
      --bg: {COLORS["background"]};
      --white: {COLORS["white"]};
      --card: {COLORS["card"]};
      --text: {COLORS["text"]};
      --muted: {COLORS["muted"]};
      --border: {COLORS["border"]};
      --primary: {COLORS["primary"]};
      --purple: {COLORS["purple"]};
      --soft-blue: {COLORS["soft_blue"]};
      --warning-bg: {COLORS["warning_bg"]};
      --warning: {COLORS["warning"]};
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      background:
        radial-gradient(circle at top left, rgba(92, 19, 153, 0.14), transparent 34%),
        radial-gradient(circle at right top, rgba(120, 134, 199, 0.16), transparent 28%),
        linear-gradient(180deg, #f4f7ff 0%, #e9eefc 100%);
      color: var(--text);
      font-family: "Segoe UI", "Aptos", "Helvetica Neue", Arial, sans-serif;
    }}
    .phone {{
      width: min(440px, calc(100% - 18px));
      min-height: calc(100vh - 18px);
      margin: 9px auto;
      background: var(--white);
      border: 1px solid rgba(219, 227, 240, 0.9);
      border-radius: 24px;
      box-shadow: 0 20px 60px rgba(24, 52, 153, 0.15);
      overflow: hidden;
    }}
    header {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 14px 16px 13px;
      border-bottom: 1px solid var(--border);
      background: var(--white);
      position: sticky;
      top: 0;
      z-index: 2;
      backdrop-filter: blur(8px);
    }}
    header img {{ width: 44px; height: 44px; object-fit: contain; filter: drop-shadow(0 4px 10px rgba(24, 52, 153, 0.14)); }}
    header strong {{ display: block; color: var(--primary); font-size: 18px; letter-spacing: 0.4px; }}
    header span {{ color: var(--muted); font-size: 11px; font-weight: 700; }}
    main {{ padding: 16px; }}
    .hero {{
      background: linear-gradient(135deg, #4e0f88 0%, var(--purple) 42%, var(--primary) 100%);
      color: white;
      padding: 22px 18px 20px;
      margin-bottom: 14px;
      border-radius: 20px;
      box-shadow: 0 14px 28px rgba(92, 19, 153, 0.18);
    }}
    .hero h1 {{ margin: 0 0 8px; font-size: 24px; line-height: 1.1; letter-spacing: -0.3px; }}
    .hero p {{ margin: 0; color: #dbeafe; font-size: 13px; line-height: 1.4; }}
    form {{ display: flex; gap: 8px; margin-bottom: 14px; }}
    input {{
      flex: 1;
      min-width: 0;
      border: 1px solid var(--border);
      background: var(--card);
      color: var(--text);
      padding: 12px 14px;
      font-size: 14px;
      outline: none;
      border-radius: 14px;
    }}
    button, .button {{
      border: 0;
      background: var(--primary);
      color: white;
      padding: 12px 14px;
      font-weight: 700;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      min-height: 42px;
      border-radius: 14px;
      transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
    }}
    button:hover, .button:hover {{ transform: translateY(-1px); box-shadow: 0 10px 18px rgba(24, 52, 153, 0.14); }}
    .back {{ background: var(--card); color: var(--text); margin-bottom: 12px; box-shadow: none; }}
    .section-title {{ margin: 4px 0 12px; }}
    .section-title h2 {{ margin: 0; color: var(--primary); font-size: 21px; }}
    .section-title p {{ margin: 5px 0 0; color: var(--muted); font-size: 13px; }}
    .card {{
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 14px;
      border: 1px solid var(--border);
      background: var(--white);
      color: var(--text);
      text-decoration: none;
      margin-bottom: 10px;
      border-radius: 18px;
      box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
      transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }}
    .card:hover {{ transform: translateY(-2px); border-color: rgba(24, 52, 153, 0.22); box-shadow: 0 14px 26px rgba(24, 52, 153, 0.12); }}
    .icon {{
      width: 44px;
      min-width: 44px;
      height: 44px;
      display: grid;
      place-items: center;
      background: var(--primary);
      color: white;
      font-weight: 800;
      font-size: 11px;
      border-radius: 14px;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }}
    .card h3 {{ margin: 0 0 4px; font-size: 16px; }}
    .card p {{ margin: 0; color: var(--muted); font-size: 12px; line-height: 1.35; }}
    .arrow {{ margin-left: auto; color: var(--primary); font-weight: 800; }}
    .panel {{
      border: 1px solid var(--border);
      background: var(--card);
      padding: 14px;
      margin-bottom: 12px;
      border-radius: 18px;
    }}
    .panel h3 {{ margin: 0 0 8px; font-size: 16px; }}
    .panel p, li {{ color: var(--muted); font-size: 13px; line-height: 1.45; }}
    .step {{ background: var(--white); }}
    .step-number {{ color: var(--purple); font-weight: 800; font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; }}
    .requirements {{ background: var(--warning-bg); border-color: rgba(146, 64, 14, 0.25); }}
    .requirements h3, .requirements li {{ color: var(--warning); }}
    @media (max-width: 420px) {{
      .phone {{ width: min(100% - 12px, 440px); margin: 6px auto; border-radius: 20px; }}
      main {{ padding: 12px; }}
      .hero h1 {{ font-size: 21px; }}
      form {{ flex-direction: column; }}
    }}
  </style>
</head>
<body>
  <div class="phone">
    <header>
      <img src="/assets/logo.png" alt="Wanbe">
      <div>
        <strong>WANBE</strong>
        <span>{escape(titulo)}</span>
      </div>
    </header>
    <main>
      {contenido}
    </main>
  </div>
</body>
</html>"""


def render_card(titulo: str, subtitulo: str, icono: str, url: str, color: str = "var(--primary)") -> str:
    """Genera una tarjeta visual reutilizable.
    
    Se usa para:
    - Mostrar categorías en la pantalla de inicio
    - Mostrar trámites dentro de una categoría
    - Mostrar resultados de búsqueda
    
    Parámetros:
        titulo: nombre del item (ej: 'Pago de Calcomanía')
        subtitulo: descripción breve (ej: 'Calcomanía y placas')
        icono: código corto (ej: 'CAR', 'DPI', 'PDF')
        url: ruta para hacer clic (ej: '/tramite/calcomania')
        color: color CSS del ícono (por defecto: azul primario)
    """
    return f"""
<a class="card" href="{escape(url)}">
  <span class="icon" style="background:{color};">{escape(icono)}</span>
  <span>
    <h3>{escape(titulo)}</h3>
    <p>{escape(subtitulo)}</p>
  </span>
  <span class="arrow">&gt;</span>
</a>"""


def render_inicio(query: str = "") -> str:
    """Pantalla principal del navegador.
    
    TEMA: Búsqueda dinámica en la web
    - Si query está vacío: muestra las guías disponibles
    - Si query tiene texto: llama buscar_recursivo (igual que en escritorio)
    - Muestra un aviso cuando hay búsqueda activa
    - Se llama desde WanbeHandler cuando hace GET /
    """
    if query:
        resultados = buscar_recursivo(MENU, query)
        if resultados:
            tarjetas = "\n".join(
                render_card(
                    item["titulo"],
                    item["subtitulo"],
                    item["icono"],
                    crear_ruta_tramite(item["id"]) if item["tipo"] == "tramite" else crear_ruta(item["id"]),
                    "var(--soft-blue)",
                )
                for item in resultados
            )
        else:
            tarjetas = '<div class="panel"><h3>No encontrado</h3><p>Intenta buscar con otra palabra.</p></div>'
    else:
        tarjetas = "\n".join(
            render_card(nodo["titulo"], nodo["subtitulo"], nodo["icono"], crear_ruta(nodo["id"]))
            for nodo in MENU
        )

    contexto_busqueda = ""
    if query:
        contexto_busqueda = f'<div class="notice">Mostrando resultados para: <strong>{escape(query)}</strong></div>'

    return render_layout(
        "Inicio",
        f"""
<section class="hero">
  <h1>¿En qué trámite te guiamos hoy?</h1>
</section>
<form action="/" method="get">
  <input name="q" value="{escape(query)}" placeholder="Buscar tramite...">
  <button type="submit">Buscar</button>
</form>
{contexto_busqueda}
<section class="section-title">
  <h2>Guías disponibles</h2>
  <p>Selecciona el tramite que deseas revisar.</p>
</section>
{tarjetas}
""",
    )


def render_categoria(categoria_id: str) -> str:
    """Muestra una categoría con sus trámites/subcategorías.
    
    Se llama desde WanbeHandler cuando hace GET /categoria/{id}
    Usa encontrar_categoria (recursivo) para buscar en el árbol MENU.
    """
    categoria = encontrar_categoria(MENU, categoria_id)
    if categoria is None:
        return render_layout("No encontrado", '<a class="button back" href="/">Volver</a><div class="panel"><h3>No encontrado</h3></div>')

    tarjetas = []
    for hijo in categoria.get("hijos", []):
        if "tramite" in hijo:
            tramite_id = hijo["tramite"]
            tramite = TRAMITES[tramite_id]
            tarjetas.append(
                render_card(
                    tramite["titulo"],
                    tramite["descripcion"],
                    tramite["icono"],
                    crear_ruta_tramite(tramite_id),
                    "var(--purple)",
                )
            )
        else:
            tarjetas.append(render_card(hijo["titulo"], hijo["subtitulo"], hijo["icono"], crear_ruta(hijo["id"])))

    return render_layout(
        categoria["titulo"],
        f"""
<a class="button back" href="/">Volver</a>
<section class="section-title">
  <h2>{escape(categoria["titulo"])}</h2>
  <p>{escape(categoria["subtitulo"])}</p>
</section>
{''.join(tarjetas)}
""",
    )


def obtener_categoria_por_portal(portal: str) -> str:
    """Mapea el portal ('SAT' o 'RENAP') a su categoria principal.
    
    Se usa para saber a donde ir al hacer 'Regresar' desde un tramite.
    """
    if portal == "SAT":
        return "sat"
    return "renap"


def render_tramite(tramite_id: str, paso_actual: int = 1) -> str:
    """Muestra un paso específico de un trámite.
    
    DIFERENCIA CON ESCRITORIO:
    - En escritorio: todos los pasos se cargan en memoria y cambias con botones
    - En web: cada paso es una URL diferente (?paso=N)
    
    Muestra:
    - Barra de progreso con porcentaje
    - Título y descripción del paso
    - Lista de ítems/instrucciones
    - Enlace oficial si existe
    - Botones para ir al paso anterior/siguiente
    - Siempre muestra los requisitos (documentos indispensables)
    """
    tramite = TRAMITES.get(tramite_id)
    if tramite is None:
        return render_layout("No encontrado", '<a class="button back" href="/">Volver</a><div class="panel"><h3>No encontrado</h3></div>')

    requisitos = "".join(f"<li>{escape(requisito)}</li>" for requisito in tramite["requisitos"])
    total_pasos = len(tramite["pasos"])
    paso_actual = max(1, min(paso_actual, total_pasos))
    paso = tramite["pasos"][paso_actual - 1]
    progreso = int((paso_actual / total_pasos) * 100)

    items = "".join(f"<li>{escape(item)}</li>" for item in paso["items"])
    enlace = ""
    if paso.get("enlace"):
        enlace = f'<a class="button" href="{escape(paso["enlace"])}" target="_blank" rel="noopener">Abrir enlace oficial</a>'

    categoria_url = crear_ruta(obtener_categoria_por_portal(tramite["portal"]))
    regresar_url = (
        f"{crear_ruta_tramite(tramite_id)}?paso={paso_actual - 1}"
        if paso_actual > 1
        else categoria_url
    )
    continuar_url = (
        f"{crear_ruta_tramite(tramite_id)}?paso={paso_actual + 1}"
        if paso_actual < total_pasos
        else "/"
    )
    continuar_texto = "Continuar" if paso_actual < total_pasos else "Finalizar"

    paso_html = f"""
<article class="panel step">
  <div class="step-number">Paso {paso_actual} de {total_pasos}</div>
  <div class="progress" aria-label="Progreso del tramite">
    <span style="width:{progreso}%"></span>
  </div>
  <h3>{escape(paso["titulo"])}</h3>
  <p>{escape(paso["texto"])}</p>
  <ul>{items}</ul>
  {enlace}
</article>
<nav class="step-nav" aria-label="Navegacion de pasos">
  <a class="button secondary" href="{escape(regresar_url)}">Regresar</a>
  <a class="button" href="{escape(continuar_url)}">{continuar_texto}</a>
</nav>"""

    return render_layout(
        tramite["titulo"],
        f"""
<a class="button back" href="/">Volver</a>
<section class="section-title">
  <h2>{escape(tramite["titulo"])}</h2>
  <p>{escape(tramite["descripcion"])}</p>
</section>
<section class="panel requirements">
  <h3>Documentos indispensables</h3>
  <ul>{requisitos}</ul>
</section>
{paso_html}
""",
    )


# ========== SERVIDOR HTTP ==========

class WanbeHandler(BaseHTTPRequestHandler):
    """Manejador HTTP que procesa las solicitudes del navegador.
    
    TEMA DE PROGRAMACION: Arquitectura cliente-servidor
    - El navegador hace GET /ruta
    - Este handler recibe la solicitud y decide qué renderizar
    - Retorna HTML para que el navegador lo muestre
    
    Rutas soportadas:
    - GET /  -> render_inicio (pantalla principal)
    - GET /categoria/{id}  -> render_categoria
    - GET /tramite/{id}?paso=N  -> render_tramite
    - GET /assets/logo.png  -> imagen (binario)
    """

    def do_GET(self) -> None:
        """Maneja las solicitudes GET del navegador.
        
        Pasos:
        1. Parsear la URL (path y query string)
        2. Determinar qué recurso se solicita
        3. Renderizar HTML o servir archivo (asset)
        4. Enviar respuesta HTTP
        """
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        # Servir imagen del logo
        if path == "/assets/logo.png":
            self.send_asset("logo.png", "image/png")
            return

        # Ruta raiz: pantalla principal
        if path == "/":
            # Extraer parametro 'q' de la URL (?q=busqueda)
            query = parse_qs(parsed.query).get("q", [""])[0].strip()
            self.send_html(render_inicio(query))
            return

        # Ruta de categoria: /categoria/sat o /categoria/renap
        if path.startswith("/categoria/"):
            categoria_id = path.removeprefix("/categoria/")
            self.send_html(render_categoria(categoria_id))
            return

        # Ruta de tramite: /tramite/calcomania?paso=2
        if path.startswith("/tramite/"):
            # Extraer numero del paso (?paso=1, ?paso=2, etc)
            tramite_id = path.removeprefix("/tramite/")
            paso_str = parse_qs(parsed.query).get("paso", ["1"])[0]
            try:
                paso_actual = int(paso_str)
            except ValueError:
                paso_actual = 1  # Por defecto: paso 1
            self.send_html(render_tramite(tramite_id, paso_actual))
            return

        # Si ninguna ruta coincide: error 404 (no encontrado)
        self.send_response(404)
        self.end_headers()

    def send_html(self, html: str) -> None:
        """Envía una respuesta HTTP con contenido HTML al navegador.
        
        Pasos:
        1. Codificar el string HTML a bytes (UTF-8)
        2. Enviar header HTTP 200 (OK)
        3. Indicar que es HTML con charset UTF-8
        4. Enviar el cuerpo de la respuesta
        """
        encoded = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def send_asset(self, filename: str, content_type: str) -> None:
        """Sirve archivos binarios (imágenes) desde la carpeta assets.
        
        Diferente a send_html porque:
        - Carga datos binarios (no es texto)
        - Usa Content-Type específíco (image/png, etc)
        - Si el archivo no existe, retorna 404
        """
        path = BASE_DIR / "assets" / filename
        if not path.exists():
            self.send_response(404)
            self.end_headers()
            return
        data = path.read_bytes()  # Leer el archivo binario
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def run_server(port: int = DEFAULT_PORT) -> None:
    """Inicia el servidor web local.
    
    TEMA: Servidores web
    - ThreadingHTTPServer: crea un servidor que maneja múltiples conexiones
    - (HOST, port): donde escucha (localhost:8000)
    - WanbeHandler: clase que procesa las solicitudes
    - serve_forever(): bloquea y espera conexiones indefinidamente
    
    Para cerrar: Ctrl+C en la terminal
    """
    server = ThreadingHTTPServer((HOST, port), WanbeHandler)
    print(f"Wanbe web disponible en http://{HOST}:{port}")
    print("Presiona Ctrl+C para detener el servidor.")
    server.serve_forever()


# ========== PUNTO DE ENTRADA ==========

if __name__ == "__main__":
    # Permite usar: python vista_web.py 9000
    # Para correr el servidor en puerto 9000 en lugar del 8000 por defecto
    selected_port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    run_server(selected_port)
