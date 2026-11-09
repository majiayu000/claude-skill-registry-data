---
name: cerebro-mockup-design
description: >
  Design system y principios visuales para mockups HTML del proyecto.
  Prohíbe emojis, define tokens, iconos SVG, y anti-patrones de diseño "AI-generated".
  Trigger: Cuando el usuario pide crear o mejorar un HTML, mockup, prototipo, o diseño visual de una
  pantalla del producto hecho a mano. Si el diseño se genera en Stitch (disenar-con-stitch), esta skill
  fija el design system y revisa la exportación. No cubre diagramas técnicos: eso es la skill archify.
license: Apache-2.0
metadata:
  author: equipo
  version: "2.0"
---

## Cuándo se usa

SIEMPRE que generes o modifiques una **pantalla o prototipo del producto** (HTML/CSS de interfaz, o la
exportación de Stitch que se revisa). NO se carga para HTML que no es interfaz del producto: informes,
documentación generada (`bin/generar-documentacion.py`, `bin/generar-informe.py`) ni diagramas de `archify`.

## El alma de esta pantalla (LEER PRIMERO)

> ⚠ **Sección a completar por el proyecto** en `cerebro-digital/diseno/diseno-sistema.md` y acá.
> Es lo que condiciona TODO lo visual, y no se adivina: se describe a partir de las pantallas
> reales del producto o del mockup de referencia que entregue el funcional.

Para completarla, contestar:

- **¿Quién la usa y cuánto tiempo?** (operadores ocho horas por día · clientes ocasionales · gerencia). Determina densidad y tamaño de letra.
- **¿Utilitaria o comercial?** Una herramienta operativa es plana, densa y gris; un producto de cara al público admite más aire y color.
- **¿Qué color manda de verdad?** En casi toda app de gestión el color más usado es el **gris de texto**, no el de marca. El de marca aparece como acento.
- **Color = significado.** Rojo/verde/amarillo se reservan para estados reales. Nunca decorativos.
- **Qué formas usa el producto:** botones pill o rectos, radios de inputs y cards, si hay sombras.

Frase resumen (a escribir): *"<formulario/tablero … serio, … discreto, toques puntuales de color solo para alertas y estados, botones …, todo plano>"*.

## Referencia visual

El archivo `entregables/disenos/<mockup-de-referencia>.html` es la implementación de referencia
(⚠ a definir: el primer mockup validado por el funcional). Seguí ese estilo como punto de partida
para cualquier nuevo mockup. Mientras no exista, se pregunta antes de inventar un estilo.

## Dónde se guarda

Todo mockup nuevo o en iteración se escribe en `borrador/disenos/` — **nunca directo en
`entregables/disenos/`**. Solo se copia a `entregables/disenos/` cuando el usuario pide
explícitamente promoverlo (ej: "metelo en funcional"), nunca por iniciativa propia.

## Design System — Tokens

Usá SIEMPRE estas variables CSS. **No inventes colores nuevos y nunca escribas un valor
hexadecimal a mano fuera de `:root`**: si una pantalla necesita un color que no está, se agrega
el token acá y en `diseno-sistema.md`, con un "sí" del equipo.

### Paleta por orden de peso visual real (de más a menos frecuente)

```css
/* 1° — Gris de texto principal (el color más usado en toda la app) */
--text-color:  <hex>;

/* 2° — Color de marca claro (fondos suaves, hover, resaltados) */
--brand-soft:  <hex>;

/* 3° — Blancos y grises de superficie */
--surface-0:   #ffffff;
--surface-100: <hex>;

/* 4° — Color de marca oscuro (acento puntual: botón primario, borde activo) */
--brand-900:   <hex>;   /* color primario real del producto */
--brand-800:   <hex>;   /* hover del primario */

/* 5° — Grises secundarios y bordes */
--neutral-500: <hex>;   /* texto secundario */
--neutral-200: <hex>;   /* bordes de inputs y tablas */
--neutral-300: <hex>;   /* divisores */

/* 6° al 10° — Estados semánticos (usar SOLO para estados reales, nunca decorativos) */
--red-600:     <hex>;   /* error / botón danger */
--green-600:   <hex>;   /* éxito */
--yellow-600:  <hex>;   /* advertencia */
--orange-600:  <hex>;   /* advertencia fuerte */

/* Acento especial — ítem seleccionado/activo en listas de estado (si el producto lo tiene) */
--accent-selected: <hex>;

/* Fondos semánticos auxiliares */
--red-100:     <hex>;
--green-100:   <hex>;
--yellow-100:  <hex>;
--brand-100:   <hex>;   /* fondo suave de marca */
--brand-50:    <hex>;   /* hover de fila */

/* Neutros de soporte */
--neutral-900: <hex>;
--neutral-800: <hex>;   /* fondo de sidebar */
--neutral-700: <hex>;
--neutral-600: <hex>;
--neutral-400: <hex>;
--neutral-100: <hex>;
--neutral-50:  <hex>;
--white:       #ffffff;
```

