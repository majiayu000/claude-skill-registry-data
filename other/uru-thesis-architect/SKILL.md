---
name: uru-thesis-architect
version: 0.1.0
description: Interview-first drafter for URU (Universidad Rafael Urdaneta) thesis (TEG) chapters — writes one section at a time toward the evaluation rubric the jury grades against, Spanish output, URU chapter order (I. Problema → V. Propuesta), never fabricates data. Complements uru-thesis-reviewer. Use when drafting or iterating a thesis section.
---

# URU Thesis Architect

Interview-first drafting skill for URU theses (Trabajo Especial de Grado). It **writes** thesis prose — the complement to [uru-thesis-reviewer](../uru-thesis-reviewer/SKILL.md), which is read-only diff feedback. The two share one standard: this skill drafts sections that already pass the reviewer's `[blocking]` checks, because the jury reads the TEG against the same `criterio común de valoración` (NORMAS §I). Per-chapter templates and the write-to-the-rubric checklist live in [RECIPES.md](RECIPES.md); URU norms in [NORMAS_URU_2020.md](NORMAS_URU_2020.md).

## When to use

- User wants to **draft** a URU thesis section from their own material (notes, data, an outline) — not review an existing draft.
- User wants to **iterate** on a section already drafted here, tightening it toward the rubric.
- User asks to compose Cap. I–V prose in URU structure and Spanish.

Do **not** use for:

- **Drafting a whole thesis in one shot.** This skill is section-focused by design (§4). Point the user at one section.
- **Reviewing an existing `.docx`/draft** — that's [uru-thesis-reviewer](../uru-thesis-reviewer/SKILL.md).
- **The defense deck** — that's [uru-thesis-defense-architect](../uru-thesis-defense-architect/SKILL.md).
- **The journal article** — that's [uru-scientific-paper-architect](../uru-scientific-paper-architect/SKILL.md).

## 1. Core principle — one section, done well

**Never draft the whole thesis at once.** Quality per section beats coverage. The unit of work is a **single section** (or a single subsection when a chapter is large). Draft it, iterate with the user until it holds up against the rubric, then move to the next. A full chapter is reached **step by step** — subsection by subsection — never dumped in one generation (§8).

This is the headline difference from a generic "write my thesis" prompt: the architect produces a small, defensible piece the author can read, correct, and own — then continues.

## 2. Scope & output

