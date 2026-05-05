#!/usr/bin/env python3
"""
Wanbe - Proyecto final en Python

Aplicacion de escritorio sencilla inspirada en la app web original.
Usa tkinter, por lo que no necesita instalar librerias externas.

Temas de programacion aplicados:
- Listas: pasos y requisitos de cada tramite.
- Matrices: rutas principales de la aplicacion.
- Diccionarios: base de datos de tramites.
- Recursion: buscador dentro del arbol de categorias.
"""

from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import unicodedata
import webbrowser


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

COLORS = {
    "background": "#eef3ff",
    "white": "#ffffff",
    "card": "#f8fafc",
    "text": "#172033",
    "muted": "#64748b",
    "border": "#dbe3f0",
    "primary": "#183499",
    "purple": "#5C1399",
    "soft_blue": "#7886C7",
    "warning_bg": "#fff7ed",
    "warning": "#92400e",
}


# Matriz: cada fila representa una ruta general de navegacion.
RUTAS = [
    ["Inicio", "SAT", "Vehiculos", "Pago de Calcomania"],
    ["Inicio", "SAT", "Individuales", "Solicitud de NIT"],
    ["Inicio", "SAT", "Juridicos", "Habilitacion de Libros"],
    ["Inicio", "RENAP", "Tramite de DPI"],
    ["Inicio", "RENAP", "Certificados en Linea"],
]


