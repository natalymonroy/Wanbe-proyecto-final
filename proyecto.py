#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wanbe en Python
---------------
Base de aplicacion visual inspirada en la app web incluida en este proyecto.

Conceptos de Python aplicados:
- Listas: requisitos, pasos y tarjetas de menu.
- Matrices: rutas de navegacion, portales municipales y agencias.
- Recursion: busqueda de tramites dentro de un arbol de categorias.
- Diccionarios y clases: datos estructurados para guias y pantallas.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import sys
import tkinter as tk
from tkinter import messagebox
import unicodedata
import webbrowser


BASE_DIR = Path(__file__).resolve().parent


LIGHT_THEME = {
    "app_bg": "#eef3ff",
    "shell_bg": "#ffffff",
    "surface": "#ffffff",
    "surface_alt": "#f8fafc",
    "text": "#0f172a",
    "muted": "#64748b",
    "border": "#dbe3f0",
    "primary": "#183499",
    "secondary": "#5C1399",
    "accent": "#7886C7",
    "success": "#15803d",
    "warning_bg": "#fff7ed",
    "warning_text": "#92400e",
    "disabled": "#cbd5e1",
}

DARK_THEME = {
    "app_bg": "#020617",
    "shell_bg": "#0f172a",
    "surface": "#111827",
    "surface_alt": "#1f2937",
    "text": "#e2e8f0",
    "muted": "#cbd5e1",
    "border": "#334155",
    "primary": "#93c5fd",
    "secondary": "#c4b5fd",
    "accent": "#a5b4fc",
    "success": "#86efac",
    "warning_bg": "#451a03",
    "warning_text": "#fdba74",
    "disabled": "#475569",
}


@dataclass
class Step:
    title: str
    body: str
    bullets: list[str] = field(default_factory=list)
    action_label: str | None = None
    action_url: str | None = None
    kind: str | None = None


@dataclass
class Guide:
    guide_id: str
    page_id: str
    title: str
    subtitle: str
    icon: str
    portal: str
    accent: str
    requirements: list[str]
    steps: list[Step]


# Matriz: cada fila representa una ruta de navegacion completa dentro de la app.
NAVIGATION_MATRIX = [
    ["home", "sat", "vehiculos", "tutorial-calcomania"],
    ["home", "sat", "individuales", "tutorial-nit"],
    ["home", "sat", "juridicos", "tutorial-libros"],
    ["home", "renap", "tutorial-dpi"],
    ["home", "renap", "tutorial-certificados"],
    ["home", "muni", "multas-transito"],
    ["home", "muni", "impuestos-municipales"],
    ["home", "muni", "pago-servicios"],
]

# Matriz: portal, nombre visible, url.
MUNICIPAL_PORTAL_MATRIX = [
    ["Muni Guate", "https://especiales.muniguate.com/remisiones.htm"],
    ["Muni Mixco", "https://consultas.munimixco.gob.gt/emixtra/consulta"],
    ["Sta. Catarina Pinula", "http://www.consultas.scp.gob.gt/transito/"],
    ["Villa Nueva", "https://www.villanueva.gob.gt/"],
    ["PNC / Provincia", "https://sistemas.transito.gob.gt/consultaremisiones/consultaremisiones"],
]

# Matriz: entidad, sede, direccion, horario.
AGENCY_MATRIX = [
    ["SAT", "Galerias Primma", "Calzada Roosevelt, zona 7", "08:00 - 16:00"],
    ["SAT", "SAT Dubai Center", "Zona 10, Ciudad de Guatemala", "08:00 - 16:00"],
    ["RENAP", "RENAP Sede Central", "Calzada Roosevelt 13-46, zona 7", "08:00 - 16:00"],
    ["RENAP", "RENAP Zona 9", "7a avenida, zona 9", "08:00 - 16:00"],
]

# Matriz: clave, titulo, descripcion. Se usa en la guia NIT para elegir ruta.
NIT_ROUTE_MATRIX = [
    ["sin_obligaciones", "Sin actividad economica", "Ruta rapida para estudiantes, desempleados o jubilados."],
    ["asalariado", "Relacion de dependencia", "Para trabajar en una empresa formal como asalariado."],
    ["negocio", "Negocio o facturacion", "Para negocio propio, freelance o emision de facturas."],
]


