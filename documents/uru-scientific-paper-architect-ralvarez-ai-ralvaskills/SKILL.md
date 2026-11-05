---
name: uru-scientific-paper-architect
version: 1.1.0
description: Format scientific manuscripts for Revista Tecnocientífica URU (Universidad Rafael Urdaneta) — cover page fields, Times New Roman 12pt/16pt typography rules, IMRyD-derived structure by article type, figure/table/equation numbering, bracketed-numeric citations, reference formats by source type, ethics checklist. Outputs one `.md` manuscript spec. Use when preparing a paper for submission to Revista Tecnocientífica URU.
---

# URU Scientific Paper Architect

Format a **scientific manuscript for Revista Tecnocientífica URU** (Universidad Rafael Urdaneta, Maracaibo, Venezuela) as a single markdown document that mirrors the journal's exact structure, typography, and citation rules. This skill is self-contained — it encodes one journal's fixed editorial norms; it does not delegate to [uru-thesis-defense-architect](../uru-thesis-defense-architect/SKILL.md), which targets defense presentation decks, not manuscripts. Reference formats by source type and the full review checklist live in [RECIPES.md](RECIPES.md).

## 1. Scope & output

- **Output is always one `.md` file.** No `.docx` generation, no PDF, no styling code. The `.md` represents exact manuscript content and structure — the user pastes/adapts it into Microsoft Word themselves, since the journal requires an editable Word document.
- **This skill is personal and self-contained.** It encodes Revista Tecnocientífica URU's norms only (No. 26, Enero–Junio 2024 edition); it is not a general-purpose paper-formatting tool.
- **Never invent content.** Every section, author detail, citation, or reference must come from the user or a source they provide. Where the norms require a field (ORCID, page range, DOI) and the user hasn't supplied it, mark it `[FALTA: <campo>]` rather than fabricating it.

## 2. Interview-first protocol

**Never start writing the manuscript spec without finishing the interview.** Ask in order; wait for each answer:

1. **Tipo de trabajo** — one of the seven types in [§3](#3-article-types--structure); this determines the required structure and page limit.
2. **Idioma del trabajo** — español or inglés (norms recommend expert review if written in English).
3. **Portada** — título completo (ES + EN), autores (máx. 6, cada uno con adscripción institucional, ciudad, país, correo, ORCID), en el formato de nombre exigido (ver [§5](#5-cover-page-portada)).
4. **Resumen / Abstract** — versión ES y EN, máx. 200 palabras cada una; confirma que cubre objetivo general, metodología, resultados relevantes y conclusión global.
5. **Palabras clave / Key words** — máx. 5, ES + EN.
6. **Cuerpo del trabajo** — content section by section per the structure in §3 (introducción, fundamentos teóricos si aplica, parte experimental, resultados, discusión, conclusiones, agradecimientos si aplica).
7. **Figuras, tablas, ecuaciones** — collect each with its caption/source and confirm numbering order of first appearance.
8. **Referencias** — collect the full bibliographic list in order of in-text appearance; classify each by source type (see [RECIPES §1](RECIPES.md#1-reference-formats-by-source-type)) so the correct template applies.

Only after all fields are collected, propose the section outline and wait for approval before expanding into the full manuscript spec.

## 3. Article types & structure

| # | Tipo | Estructura | Límite de páginas |
|---|---|---|---|
| 8 | Artículo de investigación | Portada, resumen (ES/EN), introducción, fundamentos teóricos (si aplica), parte experimental, resultados, discusión de resultados, conclusiones, agradecimiento (si aplica), referencias | 20 |
| 9 | Artículo de actualización | Portada, resumen (ES/EN), introducción, cuerpo del trabajo, conclusiones, agradecimientos (si aplica), referencias — o estructura IMRyD | 20 |
| 10 | Artículo de reflexión | ídem 9 | 20 |
| 11 | Artículo de revisión | ídem 9 | 20 |
| 12 | Artículo de discusión | ídem 9 | 20 |
| 13 | Artículo de invitados especiales | ídem 9 (requiere invitación editorial) | 20 |
| 14 | Nota técnica | Same structure as Artículo de investigación | 8 |

Definitions of each type live in [RECIPES §2](RECIPES.md#2-article-type-definitions) — confirm the user's content actually fits the chosen type before drafting (e.g. don't let a "reflexión" piece masquerade as a "revisión" — the norms define them by method, not just topic).

## 4. Typography & layout rules

- **Font:** Times New Roman, 12pt, justified body text.
- **Title:** 16pt, bold, centered.
- **Figure/Table captions and subordinate text:** 10pt.
- **Section names** (Introducción, Resultados, etc.): bold, centered.
- **Subsection names:** bold, left-aligned, Title Case (mayúsculas y minúsculas, not all-caps).
- **Line spacing:** double-spaced throughout, **except** resumen/abstract, agradecimientos, and the reference list — those three are single-spaced.
- Represent these rules in the `.md` output as an explicit style note per section, since markdown itself carries no font metadata — the point is that the user (or a copy step into Word) applies them exactly.

## 5. Cover page (Portada)

- **Título:** ES and EN, mayúsculas y minúsculas — except acronyms/siglas, which stay uppercase. No siglas/acrónimos/abreviaturas in the title unless of universal public domain.
- **Acronym first-use rule** (applies to the title, resumen/abstract, and body text alike): the first time an acronym or sigla is used anywhere in the manuscript, it must appear in parentheses immediately after its full name/meaning — e.g. `Organización Mundial de la Salud (OMS)`. Sustained uppercase (mayúsculas sostenidas) elsewhere in the text is reserved strictly for siglas/acrónimos.
- **Autores:** up to 6. Name format is fixed: `Primer nombre, inicial del segundo nombre, Primer apellido-Segundo apellido` (e.g. *Juan P. Pérez-Gómez*). Each author declares: institutional affiliation, city, country, email, ORCID.
- **Resumen/Abstract:** ES + EN, ≤200 words each, single paragraph, no indentation. Must briefly cover: objetivo general, metodología empleada, resultados más relevantes, conclusión global — in that order of emphasis, not necessarily labeled.
- **Palabras clave/Key words:** ES + EN, ≤5 each.

## 6. Figures, tables, and equations

- **Figures** (photos, maps, diagrams, flowcharts, graphs): labeled "Figura", arabic numbering, title + legend (if applicable), referenced in the surrounding text. If not the author's own, append the source in brackets at the end of the caption — e.g. `Figura 1. <título> [12].` Physical submission requirement (note in the spec, don't try to satisfy it in markdown): attached separately at 240–300 dpi, JPG, color or high-contrast B&W, max width 12.5 cm.
- **Tables:** labeled "Tabla", arabic numbering, title above the table, legend if applicable, referenced in text, source in brackets at end of title if not original.
- **Equations:** numbered consecutively with arabic numerals in parentheses, right-aligned/right-margin. Subscripts and superscripts must be legible and correctly placed.
- **Units:** SI (Sistema Internacional de Unidades) throughout — metro (m), kilogramo (kg), segundo (s), etc.

## 7. In-text citations & quotes

- **Non-textual citation:** surname + bracketed reference number, or just the number — `García [1]` or `[1]`.
- **Textual citation (with page):** `Moreno [3, p.19]`.
- **Three or more authors:** first author's surname + `et al.` — `Nishimoto et al. [2]` or `[2]`.
- **Short quotes** (<40 words): inline, in double quotes — `Según Smith [1, p.4], "..."`.
- **Long quotes** (≥40 words): block-quoted on a new line/paragraph, indented 1.25 cm (0.5 in) from the left margin, ending with the bracketed citation.
- **Multiple citations at once:** comma-separated brackets — `[1], [4], [5]`.

## 8. Reference list

References are numbered in brackets **in order of first appearance in the text**, not alphabetically. The exact field order and punctuation differ by source type (book, book chapter, journal article, standard, patent, thesis, technical report, catalog, mobile/web application) — full templates and worked examples in [RECIPES §1](RECIPES.md#1-reference-formats-by-source-type). Always classify each source before formatting; applying the wrong template (e.g. book format for a journal article) is a common norms violation.

## 9. Submission & ethics checklist

Before handing off the manuscript spec, confirm with the user:

- [ ] Trabajo original e inédito — no previously published, no active submission elsewhere, not a preprint.
- [ ] Carta de cesión de derechos de autor will be signed by all co-authors and sent alongside the manuscript to `tecnocientifica@uru.edu`.
- [ ] Page count respects the limit for the chosen article type (20 pages, or 8 for notas técnicas).
- [ ] All citations have matching numbered references, and vice versa — no orphaned citations or unused references.
- [ ] If the study involves humans, experimental animals, GMOs, or hazardous biological agents, a statement of compliance with the Código de Bioética y Bioseguridad (2008) is included.
- [ ] No plagiarism — all paraphrased/quoted material is properly attributed.

Full review checklist (typography + structure + citations combined) in [RECIPES §3](RECIPES.md#3-full-review-checklist).