# Diccionario principal de tramites.
TRAMITES = {
    "calcomania": {
        "titulo": "Pago de Calcomania",
        "portal": "SAT",
        "icono": "CAR",
        "descripcion": "Pago del Impuesto Sobre Circulacion de Vehiculos.",
        "requisitos": ["Placa del vehiculo", "NIT del propietario"],
        "pasos": [
            {
                "titulo": "Revisa datos del vehiculo",
                "texto": "Antes de iniciar, ten claros los datos que la SAT pedira para generar el formulario.",
                "items": ["Confirma la placa.", "Confirma el NIT del propietario.", "Ten acceso a Declaraguate."],
            },
            {
                "titulo": "Genera formulario SAT-4091",
                "texto": "Ingresa a Declaraguate y genera el formulario de vehiculos.",
                "items": ["Busca la seccion Vehiculos.", "Ingresa NIT y placa.", "Valida y congela."],
                "enlace": "https://declaraguate.sat.gob.gt/declaraguate-web/",
            },
            {
                "titulo": "Paga en banco",
                "texto": "Usa el numero de formulario y numero de acceso.",
                "items": ["Verifica el monto.", "Paga en linea o ventanilla.", "Guarda recibo."],
            },
            {
                "titulo": "Imprime calcomania",
                "texto": "Descarga el distintivo en PDF para portarlo en tu vehiculo.",
                "items": ["Revisa que la placa sea correcta.", "Imprime o guarda el PDF."],
                "enlace": "https://portal.sat.gob.gt/portal/impresion-calcomania/",
            },
        ],
    },
    "nit": {
        "titulo": "Solicitud de NIT",
        "portal": "SAT",
        "icono": "NIT",
        "descripcion": "Solicitud electronica para obtener NIT por primera vez.",
        "requisitos": ["DPI vigente", "Recibo de luz o agua", "Correo electronico"],
        "pasos": [
            {
                "titulo": "Abre portal SAT",
                "texto": "Inicia en el portal oficial de Solicitud Electronica de NIT.",
                "items": ["Completa captcha.", "Escribe tu correo.", "Solicita el enlace."],
                "enlace": "https://portal.sat.gob.gt/portal/solicitud-electronica-de-nit/",
            },
            {
                "titulo": "Valida correo",
                "texto": "Busca en tu correo el mensaje enviado por SAT.",
                "items": ["Revisa bandeja principal.", "Revisa spam.", "Copia el codigo recibido."],
            },
            {
                "titulo": "Datos personales",
                "texto": "Llena DPI, numero de serie y datos solicitados.",
                "items": ["El numero de serie esta atras del DPI.", "Sube documentos legibles."],
            },
            {
                "titulo": "Actividad economica",
                "texto": "Elige si eres asalariado, no tienes obligaciones o tienes negocio.",
                "items": ["Si no trabajas, elige sin obligaciones.", "Si facturas, elige negocio."],
            },
            {
                "titulo": "Enviar solicitud",
                "texto": "Revisa toda la informacion antes de finalizar.",
                "items": ["Confirma datos.", "Guarda usuario y clave.", "Espera respuesta por correo."],
            },
        ],
    },
    "libros": {
        "titulo": "Habilitacion de Libros",
        "portal": "SAT",
        "icono": "LIB",
        "descripcion": "Formulario SAT-7121 para libros contables.",
        "requisitos": ["NIT", "Clave SAT", "Boleta SAT-2000 si aplica"],
        "pasos": [
            {
                "titulo": "Abrir Declaraguate",
                "texto": "Busca el formulario SAT-7121 en la seccion Varios.",
                "items": ["Selecciona habilitacion de libros.", "Ingresa datos del contribuyente."],
                "enlace": "https://declaraguate.sat.gob.gt/declaraguate-web/",
            },
            {
                "titulo": "Configurar libros",
                "texto": "Selecciona tipo de libro y modalidad.",
                "items": ["Manual o computarizado.", "Cantidad de libros.", "Establecimiento si aplica."],
            },
            {
                "titulo": "Pagar y resolver",
                "texto": "Congela, paga SAT-2000 e imprime resolucion.",
                "items": ["Guarda boleta.", "Imprime resolucion.", "Archiva documentos."],
            },
        ],
    },
    "dpi": {
        "titulo": "Tramite de DPI",
        "portal": "RENAP",
        "icono": "DPI",
        "descripcion": "Guia basica para tramitar el Documento Personal de Identificacion.",
        "requisitos": ["Certificado de nacimiento", "Boleto de ornato"],
        "pasos": [
            {
                "titulo": "Certificado de nacimiento",
                "texto": "Solicita un certificado reciente en RENAP o ePortal.",
                "items": ["Presencial: Q15.", "En linea: Q19.", "Debe estar vigente."],
                "enlace": "https://eportal.renap.gob.gt/",
            },
            {
                "titulo": "Pago en banco",
                "texto": "Paga la tarifa del DPI.",
                "items": ["Costo usual: Q100.", "Mayores de 60 anos: gratuito."],
            },
            {
                "titulo": "Visita RENAP",
                "texto": "Acude a sede RENAP para foto, huellas y firma.",
                "items": ["No uses ropa blanca.", "Revisa tus datos antes de aprobar."],
            },
            {
                "titulo": "Recoger DPI",
                "texto": "Lleva la constancia para recoger tu documento.",
                "items": ["Ve a la misma agencia.", "Revisa el DPI al recibirlo."],
            },
        ],
    },
    "certificados": {
        "titulo": "Certificados en Linea",
        "portal": "RENAP",
        "icono": "PDF",
        "descripcion": "Solicitud de certificados desde ePortal RENAP.",
        "requisitos": ["CUI", "Correo electronico", "Medio de pago"],
        "pasos": [
            {
                "titulo": "Entrar al ePortal",
                "texto": "Ingresa con tu CUI o crea usuario.",
                "items": ["Usa correo personal.", "Crea una contrasena segura."],
                "enlace": "https://eportal.renap.gob.gt/",
            },
            {
                "titulo": "Elegir certificado",
                "texto": "Selecciona el certificado que necesitas.",
                "items": ["Nacimiento.", "Matrimonio.", "Otros disponibles."],
            },
            {
                "titulo": "Pagar y descargar",
                "texto": "Paga y guarda el PDF.",
                "items": ["Costo aproximado: Q19.", "Verifica que el PDF abra bien."],
            },
        ],
    },
}


