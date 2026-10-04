---
name: movistar-brand-guidelines
description: "Experiencia de marca Movistar — voz y tono, 19 principios de copywriting, color PLANO (sin degradados) con paleta `.ase` y reglas WCAG, tipografía Movistar Sans, logo (solo la \"M\"), banco de fotografía por momento del día y sistema de comunicación LOVE/CHOOSE/BUY. Aplica a CUALQUIER output con identidad Movistar: copy, titulares, claims, emails, contenido para redes, documentos, informes, textos de web/UI, guiones y presentaciones. Úsala siempre que la marca sea Movistar (aunque la petición no mencione un formato de archivo), salvo que el usuario pida explícitamente NO seguir la guía de marca. Movistar brand voice, copywriting, flat color palette, Movistar Sans typography, the \"M\" logo and brand photography for any Movistar-branded deliverable."
model: claude-opus-4-8
license: Propietario — uso interno de SuperReal y clientes autorizados.
compatibility: "El criterio de marca no requiere entorno especial. Para artifacts HTML/React el QA determinista (scripts/lint_artifact.py) es Python puro sin dependencias. Para generar un PDF usa el entorno de la skill prebuilt `pdf` (reportlab/pypdf/pdfplumber, ya preinstalados); opcional pdftoppm o PyMuPDF para scripts/qa_render_pdf.py (QA por visión) y un extractor de texto para scripts/lint_pdf.py; si faltan, degradan sin bloquear."
metadata:
  author: SuperReal
  version: 1.0.4
  owner: SuperReal
  status: stable
  brand: movistar
---

# Movistar Brand Guidelines

Proporciona el criterio de marca Movistar para que cualquier output suene y se vea como Movistar: voz, copy, color, tipografía, logo, fotografía y accesibilidad.

**Keywords**: voz de marca, tono, copywriting, paleta de colores, tipografía, Movistar Sans, logo, la M, fotografía de marca, identidad visual, brand guidelines, guía de estilo, LOVE CHOOSE BUY, accesibilidad WCAG.

Idioma de todo el contenido visible al usuario: **español (es-ES)**. Razonamiento interno y claves técnicas en inglés.

## Cuándo aplicar

Antes de producir **cualquier** output de marca Movistar — un email, un post, un titular, un documento, un informe, un texto de web/app o una presentación. Esta skill da el criterio de marca; no genera ficheros por sí misma (eso lo hacen la skill `pptx` para decks y la skill `movistar-pptx` para el criterio de deck).

**Única excepción:** si el usuario pide explícitamente NO seguir la guía de marca, respétalo.

## ⛔ Reglas que más se incumplen (fallos automáticos)
Antes de dar por bueno un output, comprueba que NO incurre en:
1. **Em-dash "—"** en el copy (usa comas, dos puntos o frases cortas).
2. **"M" de Movistar en minúscula**, o **titular con punto final**.
3. **Tipografía distinta de Movistar Sans** en pieza de marca.
4. **Logo recoloreado**: la M va en **Azul Movistar `#0066FF`**; blanca solo sobre fondo Azul Movistar o foto azulada legible.
5. **Blanco puro `#FFFFFF` o negro puro `#000000`** en vez de **Blanco Movistar `#FFFAF5`** / **Negro Movistar `#262423`**.
6. **Combinación "Prohibido"** de la matriz (secundario claro sobre fondo claro) o **contraste < WCAG** (ver `brand/contrast-matrix.md`).
7. **Contenedor destacado en Blanco Movistar** (no genera contraste).
8. **Texto sobre fotografía sin zona de contraste o scrim.**
9. **Contenido visible en idioma ≠ es-ES** (salvo petición explícita).
10. En decks `.pptx`, **añadir la M manualmente** cuando el master ya la aplica.
11. Si el usuario dice **"no investigues"**, aporta datos de demo o pide contenido ficticio,
    **no llames a `web_search`/`web_fetch`**: usa solo el prompt, adjuntos y assets locales.

## Esenciales de marca (referencia rápida)

Para outputs simples basta con esto; para decisiones finas, lee los ficheros de `brand/` (ver §Referencias incluidas).

