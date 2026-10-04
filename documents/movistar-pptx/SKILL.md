---
name: movistar-pptx
description: "Construye y edita exclusivamente presentaciones PowerPoint de marca Movistar a partir de la plantilla oficial: ~156 arquetipos en dos sistemas de diseño, con portadas, agenda, separadores, contenido con foto/gráfico/tabla, comparativas, timeline y cierre catalogados al detalle. Debes usarla siempre que una petición combine Movistar con PowerPoint, .pptx, presentación, deck, pitch, slides o diapositivas. Incluye convertir informes o documentos en slides Movistar y debes consultarla antes de pedir el material de origen si aún no se ha proporcionado. Elige la diapositiva que mejor encaja, clónala y rellénala. No usar para PDF, Word, HTML, redes sociales ni otros entregables que no sean una presentación. Usa `movistar-brand-guidelines` para el criterio de marca; el runtime aporta python-pptx aunque SuperStudio omita la skill prebuilt `pptx` para evitar duplicados."
model: claude-opus-4-8
license: Propietario — uso interno de SuperReal y clientes autorizados.
compatibility: "Requiere python-pptx, disponible en el runtime de SuperStudio aunque la skill prebuilt `pptx` no aparezca en la petición. soffice + PyMuPDF (`fitz`) o pdftoppm quedan para QA visual offline; no son necesarios para la entrega inicial."
metadata:
  author: SuperReal
  version: 4.0.0
  owner: SuperReal
  status: stable
  brand: movistar
---

# Movistar — PPTX: clona la diapo real que mejor encaja, rellénala

Produce una `.pptx` brand-perfect de Movistar clonando **arquetipos reales de la plantilla oficial**
(~156, en dos sistemas de diseño del cliente), no layouts abstractos. Tu trabajo tiene dos pasos:
**(1) elegir** el arquetipo que encaja con el contenido que tienes y **(2) rellenarlo**. No hace falta
"diseñar": la diapositiva ya está diseñada. Voz, copy, color, tipografía y fotografía: skill
`movistar-brand-guidelines` (siempre cargada, no se repite aquí).

**Elegir no cuesta abrir ficheros.** El §MAPA DE FAMILIAS de abajo resuelve la mayoría de los decks;
si no, le preguntas al motor (`find_slides()`, `describe()`) y él consulta el catálogo por ti.

**Keywords**: deck Movistar, presentación PowerPoint, python-pptx, mvst_pptx, arquetipos de diapo,
plantilla oficial, dos sistemas de diseño, Movistar Sans.

Idioma: **español (es-ES)**. Razonamiento interno y claves JSON en inglés.

## Dependencias

- **`python-pptx`** ya está instalado en el runtime. No busques la skill prebuilt `pptx`, no la
  importes como skill y no te detengas si no aparece entre las skills cargadas.
- **`soffice`** + **PyMuPDF (`fitz`) o `pdftoppm`** son solo para QA visual profundo offline.

## ⚡ VÍA RÁPIDA SUPERSTUDIO — entrega dentro del turno de producción

El turno completo tiene un límite duro de **20 minutos**. Para la primera entrega:

1. Lee SOLO este `SKILL.md`. Abre `references/slides-index.md` (17 KB) **únicamente si el §MAPA DE
   FAMILIAS no te resuelve el arquetipo**; **nunca** el JSON del catálogo. Si el usuario pide el
   recorrido amplio de portada+agenda+foto+gráfico+tabla+comparativas+timeline+métricas+cierre, abre
   `references/capability-recipe.md`.
2. Planifica el guion brevemente y crea **un único script Python**. Usa `set_texts()` para paneles,
   timelines y rejillas de columnas, `set_chart_data()` para el gráfico y `set_table_data()` para la
   tabla.
3. **No busques un `shape_name` en ningún sitio: `use()` los imprime** al clonar, con su rol y su
   capacidad. Rellena siguiendo ese listado y en ese mismo orden.
4. Consulta imagery una sola vez con filtros; elige una foto existente y continúa. No recorras el
   bundle ni abras imágenes una por una.
   Si el usuario dice "no investigues" o pide datos ficticios/demo, **no llames a
   `web_search`/`web_fetch`**; todo el contenido sale del prompt y de assets locales.