GUIDES: dict[str, Guide] = {
    "calcomania": Guide(
        guide_id="calcomania",
        page_id="tutorial-calcomania",
        title="Pago de Calcomania (ISCV)",
        subtitle="Guia completa paso a paso",
        icon="🚗",
        portal="SAT",
        accent="#183499",
        requirements=[
            "Placa del vehiculo",
            "NIT del propietario del vehiculo",
        ],
        steps=[
            Step(
                "Consulta de multas",
                "Antes de generar el formulario, verifica si el vehiculo tiene multas pendientes.",
                ["Selecciona tu municipalidad.", "Consulta por placa o numero de multa.", "Guarda captura o comprobante."],
                kind="municipality",
            ),
            Step(
                "Generar Formulario SAT-4091",
                "Debes congelar el formulario para obtener el numero de pago.",
                [
                    "En Declaraguate busca la seccion 5. Vehiculos.",
                    "Selecciona Vehiculos Circulacion.",
                    "Ingresa NIT y placa, valida y congela.",
                ],
                "Abrir Declaraguate",
                "https://declaraguate.sat.gob.gt/declaraguate-web/",
            ),
            Step(
                "Pago en banco",
                "Para pagar en linea o en agencia bancaria necesitas los datos generados por el formulario.",
                ["Numero de formulario.", "Numero de acceso.", "Verifica el monto antes de confirmar."],
            ),
            Step(
                "Impresion final",
                "Despues del pago descarga el distintivo en PDF para portarlo en el vehiculo.",
                ["Imprime o guarda el PDF.", "Comprueba que la placa sea correcta."],
                "Imprimir calcomania",
                "https://portal.sat.gob.gt/portal/impresion-calcomania/",
            ),
            Step(
                "Confirmacion",
                "Marca el tramite como listo cuando ya consultaste multas, pagaste y descargaste el distintivo.",
                ["Consultaste multas.", "Pagaste con numero de acceso.", "Descargaste tu calcomania."],
            ),
        ],
    ),
    "nit": Guide(
        guide_id="nit",
        page_id="tutorial-nit",
        title="Solicitud Electronica de NIT",
        subtitle="Tramite por primera vez",
        icon="👤",
        portal="SAT",
        accent="#7886C7",
        requirements=[
            "DPI original vigente",
            "Recibo de luz o agua para direccion fiscal",
            "Correo electronico valido",
        ],
        steps=[
            Step(
                "Abre el portal de la SAT",
                "Inicia el proceso desde el portal oficial de solicitud electronica de NIT.",
                ["Completa el captcha.", "Escribe tu correo personal.", "Solicita el link de acceso."],
                "Ir al portal NIT",
                "https://portal.sat.gob.gt/portal/solicitud-electronica-de-nit/",
            ),
            Step(
                "Validacion de correo",
                "Busca el mensaje de la SAT en tu bandeja de entrada y copia el codigo o link enviado.",
                ["Revisa spam o promociones si no aparece.", "Usa solamente el enlace recibido por la SAT."],
            ),
            Step(
                "Datos de identificacion",
                "Completa nacionalidad, DPI, serie del DPI y datos complementarios.",
                [
                    "El numero de serie esta al reverso del DPI.",
                    "Sube documentos legibles.",
                    "Marca NO en camaras empresariales si no participas.",
                ],
            ),
            Step(
                "Actividad economica",
                "Selecciona tu situacion para que la guia prepare la ruta correcta.",
                kind="nit_route",
            ),
            Step(
                "Ubicaciones y acceso",
                "Registra tu domicilio fiscal y crea los datos de acceso para Agencia Virtual.",
                [
                    "Copia la direccion como aparece en tu recibo.",
                    "Usa un correo que puedas revisar siempre.",
                    "Crea una clave segura y privada.",
                ],
            ),
            Step(
                "Afiliaciones",
                "Configura las obligaciones que correspondan segun tu perfil.",
                [
                    "Sin obligaciones: puedes continuar sin afiliaciones.",
                    "Asalariado: revisa ISR si corresponde.",
                    "Negocio: normalmente inicia como pequeno contribuyente.",
                ],
                kind="nit_affiliations",
            ),
            Step(
                "Establecimiento",
                "Si tienes negocio, registra los datos del establecimiento.",
                [
                    "Indica si opera en tu casa o en otra direccion.",
                    "Elige nombre comercial si aplica.",
                    "Verifica actividad, fecha de inicio y direccion.",
                ],
                kind="nit_establishment",
            ),
            Step(
                "Resumen del tramite",
                "Revisa todo antes de enviar. Al aprobarse, recibiras tu NIT y acceso a Agencia Virtual.",
                ["Protege tu usuario y contrasena.", "No compartas accesos por canales no oficiales."],
            ),
        ],
    ),
    "libros": Guide(
        guide_id="libros",
        page_id="tutorial-libros",
        title="Habilitacion de Libros",
        subtitle="Formulario SAT-7121",
        icon="🏢",
        portal="SAT",
        accent="#5C1399",
        requirements=[
            "Resoluciones de habilitacion",
            "Boletas SAT-2000 pagadas",
            "Libros operados y al dia",
        ],
        steps=[
            Step(
                "Ingreso a Declaraguate",
                "Busca en la seccion 7. Varios el formulario SAT-7121.",
                ["Selecciona Habilitacion y autorizacion de libros."],
                "Abrir formulario",
                "https://declaraguate.sat.gob.gt/declaraguate-web/",
            ),
            Step(
                "Identificacion",
                "Ingresa los datos del contribuyente o de la tercera persona autorizada.",
                ["NIT contribuyente.", "Contrasena SAT en Linea.", "NIT de tercero si aplica."],
            ),
            Step(
                "Configuracion de libros",
                "Selecciona tipo de libro, modalidad y establecimiento segun corresponda.",
                ["Manual o computarizado.", "Establecimiento si aplica.", "Cantidad y tipo de libros."],
            ),
            Step(
                "Pago de boleta",
                "Congela el formulario, imprime SAT-2000 y paga en banca en linea o ventanilla.",
                ["Guarda la boleta pagada.", "Verifica numero de formulario y acceso."],
            ),
            Step(
                "Impresion de resolucion",
                "Regresa a Declaraguate, busca el formulario e imprime la resolucion final.",
                ["Archiva resolucion.", "Archiva boleta SAT-2000.", "Mantiene libros al dia."],
            ),
        ],
    ),
    "dpi": Guide(
        guide_id="dpi",
        page_id="tutorial-dpi",
        title="Tramite de DPI",
        subtitle="Guia paso a paso para mayores de edad",
        icon="🪪",
        portal="RENAP",
        accent="#5C1399",
        requirements=[
            "Certificado de nacimiento original con vigencia maxima de 6 meses",
            "Boleto de ornato original y fotocopia del año en curso",
        ],
        steps=[
            Step(
                "Obtener certificado de nacimiento",
                "Puedes solicitarlo en una oficina RENAP o desde el ePortal.",
                ["Presencial: paga Q15.00.", "En linea: paga Q19.00 y descarga el PDF."],
                "Abrir ePortal RENAP",
                "https://eportal.renap.gob.gt/",
            ),
            Step(
                "Pago en el banco",
                "La tarifa del Documento Personal de Identificacion es Q100.00.",
                ["Bancos: Banrural, Banco Industrial o Bantrab.", "Mayores de 60 años: tramite gratuito."],
            ),
            Step(
                "Visita a sede RENAP",
                "Acude de 08:00 a 16:00. No necesitas cita previa.",
                ["Evita ropa blanca, anteojos o gorra.", "Revisaran biometria y firma.", "Verifica tus datos antes de aprobar."],
            ),
            Step(
                "Seguimiento en linea",
                "Te entregaran una constancia de solicitud. El tiempo maximo de entrega es de 30 dias habiles.",
                ["Puedes consultar estado en web.", "Conserva la constancia original."],
                "Ver RENAP",
                "https://www.renap.gob.gt/",
            ),
            Step(
                "Recogida del DPI",
                "Se recomienda ir a la misma agencia aproximadamente 8 dias despues.",
                ["Lleva constancia original.", "Revisa el DPI al recibirlo."],
            ),
        ],
    ),
    "certificados": Guide(
        guide_id="certificados",
        page_id="tutorial-certificados",
        title="Certificados en Linea",
        subtitle="Solicita certificados RENAP desde casa",
        icon="📜",
        portal="RENAP",
        accent="#7886C7",
        requirements=[
            "CUI original vigente",
            "Correo electronico valido para confirmaciones",
        ],
        steps=[
            Step(
                "Accede al ePortal RENAP",
                "Ingresa a la plataforma en linea con tu CUI.",
                ["Si es primera vez, crea solicitud de usuario."],
                "Abrir ePortal",
                "https://eportal.renap.gob.gt/",
            ),
            Step(
                "Crea tu perfil usuario",
                "Registra CUI, correo electronico y una contrasena segura.",
                ["Usa un correo personal.", "Guarda tus credenciales."],
            ),
            Step(
                "Busca el certificado",
                "Selecciona Certificado de Nacimiento u otro certificado disponible.",
                ["Agregalo al carrito.", "Verifica nombres y datos antes de pagar."],
            ),
            Step(
                "Realiza el pago",
                "Los certificados cuestan Q19.00, mas gastos de envio si aplica.",
                ["Tarjeta de debito.", "Tarjeta de credito.", "Billetera movil si esta disponible."],
            ),
            Step(
                "Descarga digital",
                "El certificado se descarga en PDF despues del pago y tambien puede llegar por correo.",
                ["Guarda el PDF.", "Verifica que el codigo sea legible."],
            ),
        ],
    ),
    "multas": Guide(
        guide_id="multas",
        page_id="multas-transito",
        title="Multas de Transito",
        subtitle="Consulta y pago de remisiones",
        icon="🚦",
        portal="MUNI",
        accent="#15803d",
        requirements=[
            "Licencia de conducir vigente o cedula de identidad",
            "Placa del vehiculo o numero de multa",
        ],
        steps=[
            Step(
                "Ingresa al portal municipal",
                "Accede al portal de tu municipalidad o al portal de remisiones.",
                ["Selecciona el municipio correcto.", "Consulta por placa o numero de multa."],
                kind="municipality",
            ),
            Step(
                "Selecciona consultar multas",
                "Busca la opcion de consulta de infracciones o multas de transito.",
                ["Algunos sitios piden placa.", "Otros permiten numero de multa."],
            ),
            Step(
                "Ingresa placa o multa",
                "Escribe la placa del vehiculo o el numero de multa si lo tienes.",
                ["Ejemplo: P123ABC.", "Evita espacios o guiones si el portal no los acepta."],
            ),
            Step(
                "Revisa detalles",
                "El sistema mostrara fecha, cantidad y motivo de la infraccion.",
                ["Toma captura para tu registro.", "Verifica si hay descuento o recargo."],
            ),
            Step(
                "Paga en linea o presencial",
                "Puedes pagar con tarjeta si el portal lo permite o acudir a oficinas municipales.",
                ["Guarda comprobante.", "Confirma que la deuda quede en cero."],
            ),
        ],
    ),
    "impuestos": Guide(
        guide_id="impuestos",
        page_id="impuestos-municipales",
        title="Impuestos Municipales",
        subtitle="Consulta y pago de obligaciones locales",
        icon="🏛️",
        portal="MUNI",
        accent="#15803d",
        requirements=[
            "DPI vigente",
            "Recibo de luz o agua",
        ],
        steps=[
            Step(
                "Accede al portal de tu municipio",
                "Busca Contribuyentes, IUSI, Boleto de Ornato o Servicios Municipales.",
                ["Usa el portal oficial de tu municipalidad."],
                kind="municipality",
            ),
            Step(
                "Ingresa tus datos",
                "El sistema puede pedir NIT, DPI o numero de cuenta.",
                ["Usa los datos del contribuyente registrado.", "Verifica que el municipio sea correcto."],
            ),
            Step(
                "Revisa deuda actualizada",
                "Verifica montos, fechas de vencimiento y recargos si aplica.",
                ["IUSI.", "Boleto de ornato.", "Servicios o arbitrios municipales."],
            ),
            Step(
                "Genera boleta de pago",
                "El portal generara un comprobante con numero de referencia.",
                ["Descarga PDF.", "Revisa fecha limite."],
            ),
            Step(
                "Paga en banco o en linea",
                "Muchas municipalidades aceptan pago online; si no, lleva la boleta al banco.",
                ["Guarda comprobante.", "Verifica el estado despues del pago."],
            ),
        ],
    ),
    "servicios": Guide(
        guide_id="servicios",
        page_id="pago-servicios",
        title="Pago de Servicios",
        subtitle="Agua, luz, basura y otros servicios",
        icon="💳",
        portal="MUNI",
        accent="#15803d",
        requirements=[
            "Documento de identidad o numero de usuario",
            "Acceso a internet y medio de pago",
        ],
        steps=[
            Step(
                "Entra al portal de servicios",
                "Busca la seccion Pago de Servicios en el sitio de tu municipio.",
                ["Usa el portal oficial.", "Ten a mano tu recibo."],
                kind="municipality",
            ),
            Step(
                "Selecciona servicio",
                "Elige agua, alumbrado, basura u otro servicio disponible.",
                ["Agua.", "Electricidad o alumbrado.", "Recoleccion de basura."],
            ),
            Step(
                "Ingresa medidor o usuario",
                "El numero suele aparecer en tu recibo o factura del servicio.",
                ["Copia el numero sin errores.", "Confirma nombre o direccion si aparece."],
            ),
            Step(
                "Revisa monto y detalles",
                "Verifica que el monto sea correcto antes de pagar.",
                ["Puede mostrar 2 o 3 meses acumulados.", "Revisa recargos."],
            ),
            Step(
                "Realiza el pago",
                "Selecciona tarjeta, billetera digital o transferencia bancaria si esta disponible.",
                ["Guarda comprobante.", "Comprueba que el pago quede aplicado."],
            ),
        ],
    ),
}


