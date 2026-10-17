---
name: graphic-design
description: "Skill paraguas de diseño: logos e iconos SVG con Gemini, CIP (mockups de papelería), slides HTML con Chart.js, banners y fotos sociales. Disparadores: logo, icono, CIP, mockup, pitch deck, banner, social photo. No para UI/CSS ni tokens."
---

# graphic-design (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (313 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: generar logo o set de iconos con IA (scripts Python + `GEMINI_API_KEY`), o un programa de identidad corporativa (CIP) con mockups.
- Usar: presentaciones HTML, banners o imágenes para redes exportadas por screenshot; o como enrutador de un "paquete de marca completo".
- NO usar: voz/guía de marca → `brand`; tokens → `design-system`; Tailwind/shadcn → `ui-styling`; sólo banners → `banner-design`; sólo slides → `slides`.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar / decidir qué sub-skill aplica | `SKILL.upstream.md` L26-38 (§Sub-skill Routing) + `references/design-routing.md` |
| Logo | `SKILL.upstream.md` L40-69 (§Logo Design) + `references/logo-design.md` |
| CIP / mockups | `SKILL.upstream.md` L71-114 (§CIP Design) + `references/cip-design.md` |
| Slides | `SKILL.upstream.md` L116-130 (§Slides) + `references/slides-create.md` |
| Banner o fotos sociales | L132-177 (§Banner Design) / L217-241 (§Social Photos) + su referencia |
| Iconos SVG | `SKILL.upstream.md` L179-215 (§Icon Design) + `references/icon-design.md` |
| Depurar scripts / entorno | `SKILL.upstream.md` L279-308 (§Scripts, §Prerequisites, §Setup) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 15-24 | When to Use | Casos de uso |
| 26-38 | Sub-skill Routing | Tabla tarea → sub-skill (externa o built-in) |
| 40-69 | Logo Design (Built-in) | Brief (L44), búsqueda de estilos/colores/industrias (L50), generación IA (L58) |
| 71-114 | CIP Design (Built-in) | Brief (L75), búsqueda (L81), mockups con/sin logo y modelo pro (L90), render HTML (L108) |
| 116-130 | Slides (Built-in) | Flujo de creación y tabla de referencias slides-* |
| 132-177 | Banner Design (Built-in) | Workflow (L138), medidas (L146), estilos (L159), reglas (L171) |
| 179-215 | Icon Design (Built-in) | Icono único (L183), batch (L191), multi-tamaño (L197), estilos (L203) |
| 217-241 | Social Photos (Built-in) | Workflow de 8 pasos (L223) y tamaños por plataforma (L234) |
| 243-255 | Workflows | Paquete de marca completo y nuevo design system |
| 257-277 | References | Tabla completa de referencias |
| 279-290 | Scripts | Propósito de cada script |
| 292-308 | Prerequisites / Setup | Python (`python` en Windows), `GEMINI_API_KEY`, `pip install google-genai pillow` |
| 310-313 | Integration | Sub-skills externas y relacionadas |

## Recursos
- `references/design-routing.md` — enrutado por tipo de tarea/pregunta y flujos multi-skill.
- Logo: `references/logo-design.md`, `logo-style-guide.md`, `logo-color-psychology.md`, `logo-prompt-engineering.md`.
- CIP: `references/cip-design.md`, `cip-deliverable-guide.md`, `cip-style-guide.md`, `cip-prompt-engineering.md`.
- Slides: `references/slides.md`, `slides-create.md`, `slides-layout-patterns.md`, `slides-html-template.md`, `slides-copywriting-formulas.md`, `slides-strategies.md` (duplican `slides/references/`).
- Banner / Social / Icono: `references/banner-sizes-and-styles.md`, `social-photos-design.md`, `icon-design.md`.
- `scripts/logo/{search,generate,core}.py` y `scripts/cip/{search,generate,render-html,core}.py` — búsqueda BM25 sobre `data/` y generación con Gemini; `scripts/icon/generate.py` — SVG con Gemini 3.1 Pro. Ejecutar `py -3 scripts/logo/search.py "…" --domain style` (Windows) o `python3 …`.
- `data/logo/{styles,colors,industries}.csv`, `data/cip/{deliverables,industries,styles,mockup-contexts}.csv`, `data/icon/styles.csv` — catálogos que alimentan la búsqueda. No hay `assets/`.

## Reglas duras
- Logos siempre con fondo blanco; tras generar, preguntar si se quiere galería HTML (`ui-ux-pro-max`).
- Logos en `senzu/design-system/<slug>/logos/`: bocetos en `generados/<tipo>/`, los ELEGIDOS en `final/<tipo>/`. Con un
  logo final de ese tipo NO se generan bocetos ni variantes sin que el usuario lo pida (el muro bloquea los scripts).
  Al elegir uno: fila en «Fijado» de `gustos.md` con su ruta y decisión en la memoria del devlog (lo exige el cierre).
- CIP: generar mockups pasando `--logo`; si no hay logo, crear uno primero con la sección Logo.
- Requiere `GEMINI_API_KEY` y `google-genai pillow`; si un script falla, intentar arreglarlo directamente.
- Banners y social photos: zonas seguras 70-80 %, una CTA, máximo 2 fuentes, texto < 20 % en anuncios, exportar a px exactos (2x deviceScaleFactor).
- Verificar visualmente los PNG exportados y corregir antes de entregar; organizar salida por campaña.

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). Las salidas son assets estáticos (PNG, SVG, HTML) agnósticos de framework; en React/Vue/Astro los iconos SVG se importan como componentes o desde `public/`. Inyecta antes el contexto de `brand` si el proyecto lo tiene.