5. Construye una vez y llama a `save()` **una sola vez**. Sus gates de ejemplo, composición y OPC son
   el control de producción. Si un gate duro falla, haz como máximo **una corrección dirigida** y
   vuelve a guardar al mismo nombre.
6. En el turno inicial **no ejecutes** `qa_render`, soffice, screenshots ni inspección PNG diapo a
   diapo. Ese QA visual profundo pertenece a evaluación offline o a un turno posterior solicitado.
7. En una edición posterior, modifica el `.pptx`/script existente dentro del mismo container y
   conserva nombre y número de diapositivas; no reconstruyas ni reinspecciones todo el catálogo.
8. El historial puede contener metadata interna de archivos. **Nunca copies al texto visible**
   `[[generated]]`, `[[/generated]]`, `file_id`, `anthropic-file://`, rutas `/tmp`/`/mnt` ni IDs de
   container/skill. Entrega el archivo mediante la herramienta y limita la respuesta a nombre y resumen.

## ⛔ CRÍTICO — cómo se construye (no negociable)

1. **USA SIEMPRE el helper `mvst_pptx` sobre la plantilla oficial.** `new_deck()` la localiza sola en
   el fichero inyectado por Files API/container upload (fallback repo-local solo en desarrollo). Trae
   los ~156 arquetipos y **Movistar Sans real embebida**. **Si `new_deck()` lanza, DETENTE y
   repórtalo. NUNCA** construyas el deck desde cero, con `Presentation()` en blanco, ni con otra
   plantilla u otra fuente.
2. **NUNCA abras `references/slides-catalog-movistar.json`** (1,1 MB — no cabe en el turno, se lo come
   entero). Ese fichero lo lee el MOTOR, no tú. El motor te da lo que necesitas:
   - el §MAPA DE FAMILIAS de abajo resuelve la mayoría de los decks sin abrir nada;
   - si no te determina el arquetipo: (a) `find_slides(family=…, n_items=…, has_image=…)`,
     (b) `describe("NOMBRE")` para la ficha corta,
   - (c) y solo si sigues sin resolverlo, `references/slides-index.md` (17 KB, una fila por maqueta).
3. **Clona con `use()`, rellena por `shape_name`, nunca por índice**:
   ```python
   s = use(deck, "INTERIOR_TXT_1IMG")     # imprime las zonas exactas de ESTA diapositiva
   set_text(s, "Title 2", "Conectamos con lo que importa")
   ```
   `use()` duplica la diapositiva de ejemplo (nunca la edita in-place) **y te imprime su fill-spec**:
   `shape_name · rol · tipo/capacidad`, en **orden de lectura**. Rellena por esos nombres; no los
   deduzcas ni los copies de otro arquetipo. `set_text()` conserva fuente/tamaño/color del texto de
   ejemplo — **no los toques ni los pases como parámetro**, ya están bien (la mayoría heredan de
   layout/master, `GOTCHAS.md` G2).
4. **`set_page_header()` — obligatorio en CADA diapositiva de contenido con cabecera de página**
   (título/subtítulo/número, distinto de la portada): `set_page_header(s, "Título de la sección",
   subtitle="Subtítulo")`. En Movistar esto es POR DIAPOSITIVA, no una vez al final (`GOTCHAS.md`
   G8): cada página interior tiene su propio título. 18 arquetipos no tienen zona de título y la
   función lanza a propósito; el fill-spec de `use()` te lo dice antes ("sin zona de título").
5. **ANTI-VACÍO**: cada diapositiva real está diseñada para llenarse ENTERA. Si un arquetipo tiene 5
   columnas o 3 fotos, rellena TODAS — dejar una vacía se ve roto, no "minimalista". Si te sobra una
   zona, es señal de que toca **otro arquetipo** (`find_slides(family=…, n_items=…)`), no de vaciar
   una con `remove_shape()`. `verify_deck()` lo mide y avisa.