MENU_TREE = [
    {
        "id": "sat",
        "title": "Portal SAT",
        "subtitle": "Vehiculos, NIT y empresas",
        "icon": "🏦",
        "children": [
            {
                "id": "vehiculos",
                "title": "Vehiculos",
                "subtitle": "Tramites de vehiculos",
                "icon": "🚗",
                "children": [{"guide": "calcomania"}],
            },
            {
                "id": "individuales",
                "title": "Individuales",
                "subtitle": "Personas individuales",
                "icon": "👤",
                "children": [{"guide": "nit"}],
            },
            {
                "id": "juridicos",
                "title": "Juridicos",
                "subtitle": "Empresas y libros",
                "icon": "🏢",
                "children": [{"guide": "libros"}],
            },
        ],
    },
    {
        "id": "renap",
        "title": "Portal RENAP",
        "subtitle": "DPI y certificados",
        "icon": "🪪",
        "children": [{"guide": "dpi"}, {"guide": "certificados"}],
    },
    {
        "id": "muni",
        "title": "Portal MUNI",
        "subtitle": "Multas, impuestos y servicios",
        "icon": "🏛️",
        "children": [{"guide": "multas"}, {"guide": "impuestos"}, {"guide": "servicios"}],
    },
]

PAGE_TITLES = {
    "home": "Inicio",
    "sat": "Portal SAT",
    "renap": "Portal RENAP",
    "muni": "Portal MUNI",
    "vehiculos": "Vehiculos",
    "individuales": "Individuales",
    "juridicos": "Juridicos",
    "settings": "Configuracion",
    "completion": "Tramite finalizado",
    "agencies-sat": "Agencias SAT",
    "agencies-renap": "Sedes RENAP",
}

