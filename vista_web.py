#!/usr/bin/env python3
"""
Vista web local para Wanbe.

Este archivo permite visualizar la app desde una URL local del navegador.
La logica y los datos vienen de proyecto.py para mantener Python como base.
"""

from __future__ import annotations

from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse
import sys

from proyecto import COLORS, MENU, TRAMITES, buscar_recursivo, encontrar_categoria


BASE_DIR = Path(__file__).resolve().parent
HOST = "127.0.0.1"
DEFAULT_PORT = 8000


def crear_ruta(categoria_id: str) -> str:
    """Crea una URL para abrir una categoria."""
    return f"/categoria/{categoria_id}"


def crear_ruta_tramite(tramite_id: str) -> str:
    """Crea una URL para abrir un tramite."""
    return f"/tramite/{tramite_id}"


def render_layout(titulo: str, contenido: str) -> str:
    """Plantilla general de la vista web."""
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(titulo)} - Wanbe</title>
  <style>
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
      background: var(--bg);
      color: var(--text);
      font-family: Arial, Helvetica, sans-serif;
    }}
    .phone {{
      width: min(430px, calc(100% - 20px));
      min-height: calc(100vh - 20px);
      margin: 10px auto;
      background: var(--white);
      border: 1px solid var(--border);
      box-shadow: 0 18px 40px rgba(24, 52, 153, 0.12);
      overflow: hidden;
    }}
    header {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 14px 16px;
      border-bottom: 1px solid var(--border);
      background: var(--white);
      position: sticky;
      top: 0;
      z-index: 2;
    }}
    header img {{ width: 44px; height: 44px; object-fit: contain; }}
    header strong {{ display: block; color: var(--primary); font-size: 18px; }}
    header span {{ color: var(--muted); font-size: 11px; font-weight: 700; }}
    main {{ padding: 16px; }}
    .hero {{
      background: linear-gradient(135deg, var(--purple), var(--primary));
      color: white;
      padding: 22px 18px;
      margin-bottom: 14px;
    }}
    .hero h1 {{ margin: 0 0 8px; font-size: 24px; line-height: 1.12; }}
    .hero p {{ margin: 0; color: #dbeafe; font-size: 13px; line-height: 1.4; }}
    form {{ display: flex; gap: 8px; margin-bottom: 14px; }}
    input {{
      flex: 1;
      min-width: 0;
      border: 1px solid var(--border);
      background: var(--card);
      color: var(--text);
      padding: 12px;
      font-size: 14px;
      outline: none;
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
    }}
    .back {{ background: var(--card); color: var(--text); margin-bottom: 12px; }}
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
    }}
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
    }}
    .card h3 {{ margin: 0 0 4px; font-size: 16px; }}
    .card p {{ margin: 0; color: var(--muted); font-size: 12px; line-height: 1.35; }}
    .arrow {{ margin-left: auto; color: var(--primary); font-weight: 800; }}
    .panel {{
      border: 1px solid var(--border);
      background: var(--card);
      padding: 14px;
      margin-bottom: 12px;
    }}
    .panel h3 {{ margin: 0 0 8px; font-size: 16px; }}
    .panel p, li {{ color: var(--muted); font-size: 13px; line-height: 1.45; }}
    .step {{ background: var(--white); }}
    .step-number {{ color: var(--purple); font-weight: 800; font-size: 12px; }}
    .requirements {{ background: var(--warning-bg); border-color: var(--warning); }}
    .requirements h3, .requirements li {{ color: var(--warning); }}
    @media (max-width: 420px) {{
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
    """Genera una tarjeta visual reutilizable."""
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
    """Pagina principal con SAT y RENAP."""
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

    return render_layout(
        "Inicio",
        f"""
<section class="hero">
  <h1>En que tramite te guiamos hoy?</h1>
  <p>Guia visual sencilla para tramites de SAT y RENAP.</p>
</section>
<form action="/" method="get">
  <input name="q" value="{escape(query)}" placeholder="Buscar tramite...">
  <button type="submit">Buscar</button>
</form>
<section class="section-title">
  <h2>Categorias</h2>
  <p>Selecciona el portal del tramite que deseas revisar.</p>
</section>
{tarjetas}
""",
    )


def render_categoria(categoria_id: str) -> str:
    """Pagina de categoria SAT o RENAP."""
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


def render_tramite(tramite_id: str) -> str:
    """Pagina de detalle de un tramite."""
    tramite = TRAMITES.get(tramite_id)
    if tramite is None:
        return render_layout("No encontrado", '<a class="button back" href="/">Volver</a><div class="panel"><h3>No encontrado</h3></div>')

    requisitos = "".join(f"<li>{escape(requisito)}</li>" for requisito in tramite["requisitos"])
    pasos = []
    for numero, paso in enumerate(tramite["pasos"], start=1):
        items = "".join(f"<li>{escape(item)}</li>" for item in paso["items"])
        enlace = ""
        if paso.get("enlace"):
            enlace = f'<a class="button" href="{escape(paso["enlace"])}" target="_blank" rel="noopener">Abrir enlace oficial</a>'
        pasos.append(
            f"""
<article class="panel step">
  <div class="step-number">Paso {numero}</div>
  <h3>{escape(paso["titulo"])}</h3>
  <p>{escape(paso["texto"])}</p>
  <ul>{items}</ul>
  {enlace}
</article>"""
        )

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
{''.join(pasos)}
""",
    )


class WanbeHandler(BaseHTTPRequestHandler):
    """Manejador HTTP de la vista web."""

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        if path == "/assets/logo.png":
            self.send_asset("logo.png", "image/png")
            return

        if path == "/":
            query = parse_qs(parsed.query).get("q", [""])[0].strip()
            self.send_html(render_inicio(query))
            return

        if path.startswith("/categoria/"):
            self.send_html(render_categoria(path.removeprefix("/categoria/")))
            return

        if path.startswith("/tramite/"):
            self.send_html(render_tramite(path.removeprefix("/tramite/")))
            return

        self.send_response(404)
        self.end_headers()

    def send_html(self, html: str) -> None:
        encoded = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def send_asset(self, filename: str, content_type: str) -> None:
        path = BASE_DIR / "assets" / filename
        if not path.exists():
            self.send_response(404)
            self.end_headers()
            return
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def run_server(port: int = DEFAULT_PORT) -> None:
    """Inicia el servidor web local."""
    server = ThreadingHTTPServer((HOST, port), WanbeHandler)
    print(f"Wanbe web disponible en http://{HOST}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    selected_port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    run_server(selected_port)