# Arbol de categorias. El buscador lo recorre con recursion.
MENU = [
    {
        "id": "sat",
        "titulo": "Portal SAT",
        "subtitulo": "Vehiculos, NIT y empresas",
        "icono": "SAT",
        "hijos": [
            {
                "id": "vehiculos",
                "titulo": "Vehiculos",
                "subtitulo": "Calcomania y placas",
                "icono": "CAR",
                "hijos": [{"tramite": "calcomania"}],
            },
            {
                "id": "individuales",
                "titulo": "Individuales",
                "subtitulo": "NIT personal",
                "icono": "NIT",
                "hijos": [{"tramite": "nit"}],
            },
            {
                "id": "juridicos",
                "titulo": "Juridicos",
                "subtitulo": "Empresas y libros",
                "icono": "EMP",
                "hijos": [{"tramite": "libros"}],
            },
        ],
    },
    {
        "id": "renap",
        "titulo": "Portal RENAP",
        "subtitulo": "DPI y certificados",
        "icono": "DPI",
        "hijos": [{"tramite": "dpi"}, {"tramite": "certificados"}],
    },
]


def normalizar(texto: str) -> str:
    """Convierte texto a minusculas y elimina tildes para mejorar busquedas."""
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(letra for letra in texto if unicodedata.category(letra) != "Mn")


def buscar_recursivo(nodos: list[dict], consulta: str, ruta: str = "") -> list[dict]:
    """Busca tramites dentro del arbol MENU usando recursion."""
    resultados = []
    consulta = normalizar(consulta)

    for nodo in nodos:
        if "tramite" in nodo:
            clave = nodo["tramite"]
            tramite = TRAMITES[clave]
            texto = " ".join([tramite["titulo"], tramite["descripcion"], tramite["portal"]])
            if consulta in normalizar(texto):
                resultados.append(
                    {
                        "tipo": "tramite",
                        "id": clave,
                        "titulo": tramite["titulo"],
                        "subtitulo": ruta,
                        "icono": tramite["icono"],
                    }
                )
            continue

        texto_categoria = f"{nodo['titulo']} {nodo['subtitulo']}"
        if consulta in normalizar(texto_categoria):
            resultados.append(
                {
                    "tipo": "categoria",
                    "id": nodo["id"],
                    "titulo": nodo["titulo"],
                    "subtitulo": nodo["subtitulo"],
                    "icono": nodo["icono"],
                }
            )

        nueva_ruta = f"{ruta} > {nodo['titulo']}" if ruta else nodo["titulo"]
        resultados.extend(buscar_recursivo(nodo.get("hijos", []), consulta, nueva_ruta))

    return resultados


def encontrar_categoria(nodos: list[dict], categoria_id: str) -> dict | None:
    """Encuentra una categoria dentro del arbol usando recursion."""
    for nodo in nodos:
        if nodo.get("id") == categoria_id:
            return nodo
        encontrado = encontrar_categoria(nodo.get("hijos", []), categoria_id)
        if encontrado:
            return encontrado
    return None


class WanbeApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Wanbe - Proyecto Final")
        self.root.geometry("430x720")
        self.root.minsize(390, 620)
        self.root.configure(bg=COLORS["background"])

        self.historial = ["inicio"]
        self.paso_actual = {clave: 0 for clave in TRAMITES}
        self.checklist_listo = {clave: False for clave in TRAMITES}
        self.imagenes = {}

        self.construir_base()
        self.mostrar_inicio()

    def construir_base(self) -> None:
        self.marco_app = tk.Frame(self.root, bg=COLORS["white"])
        self.marco_app.pack(fill="both", expand=True, padx=10, pady=10)

        self.header = tk.Frame(self.marco_app, bg=COLORS["white"], height=70)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.boton_atras = tk.Button(
            self.header,
            text="<",
            command=self.volver,
            bg=COLORS["card"],
            fg=COLORS["text"],
            relief="flat",
            width=3,
            font=("Helvetica", 14, "bold"),
        )
        self.boton_atras.pack(side="left", padx=(12, 6), pady=16)

        logo = self.cargar_imagen("logo.png", 45)
        if logo:
            tk.Label(self.header, image=logo, bg=COLORS["white"]).pack(side="left", padx=(0, 6))

        titulo = tk.Frame(self.header, bg=COLORS["white"])
        titulo.pack(side="left", fill="y", pady=12)
        tk.Label(
            titulo,
            text="WANBE",
            bg=COLORS["white"],
            fg=COLORS["primary"],
            font=("Helvetica", 18, "bold"),
        ).pack(anchor="w")
        self.subtitulo_header = tk.Label(
            titulo,
            text="Inicio",
            bg=COLORS["white"],
            fg=COLORS["muted"],
            font=("Helvetica", 9, "bold"),
        )
        self.subtitulo_header.pack(anchor="w")

        tk.Button(
            self.header,
            text="?",
            command=self.mostrar_ayuda,
            bg=COLORS["card"],
            fg=COLORS["text"],
            relief="flat",
            width=3,
            font=("Helvetica", 13, "bold"),
        ).pack(side="right", padx=12, pady=16)

        self.canvas = tk.Canvas(self.marco_app, bg=COLORS["white"], highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(self.marco_app, orient="vertical", command=self.canvas.yview)
        scroll.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scroll.set)

        self.contenido = tk.Frame(self.canvas, bg=COLORS["white"])
        self.ventana_contenido = self.canvas.create_window((0, 0), window=self.contenido, anchor="nw")

        self.contenido.bind("<Configure>", lambda _e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.ventana_contenido, width=e.width))
        self.root.bind_all("<MouseWheel>", self.mover_scroll)

    def cargar_imagen(self, archivo: str, tamano: int) -> tk.PhotoImage | None:
        ruta = ASSETS_DIR / archivo
        if not ruta.exists():
            return None
        try:
            imagen = tk.PhotoImage(file=str(ruta))
            factor = max(1, imagen.width() // tamano, imagen.height() // tamano)
            imagen = imagen.subsample(factor, factor)
            self.imagenes[archivo] = imagen
            return imagen
        except tk.TclError:
            return None

    def mover_scroll(self, evento: tk.Event) -> None:
        self.canvas.yview_scroll(int(-1 * (evento.delta / 120)), "units")

    def limpiar(self) -> None:
        for widget in self.contenido.winfo_children():
            widget.destroy()
        self.canvas.yview_moveto(0)

    def cambiar_pantalla(self, pantalla: str, guardar: bool = True) -> None:
        if guardar and self.historial[-1] != pantalla:
            self.historial.append(pantalla)

        if pantalla == "inicio":
            self.mostrar_inicio(guardar=False)
        elif pantalla in TRAMITES:
            self.mostrar_tramite(pantalla, guardar=False)
        else:
            self.mostrar_categoria(pantalla, guardar=False)

    def volver(self) -> None:
        if len(self.historial) <= 1:
            return
        self.historial.pop()
        self.cambiar_pantalla(self.historial[-1], guardar=False)

    def actualizar_header(self, texto: str) -> None:
        self.subtitulo_header.configure(text=texto)
        estado = "normal" if len(self.historial) > 1 else "disabled"
        self.boton_atras.configure(state=estado)

    def titulo_seccion(self, titulo: str, subtitulo: str = "") -> None:
        caja = tk.Frame(self.contenido, bg=COLORS["white"])
        caja.pack(fill="x", padx=18, pady=(14, 8))
        tk.Label(
            caja,
            text=titulo,
            bg=COLORS["white"],
            fg=COLORS["primary"],
            font=("Helvetica", 18, "bold"),
            anchor="w",
            justify="left",
            wraplength=340,
        ).pack(fill="x")
        if subtitulo:
            tk.Label(
                caja,
                text=subtitulo,
                bg=COLORS["white"],
                fg=COLORS["muted"],
                font=("Helvetica", 10),
                anchor="w",
                justify="left",
                wraplength=340,
            ).pack(fill="x", pady=(3, 0))

    def tarjeta(self, titulo: str, subtitulo: str, icono: str, comando, color: str = COLORS["primary"]) -> None:
        tarjeta = tk.Frame(
            self.contenido,
            bg=COLORS["white"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
        )
        tarjeta.pack(fill="x", padx=18, pady=7)

        tk.Label(
            tarjeta,
            text=icono,
            bg=color,
            fg="white",
            width=4,
            font=("Helvetica", 11, "bold"),
        ).pack(side="left", padx=12, pady=14)

        textos = tk.Frame(tarjeta, bg=COLORS["white"])
        textos.pack(side="left", fill="both", expand=True, pady=12)

        tk.Label(
            textos,
            text=titulo,
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=("Helvetica", 13, "bold"),
            anchor="w",
            justify="left",
            wraplength=250,
        ).pack(fill="x")
        tk.Label(
            textos,
            text=subtitulo,
            bg=COLORS["white"],
            fg=COLORS["muted"],
            font=("Helvetica", 9),
            anchor="w",
            justify="left",
            wraplength=250,
        ).pack(fill="x", pady=(2, 0))

        tk.Label(tarjeta, text=">", bg=COLORS["white"], fg=color, font=("Helvetica", 15, "bold")).pack(side="right", padx=12)

        for widget in [tarjeta, *tarjeta.winfo_children(), *textos.winfo_children()]:
            widget.bind("<Button-1>", lambda _e: comando())
            widget.configure(cursor="hand2")

    def boton(self, texto: str, comando, color: str = COLORS["primary"], estado: str = "normal") -> tk.Button:
        boton = tk.Button(
            self.contenido,
            text=texto,
            command=comando,
            state=estado,
            bg=color,
            fg="white",
            relief="flat",
            font=("Helvetica", 11, "bold"),
            padx=12,
            pady=10,
        )
        boton.pack(fill="x", padx=18, pady=6)
        return boton

    def mostrar_inicio(self, guardar: bool = True) -> None:
        if guardar:
            self.historial = ["inicio"]
        self.limpiar()
        self.actualizar_header("Inicio")

        hero = tk.Frame(self.contenido, bg=COLORS["primary"])
        hero.pack(fill="x", padx=18, pady=(14, 12))
        tk.Label(
            hero,
            text="En que tramite te guiamos hoy?",
            bg=COLORS["primary"],
            fg="white",
            font=("Helvetica", 19, "bold"),
            justify="left",
            anchor="w",
            wraplength=330,
        ).pack(fill="x", padx=16, pady=(20, 4))
        tk.Label(
            hero,
            text="Guia visual sencilla para tramites de SAT y RENAP.",
            bg=COLORS["primary"],
            fg="#dbeafe",
            font=("Helvetica", 10),
            justify="left",
            anchor="w",
            wraplength=330,
        ).pack(fill="x", padx=16, pady=(0, 20))

        busqueda = tk.Entry(self.contenido, font=("Helvetica", 12), relief="flat", bg=COLORS["card"], fg=COLORS["text"])
        busqueda.pack(fill="x", padx=18, pady=(0, 10), ipady=10)
        busqueda.insert(0, "Buscar tramite...")

        resultados = tk.Frame(self.contenido, bg=COLORS["white"])
        resultados.pack(fill="x")

        def pintar_menu() -> None:
            for widget in resultados.winfo_children():
                widget.destroy()
            for nodo in MENU:
                self.tarjeta_en(resultados, nodo["titulo"], nodo["subtitulo"], nodo["icono"], lambda n=nodo: self.cambiar_pantalla(n["id"]))

        def buscar(_evento: tk.Event | None = None) -> None:
            texto = busqueda.get().strip()
            for widget in resultados.winfo_children():
                widget.destroy()
            if not texto or texto == "Buscar tramite...":
                pintar_menu()
                return
            encontrados = buscar_recursivo(MENU, texto)
            if not encontrados:
                self.mensaje_en(resultados, "No encontrado", "Intenta buscar con otra palabra.")
                return
            for item in encontrados:
                self.tarjeta_en(
                    resultados,
                    item["titulo"],
                    item["subtitulo"],
                    item["icono"],
                    lambda item=item: self.cambiar_pantalla(item["id"]),
                    COLORS["soft_blue"],
                )

        def limpiar_placeholder(_evento: tk.Event) -> None:
            if busqueda.get() == "Buscar tramite...":
                busqueda.delete(0, "end")

        busqueda.bind("<FocusIn>", limpiar_placeholder)
        busqueda.bind("<KeyRelease>", buscar)
        pintar_menu()

    def tarjeta_en(self, padre: tk.Widget, titulo: str, subtitulo: str, icono: str, comando, color: str = COLORS["primary"]) -> None:
        tarjeta = tk.Frame(padre, bg=COLORS["white"], highlightbackground=COLORS["border"], highlightthickness=1)
        tarjeta.pack(fill="x", padx=18, pady=7)

        tk.Label(tarjeta, text=icono, bg=color, fg="white", width=4, font=("Helvetica", 11, "bold")).pack(side="left", padx=12, pady=14)
        texto = tk.Frame(tarjeta, bg=COLORS["white"])
        texto.pack(side="left", fill="both", expand=True, pady=12)
        tk.Label(texto, text=titulo, bg=COLORS["white"], fg=COLORS["text"], font=("Helvetica", 13, "bold"), anchor="w").pack(fill="x")
        tk.Label(texto, text=subtitulo, bg=COLORS["white"], fg=COLORS["muted"], font=("Helvetica", 9), anchor="w", wraplength=250).pack(fill="x")
        tk.Label(tarjeta, text=">", bg=COLORS["white"], fg=color, font=("Helvetica", 15, "bold")).pack(side="right", padx=12)

        for widget in [tarjeta, *tarjeta.winfo_children(), *texto.winfo_children()]:
            widget.bind("<Button-1>", lambda _e: comando())
            widget.configure(cursor="hand2")

    def mensaje_en(self, padre: tk.Widget, titulo: str, texto: str) -> None:
        caja = tk.Frame(padre, bg=COLORS["card"], highlightbackground=COLORS["border"], highlightthickness=1)
        caja.pack(fill="x", padx=18, pady=12)
        tk.Label(caja, text=titulo, bg=COLORS["card"], fg=COLORS["text"], font=("Helvetica", 13, "bold")).pack(anchor="w", padx=14, pady=(14, 3))
        tk.Label(caja, text=texto, bg=COLORS["card"], fg=COLORS["muted"], font=("Helvetica", 10), wraplength=320, justify="left").pack(anchor="w", padx=14, pady=(0, 14))

    def mostrar_categoria(self, categoria_id: str, guardar: bool = True) -> None:
        if guardar:
            self.historial.append(categoria_id)
        self.limpiar()

        categoria = encontrar_categoria(MENU, categoria_id)
        if categoria is None:
            self.mensaje_en(self.contenido, "Error", "No se encontro la categoria.")
            return

        self.actualizar_header(categoria["titulo"])
        self.titulo_seccion(categoria["titulo"], categoria["subtitulo"])

        for hijo in categoria.get("hijos", []):
            if "tramite" in hijo:
                tramite_id = hijo["tramite"]
                tramite = TRAMITES[tramite_id]
                self.tarjeta(tramite["titulo"], tramite["descripcion"], tramite["icono"], lambda t=tramite_id: self.cambiar_pantalla(t), COLORS["purple"])
            else:
                self.tarjeta(hijo["titulo"], hijo["subtitulo"], hijo["icono"], lambda h=hijo: self.cambiar_pantalla(h["id"]))

    def mostrar_tramite(self, tramite_id: str, guardar: bool = True) -> None:
        if guardar:
            self.historial.append(tramite_id)
        self.limpiar()

        tramite = TRAMITES[tramite_id]
        self.actualizar_header(tramite["titulo"])
        self.titulo_seccion(f"{tramite['icono']}  {tramite['titulo']}", tramite["descripcion"])

        if not self.checklist_listo[tramite_id]:
            self.mostrar_checklist(tramite_id)
        else:
            self.mostrar_paso(tramite_id)

    def mostrar_checklist(self, tramite_id: str) -> None:
        tramite = TRAMITES[tramite_id]
        caja = tk.Frame(self.contenido, bg=COLORS["card"], highlightbackground=COLORS["border"], highlightthickness=1)
        caja.pack(fill="x", padx=18, pady=10)

        tk.Label(caja, text="Antes de empezar", bg=COLORS["card"], fg=COLORS["text"], font=("Helvetica", 14, "bold")).pack(anchor="w", padx=14, pady=(14, 4))
        tk.Label(
            caja,
            text="Marca los documentos que ya tienes para iniciar la guia.",
            bg=COLORS["card"],
            fg=COLORS["muted"],
            font=("Helvetica", 10),
            wraplength=320,
            justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 8))

        variables = []

        boton_inicio = tk.Button(
            caja,
            text="Ir al paso 1",
            state="disabled",
            command=lambda: self.iniciar_tramite(tramite_id),
            bg=COLORS["soft_blue"],
            fg="white",
            relief="flat",
            font=("Helvetica", 11, "bold"),
            padx=10,
            pady=10,
        )

        def revisar() -> None:
            listo = all(variable.get() for variable in variables)
            boton_inicio.configure(state="normal" if listo else "disabled")

        for requisito in tramite["requisitos"]:
            variable = tk.BooleanVar(value=False)
            variables.append(variable)
            tk.Checkbutton(
                caja,
                text=requisito,
                variable=variable,
                command=revisar,
                bg=COLORS["card"],
                fg=COLORS["text"],
                selectcolor=COLORS["white"],
                activebackground=COLORS["card"],
                anchor="w",
                justify="left",
                wraplength=310,
                font=("Helvetica", 10),
            ).pack(fill="x", padx=14, pady=4)

        boton_inicio.pack(fill="x", padx=14, pady=(10, 14))

    def iniciar_tramite(self, tramite_id: str) -> None:
        self.checklist_listo[tramite_id] = True
        self.paso_actual[tramite_id] = 0
        self.mostrar_tramite(tramite_id, guardar=False)

    def mostrar_paso(self, tramite_id: str) -> None:
        tramite = TRAMITES[tramite_id]
        indice = self.paso_actual[tramite_id]
        pasos = tramite["pasos"]
        paso = pasos[indice]

        tk.Label(
            self.contenido,
            text=f"Paso {indice + 1} de {len(pasos)}",
            bg=COLORS["white"],
            fg=COLORS["muted"],
            font=("Helvetica", 10, "bold"),
        ).pack(anchor="w", padx=18, pady=(4, 2))

        progreso = tk.Frame(self.contenido, bg=COLORS["border"], height=10)
        progreso.pack(fill="x", padx=18, pady=(0, 12))
        progreso.pack_propagate(False)
        tk.Frame(progreso, bg=COLORS["purple"], width=int(360 * ((indice + 1) / len(pasos))), height=10).pack(side="left")

        caja = tk.Frame(self.contenido, bg=COLORS["white"], highlightbackground=COLORS["border"], highlightthickness=1)
        caja.pack(fill="x", padx=18, pady=8)

        tk.Label(caja, text=paso["titulo"], bg=COLORS["white"], fg=COLORS["text"], font=("Helvetica", 15, "bold"), wraplength=330, justify="left").pack(anchor="w", padx=14, pady=(14, 5))
        tk.Label(caja, text=paso["texto"], bg=COLORS["white"], fg=COLORS["muted"], font=("Helvetica", 10), wraplength=330, justify="left").pack(anchor="w", padx=14, pady=(0, 8))

        for numero, item in enumerate(paso["items"], start=1):
            tk.Label(caja, text=f"{numero}. {item}", bg=COLORS["white"], fg=COLORS["text"], font=("Helvetica", 10), wraplength=320, justify="left").pack(anchor="w", padx=20, pady=2)

        if paso.get("enlace"):
            tk.Button(
                caja,
                text="Abrir enlace oficial",
                command=lambda url=paso["enlace"]: webbrowser.open(url),
                bg=COLORS["primary"],
                fg="white",
                relief="flat",
                font=("Helvetica", 10, "bold"),
                padx=10,
                pady=9,
            ).pack(fill="x", padx=14, pady=12)

        self.documentos(tramite)
        self.navegacion_pasos(tramite_id)

    def documentos(self, tramite: dict) -> None:
        caja = tk.Frame(self.contenido, bg=COLORS["warning_bg"], highlightbackground=COLORS["warning"], highlightthickness=1)
        caja.pack(fill="x", padx=18, pady=8)
        tk.Label(caja, text="Documentos indispensables", bg=COLORS["warning_bg"], fg=COLORS["warning"], font=("Helvetica", 11, "bold")).pack(anchor="w", padx=14, pady=(12, 4))
        for requisito in tramite["requisitos"]:
            tk.Label(caja, text=f"- {requisito}", bg=COLORS["warning_bg"], fg=COLORS["warning"], font=("Helvetica", 10), wraplength=320, justify="left").pack(anchor="w", padx=20, pady=2)

    def navegacion_pasos(self, tramite_id: str) -> None:
        barra = tk.Frame(self.contenido, bg=COLORS["white"])
        barra.pack(fill="x", padx=18, pady=(8, 20))

        indice = self.paso_actual[tramite_id]
        total = len(TRAMITES[tramite_id]["pasos"])

        tk.Button(
            barra,
            text="Anterior",
            command=lambda: self.cambiar_paso(tramite_id, -1),
            state="normal" if indice > 0 else "disabled",
            bg=COLORS["card"],
            fg=COLORS["text"],
            relief="flat",
            font=("Helvetica", 10, "bold"),
            pady=10,
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))

        texto = "Finalizar" if indice == total - 1 else "Siguiente"
        comando = lambda: self.finalizar(tramite_id) if indice == total - 1 else self.cambiar_paso(tramite_id, 1)
        tk.Button(
            barra,
            text=texto,
            command=comando,
            bg=COLORS["purple"],
            fg="white",
            relief="flat",
            font=("Helvetica", 10, "bold"),
            pady=10,
        ).pack(side="left", fill="x", expand=True, padx=(5, 0))

    def cambiar_paso(self, tramite_id: str, cambio: int) -> None:
        total = len(TRAMITES[tramite_id]["pasos"])
        self.paso_actual[tramite_id] = max(0, min(total - 1, self.paso_actual[tramite_id] + cambio))
        self.mostrar_tramite(tramite_id, guardar=False)

    def finalizar(self, tramite_id: str) -> None:
        self.checklist_listo[tramite_id] = False
        self.paso_actual[tramite_id] = 0
        messagebox.showinfo("Wanbe", "Guia finalizada. Puedes volver al inicio.")
        self.historial = ["inicio"]
        self.mostrar_inicio(guardar=False)

    def mostrar_ayuda(self) -> None:
        texto = (
            "Proyecto Python sencillo de Wanbe.\n\n"
            "Incluye:\n"
            "- Listas para requisitos y pasos.\n"
            "- Matrices para rutas de navegacion.\n"
            "- Diccionarios para tramites.\n"
            "- Recursion en el buscador."
        )
        messagebox.showinfo("Acerca del proyecto", texto)

    def ejecutar(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    app = WanbeApp()
    app.ejecutar()