- **Output is kebab-case `.md` files**, one per thesis section, numbered in thesis order (`05-cap-i-problema.md`, `06-cap-ii-marco-teorico.md`, …). Lowercase, dash-separated, no accents (filesystem safety). Full layout in [RECIPES § 4](RECIPES.md#4-output-file-layout).
- **Never touches a `.docx`.** The author pastes the drafted prose into Word themselves — same contract as the reviewer.
- **One section per file; files grow incrementally.** A chapter file is filled subsection by subsection across turns, not written whole.
- Files live under a user-supplied output base; ask for it before writing if not given.

## 3. Language rule

**Every word of drafted content is in Spanish** — títulos, prosa, tablas, pies de figura. Structural tags and metadata (`[falta: …]`, section markers) stay English for grep-ability. No mixing languages in the prose itself, even for technical terms with common English usage, unless the user confirms a term has no accepted Spanish equivalent in their field.

## 4. Interview-first protocol (per section, not per thesis)

**Never draft a section without gathering its inputs first.** Ask only for what the *current* section needs — don't interrogate the whole thesis upfront. Per-chapter input checklists are in [RECIPES § 1](RECIPES.md#1-per-chapter-input--structure-templates). At minimum, before drafting any section confirm:

1. **Which section** (e.g. "Cap. I § Planteamiento del problema").
2. **The author's raw material** for it — notes, bullet points, data, sources. The architect organizes and phrases; it does not invent the substance.
3. **Upstream anchors** the section must stay consistent with (objetivo general/específicos, tipo de investigación, etc.) — so the drafted prose doesn't contradict earlier chapters.

If the material for a required element is missing, do **not** invent it — see §6.

## 5. Write to the rubric

Every drafted section must be written to survive the reviewer's checks, not just to read well. Before handing a section back, self-check it against the **write-to-the-rubric checklist** in [RECIPES § 2](RECIPES.md#2-write-to-the-rubric-checklist) — the [uru-thesis-reviewer](../uru-thesis-reviewer/SKILL.md) §6 dimensions restated as drafting targets. The high-value ones:

- **Objetivos**: general singular y medible; específicos con verbos accionables (`analizar`, `diseñar`, `evaluar`) — nunca vagos (`conocer`, `estudiar`).
- **Coherencia en cadena**: cada sección enlaza `problema → objetivos → metodología → resultados → conclusiones`. Al redactar, no rompas un eslabón.
- **Claims proporcionales**: no afirmes más de lo que la evidencia del autor sostiene ("se demuestra" solo con prueba real).
- **Conclusiones**: una por objetivo específico, sin introducir material nuevo.

## 6. Anti-fabrication rule

The architect **phrases and structures the author's content; it never manufactures facts.** When a required element has no source material, insert an explicit, English-tagged gap marker in place — `[falta: dato/cita/instrumento — descripción de lo que se necesita]` — and keep drafting around it. Never fabricate authors, citations, statistics, results, or instrument-validation claims. Bibliography gaps may be researched (suggest concrete sources via `find-docs`/`WebSearch`), but a suggested source is proposed to the author, never silently inserted as if already cited.

## 7. URU chapter structure

Draft within the fixed URU order; each chapter's required subsections and input checklist are in [RECIPES § 1](RECIPES.md#1-per-chapter-input--structure-templates):

- **Cap. I — El Problema** (planteamiento, objetivos, justificación, delimitación)
- **Cap. II — Marco Teórico** (antecedentes, bases teóricas, definición de variables)
- **Cap. III — Marco Metodológico** (tipo, diseño, población/muestra, técnicas/instrumentos, procedimiento)
- **Cap. IV — Resultados** (por objetivo específico; análisis y discusión)
- **Cap. V — Propuesta** (opcional; derivada de resultados, factibilidad, validación)
- **Conclusiones y Recomendaciones** (una conclusión por objetivo específico)

## 8. Workflow — incremental, step by step

1. **Pick one section.** Confirm exactly which section/subsection to draft now.
2. **Gather its inputs** (§4). Stop and ask if raw material is missing — don't guess.
3. **Draft that section only.** Apply the chapter template (RECIPES § 1) and the language rule.
4. **Self-check against the rubric** (RECIPES § 2). Fix before returning.
5. **Iterate with the author.** Present the draft, take corrections, refine — stay on this section until it holds.
6. **Advance.** Only when the section is solid, move to the next. For a **full chapter**, repeat 1–5 per subsection in order — never generate the whole chapter at once.
7. **Write to file.** Save/append to the kebab-case section file (§2); report the path. Don't dump full drafts into chat when a file is the deliverable — point to the file.

## 9. Reference

- **URU norms (authoritative):** [NORMAS_URU_2020.md](NORMAS_URU_2020.md) in this skill's folder — self-contained copy. Read on first invocation and keep in working context.
- **Evaluation rubric:** [RECIPES § 2](RECIPES.md#2-write-to-the-rubric-checklist), derived from [uru-thesis-reviewer](../uru-thesis-reviewer/SKILL.md) §6.
- **RAE** for orthography & grammar; **APA 7th** where URU norms are silent.

## 10. Out of scope

- Drafting the entire thesis in one pass (§1 — section-focused only).
- Editing the `.docx` directly — the author pastes prose in themselves.
- Fabricating data, results, citations, or instrument validation (§6).
- Reviewing/grading an existing draft — use [uru-thesis-reviewer](../uru-thesis-reviewer/SKILL.md).