> Los `<hex>` se completan desde las pantallas reales del producto, ordenados por frecuencia de
> uso (los primeros sostienen la interfaz; los últimos son acentos). El documento descriptivo es
> `cerebro-digital/diseno/diseno-sistema.md`; este SKILL es el prescriptivo y los dos tienen que
> decir lo mismo.

### Tipografía

```css
--font: '<tipografía del producto>', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'SF Mono', 'Fira Code', 'Cascadia Code', Consolas, monospace;
```

### Sombras y radios

```css
--shadow-float: 0px 2px 12px rgba(0,0,0,.12);  /* SOLO para overlays flotantes */
--radius-sm:  4px;
--radius-md:  6px;
--radius-lg:  8px;   /* inputs, cards, paneles */
--radius-pill: 999px; /* botones y switches, si el producto usa pill */
--radius-circle: 50%; /* íconos de acción circulares */
```

## Reglas de diseño (MANDATORIAS)

### 1. NADA DE EMOJIS
- **PROHIBIDO** usar emojis como íconos (📞 👤 📍 💬 🔒 ❌ ⚙️ etc.)
- Usá **SVGs inline** (estilo Heroicons, 16-20px, stroke-width 1.5, currentColor)
- Si no tenés el ícono exacto, usá un genérico equivalente — no intentar recrear SVGs custom de dominio.

> ⚠ **Lo que sigue (2 a 8) describe el alma visual del producto de origen** y vale como punto de partida:
> el proyecto nuevo lo confirma o lo reemplaza con su propio mockup antes de darlo por obligatorio.

### 2. Sidebar con gris oscuro, NO el color de marca
- La sidebar va con `background: var(--neutral-800)` y texto blanco.
- El color de marca (`--brand-900`) se usa en: botones primarios, active states, links, tab activo.
- **NO uses el color de marca en fondos grandes.** Usalo con moderación — 1 o 2 elementos de foco por pantalla.

### 3. Jerarquía tipográfica (sin H1-H6 elaborados — es una app de formularios/tablas)
```
título de card  → 1.5rem (24px), 700, --neutral-900
encabezado panel → 0.875rem (14px), 600, --neutral-800
body/tabla       → 0.875rem (14px), 400, --text-color
label/columna    → 0.75rem (12px), 600, uppercase, --neutral-500
small/timestamp  → 0.75rem (12px), 400, --neutral-500
```
**Nunca** usar títulos ≥ 2rem — no es el lenguaje visual de una app de gestión.
El color de texto por defecto **no es negro puro**: es el gris de `--text-color`.

### 4. Espaciado compacto (pasos de 0.5rem)
- Padding de paneles: `~0.5rem`
- Padding de cards: `~1.25rem`
- Gap entre fields: `8px`
- **No dejar mucho espacio en blanco** — la densidad de información es parte del carácter de una app operativa.

### 5. Bordes, radios y formas
- **Botones y switches**: `border-radius: var(--radius-pill)` (o el radio que fije el producto), siempre igual.
- **Inputs, cards y paneles**: `border-radius: var(--radius-lg)` (8px) — moderado.
- **Íconos de acción solos**: `border-radius: var(--radius-circle)` — completamente circulares.
- **Filas de listas/menús desplegables**: `border-radius: 0` — rectas.
- Borde de cards: `1px solid var(--neutral-200)`.

### 6. Sombras — solo en elementos flotantes
- **NO** usar `box-shadow` en cards, paneles, botones ni contenido estático. El diseño es plano.
- **SÍ** usar `var(--shadow-float)` únicamente en: dropdowns abiertos, autocomplete, calendarios, menús contextuales.

### 7. Layout — no hay sidebar como patrón dominante
- El layout típico es **barra/toolbar superior + paneles apilados verticalmente**.
- La sidebar de navegación existe pero no es el patrón central de todas las pantallas.
- Uso frecuente de **tablas/listados** — es una app de gestión, no de tarjetas.