6. **Valida SIEMPRE**: `save()` elimina los arquetipos sin usar (nunca deben llegar al entregable),
   ejecuta `finalize_pptx.py` + `verify_pptx.py` (OPC; gate duro, incluye notesSlide-compartida /
   diapositivas-huérfanas / físico==lógico — `GOTCHAS.md` G5/G6) e imprime los avisos **`[deck-qa]`**
   de `verify_deck()`. Si `verify_pptx` falla → una corrección dirigida y repite una vez.
   `verify_deck(deck)` es seguro antes y después de `save()`.
7. **QA visual por render: OFFLINE, no en la primera entrega.** Ver §QA VISUAL.

## §MAPA DE FAMILIAS — empieza aquí, resuelve la mayoría de los decks

12 familias. `[C]` es el arquetipo **por defecto**: si no tienes una razón para otro, es siempre
seguro. El "eje de variante" es lo único que decides dentro de la familia.

| Familia | Qué resuelve | `[C]` por defecto | nº | Eje de variante |
|---|---|---|---:|---|
| **AVISO** | aviso de confidencialidad, la primera diapo del deck | `AVISO_CONFIDENCIALIDAD` | 1 | — |
| **PORTADA** | abrir el deck | `PORTADA_TITULO` | 26 | con/sin foto · foto a sangre, con margen o partida · color |
| **INDICE** | índice / agenda | `INDICE_SIMPLE` | 6 | nº de columnas (3 o 5) · fondo claro u oscuro |
| **SEPARADOR** | abrir capítulo o sección | `SEPARADOR_TITULO` | 42 | **color de capítulo** · con número, con una palabra o con 5 columnas |
| **TITULAR** | una idea o cifra sin foto | `TITULAR_GRANDE` | 3 | una o dos columnas de texto |
| **INTERIOR** | idea + foto: el cuerpo del deck | `INTERIOR_TXT_1IMG` | 34 | nº de fotos (0-3) · nº de columnas (2-6) · foto a la derecha, a sangre o con margen |
| **GRID** | galería o mosaico de fotos con pie | `GRID_3IMG_CAPTION` | 19 | nº de fotos (2, 3, 4, 6, 12 o 15) · con pie o mosaico limpio |
| **DATOS** | gráfica, tabla, KPI, dashboard | `DATOS_CHART_CLASICO` | 5 | gráfica · gráfica hero · dashboard de 6 · tabla · gauges de 5 KPI |
| **QUOTE** | cita o frase protagonista (máx. 1 por deck) | `QUOTE_PLANO` | 7 | con o sin foto · color de fondo |
| **COMPARATIVA** | 2 o 3 paneles enfrentados | `COMPARATIVA_2_PANEL_CLASICO` | 2 | 2 o 3 paneles |
| **TIMELINE** | cronología, roadmap, planograma | `TIMELINE_PROCESO_CLASICO` | 3 | planograma de bandas · tabla de fases · multi-hito |
| **CIERRE** | cerrar el deck | `CIERRE_M` | 8 | M sola · marca Telefónica · con título · color |

**No hay familia de listas ni de pasos**, a propósito: una enumeración va en `INDICE_*` o en un
`INTERIOR_TXT_*COL_CLASICO`; unos pasos secuenciales, en `TIMELINE_*` o `COMPARATIVA_*`.

## §DOS SISTEMAS DE DISEÑO

La plantilla trae **dos `slideMaster` oficiales del cliente**:

- **refresh** (vigente): arquetipos **sin sufijo**. Es el que ve un humano al pulsar "Nueva
  diapositiva" y **el que se usa por defecto**.
- **clásico**: arquetipos con sufijo **`_CLASICO`**. Igual de válidos y con mucha más variedad de
  rejillas, datos y comparativas — de ahí que el `[C]` de DATOS, COMPARATIVA y TIMELINE sea `_CLASICO`.

**No los mezcles en un mismo deck** salvo petición explícita: son dos lenguajes visuales distintos.
`verify_deck()` avisa si uno queda como residuo minoritario (<25%) y propone el hermano equivalente
del dominante. Un deck 50/50 es una decisión y no dispara nada.

## §CONTENT-FIRST — el embudo de 3 pasos (regla nº1)

**Paso 1 · Guion antes de arquetipos.** Reúne el contenido real y escribe, por diapositiva, la
*intención* y el *número de bloques*: «abrir», «índice de 3 capítulos», «una idea + foto», «tabla de
6 filas», «cerrar». Vocabulario cerrado y corto — nada de prosa.

