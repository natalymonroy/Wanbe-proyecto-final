# Documentacion: Guia de Solicitud de NIT

## 1. Descripcion general

La guia de Solicitud de NIT forma parte del proyecto Wanbe y orienta al usuario para obtener su NIT por primera vez por medio del portal SAT.

Esta documentacion explica:
- Como esta representado el tramite en el codigo.
- Que datos utiliza la interfaz.
- Cual es el flujo paso a paso.
- Que decisiones de programacion se aplicaron.

---

## 2. Ubicacion en el codigo

El tramite NIT se define dentro del diccionario principal TRAMITES en el archivo proyecto.py, bajo la clave "nit".

Estructura base:

```python
"nit": {
    "titulo": "Solicitud de NIT",
    "portal": "SAT",
    "icono": "NIT",
    "descripcion": "Solicitud electronica para obtener NIT por primera vez.",
    "requisitos": [ ... ],
    "pasos": [ ... ]
}
```

---

## 3. Campos del tramite NIT

### 3.1 titulo
- Valor: Solicitud de NIT
- Uso: Se muestra en tarjetas, encabezados y pantallas del tramite.

### 3.2 portal
- Valor: SAT
- Uso: Clasifica la guia dentro del menu de SAT y permite volver a la categoria correcta.

### 3.3 icono
- Valor: NIT
- Uso: Se muestra como etiqueta visual corta dentro de tarjetas.

### 3.4 descripcion
- Valor: Solicitud electronica para obtener NIT por primera vez.
- Uso: Resume el objetivo del tramite antes de entrar al detalle.

### 3.5 requisitos
Lista usada para validar que el usuario este preparado antes de iniciar:
- DPI vigente
- Recibo de luz o agua
- Correo electronico

### 3.6 pasos
Lista ordenada de acciones. Cada paso es un diccionario con:
- titulo
- texto
- items
- enlace (opcional)

---

## 4. Flujo del tramite NIT

### Paso 1: Abre portal SAT
- Objetivo: Ingresar al portal oficial de Solicitud Electronica de NIT.
- Items:
  - Completa captcha.
  - Escribe tu correo.
  - Solicita el enlace.
- Enlace oficial:
  - https://portal.sat.gob.gt/portal/solicitud-electronica-de-nit/

### Paso 2: Valida correo
- Objetivo: Confirmar el mensaje enviado por SAT.
- Items:
  - Revisa bandeja principal.
  - Revisa spam.
  - Copia el codigo recibido.

### Paso 3: Datos personales
- Objetivo: Registrar datos de identificacion y soporte.
- Items:
  - El numero de serie esta atras del DPI.
  - Sube documentos legibles.

### Paso 4: Actividad economica
- Objetivo: Seleccionar perfil tributario correcto.
- Items:
  - Si no trabajas, elige sin obligaciones.
  - Si facturas, elige negocio.

### Paso 5: Enviar solicitud
- Objetivo: Confirmar y finalizar el tramite.
- Items:
  - Confirma datos.
  - Guarda usuario y clave.
  - Espera respuesta por correo.

---

## 5. Logica de navegacion en la app

En escritorio y web el tramite NIT usa la misma idea:
- Se carga la informacion desde TRAMITES["nit"].
- Se muestra checklist de requisitos.
- Se avanza por pasos secuenciales.
- Se calcula progreso segun paso actual y total de pasos.

Formula de progreso:

```text
progreso = (paso_actual / total_pasos) * 100
```

Con 5 pasos:
- Paso 1 = 20%
- Paso 2 = 40%
- Paso 3 = 60%
- Paso 4 = 80%
- Paso 5 = 100%

---

## 6. Temas de programacion aplicados

### Listas
Se usan en:
- requisitos
- pasos
- items de cada paso

### Diccionarios
Se usan en:
- TRAMITES
- cada paso del NIT

### Recursion
No cambia el contenido del NIT, pero permite encontrar el tramite desde el arbol MENU por busqueda.

### Interfaz grafica y web
La misma informacion del NIT se renderiza en:
- App de escritorio (tkinter)
- Vista web local (HTTP + HTML)

---

## 7. Recomendaciones de uso para el usuario final

- Tener correo activo y acceso inmediato para validar codigo.
- Verificar datos del DPI antes de enviar.
- Guardar usuario y clave en un lugar seguro.
- Revisar carpeta de spam si no llega correo SAT.

---

## 8. Conclusion

La guia de NIT esta modelada de forma clara y modular:
- Datos centralizados en una sola estructura.
- Flujo secuencial facil de seguir.
- Reutilizable en interfaz de escritorio y web.

Esto facilita mantenimiento, explicacion academica y futuras mejoras del tramite.