### Paleta
- **Azul Movistar `#0066FF`** — presente en toda comunicación.
- **Blanco Movistar `#FFFAF5`** — NO blanco puro.
- **Negro Movistar `#262423`** — NO negro puro.
- **Secundarios** (azul claro `#D3EEFF`, verde claro `#CEF7BF`, amarillo claro `#FFE99C`, coral claro `#FFC5A8`) — acentos por sección/capítulo.
- **Distribución cromática objetivo**: ~40% azul · 30% blanco · 10% negro · 20% secundarios.
- **Mapa capítulo → color**: 01 azul · 02 verde · 03 amarillo · 04 negro.
- Detalle, casos de uso, semánticos y best practices: `brand/color-palette.md` §4.

### Voz y tono
- Cercana, optimista, clara y humana; nunca corporativa fría ni grandilocuente.
- "Hablamos como personas que cuidan de personas": habla de beneficios para la persona, no de specs por las specs.
- La "M" de Movistar siempre en mayúscula; hablamos en primera persona del plural y te tuteamos.
- Detalle (plataforma de marca + tono + matices por contexto): `brand/copywriting.md` §1.1 y §1.2.

### Copy — reglas que más se incumplen
- **Sin em-dashes** ("—"). Usa comas, dos puntos o frases cortas.
- Una idea central por pieza; titulares cortos y concretos; titulares sin punto final.
- Beneficio antes que característica; escenas cotidianas, no tecnológicas.
- Lenguaje inclusivo y directo; evita tecnicismos innecesarios.
- Precios, símbolos (`45€`, `5 GB`, `300Mb`) y modalidades con el sistema de la guía (no inventes formatos).
- Las reglas completas: **19 principios rectores** (`brand/copywriting.md` §1.3) + **9 principios de copywriting** (§1.2). Validación de copy: §1.1.

### Tipografía
- La marca usa **Movistar Sans**. No sustituir por otras fuentes en piezas de marca.
- **En este agente el runtime inyecta la fuente automáticamente en los artifacts web**: escribe solo `font-family: 'Movistar Sans'` en tu CSS y **NO** pegues `@font-face` ni el base64 de la fuente (ralentiza y puede cortar el stream).
- **Artifacts autocontenidos**: un artifact web debe funcionar sin red (CSP estricta) — todo **inline** (CSS y JS), **sin CDN, fuentes ni imágenes externas**. La fuente la inyecta el runtime; para imágenes usa SVG inline o data URIs (el banco de fotos NO se puede incrustar, ver §Fotografía).
- **Si el entorno NO inyecta la fuente** (HTML standalone, PDF): enlaza el fichero bundleado por ruta. Para PDF con WeasyPrint usa `@font-face { src: url('file:///skills/movistar-brand-guidelines/assets/fonts/MovistarSans-Variable.woff2'); }`. El `.woff` queda de fallback. Nunca pegues el base64 en el output visible.
- **Formatos bundleados**: variable en `assets/fonts/MovistarSans-Variable.woff2/.woff`; estáticos por peso en `assets/fonts/web/` (woff2+woff), `assets/fonts/ttf/` (PPTX/escritorio/PDF) y `assets/fonts/otf/` (impresión). Pesos: Light, Regular, Medium, Bold, Extrabold (+ itálicas).
- Jerarquía headline/subhead/cuerpo según `brand/typography.md` §3 y `brand/layout-grid.md` §7.3–7.4.

### Logo (la "M")
- **La M es el identificador por defecto** (SVG en `assets/logo/`: `movistar-m-blue.svg` azul sobre fondo claro, `movistar-m-white.svg` blanco sobre fondo oscuro/foto, `movistar-m.svg` monocromo/neutro).
- **En artifacts web (HTML/React), dos niveles, en este orden:** (1) **preferente** — emite `<img src="movistar://logo-m-blue">` (o `-white`/`-mono`); el backend resuelve el `movistar://<id>` a una URL de blob firmada, igual que el banco de fotos (Movistar es company propia → prefijo `movistar://`). Coste de tokens casi nulo. (2) **fallback** (si esa resolución no aplica en tu contexto) — incrusta el SVG **limpio** de `assets/logo/` con el patrón `<symbol id="mvst-m">…</symbol>` + `<use href="#mvst-m">`, para no duplicar el `<path>` completo cada vez que aparece la M. En email/documentos/`.docx` incrusta el SVG inline directamente. Ver `brand/logo.md` y `brand/artifact-qa.md`.
- **Wordmark y lockups — SOLO para casos especiales** (patrocinios, photocalls/entornos multimarca, merchandising; ver `brand/logo.md` §2.1.4–2.1.5): `assets/logo/wordmark/` (**solo la palabra "movistar", SIN la M**: 8 formas = 8 letras, verificado sobre los SVG), `assets/logo/lockup-horizontal/` y `assets/logo/lockup-vertical/` (**M + wordmark**: 9 formas), cada uno en variante `-blue`/`-white`/`-mono`. **No los uses por defecto** — si dudas entre la M sola y un lockup, usa la M sola.
- La M va siempre en Azul Movistar; en blanco solo sobre fondo Azul Movistar (o foto azulada que garantice legibilidad).
- Posición por defecto: arriba a la derecha; respeta el área de protección. No deformar ni recolorear fuera de la guía. En decks `.pptx` **NO** lo añadas manualmente (el master ya lo aplica).
- Reglas y prioridades de color: `brand/logo.md` §2. "Emes expresivas": `brand/expressive-m.md` §9.

