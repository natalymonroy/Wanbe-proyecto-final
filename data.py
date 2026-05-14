#!/usr/bin/env python3
"""Datos y constantes del proyecto Wanbe.

Contiene la definición de `TRAMITES`, `MENU`, colores y funciones de
persistencia (`cargar_estado`, `guardar_estado`).
"""
from __future__ import annotations

from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
# Directorio para persistencia de estado
DATA_DIR = BASE_DIR / "data"
STATE_FILE = DATA_DIR / "state.json"

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

RUTAS = [
    ["Inicio", "SAT", "Vehiculos", "Pago de Calcomanía"],
    ["Inicio", "SAT", "Individuales", "Solicitud de NIT"],
    ["Inicio", "RENAP", "Tramite de DPI"],
    ["Inicio", "RENAP", "Certificados en Linea"],
]

TRAMITES = {
    "calcomania": {
        "titulo": "Pago de Calcomanía",
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
                "titulo": "Imprime calcomanía",
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
    "dpi":  {
        "titulo": "Trámite de DPI",
        "portal": "RENAP",
        "icono": "DPI",
        "descripcion": "Guía básica para tramitar el Documento Personal de Identificación.",
        "requisitos": [
            "Certificado de nacimiento",
            "Boleto de ornato"
        ],
        "pasos": [
            {
                "titulo": "Certificado de nacimiento",
                "texto": "Solicita un certificado reciente en RENAP o ePortal.",
                "items": [
                    "Presencial: Q15.",
                    "En línea: Q19.",
                    "Debe estar vigente."
                ],
                "enlace": "https://eportal.renap.gob.gt/"
            },
            {
                "titulo": "Pago en banco",
                "texto": "Paga la tarifa del DPI.",
                "items": [
                    "Costo usual: Q100.",
                    "Mayores de 60 años: gratuito."
                ]
            },
            {
                "titulo": "Visita RENAP",
                "texto": "Acude a una sede RENAP para foto, huellas y firma.",
                "items": [
                    "No uses ropa blanca.",
                    "Revisa tus datos antes de aprobar."
                ]
            },
            {
                "titulo": "Recoger DPI",
                "texto": "Lleva la constancia para recoger tu documento.",
                "items": [
                    "Ve a la misma agencia.",
                    "Revisa el DPI al recibirlo."
                ]
            }
        ]
    },
}

MENU = [
    {
        "id": "sat",
        "titulo": "Portal SAT",
        "subtitulo": "Vehiculos y NIT",
        "icono": "SAT",
        "hijos": [
            {
                "id": "vehiculos",
                "titulo": "Vehiculos",
                "subtitulo": "Calcomanía y placas",
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
        ],
    },
    {
        "id": "renap",
        "titulo": "Portal RENAP",
        "subtitulo": "DPI y certificados",
        "icono": "DPI",
        "hijos": [{"tramite": "dpi"}],
    },
]


import shutil
import tempfile
from datetime import datetime
from json import JSONDecodeError


def cargar_estado() -> dict:
    """Carga el estado persistido desde `STATE_FILE`.

    Devuelve un diccionario con claves opcionales: `paso_actual`, `checklist_listo`,
    `configuracion` y `historial`.

    Si el JSON está corrupto, el archivo se respalda como `state.json.corrupt.TIMESTAMP`
    y se devuelve un dict vacío para no romper la aplicación.
    """
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not STATE_FILE.exists():
            return {}
        with STATE_FILE.open("r", encoding="utf-8") as fh:
            raw = fh.read()
        try:
            estado = json.loads(raw)
        except JSONDecodeError as exc:
            # Respaldar archivo corrupto y devolver estado vacío
            ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            backup = STATE_FILE.with_name(f"state.json.corrupt.{ts}")
            try:
                shutil.move(str(STATE_FILE), str(backup))
                print(f"Warning: state.json corrupto; se movió a {backup}")
            except Exception:
                print("Warning: state.json corrupto y no se pudo mover el archivo de respaldo", exc)
            return {}

        # Validar estructura mínima esperada
        if not isinstance(estado, dict):
            return {}

        paso_actual = estado.get("paso_actual", {})
        checklist = estado.get("checklist_listo", {})
        if not isinstance(paso_actual, dict) or not isinstance(checklist, dict):
            return {}

        return estado
    except Exception as exc:  # noqa: BLE001 - queremos capturar errores de I/O
        print("Warning: no se pudo cargar el estado:", exc)
        return {}


def guardar_estado(estado: dict) -> None:
    """Guarda el `estado` en formato JSON en `STATE_FILE`.

    Escritura atómica: se escribe en un fichero temporal en el mismo directorio
    y luego se reemplaza el `state.json` para evitar archivos parcialmente escritos.
    """
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        # Escritura atómica: escribir en fichero temporal y mover
        dirpath = STATE_FILE.parent
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=str(dirpath), delete=False) as tmp:
            json.dump(estado, tmp, ensure_ascii=False, indent=2)
            tmp_path = Path(tmp.name)
        try:
            tmp_path.replace(STATE_FILE)
        except Exception:
            # fallback: intentar copiar y remover temporal
            try:
                shutil.copy(str(tmp_path), str(STATE_FILE))
                tmp_path.unlink(missing_ok=True)
            except Exception as exc:
                print("Warning: no se pudo guardar el estado (fallback):", exc)
    except Exception as exc:
        print("Warning: no se pudo guardar el estado:", exc)
