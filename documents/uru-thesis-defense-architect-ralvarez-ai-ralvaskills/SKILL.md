---
name: uru-thesis-defense-architect
version: 1.0.1
description: Design URU-style thesis defense presentation specs — fixed institutional slide structure (portada, problema, objetivos, antecedentes, variables, metodología, resultados, conclusiones), Spanish-only content, logo placement rules (large centered cover, small top-left from slide 2). Outputs one `.md` slide-by-slide spec. Use when authoring a thesis/tesis defense deck for Universidad Real (URU).
---

# URU Thesis Defense Architect

Design **thesis defense presentation specifications** for Universidad Real (URU) as a single markdown document. Every slide is described by its section role, its logo placement, and its exact Spanish-language text content. This skill is self-contained — it does not delegate to [demo-presentation-architect](../demo-presentation-architect/SKILL.md), which targets general demo decks with a different layout system and audience. Full structure table, per-slide template, and review checklist live in [RECIPES.md](RECIPES.md).

## 1. Scope & output

- **Output is always one `.md` file.** No HTML, PDF, PPTX, image generation, or styling code. If asked for a rendered deck, refuse and offer the `.md` instead.
- **This skill is personal and self-contained.** It encodes one institution's fixed defense structure; it is not a general-purpose deck tool and does not chain with other presentation skills.
- **The university logo is a user-supplied asset**, expected at `assets/uru-logo.png` inside this skill folder. Every slide spec references it by that path — never regenerate or describe the logo's visual content.

## 2. Interview-first protocol

**Never start writing the deck without finishing the interview.** Ask in order; wait for each answer, and confirm nothing is invented — every field below must come from the user or their thesis document:

1. **Portada** — título completo del trabajo, autor(es), tutor, lugar, año.
2. **El Problema** — la síntesis del problema o necesidad (no el capítulo completo; pide al usuario que lo resuma si aún no lo ha hecho).
3. **Objetivos** — objetivo general (una frase) y objetivos específicos (lista).
4. **Justificación e Importancia / Delimitación** — el argumento de valor y el alcance (qué cubre y qué no).
5. **Antecedentes** — filas de `AUTOR, AÑO | TÍTULO | APORTE` (mínimo 2-3, cuantas el usuario tenga).
6. **Variables** — filas de `VARIABLE | AUTOR | DEFINICIÓN`.
7. **Metodología** — tipo, diseño, población-muestra (o unidad de análisis), técnicas e instrumentos.
8. **Metodología de Desarrollo** — lista de FASES y, por cada fase, sus ACTIVIDADES.
9. **Resultados** — por cada fase de §8, qué se hizo y qué evidencia existe (diagramas, capturas, arquitecturas, analíticas). Confirma cuántas láminas se necesitan por fase; no fuerces una fase compleja a una sola lámina.
10. **Conclusiones y Recomendaciones** — hallazgos de cierre, mejoras futuras, y confirmación de que habrá demostración en vivo del producto.

Only after all fields are collected, propose the **outline** (one line per slide: sección + resumen) and wait for approval before expanding into full slide specs.

## 3. Language rule

**Every word of slide content is in Spanish** — títulos, viñetas, texto de tablas, notas del orador. No mixing languages, even for technical terms with common English usage, unless the user explicitly confirms a term has no accepted Spanish equivalent in their field. This is non-negotiable for this skill; it exists specifically for a Spanish-language institutional defense.

## 4. Logo & branding rules

- **Lámina 1 (Portada):** logo grande, centrado, en la parte superior de la lámina — la identidad institucional predomina visualmente.
- **Lámina 2 en adelante:** logo pequeño, esquina superior izquierda, en todas las láminas sin excepción — incluidas las láminas adicionales de una misma sección (p. ej. Resultados 9a, 9b, 9c).
- **Ruta del asset:** `assets/uru-logo.png`. Cada bloque de lámina en el `.md` de salida incluye un campo `**Logo:**` con la ruta y el tamaño/posición (`grande, centrado` o `pequeño, superior-izquierda`).
- Never invent logo content or describe what the logo looks like — it is opaque to this skill; only its placement and size are specified.

## 5. Fixed slide structure & flexible slide count

The defense follows nine fixed sections, in order. **Slide numbers are reference points, not a hard 1:1 mapping** — any section may expand to multiple slides when its content doesn't fit one canvas without becoming a wall of text. The full structure table (distribución de elementos + énfasis del documento per section) lives in [RECIPES §1](RECIPES.md#1-fixed-structure-table).

Two expansion rules are mandatory:

- **Resultados (§9 of the interview) must correlate 1:1 with the phases defined in Metodología de Desarrollo (§8).** If Metodología de Desarrollo lists 4 fases, Resultados opens with (at minimum) one slide per fase, explicitly explaining what was done in that phase — never a generic results dump disconnected from the phase list.
- **Any section can take "varias láminas" when needed** — Antecedentes with 6 references, or a Resultados phase with three diagrams, both justify a split. Splitting is a content-fit decision, not a numbering convenience: don't split just to hit a target slide count, and don't cram to avoid a split.

## 6. Per-slide content-emphasis rules

Each section has a specific emphasis the slide content must honor — these are the difference between a correct URU-format slide and a generic one:

- **El Problema** → síntesis only: un esquema, un diagrama, o un par de viñetas contundentes. Never a paragraph-dense wall of text.
- **Objetivos** → hard visual separation between GENERAL (bloque único destacado) and ESPECÍFICOS (lista secuencial) — never merge them into one list.
- **Justificación e Importancia / Delimitación** → two distinct halves on the same canvas; each argument stands alone, not interleaved.
- **Antecedentes** → strict three-column table (`AUTOR, AÑO | TÍTULO | APORTE`); the APORTE column must state a direct, concrete contribution to this project — not a summary of the cited work.
- **Definición de las Variables** → strict three-column table (`VARIABLE | AUTOR | DEFINICIÓN`); every technical/engineering variable needs a cited author backing its definition.
- **Metodología** → four fixed fields only: Tipo, Diseño, Población-Muestra (o Unidad de Análisis), Técnicas e Instrumentos.
- **Metodología de Desarrollo** → table or process map crossing FASES × ACTIVIDADES; this table is the anchor Resultados must reference back to.
- **Resultados** → per-phase explanation of what was built, correlated to §5's phase list; the visually richest, most extensible section.
- **Conclusiones y Recomendaciones** → closes with an explicit handoff line to the live product demonstration — this is the culminating moment of the defense, state it as such.

## 7. Output specification format

Every slide in the output `.md` follows the same block shape: `## Lámina N — <Sección>`, `**Logo:**`, `**Contenido:**` (with sub-fields matching the section's required data per §6), and optional `**Notas del orador:**`. Full template in [RECIPES §2](RECIPES.md#2-per-slide-specification-format).

## 8. Review checklist

Before handing off the deck spec, run the checklist in [RECIPES §3](RECIPES.md#3-review-checklist) — covers language purity, logo placement per slide, section-emphasis compliance, Resultados/Metodología-de-Desarrollo correlation, and no invented content.