### Accesibilidad (WCAG)
- Garantiza contraste suficiente texto/fondo; nunca texto sobre foto sin zona de contraste o scrim.
- Matriz de contraste por combinación y colores semánticos: `brand/contrast-matrix.md`.

### Fotografía de marca
- **Tú (el modelo) decides cuándo una foto de marca mejora el output y cuál**, usando el banco curado y el algoritmo de `imagery/imagery-guide.md` (+ catálogo `imagery/imagery-index.json`). Aplica a portadas, separadores, fondos, acompañamiento, hero, etc.
- El banco tiene **81 imágenes**: set temático (23) + **46 fotos oficiales Movistar 2025** organizadas por **momento del día** (`manana/mediodia/tarde/atardecer/noche/general`) + **12 fondos de color plano** (`categoria: "fondo"`, ver punto aparte abajo). Filtra por `momento_dia` + `categoria` + `tags` + `mood`.
- **Excepción — en decks `.pptx` manda `movistar-pptx`**: si esa skill da reglas de imagen/variedad/colocación, prevalecen sobre esta sección.
- **En `.pptx`/PDF**: localiza el fichero siempre con `list_brand_images()` de `movistar-pptx` (nunca construyas la ruta a mano) — vive en el sandbox, bundle inyectado por `container_upload` o bundleado en la skill.
- **En artifacts web (HTML/React)**: NO incrustes el binario (CSP/offline) — en su lugar emite la referencia `movistar://<id>` (el `id` es el de `imagery-index.json`); el backend la resuelve a una URL de blob firmada antes de servir el artifact al usuario. Si por lo que sea esa resolución no aplica en tu contexto, prioriza copy/paleta/logo/tipografía sin foto.
- El campo `source_file` de cada entrada del índice es su ruta relativa a `imagery/assets/imagery/` (no una ruta garantizada en todos los formatos — en `.pptx` resuélvela siempre vía `list_brand_images()`).
- **`categoria: "fondo"`** (12 entradas, en `imagery/assets/imagery/fondos/`) — fondos de color plano con el lockup y el claim fijo **"es por todos."**, uno por color de marca (blanco/azul/azul-claro/coral/verde/amarillo, centrado/horizontal). **Uso muy acotado**: solo cuando ese claim encaje literalmente con el mensaje de la pieza (employer branding/cultura interna) — **nunca como fondo genérico**; respeta siempre `usos_evitar`/`reglas`/`notas` de cada entrada antes de elegir una. ⚠️ El fondo "azul" de este set es `#3a66fb`, ligeramente distinto del Azul Movistar oficial (`#0066FF`) — no lo uses como referencia de color.
- Nunca fabriques imágenes ni uses fotos fuera de marca.

## Flujo de revisión de marca (validation loop)

1. Redacta el output (copy/diseño) con los esenciales de arriba.
2. Revísalo contra las reglas: paleta y distribución, tono, principios de copy, tipografía, logo/área de protección, contraste WCAG.
3. Si hay incumplimientos, anótalos con referencia al fichero de `brand/` correspondiente y corrige.
4. Repite hasta que todo cumpla. En caso de duda, **gana el Brand Guardian v4** (los ficheros de `brand/`, spec autoritativa 2026-06-08).

## Revisión final de composición y estructura (obligatoria, antes de dar CUALQUIER output por terminado)

