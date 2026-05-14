# Documentación: Guía de Pago de Calcomanía

## Descripción General

La guía de **Pago de Calcomanía** es una de las tres guías principales del proyecto Wanbe. Esta guía proporciona a los usuarios un paso a paso para realizar el pago del Impuesto Sobre Circulación de Vehículos en Guatemala a través del portal SAT (Superintendencia de Administración Tributaria).

---

## Estructura del Código (Diccionario)

En `proyecto.py`, la guía de calcomanía se define como un **diccionario** dentro del diccionario principal `TRAMITES`. Aquí explicamos cada campo:

### 1. **Identificador único: `"calcomania"`**

```python
"calcomania": {
    # contenido aquí
}
```

- **Qué es**: La clave del diccionario que identifica de forma única esta guía en el sistema.
- **Para qué sirve**: Cuando el usuario hace clic en "Pago de Calcomanía", la aplicación busca `TRAMITES["calcomania"]` para obtener toda la información.
- **Analogía**: Es como el "ID" o número de identidad de esta guía.

---

### 2. **Título: `"titulo"`**

```python
"titulo": "Pago de Calcomanía",
```

- **Qué es**: El nombre que se muestra al usuario.
- **Dónde aparece**: 
  - En la pantalla de inicio como tarjeta seleccionable
  - En el header de la aplicación cuando entra a la guía
  - En resultados de búsqueda
- **Uso en código**: Se accede con `TRAMITES["calcomania"]["titulo"]`

---

### 3. **Portal: `"portal"`**

```python
"portal": "SAT",
```

- **Qué es**: Indica a qué institución gubernamental pertenece este trámite.
- **Opciones disponibles**: 
  - `"SAT"` - Superintendencia de Administración Tributaria
  - `"RENAP"` - Registro Nacional de Personas
- **Para qué sirve**: 
  - Organizar las guías por institución en el menú
  - Filtrar búsquedas por portal
  - Determinar a dónde ir si el usuario regresa desde la guía

---

### 4. **Ícono: `"icono"`**

```python
"icono": "CAR",
```

- **Qué es**: Un código de 3 letras que se muestra como ícono visual.
- **Valores disponibles**: 
  - `"CAR"` - Para vehículos/calcomanía (de CAR = automóvil)
  - `"NIT"` - Para la guía de NIT
  - `"DPI"` - Para la guía de DPI
- **Visualización**: Aparece como un cuadro de color con letras blancas en la interfaz

---

### 5. **Descripción: `"descripcion"`**

```python
"descripcion": "Pago del Impuesto Sobre Circulación de Vehículos.",
```

- **Qué es**: Un resumen breve de qué trata la guía.
- **Dónde aparece**: Debajo del título en las tarjetas de la interfaz.
- **Longitud recomendada**: 1-2 oraciones máximo
- **Propósito**: Ayudar al usuario a entender de qué trata sin entrar a la guía

---

### 6. **Requisitos: `"requisitos"`**

```python
"requisitos": ["Placa del vehículo", "NIT del propietario"],
```

- **Qué es**: Una **lista** de documentos/datos que el usuario necesita ANTES de comenzar la guía.
- **Estructura**: Array (lista) de strings
- **Número de elementos**: 2 requisitos para calcomanía
- **Flujo de uso**:
  1. El usuario abre la guía
  2. Aparece una pantalla de "Antes de empezar"
  3. El usuario marca cada requisito que tiene
  4. Solo cuando marca TODOS los requisitos se habilita el botón "Ir al paso 1"

**Lógica en código** (ubicada en `mostrar_checklist`):
```python
def revisar():
    listo = all(variable.get() for variable in variables)
    # Si todas las variables están marcadas, habilita el botón
    boton_inicio.configure(state="normal" if listo else "disabled")
```

---

### 7. **Pasos: `"pasos"`**

```python
"pasos": [
    { paso 1 },
    { paso 2 },
    { paso 3 },
    { paso 4 }
]
```

- **Qué es**: Una **lista** de diccionarios, donde cada diccionario es un paso de la guía.
- **Cantidad para calcomanía**: 4 pasos
- **Orden**: Se ejecutan secuencialmente, el usuario navega con botones "Regresar" y "Continuar"

---

## Detalle de Cada Paso

### **PASO 1: Revisa datos del vehículo**

```python
{
    "titulo": "Revisa datos del vehiculo",
    "texto": "Antes de iniciar, ten claros los datos que la SAT pedira para generar el formulario.",
    "items": [
        "Confirma la placa.",
        "Confirma el NIT del propietario.",
        "Ten acceso a Declaraguate."
    ],
}
```

#### Estructura:

| Campo | Valor | Propósito |
|-------|-------|-----------|
| `titulo` | "Revisa datos del vehículo" | Título que ve el usuario (1ª línea grande) |
| `texto` | Instrucción descriptiva | Explicación del paso (texto mediano) |
| `items` | Lista de 3 instrucciones | Checklist de cosas a hacer (viñetas) |
| `enlace` | NO TIENE | No hay botón "Abrir enlace oficial" en este paso |

#### Visualización en la app:
```
┌─────────────────────────────────┐
│ Paso 1 de 4                     │
│ [████░░░░░░░░░░░░░░░░░░░░░░░░] │  ← Barra de progreso (25%)
│                                 │
│ Revisa datos del vehículo       │  ← Título (grande y azul)
│ Antes de iniciar, ten claros... │  ← Texto descriptivo
│                                 │
│ 1. Confirma la placa.           │  ← Items (instrucciones)
│ 2. Confirma el NIT...           │
│ 3. Ten acceso a Declaraguate.   │
│                                 │
│ [Regresar] [Continuar]          │
└─────────────────────────────────┘
```

#### ¿Por qué este paso?
- Prepara al usuario mentalmente
- Verifica que tenga los datos listos
- Avisa que necesita acceso a Declaraguate (portal en línea del SAT)

---

### **PASO 2: Genera formulario SAT-4091**

```python
{
    "titulo": "Genera formulario SAT-4091",
    "texto": "Ingresa a Declaraguate y genera el formulario de vehículos.",
    "items": [
        "Busca la sección Vehículos.",
        "Ingresa NIT y placa.",
        "Valida y congela."
    ],
    "enlace": "https://declaraguate.sat.gob.gt/declaraguate-web/",
}
```

#### Estructura:

| Campo | Valor | Propósito |
|-------|-------|-----------|
| `titulo` | "Genera formulario SAT-4091" | Nombre del paso |
| `texto` | Instrucción para Declaraguate | Qué hacer en este paso |
| `items` | 3 instrucciones | Pasos específicos |
| `enlace` | URL del portal SAT | **BOTÓN NUEVO**: "Abrir enlace oficial" |

#### Campo especial `"enlace"`:

- **Qué es**: Una URL que el usuario puede abrir haciendo clic en el botón "Abrir enlace oficial"
- **Función**: Abre el navegador web en `https://declaraguate.sat.gob.gt/declaraguate-web/`
- **En código**: 
  ```python
  if paso.get("enlace"):
      tk.Button(
          caja,
          text="Abrir enlace oficial",
          command=lambda url=paso["enlace"]: webbrowser.open(url),
          ...
      ).pack()
  ```

#### Visualización en la app:
```
┌─────────────────────────────────────────────┐
│ Paso 2 de 4                                 │
│ [████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] │  ← 50% completado
│                                             │
│ Genera formulario SAT-4091                  │
│ Ingresa a Declaraguate y genera...          │
│                                             │
│ 1. Busca la sección Vehículos.              │
│ 2. Ingresa NIT y placa.                     │
│ 3. Valida y congela.                        │
│                                             │
│ [ABRIR ENLACE OFICIAL]  ← Botón azul       │
│                                             │
│ [Regresar] [Continuar]                      │
└─────────────────────────────────────────────┘
```

#### ¿Por qué este paso?
- Guía al usuario a la plataforma correcta
- Le dice exactamente dónde buscar (sección Vehículos)
- Proporciona un acceso rápido con el botón de enlace

---

### **PASO 3: Paga en banco**

```python
{
    "titulo": "Paga en banco",
    "texto": "Usa el número de formulario y número de acceso.",
    "items": [
        "Verifica el monto.",
        "Paga en línea o ventanilla.",
        "Guarda recibo."
    ],
}
```

#### Estructura:

| Campo | Valor | Propósito |
|-------|-------|-----------|
| `titulo` | "Paga en banco" | Paso de pago |
| `texto` | Instrucción del pago | Referencia para pagar |
| `items` | 3 instrucciones | Cómo pagar |
| `enlace` | NO TIENE | No hay enlace externo en este paso |

#### Contenido específico:
- **"Verifica el monto"**: El usuario debe confirmar cuánto cuesta antes de pagar
- **"Paga en línea o ventanilla"**: Opciones de pago flexibles
- **"Guarda recibo"**: Importante para referencias futuras

---

### **PASO 4: Imprime calcomanía**

```python
{
    "titulo": "Imprime calcomanía",
    "texto": "Descarga el distintivo en PDF para portarlo en tu vehiculo.",
    "items": [
        "Revisa que la placa sea correcta.",
        "Imprime o guarda el PDF."
    ],
    "enlace": "https://portal.sat.gob.gt/portal/impresion-calcomania/",
}
```

#### Estructura:

| Campo | Valor | Propósito |
|-------|-------|-----------|
| `titulo` | "Imprime calcomanía" | Paso final |
| `texto` | Instrucción de descarga | Qué hacer con el PDF |
| `items` | 2 instrucciones | Verificación e impresión |
| `enlace` | URL del portal de impresión | Acceso al formulario de calcomanía |

#### Nota especial:
- Este es el **paso final** (4 de 4)
- El botón "Continuar" se convierte en **"Finalizar"**
- Después de completar, se pregunta si regresar al inicio

---

## Flujo Completo de la Guía de Calcomanía

```
INICIO
  ↓
[Usuario hace clic en "Pago de Calcomanía"]
  ↓
Pantalla de requisitos (Checklist)
  ├─ Placa del vehículo
  ├─ NIT del propietario
  └─ [Todos marcados → "Ir al paso 1"]
  ↓
PASO 1: Revisa datos del vehículo
  [Regresar] [Continuar]
  ↓
PASO 2: Genera formulario SAT-4091
  [Abrir enlace oficial]
  [Regresar] [Continuar]
  ↓
PASO 3: Paga en banco
  [Regresar] [Continuar]
  ↓
PASO 4: Imprime calcomanía (FINAL)
  [Abrir enlace oficial]
  [Regresar] [Finalizar]
  ↓
Pregunta: ¿Volver al inicio?
  ├─ Sí → Vuelve a la pantalla principal
  └─ No → Se queda en pantalla de conclusión
```

---

## Integración con el Rest del Sistema

### 1. **En el Menú Principal**

La calcomanía aparece bajo:
```
Portal SAT
  └─ Vehículos
      └─ Pago de Calcomanía  ← AQUÍ
```

Esto se define en el diccionario `MENU` y se busca usando la función `encontrar_categoria()`.

### 2. **En Búsqueda**

Cuando el usuario busca "calcomanía", la función `buscar_recursivo()` encuentra:
- El título: "Pago de Calcomanía" ✓
- La descripción: "Pago del Impuesto..." ✓
- El portal: "SAT" ✓

### 3. **En la Interfaz Gráfica**

La clase `WanbeApp` gestiona:
- `mostrar_tramite("calcomania")` → Carga toda la información
- `mostrar_checklist("calcomania")` → Muestra requisitos
- `mostrar_paso("calcomania")` → Muestra cada paso
- `cambiar_paso("calcomania", 1)` → Navega entre pasos

---

## Resumen de Tipos de Datos

```python
TRAMITES = {
    "calcomania": {              # str (clave única)
        "titulo": str,           # string visible
        "portal": str,           # string ("SAT" o "RENAP")
        "icono": str,            # string 3 letras ("CAR", "NIT", "DPI")
        "descripcion": str,      # string (1-2 oraciones)
        "requisitos": [str],     # lista de strings
        "pasos": [               # lista de diccionarios
            {
                "titulo": str,
                "texto": str,
                "items": [str],
                "enlace": str (opcional)
            },
            ...
        ]
    }
}
```

---

## Cómo Agregar o Modificar Contenido

### Para cambiar el título:
```python
"titulo": "Nuevo Título Aquí",
```

### Para agregar un requisito más:
```python
"requisitos": [
    "Placa del vehículo",
    "NIT del propietario",
    "Nuevo requisito aquí"  # ← Agregado
],
```

### Para agregar un nuevo paso:
```python
"pasos": [
    # ... pasos existentes ...
    {
        "titulo": "Nuevo Paso",
        "texto": "Descripción del nuevo paso",
        "items": ["Instrucción 1", "Instrucción 2"],
        "enlace": "https://ejemplo.com" # opcional
    }
]
```

---

## Palabras Clave en el Código

| Palabra | Significado |
|---------|------------|
| `TRAMITES` | Diccionario principal que contiene todas las guías |
| `"calcomania"` | Clave única de esta guía |
| `requisitos` | Documentos necesarios ANTES de empezar |
| `pasos` | Lista de instrucciones secuenciales |
| `enlace` | URL que abre el navegador |
| `SAT` | Superintendencia de Administración Tributaria |
| `Declaraguate` | Portal en línea del SAT |
| `SAT-4091` | Número de formulario de vehículos |

---

## Conexión con la Vista Web

En `vista_web.py`, la información se renderiza en HTML:

```python
def render_tramite(tramite_id: str):
    tramite = TRAMITES.get(tramite_id)  # Obtiene {"titulo": "...", ...}
    # Luego renderiza como HTML para el navegador
```

Los datos de la calcomanía se transmiten sin cambios entre `proyecto.py` (escritorio) y `vista_web.py` (navegador).

---

**Última actualización**: 7 de mayo de 2026  
**Autor**: Documentación del Proyecto Wanbe