### 8. Botones
- Tamaño por defecto: **small** (`padding: 0.5rem 1rem`).
- Borde: `1px solid`, sólido (no grueso). Sin sombra.
- Peso de fuente: **500 (medium)**.
- El botón por defecto en la mayoría de pantallas es **neutro/secundario** (gris/marca suave), no saturado.
- El color de marca fuerte se reserva para **la acción primaria puntual** de cada pantalla, no se repite.
- Hover: oscurecer/saturar levemente el fondo.

### 9. Iconografía
- Íconos genéricos: check, X, buscar, flechas, teléfono, +/-, copiar, guardar.
- **Color de ícono por defecto**: `var(--text-color)` para acciones genéricas.
- Rojo/verde/amarillo en íconos **solo** cuando representan un estado real (alerta, éxito, advertencia).
- No intentar clonar paleta de color a partir de los íconos de dominio — usan color por contexto/props.

### 10. Ítem seleccionado/activo en listas de estado
- Usar `background: var(--accent-selected)` con texto blanco para el ítem de estado activo seleccionado, si el producto tiene ese acento.
- Es un acento distintivo del sistema, no un color de error.

### 11. Componentes con naming BEM
```
.card__header, .card__body, .card__field, .card__input
.btn--primary, .btn--secondary, .btn--outline
.panel-<nombre>__title, .panel-<nombre>__row, .panel-<nombre>__field
.sidebar__item, .sidebar__item--active
```

### 12. Estados interactivos (hacé que se vea clickeable aunque sea mockup)
- `transition: 150ms cubic-bezier(0.4, 0, 0.2, 1)` en todos los elementos interactivos.
- Hover en botones: darken 10%.
- Hover en filas de tabla: `background: var(--brand-50)`.
- Hover en sidebar items: `background: rgba(255,255,255,0.06)`, texto blanco.

### 13. Badges FAKE / Sin regla
Usá esta estructura, NUNCA con `::after` o posicionamiento absoluto:
```html
<span class="badge badge--red">FAKE</span>
<span class="badge badge--yellow">Sin regla</span>
```
Todo control que no tenga una regla `[RN-…]` que lo respalde lleva el badge: es lo que después
revisa `cerebro-architect-ui`.

## Anti-patrones (lo que NO hay que hacer)

| Anti-patrón | Por qué |
|-------------|---------|
| Emojis en lugar de iconos | Parece PPT, no sistema enterprise |
| Sidebar con el color de marca sólido | Satura, cansa la vista |
| Color de marca oscuro como fondo dominante | Es acento puntual, no color de superficie |
| Tipografía ≥ 2rem o jerarquía tipo landing | Esta app no tiene esa jerarquía |
| Sombras en cards/paneles/botones | El diseño real es plano — solo overlays flotantes |
| Texto negro puro (#000 o #111) como color de body | El real es el gris de `--text-color` |
| Paleta de colores elaborada "por estado de caso" | No existe en el sistema; usar semántica genérica |
| Intentar replicar color exacto de íconos de dominio | Generaría paleta infinita e inconsistente |
| Un hexadecimal escrito a mano fuera de `:root` | Rompe el design system; se agrega el token o se pregunta |
| Esquinas que no respetan el radio del producto | Inconsistencia inmediata con las pantallas reales |
| Inline styles mezclados con CSS vars | Inconsistencia, difícil de mantener |
| Badges con `position: absolute` o `::after` | Rompen el layout |
| Sin hover states en tablas/botones | No hay feedback visual |

## Proceso para generar un mockup nuevo

1. Cargá este skill (`cerebro-mockup-design`)
2. Leé `contexto.md` del OKF para entender el dominio, y la ficha funcional de la pantalla
3. Internalizá el "alma" de la sección superior antes de escribir una línea de CSS (si está sin completar, preguntá)
4. Usá el HTML de referencia (`<mockup-de-referencia>.html`) como base visual
5. Aplicá los tokens en orden de peso visual: primero gris, luego marca suave, luego marca oscura puntual
6. Reservá rojo/verde/amarillo/acento únicamente para estados reales
7. NO uses emojis, NO inventes colores, NO pongas sombras en contenido estático
8. Marcá con badge todo control sin regla que lo respalde
9. Guardá el resultado en `borrador/disenos/` — recién se mueve a `entregables/disenos/` si el usuario lo pide explícitamente