**Paso 2 · Intención → FAMILIA**, con el mapa de arriba. Sin abrir ficheros. Un deck estándar es
`AVISO?` → `PORTADA` → `INDICE` → (`SEPARADOR` + 2-4 de `INTERIOR`/`TITULAR`/`DATOS`/`GRID`) × capítulos
→ `QUOTE?` → `CIERRE`.

**Paso 3 · Dentro de la familia, dos preguntas y ya está determinado**: (a) ¿cuántos bloques
repetidos necesito? → es el `n_items`; (b) ¿de qué color va este capítulo? → es la variante. Si aun
así queda ambiguo, **UNA** llamada: `find_slides(family="INTERIOR", n_items=3, has_image=True)`. Si no
tienes preferencia, el `[C]` es siempre seguro.

Además: abre cada bloque temático con un `SEPARADOR_*` y **mantén un color por capítulo**
(`verify_deck()` avisa si repites color entre capítulos o te sales del sistema declarado en
`assets/brand-config.json`). Evita que una misma **maqueta** domine el deck: `verify_deck()` lo mide
sobre la composición física, no sobre el nombre, así que usar seis nombres distintos que se ven igual
no cuela. Criterio de composición: `references/design-principles.md`.

**Nº de diapositivas: lo decide el contenido**, no una cifra fija.

## Patrón de construcción

```python
import sys, glob
_c = (glob.glob("/skills/**/movistar-pptx*/scripts", recursive=True)
      or glob.glob("/mnt/skills/**/movistar-pptx*/scripts", recursive=True)
      or glob.glob("/**/movistar-pptx*/scripts", recursive=True))
sys.path.insert(0, _c[0])
from mvst_pptx import (new_deck, use, set_text, set_texts, set_image, set_page_header,
                       set_chart_data, set_table_data, save, list_brand_images,
                       confirm_example_text, find_slides, describe, fill_spec, families)

deck = new_deck()                       # NUNCA Presentation() en blanco.

s = use(deck, "PORTADA_TITULO")         # -> imprime: Text Placeholder 1 (title, ≤34) …
set_text(s, "Text Placeholder 1", "Conectamos lo que importa")
set_text(s, "Text Placeholder 2", "Plan de marca 2026")

s = use(deck, "INDICE_SIMPLE")
set_text(s, "Text Placeholder 3", "Índice")
set_text(s, "Text Placeholder 1", "1.\n2.\n3.")
confirm_example_text(s, "Text Placeholder 1")   # el valor real coincide con el ejemplo (G13)
set_text(s, "Text Placeholder 2", "Orígenes\nPropuesta\nPróximos pasos")

s = use(deck, "SEPARADOR_NUMERO_06_AZUL")       # capítulo 01 -> AZUL
set_text(s, "Title 1", "Orígenes")
set_text(s, "Text Placeholder 3", "01")

s = use(deck, "INTERIOR_TXT_1IMG")
set_page_header(s, "Antes de Movistar había Telefónica", subtitle="De 1924 a 1994")
set_text(s, "Text Placeholder 4", "Párrafo real, dentro de la capacidad que imprime use().")
fotos = [r["path"] for r in list_brand_images(with_meta=True)
         if r["exists"] and r["categoria"] != "fondo"]
if not fotos:
    raise RuntimeError("No hay imagery Movistar montado; elige un arquetipo sin foto")
set_image(s, "Content Placeholder 8", fotos[0])

use(deck, "CIERRE_M")
save(deck, "plan-marca-2026.pptx")      # gates + finalize + verify
```

## §IMÁGENES

Las fotos que trae la plantilla son de ejemplo o **semilla del build**, no banco reutilizable: se
sustituyen SIEMPRE con `list_brand_images()` (nunca construyas la ruta a mano; resuelve el bundle
inyectado por `container_upload` y devuelve solo rutas que existen). **12 de sus 35 entradas son
`categoria: "fondo"`** — fondos de color plano con el claim de marca, no fotografía: fíltralas.
`set_image()` recorta en vez de estirar (crop-to-fill) y avisa si el recorte pasa del 30% de un lado;
funciona igual sobre un hueco ya poblado, uno vacío o uno maquetado como forma. `list_brand_images(
with_meta=True)` da categoría/tags/mood/`momento_dia` para elegir con criterio — mismo algoritmo que
`movistar-brand-guidelines/imagery/imagery-guide.md`. Si no hay match decente, usa un arquetipo SIN
foto: mejor sin foto que con una foto que no dice nada. Composición y dirección de arte (scrim, 1
logo por pieza, M siempre azul): `movistar-brand-guidelines/brand/photography-style.md`.

