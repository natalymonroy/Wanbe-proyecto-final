#!/usr/bin/env python3
"""Launcher backward-compatible para la aplicación Wanbe.

Este archivo mantiene el mismo entrypoint `python proyecto.py` pero
delegando la implementación a `app.py` y los datos a `data.py`.
"""
from __future__ import annotations

from app import WanbeApp


def main() -> None:
    app = WanbeApp()
    app.ejecutar()


if __name__ == "__main__":
    main()