GUIDE_PAGE_TO_ID = {guide.page_id: guide_id for guide_id, guide in GUIDES.items()}


def normalize_text(value: str) -> str:
    """Quita tildes y cambia a minusculas para comparar textos."""
    text = unicodedata.normalize("NFD", value.lower())
    return "".join(char for char in text if unicodedata.category(char) != "Mn")


def find_node_by_id(nodes: list[dict], page_id: str) -> dict | None:
    """Busqueda recursiva de una categoria por id."""
    for node in nodes:
        if node.get("id") == page_id:
            return node
        child = find_node_by_id(node.get("children", []), page_id)
        if child:
            return child
    return None


def recursive_search(nodes: list[dict], query: str, path: list[str] | None = None) -> list[dict]:
    """Busca categorias o tramites recorriendo el arbol MENU_TREE con recursion."""
    path = path or []
    results: list[dict] = []
    clean_query = normalize_text(query)

    for node in nodes:
        if "guide" in node:
            guide = GUIDES[node["guide"]]
            haystack = normalize_text(" ".join([guide.title, guide.subtitle, guide.portal, *guide.requirements]))
            if clean_query in haystack:
                results.append(
                    {
                        "type": "guide",
                        "target": guide.page_id,
                        "title": guide.title,
                        "subtitle": " > ".join(path + [guide.portal]),
                        "icon": guide.icon,
                    }
                )
            continue

        title = node.get("title", "")
        subtitle = node.get("subtitle", "")
        haystack = normalize_text(f"{title} {subtitle}")
        if clean_query in haystack:
            results.append(
                {
                    "type": "page",
                    "target": node["id"],
                    "title": title,
                    "subtitle": " > ".join(path) or subtitle,
                    "icon": node.get("icon", "•"),
                }
            )

        results.extend(recursive_search(node.get("children", []), query, path + [title]))

    return results


def count_guides_recursively(nodes: list[dict]) -> int:
    """Cuenta tramites del arbol con recursion; se muestra en configuracion."""
    total = 0
    for node in nodes:
        if "guide" in node:
            total += 1
        else:
            total += count_guides_recursively(node.get("children", []))
    return total


class GradientCard(tk.Canvas):
    def __init__(self, parent: tk.Widget, color_a: str, color_b: str, **kwargs):
        super().__init__(parent, highlightthickness=0, bd=0, **kwargs)
        self.color_a = color_a
        self.color_b = color_b
        self.bind("<Configure>", self._draw)

    @staticmethod
    def _hex_to_rgb(color: str) -> tuple[int, int, int]:
        color = color.lstrip("#")
        return tuple(int(color[index : index + 2], 16) for index in (0, 2, 4))

    @staticmethod
    def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
        return "#%02x%02x%02x" % rgb

    def _draw(self, _event: tk.Event | None = None) -> None:
        self.delete("gradient")
        width = max(self.winfo_width(), 1)
        height = max(self.winfo_height(), 1)
        start = self._hex_to_rgb(self.color_a)
        end = self._hex_to_rgb(self.color_b)

        for x in range(width):
            ratio = x / max(width - 1, 1)
            rgb = tuple(int(start[i] + (end[i] - start[i]) * ratio) for i in range(3))
            self.create_line(x, 0, x, height, fill=self._rgb_to_hex(rgb), tags=("gradient",))
        self.lower("gradient")


class WanbeApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Wanbe - Python")
        self.root.geometry("430x760")
        self.root.minsize(380, 620)

        self.dark_mode = False
        self.palette = LIGHT_THEME
        self.history: list[str] = ["home"]
        self.current_page = "home"
        self.images: dict[str, tk.PhotoImage] = {}
        self.guide_started = {guide_id: False for guide_id in GUIDES}
        self.guide_step = {guide_id: 0 for guide_id in GUIDES}
        self.nit_route = "sin_obligaciones"

        self._build_shell()
        self._bind_mousewheel()
        self.show_page("home", push=False)

    def _build_shell(self) -> None:
        self.root.configure(bg=self.palette["app_bg"])

        self.shell = tk.Frame(
            self.root,
            bg=self.palette["shell_bg"],
            highlightbackground=self.palette["border"],
            highlightthickness=1,
        )
        self.shell.pack(fill="both", expand=True, padx=10, pady=10)

        self.header = tk.Frame(self.shell, bg=self.palette["shell_bg"], height=76)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        self.back_button = tk.Button(
            self.header,
            text="‹",
            width=3,
            command=self.go_back,
            font=("Helvetica", 20, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
        )
        self.back_button.pack(side="left", padx=(12, 4), pady=14)

        brand = tk.Frame(self.header, bg=self.palette["shell_bg"])
        brand.pack(side="left", fill="y", pady=8)

        logo = self._load_image("logo.png", 48, 48)
        if logo:
            tk.Label(brand, image=logo, bg=self.palette["shell_bg"]).pack(side="left", padx=(0, 2))
        else:
            tk.Label(brand, text="W", bg=self.palette["shell_bg"], fg=self.palette["primary"], font=("Helvetica", 24, "bold")).pack(side="left")

        title_box = tk.Frame(brand, bg=self.palette["shell_bg"])
        title_box.pack(side="left", fill="y")

        wordmark = self._load_image("Wanbe_letras.png", 128, 42)
        if wordmark:
            tk.Label(title_box, image=wordmark, bg=self.palette["shell_bg"]).pack(anchor="w")
        else:
            tk.Label(title_box, text="Wanbe", bg=self.palette["shell_bg"], fg=self.palette["primary"], font=("Helvetica", 18, "bold")).pack(anchor="w")

        self.nav_title = tk.Label(
            title_box,
            text="Inicio",
            bg=self.palette["shell_bg"],
            fg=self.palette["muted"],
            font=("Helvetica", 8, "bold"),
        )
        self.nav_title.pack(anchor="w", pady=(0, 4))

        self.settings_button = tk.Button(
            self.header,
            text="⚙",
            width=3,
            command=lambda: self.show_page("settings"),
            font=("Helvetica", 16),
            relief="flat",
            bd=0,
            cursor="hand2",
        )
        self.settings_button.pack(side="right", padx=12, pady=16)

        body = tk.Frame(self.shell, bg=self.palette["shell_bg"])
        body.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(body, bg=self.palette["shell_bg"], highlightthickness=0, bd=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(body, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.content = tk.Frame(self.canvas, bg=self.palette["shell_bg"])
        self.content_window = self.canvas.create_window((0, 0), window=self.content, anchor="nw")

        self.content.bind("<Configure>", self._update_scrollregion)
        self.canvas.bind("<Configure>", self._resize_content)

    def _bind_mousewheel(self) -> None:
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.bind_all("<Button-4>", lambda _event: self.canvas.yview_scroll(-1, "units"))
        self.root.bind_all("<Button-5>", lambda _event: self.canvas.yview_scroll(1, "units"))

    def _on_mousewheel(self, event: tk.Event) -> None:
        if sys.platform == "darwin":
            delta = -1 * int(event.delta)
        else:
            delta = -1 * int(event.delta / 120)
        self.canvas.yview_scroll(delta, "units")

    def _update_scrollregion(self, _event: tk.Event | None = None) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_content(self, event: tk.Event) -> None:
        self.canvas.itemconfigure(self.content_window, width=event.width)

    def _load_image(self, filename: str, max_width: int, max_height: int) -> tk.PhotoImage | None:
        path = BASE_DIR / filename
        if not path.exists():
            return None
        try:
            original = tk.PhotoImage(file=str(path))
            factor = max(1, int(max(original.width() / max_width, original.height() / max_height)))
            image = original.subsample(factor, factor)
            self.images[filename] = image
            return image
        except tk.TclError:
            return None

    def _clear_content(self) -> None:
        for child in self.content.winfo_children():
            child.destroy()
        self.canvas.yview_moveto(0)

    def _apply_theme(self) -> None:
        self.palette = DARK_THEME if self.dark_mode else LIGHT_THEME
        self.root.configure(bg=self.palette["app_bg"])
        self.shell.configure(bg=self.palette["shell_bg"], highlightbackground=self.palette["border"])
        self.header.configure(bg=self.palette["shell_bg"])
        self.canvas.configure(bg=self.palette["shell_bg"])
        self.content.configure(bg=self.palette["shell_bg"])

        for button in (self.back_button, self.settings_button):
            button.configure(
                bg=self.palette["surface_alt"],
                fg=self.palette["text"],
                activebackground=self.palette["border"],
                activeforeground=self.palette["text"],
            )

        self.nav_title.configure(bg=self.palette["shell_bg"], fg=self.palette["muted"])
        self.show_page(self.current_page, push=False)

    def show_page(self, page_id: str, push: bool = True) -> None:
        if page_id in GUIDE_PAGE_TO_ID:
            self.current_page = page_id
        else:
            self.current_page = page_id

        if push and (not self.history or self.history[-1] != page_id):
            self.history.append(page_id)

        self._clear_content()
        self._update_header(page_id)

        if page_id == "home":
            self._render_home()
        elif page_id == "settings":
            self._render_settings()
        elif page_id == "completion":
            self._render_completion()
        elif page_id.startswith("agencies-"):
            entity = "SAT" if page_id.endswith("sat") else "RENAP"
            self._render_agencies(entity)
        elif page_id in GUIDE_PAGE_TO_ID:
            self._render_guide(GUIDE_PAGE_TO_ID[page_id])
        else:
            self._render_category(page_id)

    def _update_header(self, page_id: str) -> None:
        self.back_button.configure(state="normal" if page_id != "home" else "disabled")
        self.back_button.configure(fg=self.palette["muted"] if page_id != "home" else self.palette["disabled"])

        if page_id in GUIDE_PAGE_TO_ID:
            title = GUIDES[GUIDE_PAGE_TO_ID[page_id]].title
        else:
            title = PAGE_TITLES.get(page_id, page_id.title())
        self.nav_title.configure(text=title)

    def go_back(self) -> None:
        if len(self.history) <= 1:
            return
        self.history.pop()
        previous = self.history[-1]
        self.show_page(previous, push=False)

    def _text_label(
        self,
        parent: tk.Widget,
        text: str,
        size: int = 11,
        weight: str = "normal",
        color: str | None = None,
        **pack_options,
    ) -> tk.Label:
        label = tk.Label(
            parent,
            text=text,
            bg=parent.cget("bg"),
            fg=color or self.palette["text"],
            font=("Helvetica", size, weight),
            justify="left",
            anchor="w",
            wraplength=340,
        )
        label.pack(fill="x", **pack_options)
        return label

    def _card(
        self,
        parent: tk.Widget,
        title: str,
        subtitle: str,
        icon: str,
        command,
        accent: str | None = None,
    ) -> tk.Frame:
        card = tk.Frame(
            parent,
            bg=self.palette["surface"],
            highlightbackground=self.palette["border"],
            highlightthickness=1,
            cursor="hand2",
        )
        card.pack(fill="x", padx=16, pady=7)

        icon_box = tk.Label(
            card,
            text=icon,
            width=3,
            bg=accent or self.palette["primary"],
            fg="white",
            font=("Helvetica", 18, "bold"),
        )
        icon_box.pack(side="left", padx=12, pady=14)

        text_box = tk.Frame(card, bg=self.palette["surface"])
        text_box.pack(side="left", fill="both", expand=True, pady=12)

        tk.Label(
            text_box,
            text=title,
            bg=self.palette["surface"],
            fg=self.palette["text"],
            font=("Helvetica", 13, "bold"),
            anchor="w",
            justify="left",
        ).pack(fill="x")
        tk.Label(
            text_box,
            text=subtitle,
            bg=self.palette["surface"],
            fg=self.palette["muted"],
            font=("Helvetica", 9),
            anchor="w",
            justify="left",
            wraplength=240,
        ).pack(fill="x", pady=(2, 0))

        tk.Label(
            card,
            text="→",
            bg=self.palette["surface"],
            fg=accent or self.palette["primary"],
            font=("Helvetica", 16, "bold"),
        ).pack(side="right", padx=12)

        self._bind_click_recursive(card, command)
        return card

    def _bind_click_recursive(self, widget: tk.Widget, command) -> None:
        widget.bind("<Button-1>", lambda _event: command())
        for child in widget.winfo_children():
            self._bind_click_recursive(child, command)

    def _button(
        self,
        parent: tk.Widget,
        text: str,
        command,
        bg: str | None = None,
        fg: str = "white",
        state: str = "normal",
    ) -> tk.Button:
        button = tk.Button(
            parent,
            text=text,
            command=command,
            state=state,
            bg=bg or self.palette["primary"],
            fg=fg,
            activebackground=self.palette["accent"],
            activeforeground="white",
            disabledforeground=self.palette["muted"],
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Helvetica", 11, "bold"),
            padx=14,
            pady=10,
        )
        button.pack(fill="x", padx=16, pady=6)
        return button

    def _render_home(self) -> None:
        hero = GradientCard(self.content, "#5C1399", "#183499", height=140, bg=self.palette["shell_bg"])
        hero.pack(fill="x", padx=16, pady=(12, 14))
        hero.create_text(
            22,
            38,
            text="¿En que tramite te guiamos hoy?",
            fill="white",
            font=("Helvetica", 20, "bold"),
            anchor="nw",
            width=330,
        )
        hero.create_text(
            22,
            88,
            text="Tu ruta clara y verificada hacia tramites administrativos.",
            fill="#dbeafe",
            font=("Helvetica", 10),
            anchor="nw",
            width=330,
        )

        search_shell = tk.Frame(
            self.content,
            bg=self.palette["surface"],
            highlightbackground=self.palette["border"],
            highlightthickness=1,
        )
        search_shell.pack(fill="x", padx=16, pady=(0, 10))

        search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_shell,
            textvariable=search_var,
            bg=self.palette["surface_alt"],
            fg=self.palette["text"],
            insertbackground=self.palette["text"],
            relief="flat",
            font=("Helvetica", 12),
        )
        search_entry.pack(fill="x", padx=12, pady=12, ipady=8)
        search_entry.insert(0, "Buscar tramite...")
        search_entry.configure(fg=self.palette["muted"])

        results_box = tk.Frame(self.content, bg=self.palette["shell_bg"])
        results_box.pack(fill="x")

        def clear_placeholder(_event: tk.Event) -> None:
            if search_entry.get() == "Buscar tramite...":
                search_entry.delete(0, "end")
                search_entry.configure(fg=self.palette["text"])

        def restore_placeholder(_event: tk.Event) -> None:
            if not search_entry.get():
                search_entry.insert(0, "Buscar tramite...")
                search_entry.configure(fg=self.palette["muted"])
                render_default_cards()

        def render_default_cards() -> None:
            for child in results_box.winfo_children():
                child.destroy()
            for node in MENU_TREE:
                self._card(
                    results_box,
                    node["title"],
                    node["subtitle"],
                    node["icon"],
                    lambda target=node["id"]: self.show_page(target),
                    self.palette["primary"] if node["id"] == "sat" else self.palette["secondary"],
                )

        def update_search(_event: tk.Event | None = None) -> None:
            query = search_entry.get().strip()
            if not query or query == "Buscar tramite...":
                render_default_cards()
                return

            for child in results_box.winfo_children():
                child.destroy()

            results = recursive_search(MENU_TREE, query)
            if not results:
                self._empty_state(
                    results_box,
                    "Tramite no encontrado",
                    "No encontramos ese tramite en esta base. Puedes volver a buscar con otra palabra.",
                )
                return

            for result in results[:8]:
                self._card(
                    results_box,
                    result["title"],
                    result["subtitle"],
                    result["icon"],
                    lambda target=result["target"]: self.show_page(target),
                    self.palette["accent"],
                )

        search_entry.bind("<FocusIn>", clear_placeholder)
        search_entry.bind("<FocusOut>", restore_placeholder)
        search_entry.bind("<KeyRelease>", update_search)

        render_default_cards()

    def _empty_state(self, parent: tk.Widget, title: str, body: str) -> None:
        box = tk.Frame(
            parent,
            bg=self.palette["surface_alt"],
            highlightbackground=self.palette["border"],
            highlightthickness=1,
        )
        box.pack(fill="x", padx=16, pady=20)
        self._text_label(box, title, 14, "bold", self.palette["text"], padx=16, pady=(16, 4))
        self._text_label(box, body, 10, "normal", self.palette["muted"], padx=16, pady=(0, 16))

    def _render_category(self, page_id: str) -> None:
        node = find_node_by_id(MENU_TREE, page_id)
        if not node:
            self._empty_state(self.content, "Pantalla no encontrada", "La ruta solicitada no existe en la base.")
            return

        self._section_title(node["title"], node.get("subtitle", ""))

        for child in node.get("children", []):
            if "guide" in child:
                guide = GUIDES[child["guide"]]
                self._card(
                    self.content,
                    guide.title,
                    guide.subtitle,
                    guide.icon,
                    lambda target=guide.page_id: self.show_page(target),
                    guide.accent,
                )
            else:
                self._card(
                    self.content,
                    child["title"],
                    child.get("subtitle", ""),
                    child.get("icon", "•"),
                    lambda target=child["id"]: self.show_page(target),
                    self.palette["primary"],
                )

        if page_id == "sat":
            self._button(self.content, "Ver agencias SAT", lambda: self.show_page("agencies-sat"), self.palette["secondary"])
        elif page_id == "renap":
            self._button(self.content, "Ver sedes RENAP", lambda: self.show_page("agencies-renap"), self.palette["secondary"])

    def _section_title(self, title: str, subtitle: str = "") -> None:
        box = tk.Frame(self.content, bg=self.palette["shell_bg"])
        box.pack(fill="x", padx=16, pady=(16, 8))
        self._text_label(box, title, 18, "bold", self.palette["primary"])
        if subtitle:
            self._text_label(box, subtitle, 10, "normal", self.palette["muted"], pady=(3, 0))

    def _render_guide(self, guide_id: str) -> None:
        guide = GUIDES[guide_id]

        header = tk.Frame(
            self.content,
            bg=self.palette["surface_alt"],
            highlightbackground=guide.accent,
            highlightthickness=2,
        )
        header.pack(fill="x", padx=16, pady=(14, 10))
        tk.Label(
            header,
            text=f"{guide.icon}  {guide.title}",
            bg=self.palette["surface_alt"],
            fg=guide.accent if not self.dark_mode else self.palette["primary"],
            font=("Helvetica", 14, "bold"),
            anchor="w",
            justify="left",
            wraplength=340,
        ).pack(fill="x", padx=14, pady=(12, 2))
        tk.Label(
            header,
            text=guide.subtitle,
            bg=self.palette["surface_alt"],
            fg=self.palette["muted"],
            font=("Helvetica", 10),
            anchor="w",
        ).pack(fill="x", padx=14, pady=(0, 12))

        if not self.guide_started[guide_id]:
            self._render_precheck(guide)
        else:
            self._render_guide_step(guide)

    def _render_precheck(self, guide: Guide) -> None:
        box = tk.Frame(
            self.content,
            bg=self.palette["surface"],
            highlightbackground=self.palette["border"],
            highlightthickness=1,
        )
        box.pack(fill="x", padx=16, pady=8)

        self._text_label(
            box,
            "Antes de comenzar: documentos indispensables",
            13,
            "bold",
            self.palette["text"],
            padx=14,
            pady=(14, 3),
        )
        self._text_label(
            box,
            "Marca todos los requisitos para confirmar que ya puedes iniciar el tramite.",
            10,
            "normal",
            self.palette["muted"],
            padx=14,
            pady=(0, 10),
        )

        checks: list[tk.BooleanVar] = []
        start_button: tk.Button | None = None

        def update_state(*_args) -> None:
            if not start_button:
                return
            complete = all(var.get() for var in checks)
            start_button.configure(
                state="normal" if complete else "disabled",
                bg=guide.accent if complete else self.palette["disabled"],
                fg="white" if complete else self.palette["muted"],
            )

        for req in guide.requirements:
            var = tk.BooleanVar(value=False)
            checks.append(var)
            row = tk.Checkbutton(
                box,
                text=req,
                variable=var,
                bg=self.palette["surface"],
                fg=self.palette["text"],
                selectcolor=self.palette["surface_alt"],
                activebackground=self.palette["surface"],
                activeforeground=self.palette["text"],
                anchor="w",
                justify="left",
                wraplength=320,
                font=("Helvetica", 10),
            )
            row.pack(fill="x", padx=14, pady=4)
            var.trace_add("write", update_state)

        def start_guide() -> None:
            self.guide_started[guide.guide_id] = True
            self.guide_step[guide.guide_id] = 0
            self.show_page(guide.page_id, push=False)

        start_button = self._button(box, "Ir al paso 1", start_guide, self.palette["disabled"], self.palette["muted"], "disabled")
        update_state()

    def _render_guide_step(self, guide: Guide) -> None:
        step_index = self.guide_step[guide.guide_id]
        total = len(guide.steps)
        step = guide.steps[step_index]

        progress_box = tk.Frame(self.content, bg=self.palette["shell_bg"])
        progress_box.pack(fill="x", padx=16, pady=(4, 10))

        tk.Label(
            progress_box,
            text=f"Paso {step_index + 1}/{total}",
            bg=self.palette["shell_bg"],
            fg=self.palette["muted"],
            font=("Helvetica", 10, "bold"),
            anchor="w",
        ).pack(fill="x")

        bar = tk.Canvas(progress_box, height=10, bg=self.palette["border"], highlightthickness=0, bd=0)
        bar.pack(fill="x", pady=(6, 0))
        self.root.update_idletasks()
        width = max(bar.winfo_width(), 330)
        bar.create_rectangle(0, 0, width, 10, fill=self.palette["border"], outline="")
        bar.create_rectangle(0, 0, int(width * ((step_index + 1) / total)), 10, fill=guide.accent, outline="")

        step_card = tk.Frame(
            self.content,
            bg=self.palette["surface"],
            highlightbackground=self.palette["border"],
            highlightthickness=1,
        )
        step_card.pack(fill="x", padx=16, pady=8)

        self._text_label(step_card, step.title, 16, "bold", self.palette["text"], padx=14, pady=(16, 4))
        self._text_label(step_card, step.body, 11, "normal", self.palette["muted"], padx=14, pady=(0, 10))

        if step.bullets:
            for index, bullet in enumerate(step.bullets, start=1):
                self._text_label(
                    step_card,
                    f"{index}. {bullet}",
                    10,
                    "normal",
                    self.palette["text"],
                    padx=20,
                    pady=2,
                )

        if step.kind == "municipality":
            self._render_municipality_selector(step_card)
        elif step.kind == "nit_route":
            self._render_nit_route_selector(step_card)
        elif step.kind == "nit_affiliations":
            self._render_nit_route_note(step_card)
        elif step.kind == "nit_establishment":
            self._render_nit_establishment_note(step_card)

        if step.action_label and step.action_url:
            self._button(
                step_card,
                step.action_label,
                lambda url=step.action_url: webbrowser.open(url),
                guide.accent,
            )

        self._render_required_documents(guide)
        self._render_guide_navigation(guide)

    def _render_required_documents(self, guide: Guide) -> None:
        box = tk.Frame(
            self.content,
            bg=self.palette["warning_bg"],
            highlightbackground=self.palette["warning_text"],
            highlightthickness=1,
        )
        box.pack(fill="x", padx=16, pady=8)

        self._text_label(
            box,
            "Documentos indispensables",
            11,
            "bold",
            self.palette["warning_text"],
            padx=14,
            pady=(12, 4),
        )
        for req in guide.requirements:
            self._text_label(
                box,
                f"• {req}",
                10,
                "normal",
                self.palette["warning_text"],
                padx=20,
                pady=2,
            )

    def _render_municipality_selector(self, parent: tk.Widget) -> None:
        box = tk.Frame(parent, bg=self.palette["surface_alt"], highlightbackground=self.palette["border"], highlightthickness=1)
        box.pack(fill="x", padx=14, pady=12)

        tk.Label(
            box,
            text="Municipalidad",
            bg=self.palette["surface_alt"],
            fg=self.palette["text"],
            font=("Helvetica", 10, "bold"),
            anchor="w",
        ).pack(fill="x", padx=12, pady=(10, 4))

        selected = tk.StringVar(value=MUNICIPAL_PORTAL_MATRIX[0][0])
        menu = tk.OptionMenu(box, selected, *[row[0] for row in MUNICIPAL_PORTAL_MATRIX])
        menu.configure(
            bg=self.palette["surface"],
            fg=self.palette["text"],
            activebackground=self.palette["border"],
            relief="flat",
            highlightthickness=0,
            font=("Helvetica", 10),
        )
        menu.pack(fill="x", padx=12, pady=4)

        def open_selected() -> None:
            chosen = selected.get()
            for name, url in MUNICIPAL_PORTAL_MATRIX:
                if name == chosen:
                    webbrowser.open(url)
                    return

        self._button(box, "Abrir portal seleccionado", open_selected, self.palette["success"])

    def _render_nit_route_selector(self, parent: tk.Widget) -> None:
        box = tk.Frame(parent, bg=self.palette["surface_alt"], highlightbackground=self.palette["border"], highlightthickness=1)
        box.pack(fill="x", padx=14, pady=12)

        self._text_label(box, "Selecciona tu ruta", 11, "bold", self.palette["text"], padx=12, pady=(12, 6))

        for key, title, description in NIT_ROUTE_MATRIX:
            prefix = "✓ " if self.nit_route == key else ""
            self._card(
                box,
                f"{prefix}{title}",
                description,
                "✓" if self.nit_route == key else "•",
                lambda route_key=key: self._select_nit_route(route_key),
                self.palette["secondary"] if self.nit_route == key else self.palette["accent"],
            )

    def _select_nit_route(self, route_key: str) -> None:
        self.nit_route = route_key
        self.show_page("tutorial-nit", push=False)

    def _render_nit_route_note(self, parent: tk.Widget) -> None:
        notes = {
            "sin_obligaciones": "Tu ruta no necesita afiliaciones tributarias adicionales. Puedes continuar al cierre.",
            "asalariado": "En esta ruta revisa ISR como asalariado. Si no facturas, evita seleccionar obligaciones de negocio.",
            "negocio": "Para negocio, prepara afiliacion de IVA pequeno contribuyente y datos de ingresos estimados.",
        }
        self._info_panel(parent, "Ruta activa", notes.get(self.nit_route, notes["sin_obligaciones"]))

    def _render_nit_establishment_note(self, parent: tk.Widget) -> None:
        if self.nit_route == "negocio":
            text = "Completa establecimiento porque elegiste negocio o facturacion."
        else:
            text = "Si no registraras negocio, este paso puede no aplicar. Verifica lo que te muestre el portal SAT."
        self._info_panel(parent, "Establecimiento", text)

    def _info_panel(self, parent: tk.Widget, title: str, body: str) -> None:
        box = tk.Frame(parent, bg=self.palette["surface_alt"], highlightbackground=self.palette["border"], highlightthickness=1)
        box.pack(fill="x", padx=14, pady=12)
        self._text_label(box, title, 11, "bold", self.palette["primary"], padx=12, pady=(12, 4))
        self._text_label(box, body, 10, "normal", self.palette["text"], padx=12, pady=(0, 12))

    def _render_guide_navigation(self, guide: Guide) -> None:
        nav = tk.Frame(self.content, bg=self.palette["shell_bg"])
        nav.pack(fill="x", padx=16, pady=(8, 20))

        index = self.guide_step[guide.guide_id]
        total = len(guide.steps)

        previous = tk.Button(
            nav,
            text="← Anterior",
            command=lambda: self._previous_step(guide.guide_id),
            state="normal" if index > 0 else "disabled",
            bg=self.palette["surface_alt"],
            fg=self.palette["text"],
            disabledforeground=self.palette["muted"],
            relief="flat",
            bd=0,
            font=("Helvetica", 11, "bold"),
            pady=10,
        )
        previous.pack(side="left", fill="x", expand=True, padx=(0, 6))

        if index == total - 1:
            label = "Finalizar guia"
            command = lambda: self._finish_guide(guide.guide_id)
        else:
            label = "Siguiente →"
            command = lambda: self._next_step(guide.guide_id)

        next_button = tk.Button(
            nav,
            text=label,
            command=command,
            bg=guide.accent,
            fg="white",
            relief="flat",
            bd=0,
            font=("Helvetica", 11, "bold"),
            pady=10,
        )
        next_button.pack(side="left", fill="x", expand=True, padx=(6, 0))

    def _next_step(self, guide_id: str) -> None:
        total = len(GUIDES[guide_id].steps)
        self.guide_step[guide_id] = min(self.guide_step[guide_id] + 1, total - 1)
        self.show_page(GUIDES[guide_id].page_id, push=False)

    def _previous_step(self, guide_id: str) -> None:
        self.guide_step[guide_id] = max(self.guide_step[guide_id] - 1, 0)
        self.show_page(GUIDES[guide_id].page_id, push=False)

    def _finish_guide(self, guide_id: str) -> None:
        self.guide_started[guide_id] = False
        self.guide_step[guide_id] = 0
        self.show_page("completion")

    def _render_agencies(self, entity: str) -> None:
        self._section_title(f"{'Agencias SAT' if entity == 'SAT' else 'Sedes RENAP'}", "Referencias cercanas incluidas como matriz de datos.")
        rows = [row for row in AGENCY_MATRIX if row[0] == entity]
        for _portal, name, address, schedule in rows:
            self._card(
                self.content,
                name,
                f"{address} • {schedule}",
                "📍",
                lambda address=address: webbrowser.open(f"https://www.google.com/maps/search/{address.replace(' ', '+')}"),
                self.palette["secondary"],
            )

    def _render_settings(self) -> None:
        self._section_title("Configuracion general", "Preferencias visuales y estado de la base.")

        mode_text = "Desactivar modo oscuro" if self.dark_mode else "Activar modo oscuro"
        self._button(self.content, mode_text, self._toggle_dark_mode, self.palette["secondary"])

        total_guides = count_guides_recursively(MENU_TREE)
        paths = len(NAVIGATION_MATRIX)

        stats = tk.Frame(
            self.content,
            bg=self.palette["surface"],
            highlightbackground=self.palette["border"],
            highlightthickness=1,
        )
        stats.pack(fill="x", padx=16, pady=10)
        self._text_label(stats, "Base de datos de tramites", 13, "bold", self.palette["text"], padx=14, pady=(14, 4))
        self._text_label(stats, f"Tramites cargados: {total_guides}", 10, "normal", self.palette["muted"], padx=14, pady=2)
        self._text_label(stats, f"Rutas de navegacion en matriz: {paths}", 10, "normal", self.palette["muted"], padx=14, pady=2)
        self._text_label(stats, "Estructuras usadas: listas, matrices, diccionarios, clases y recursion.", 10, "normal", self.palette["muted"], padx=14, pady=(2, 14))

        self._button(self.content, "Volver al inicio", lambda: self.show_page("home"), self.palette["primary"])

    def _toggle_dark_mode(self) -> None:
        self.dark_mode = not self.dark_mode
        self._apply_theme()

    def _render_completion(self) -> None:
        spacer = tk.Frame(self.content, height=80, bg=self.palette["shell_bg"])
        spacer.pack(fill="x")

        box = tk.Frame(
            self.content,
            bg=self.palette["surface"],
            highlightbackground=self.palette["border"],
            highlightthickness=1,
        )
        box.pack(fill="x", padx=24, pady=16)

        tk.Label(
            box,
            text="✓",
            bg=self.palette["surface"],
            fg=self.palette["success"],
            font=("Helvetica", 48, "bold"),
        ).pack(pady=(20, 4))
        self._text_label(box, "Tramite finalizado", 18, "bold", self.palette["text"], padx=20, pady=4)
        self._text_label(
            box,
            "La guia se reinicio para que puedas practicar o revisar otro tramite.",
            11,
            "normal",
            self.palette["muted"],
            padx=20,
            pady=(0, 16),
        )
        self._button(box, "Volver al inicio", lambda: self.show_page("home"), self.palette["primary"])

    def run(self) -> None:
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.destroy()


def main() -> None:
    try:
        app = WanbeApp()
        app.run()
    except tk.TclError as error:
        messagebox.showerror(
            "Wanbe",
            f"No se pudo iniciar la interfaz grafica.\n\nDetalle: {error}",
        )


if __name__ == "__main__":
    main()