## §QA VISUAL

Checklist completo en **`references/qa-visual-checklist.md`** (qué mirar, los 7 fallos automáticos de
marca, y los dos artefactos del renderizador que no son defectos del fichero). **No lo ejecutes en la
primera entrega de SuperStudio**: en el turno inicial el control de calidad son los gates de `save()`
y los avisos `[deck-qa]`.

## Nota de fuentes

La plantilla embebe **Movistar Sans real** (EOT), la fuente oficial que ya usan los runs del cliente.
No cambies la fuente de un run al rellenarlo: `set_text()` la conserva. Detalle en `GOTCHAS.md` G1
(sufijo "TT" del nombre de familia) y G19 (la plantilla anterior de producción embebía Calibri
etiquetado como Movistar Sans).

## §OUTPUT

Respuesta final: una línea `OUTPUT_FILE: <kebab-case>.pptx` + resumen ≤4 líneas (nº diapositivas,
arquetipos usados, qa_flags). Guarda y valida ANTES de resumir.

## §FICHEROS

- `scripts/mvst_pptx.py` — el motor. **Úsalo siempre.**
  - Consulta: `families()`, **`find_slides()`**, `describe()`, `fill_spec()`, `slide_names()`.
  - Construcción: `new_deck()`, **`use()`**, `set_text()`/`set_texts()`, `set_image()`,
    `set_page_header()`, `set_chart_data()`/`set_charts_data()`, `set_table_data()`, `save()`.
  - Escapes: `remove_shape()`, `confirm_example_text()` (acepta `"*"`), `confirm_example_image()`.
  - QA: `verify_deck()`. Imagery: `list_brand_images()`. Salida: `outputs_dir()`.
  - Último recurso: `content_rect(slide)` da el rectángulo libre bajo la cabecera para
    `slide.shapes.add_table()`/`add_chart()` nativos. **Evítalo para gráficas**: una `add_chart()`
    sobre un rectángulo vacío sale con la paleta por defecto de Office, no la de Movistar (ver
    `GOTCHAS.md` G22). Busca antes un arquetipo con la gráfica ya compuesta.
- `references/slides-index.md` — **autogenerado**: una fila por maqueta, con sus variantes, zonas y
  sistema. El atajo cuando el §MAPA DE FAMILIAS no te basta (17 KB).
- `references/capability-recipe.md` — receta compacta con arquetipos y `shape_name` ya validados para
  un deck que demuestra todas las capacidades. Hay una versión por sistema.
- `references/qa-visual-checklist.md` — el QA por render (offline).
- `references/design-principles.md` · `references/naming-grammar.md` · `references/GOTCHAS.md` —
  criterio de composición, gramática de los nombres de arquetipo, y bugs conocidos.
- `references/slides-catalog-movistar.json` — catálogo completo (1,1 MB). **Lo lee el motor, no tú.**
- `references/deck-source-analysis.md` — diagnóstico de las dos plantillas del cliente y cómo se
  seleccionaron los arquetipos.
- `assets/brand-config.json` — paleta, sistema de color de capítulos y `qa_gates` (fuente única de
  los umbrales deterministas que lee el motor).
- `assets/template/movistar.pptx` — la plantilla. **No viaja en el `.zip`** (excluida vía
  `.skillignore`): se inyecta vía Files API/`container_upload` y `new_deck()` la localiza.

## Relación con otras skills

Un **deck** usa `movistar-brand-guidelines` (criterio de marca — voz, copy, color, tipografía,
fotografía) + `movistar-pptx` (este: arquetipos + mecánica). El runtime aporta python-pptx; la
prebuilt `pptx` puede estar filtrada y no debe buscarse. Cualquier otro output usa solo la skill de
marca.