Un output puede cumplir todas las reglas de marca (color, tono, logo, tipografía) y aun así fallar
si la **composición** está rota: secciones que se solapan, un título pisando una foto, bloques de
texto encima de otros, poco aire entre elementos. Esta revisión es **aparte** de la de marca de
arriba — no la sustituye, la complementa. No des ningún output por terminado sin pasar por ella.

**Por qué existe esta regla:** feedback real de producción (2026-07) — un output en `_pre` cumplía
la marca pero tenía varias secciones solapadas con fotos y títulos. Al pedir explícitamente "mejora
la composición, corrige los solapamientos" el resultado fue muy bueno en el siguiente turno. La
lección: el modelo sabe corregir estos problemas cuando se le pide — el fallo es no revisarlos por
su cuenta la primera vez. Esta sección fuerza ese paso en vez de esperar a que el usuario lo pida dos veces.

### Checklist general (todos los formatos)
1. ¿Algún bloque de texto se superpone con otro bloque de texto, una foto o un elemento gráfico?
2. ¿Hay aire suficiente entre título, foto y cuerpo (nada "pegado" ni cortado)?
3. ¿Cada sección/columna tiene su propio espacio, sin invadir el de la siguiente?
4. ¿El logo o cualquier elemento fijo (breadcrumb, footer) queda tapado por otro elemento?

### QA determinista para artifacts HTML/React (obligatorio — con linter, no simulando a mano)

Un artifact HTML/React **no se renderiza dentro de tu sandbox** (se renderiza después, en el
navegador del usuario, vía `artifact-flow`), así que no tienes captura del resultado. Pero SÍ tienes
un **gate mecánico**: `scripts/lint_artifact.py`, un analizador estático (Python puro, sin
dependencias, corre en el sandbox `code_execution`) que aplica las reglas de marca y composición de
Movistar sobre el HTML/CSS final. No sustituye tu criterio: lo hace determinista.

**Flujo obligatorio:**

1. **Compón desde bloques ya validados.** Parte de `assets/html/patterns.html` (+ sus clases en
   `assets/html/brand-tokens.css`): hero, tarjeta, sección, badge y uso de logo con los pares de
   contraste, la tipografía y el color plano ya resueltos. No inventes combinaciones de color/fondo
   desde cero — reutiliza las clases de `brand-tokens.css` (evita la mayoría de los FAIL de entrada).
2. **Ejecuta el linter** sobre el fichero generado y corrige **todos** los FAIL, repitiendo hasta 0:
   ```
   python3 scripts/lint_artifact.py mi-artifact.html
   ```
   Detecta de forma determinista: degradados (Movistar es color plano → FAIL), em-dash "—", "movistar"
   en minúscula, blanco/negro puros, combinaciones "Prohibido" de contraste (claro sobre claro),
   contraste WCAG bajo, tipografía distinta de Movistar Sans, `@font-face` base64 pegado (ver
   §Tipografía — en Movistar es un FAIL, el runtime ya inyecta la fuente), imagen sin dimensiones,
   texto sobre foto sin scrim, `position:absolute` sin ancestro `relative`, clase usada sin definir,
   color fuera de paleta y titular acabado en punto.
3. **Cada WARN que decidas dejar**, justifícalo en la tabla de auto-verificación de
   `brand/artifact-qa.md` — no lo ignores en silencio.
4. **Revisa además la composición** con el checklist general de arriba (solapamientos, aire entre
   bloques, secciones que invaden a la siguiente) — el linter cubre lo mecánico, no sustituye tu
   lectura de la maqueta (bloques absolutos, grids sin `flex-wrap`, alturas fijas que desbordan).

El catálogo de anti-patrones (código incorrecto vs correcto, uno por regla) y la tabla de
auto-verificación están en **`brand/artifact-qa.md`** — léelo antes de tu primer artifact de Movistar.

Para decks `.pptx`, `movistar-pptx` hace su propio QA por visión (render real a PNG con `qa_render.py`)
— no lo dupliques aquí, pero tampoco te lo saltes si generas un deck sin pasar por esa skill.

## Sistema de marca por comm_type (LOVE / CHOOSE / BUY)

Movistar adapta la aplicación del sistema según el tipo de comunicación:
- **LOVE** — marca/emocional (máxima libertad y expresividad) · **CHOOSE** — consideración (beneficios elevados, sin precio) · **BUY** — conversión/precio (sistema rígido, CTAs y contenedores).
Cómo cambia layout, peso del precio y rol de la M en cada uno: `brand/system-application.md` §8 y `brand/expressive-m.md` §9.

