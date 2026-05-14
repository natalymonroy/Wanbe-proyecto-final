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

from app import WanbeApp


def main() -> None:
    app = WanbeApp()
    app.ejecutar()


if __name__ == "__main__":
    main()

    def iniciar_tramite(self, tramite_id: str) -> None:
        self.checklist_listo[tramite_id] = True
        self.paso_actual[tramite_id] = 0
        self.mostrar_tramite(tramite_id, guardar=False)
        guardar_estado(
            {
                "paso_actual": self.paso_actual,
                "checklist_listo": self.checklist_listo,
                "configuracion": self.configuracion,
                "historial": self.historial,
            }
        )

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
            text="Regresar",
            command=lambda: self.cambiar_paso(tramite_id, -1),
            state="normal" if indice > 0 else "disabled",
            bg=COLORS["card"],
            fg=COLORS["text"],
            relief="flat",
            font=("Helvetica", 10, "bold"),
            pady=10,
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))

        texto = "Finalizar" if indice == total - 1 else "Continuar"
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
        guardar_estado(
            {
                "paso_actual": self.paso_actual,
                "checklist_listo": self.checklist_listo,
                "configuracion": self.configuracion,
                "historial": self.historial,
            }
        )

    def finalizar(self, tramite_id: str) -> None:
        if self.configuracion["confirmar_finalizacion"]:
            respuesta = messagebox.askyesno("Wanbe", "Se completo la guia. Deseas volver al inicio?")
            if not respuesta:
                return
        self.checklist_listo[tramite_id] = False
        self.paso_actual[tramite_id] = 0
        self.historial = ["inicio"]
        self.mostrar_inicio(guardar=False)
        guardar_estado(
            {
                "paso_actual": self.paso_actual,
                "checklist_listo": self.checklist_listo,
                "configuracion": self.configuracion,
                "historial": self.historial,
            }
        )

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

    def aplicar_configuracion(self) -> None:
        if self.configuracion["ventana_compacta"]:
            self.root.geometry("390x620")
        else:
            self.root.geometry("430x720")

    def mostrar_configuracion(self) -> None:
        ventana = tk.Toplevel(self.root)
        ventana.title("Configuracion")
        ventana.transient(self.root)
        ventana.grab_set()
        ventana.configure(bg=COLORS["white"])
        ventana.resizable(False, False)

        tk.Label(
            ventana,
            text="Preferencias de la aplicacion",
            bg=COLORS["white"],
            fg=COLORS["primary"],
            font=("Helvetica", 13, "bold"),
        ).pack(anchor="w", padx=16, pady=(16, 6))

        tk.Label(
            ventana,
            text="Activa o desactiva las opciones y guarda los cambios.",
            bg=COLORS["white"],
            fg=COLORS["muted"],
            font=("Helvetica", 10),
            wraplength=320,
            justify="left",
        ).pack(anchor="w", padx=16, pady=(0, 10))

        ventana_compacta = tk.BooleanVar(value=self.configuracion["ventana_compacta"])
        confirmar_finalizacion = tk.BooleanVar(value=self.configuracion["confirmar_finalizacion"])

        tk.Checkbutton(
            ventana,
            text="Usar ventana compacta",
            variable=ventana_compacta,
            bg=COLORS["white"],
            fg=COLORS["text"],
            activebackground=COLORS["white"],
            selectcolor=COLORS["white"],
            font=("Helvetica", 10),
        ).pack(anchor="w", padx=16, pady=4)

        tk.Checkbutton(
            ventana,
            text="Confirmar al finalizar un tramite",
            variable=confirmar_finalizacion,
            bg=COLORS["white"],
            fg=COLORS["text"],
            activebackground=COLORS["white"],
            selectcolor=COLORS["white"],
            font=("Helvetica", 10),
        ).pack(anchor="w", padx=16, pady=4)

        botones = tk.Frame(ventana, bg=COLORS["white"])
        botones.pack(fill="x", padx=16, pady=(14, 16))

        def guardar() -> None:
            self.configuracion["ventana_compacta"] = ventana_compacta.get()
            self.configuracion["confirmar_finalizacion"] = confirmar_finalizacion.get()
            self.aplicar_configuracion()
            ventana.destroy()
            guardar_estado(
                {
                    "paso_actual": self.paso_actual,
                    "checklist_listo": self.checklist_listo,
                    "configuracion": self.configuracion,
                    "historial": self.historial,
                }
            )
            messagebox.showinfo("Configuracion", "Cambios guardados correctamente.")

        tk.Button(
            botones,
            text="Cancelar",
            command=ventana.destroy,
            bg=COLORS["card"],
            fg=COLORS["text"],
            relief="flat",
            font=("Helvetica", 10, "bold"),
            padx=12,
            pady=8,
        ).pack(side="left")

        tk.Button(
            botones,
            text="Guardar",
            command=guardar,
            bg=COLORS["primary"],
            fg="white",
            relief="flat",
            font=("Helvetica", 10, "bold"),
            padx=12,
            pady=8,
        ).pack(side="right")

    def ejecutar(self) -> None:
        self.root.mainloop()

    def _on_close(self) -> None:
        """Handler para el cierre de la aplicacion: persiste estado y destruye la ventana."""
        try:
            guardar_estado(
                {
                    "paso_actual": self.paso_actual,
                    "checklist_listo": self.checklist_listo,
                    "configuracion": self.configuracion,
                    "historial": self.historial,
                }
            )
        except Exception:
            pass
        self.root.destroy()


if __name__ == "__main__":
    app = WanbeApp()
    app.ejecutar()
