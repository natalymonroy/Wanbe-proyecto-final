#!/usr/bin/env python3
"""Funciones utilitarias para Wanbe (busqueda, normalizacion, recursion)."""
from __future__ import annotations

import unicodedata
from typing import List, Dict
from data import TRAMITES


def normalizar(texto: str) -> str:
    """Convierte texto a minúsculas y elimina tildes para mejorar búsquedas."""
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(letra for letra in texto if unicodedata.category(letra) != "Mn")


def buscar_recursivo(nodos: List[Dict], consulta: str, ruta: str = "") -> List[Dict]:
    """Busca trámites dentro del árbol MENU usando recursión."""
    resultados = []
    consulta = normalizar(consulta)

    for nodo in nodos:
        if "tramite" in nodo:
            clave = nodo["tramite"]
            tramite = TRAMITES.get(clave, {})
            texto = " ".join([tramite.get("titulo", ""), tramite.get("descripcion", ""), tramite.get("portal", "")])
            if consulta in normalizar(texto):
                resultados.append(
                    {
                        "tipo": "tramite",
                        "id": clave,
                        "titulo": tramite.get("titulo", clave),
                        "subtitulo": ruta,
                        "icono": tramite.get("icono", ""),
                    }
                )
            continue

        texto_categoria = f"{nodo['titulo']} {nodo.get('subtitulo', '')}"
        if consulta in normalizar(texto_categoria):
            resultados.append(
                {
                    "tipo": "categoria",
                    "id": nodo["id"],
                    "titulo": nodo["titulo"],
                    "subtitulo": nodo["subtitulo"],
                    "icono": nodo.get("icono", ""),
                }
            )

        nueva_ruta = f"{ruta} > {nodo['titulo']}" if ruta else nodo["titulo"]
        resultados.extend(buscar_recursivo(nodo.get("hijos", []), consulta, nueva_ruta))

    return resultados


def encontrar_categoria(nodos: List[Dict], categoria_id: str) -> Dict | None:
    """Encuentra una categoría dentro del árbol usando recursión."""
    for nodo in nodos:
        if nodo.get("id") == categoria_id:
            return nodo
        encontrado = encontrar_categoria(nodo.get("hijos", []), categoria_id)
        if encontrado:
            return encontrado
    return None