## Referencias incluidas (leer bajo demanda)

- **`brand/`** — Brand Guardian v4 (spec autoritativa, 2026-06-08), dividido por tema (léelos bajo demanda, no todos a la vez):
  - `copywriting.md` §1 — plataforma de marca, tono, 19 principios de copywriting.
  - `logo.md` §2 — la "M", versiones de color, área de protección.
  - `typography.md` §3 — Movistar Sans, pesos, variable.
  - `color-palette.md` §4 — paleta, proporciones, casos de uso por fondo, gama de 10 grises (§4.5).
  - `photography-style.md` §5 — dirección de arte del banco de fotos (criterio, no el catálogo).
  - `contrast-matrix.md` — accesibilidad WCAG + colores semánticos (antes §6).
  - `layout-grid.md` §7 — grid del logo, layout, jerarquía tipográfica, estilo de precios (relevante sobre todo para `movistar-pptx`).
  - `system-application.md` §8 — aplicación LOVE/CHOOSE/BUY.
  - `expressive-m.md` §9 — usos expresivos de la M.
  - `word-document.md` — criterio de documentos Word (`.docx`): jerarquía de estilos, tamaños,
    tablas, con el remapeo obligatorio de fuente/color de la plantilla heredada. Úsalo junto a la
    skill prebuilt `docx` cuando te pidan generar un documento Word de marca.
  - `artifact-qa.md` — catálogo de anti-patrones de artifacts HTML/React (código incorrecto vs
    correcto, uno por regla del linter) + tabla de auto-verificación. Úsalo con `scripts/lint_artifact.py`.
- **`scripts/lint_artifact.py`** — gate determinista de QA de artifacts HTML/React (ver §QA
  determinista). Hermanos para el camino de PDF: `scripts/lint_pdf.py` (texto) + `scripts/qa_render_pdf.py`
  (visión) + `scripts/mvst_pdf_helpers.py` (helper reportlab). `scripts/qa_render_html.py` es dev-only
  (Playwright) y no va en el zip de Console.
- **`assets/html/patterns.html` + `assets/html/brand-tokens.css`** — bloques HTML y clases CSS
  pre-validados (contraste/tipografía/color plano ya resueltos) para componer artifacts que pasan el
  linter a la primera.
- **`imagery/imagery-guide.md`** — algoritmo de selección de fotografía de marca (4 pasos + reglas duras + rotación anti-repetición).
- **`imagery/imagery-index.json`** — catálogo semántico de las imágenes (tags, mood, colores dominantes, usos recomendados/evitar).
- **`assets/logo/`** — logo "M" oficial en SVG (azul / blanco / neutro) + `wordmark/` (solo la palabra, sin la M) y `lockup-horizontal/`/`lockup-vertical/` (M + palabra), cada uno en azul/blanco/mono, para los casos especiales de `brand/logo.md` §2.1.4–2.1.5.
- **`assets/fonts/`** — Movistar Sans: variable (`.woff2` + `.woff`) + estáticos por peso en `web/` (woff2+woff), `ttf/` (PPTX/escritorio/PDF) y `otf/` (impresión).
- **`assets/colors/movistar-palette.ase`** — paleta oficial (Adobe Swatch Exchange); **fuente de verdad del color**. Movistar es **color plano** (sin degradados).
- **`assets/colors/palette.generated.json`** — paleta derivada del `.ase` (hex/rgb + rol), lista para usar. Regenerar con `scripts/parse_ase.py`.
- **`scripts/parse_ase.py`** — parsea el `.ase` y regenera `palette.generated.json` (Python 3.6+).

## Relación con otras skills

- **Decks `.pptx`**: usa también la skill **`movistar-pptx`** (criterio de layout y mecánica de deck Movistar) junto con la skill prebuilt **`pptx`** (construcción del fichero). En decks, `movistar-pptx` manda sobre las reglas de imagen de esta skill.
- **Documentos Word `.docx`**: usa la skill prebuilt **`docx`** (mecánica de construcción) junto con `brand/word-document.md` de esta skill (criterio de marca — jerarquía, tamaños, remapeo de color). No hay una skill `movistar-docx` dedicada; el criterio vive aquí.
- Esta skill aporta el **criterio de marca** (voz, copy, color, tipografía, logo, foto) común a todos los formatos.
