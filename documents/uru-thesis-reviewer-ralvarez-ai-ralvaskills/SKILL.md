---
name: uru-thesis-reviewer
version: 0.2.0
description: Continuous-feedback reviewer for URU (Universidad Rafael Urdaneta) theses. Emits ordered `.md` diff files (- old / + new) the author applies manually — never edits the `.docx`. Covers substance, structure, prose, citations vs `NORMAS_URU_2020`. Tracks issues across sessions via stable IDs and carry-forward. Use when the user shares a thesis or chapter.
---

# URU Thesis Reviewer

Iterative feedback skill for URU theses. Each invocation produces a **review session folder** with numbered Markdown files the author reads, accepts/rejects, and applies to the source document. File templates in [TEMPLATES.md](TEMPLATES.md); formal/linguistic check catalog in [CHECKS.md](CHECKS.md); URU norms in [NORMAS_URU_2020.md](NORMAS_URU_2020.md).

## When to use

- User shares a `.docx` (or a converted `.md`/`.txt`) of a URU thesis or chapter and asks for review, feedback, suggestions, or revision.
- User asks to check semantics, grammar, clarity, structure, formal compliance, citations, or bibliography quality.
- User asks to compare against URU norms.

Do **not** use for:

- Editing the source document directly (this skill never touches the `.docx`).
- Evaluation / grading (this is improvement feedback, not a verdict).
- Non-URU theses (use a generic editor — URU norms are baked in).

## 1. Operating principles

- **Read-only on source.** Never edit, rewrite, or replace the `.docx`. All output is review files the author applies manually.
- **Sequential & ordered.** Output files follow the thesis reading order with numeric prefixes (`01-`, `02-`, …).
- **One session per invocation.** Each review goes in a fresh `YYYY-MM-DD/` folder. Multiple sessions in one day → suffix `-a`, `-b`, … (`2026-05-21-a/`).
- **Diff format, not prose.** Show the exact text to remove (`-`) and the proposed replacement (`+`).
- **Severity-tagged.** Every block carries one of: `[blocking]` (norm violation or factual error), `[suggest]` (real improvement), `[nit]` (taste/polish).
- **Cite the rule.** When the suggestion is driven by URU norms, link the section (e.g., `NORMAS §V. CITAS`). For language, cite RAE if relevant.
- **Bibliography: suggest, don't fabricate.** When flagging a weak source, propose a concrete replacement using `find-docs` / `WebSearch`. If no credible alternative is found, mark as `[suggest] needs stronger source — none found in search`.
- **Spanish output.** Feedback prose and rewrites are in Spanish. Tags, headers, and metadata stay English for grep-ability.

## 2. Inputs

User provides:

1. **Source path** — `.docx` (preferred) or already-converted `.md`/`.txt`.
2. **Output base path** — directory where `YYYY-MM-DD/` session folder is created.
3. *(Optional)* **Scope filter** — e.g., "only Capítulo II", "skip bibliography", "focus on grammar only".

If the user only provides the `.docx` and no output path, **ask** before proceeding.

## 3. Ingestion (`.docx` → reviewable text)

Claude cannot Read `.docx` directly. Pick the first available path:

1. **Anthropic official `docx` skill** (preferred). Preserves structure (headings, lists, tables, footnotes, comments). Check the available-skills list at session start.
2. **Pandoc fallback** — `pandoc "<source>.docx" -t markdown -o "<source>.review.md"`.
3. **Manual.** Ask the user to paste content or "Save as .txt" from Word.

The intermediate `.review.md` (from pandoc) is **scratch** — don't commit it, don't put it in the session folder.

After ingestion, identify section boundaries by matching headings against URU's expected structure (§6.1).

## 4. Output structure & cross-session tracking

### 4.1 Session folder

Sessions live under `<output-base>/YYYY-MM-DD/` with one numbered file per thesis section (`01-index.md`, `02-resumen.md`, …, `11-referencias.md`, `12-anexos.md`), kebab-case (lowercase, dash-separated, no accents). Full folder layout and naming rules in [TEMPLATES § 5](TEMPLATES.md#5-folder-layout-numbered-thesis-order).

`01-index.md` is **mandatory every session**, even one that only drafted prose and touched no tracked issue — a 5-line index (executive summary + "sin cambios en seguimiento de issues") beats a missing one. There is no separate cross-session registry file: `01-index.md` *is* the record, session over session.

Any file the session produces that isn't a numbered section review — free-form drafting (`redaccion-*.md`), a handoff note — still gets listed in `01-index.md`'s Mapa de archivos, tagged by type (see [TEMPLATES § 1](TEMPLATES.md#1-01-indexmd)).

### 4.2 Cross-session issue tracking

Each `01-index.md` carries a **Seguimiento de issues** table (template in [TEMPLATES § 1](TEMPLATES.md#1-01-indexmd)) that is the running state of every issue ever raised, not just this session's.

- **Stable IDs.** Assign each issue an ID at first discovery: `yyyy-mm-dd-<chapter>-<slug>` (e.g. `2026-06-06-cap-ii-mcp-como-agente`). On recurrence, reference the existing ID — never restate the finding as new.
- **Status is orthogonal to severity.** Severity (`[blocking]/[suggest]/[nit]`) says how bad it is; status says where it stands: `abierto` (found, not addressed) → `resuelto-en-borrador` (fix drafted in a review file, not yet in the `.docx`) → `aplicado` (author confirmed it's in the `.docx`) → `rechazado` (author declined) → `needs-decision` (open question for the author/tutor). Only the author can move an issue to `aplicado` — Claude cannot verify the `.docx` was edited.
- **Carry-forward, mandatory.** At the start of every session after the first, read the previous session's `01-index.md` Seguimiento table before writing anything new. Copy every issue not at `aplicado`/`rechazado` forward into this session's table unchanged unless its status actually moved. This is what makes the per-session file sufficient as a registry — skipping it is how issues silently go stale.
- **Reversed decisions need a reason.** If this session overturns or drops a prior decision (not just a status update — an actual reversal), add a one-line `**Por qué se revirtió:**` next to that issue's row. A diff showing the old text gone is not enough.
- **Tutor comment numbers drift.** `.docx` comment numbers renumber across edits. Always pair a referenced comment number with the verbatim quoted text it points to — never cite the number alone.

## 5. File templates

Three templates drive the output:

- **`01-index.md`** — executive summary, severity counts, file map, cross-cutting themes, and the cross-session Seguimiento de issues table (§4.2). Template in [TEMPLATES § 1](TEMPLATES.md#1-01-indexmd).
- **`nn-section.md`** — per-section diffs grouped by severity. Template + diff shape in [TEMPLATES § 2](TEMPLATES.md#2-nn-sectionmd--one-per-reviewed-section).
- **`11-referencias.md`** — bibliography-specific structure (missing/orphan sources, weak-source replacements, format fixes). Template in [TEMPLATES § 3](TEMPLATES.md#3-11-referenciasmd--bibliography-section).

For substantive issues, the `+` side is a **prompt** for the author, not rewritten text — see [TEMPLATES § 4](TEMPLATES.md#4-substantive-feedback-diff-shape).

## 6. Review dimensions (what to check, in order)

For each section, walk these dimensions in order. Stop reading prose once a `[blocking]` structural issue makes downstream feedback premature (note it in INDEX and move on).

Dimensions split into two groups:

- **Substantive** (§6.1–6.2 below): does the research itself hold up? This is the headline value of the review.
- **Formal & linguistic** ([CHECKS.md](CHECKS.md)): URU norms, prose quality, citation hygiene. Six checklists — formal aspects, redacción, grammar, semantics, citations, bibliography.

### 6.1 Structural compliance (URU §II)

- Are all required preliminary sections present? (portada, frontispicio, índices, resumen, abstract)
- Are chapters in URU order? (I. Problema → II. Marco Teórico → III. Marco Metodológico → IV. Resultados → V. Propuesta opt.)
- Does each chapter have the expected sub-sections per URU template?
- Are conclusiones organized by objetivos específicos?

### 6.2 Substantive content (proposals, information, argument)

Evaluate the thesis on its own merits as a piece of research, independent of URU formatting. Read each chapter as a domain reviewer would.

**Cap. I — El Problema**

- Problem clearly defined and bounded? Can the reader state it back in one sentence?
- Justification specific and evidence-backed, or generic ("este tema es muy importante")?
- Objetivo general: singular, measurable, achievable within the thesis scope?
- Objetivos específicos: decompose the general into independently-verifiable steps? Actionable verbs (`analizar`, `diseñar`, `evaluar`), not vague (`estudiar`, `conocer`)?
- Delimitación: clear scope boundaries.

**Cap. II — Marco Teórico**

- Antecedentes: *actually* relevant to this thesis's problem, or padding? Each should connect explicitly.
- Bases teóricas: depth matches the thesis's needs (not textbook summary, not off-topic monograph).
- Currency: dominant sources reasonably recent (varies by field — flag pre-2010 in fast-moving areas).
- Coverage gaps: obvious schools, key authors, recent developments missing?
- Operational definitions: key terms defined precisely and consistently.

**Cap. III — Marco Metodológico**

- Tipo y nivel: chosen design (descriptiva / explicativa / correlacional) appropriate for the objectives? Mismatches are `[blocking]`.
- Diseño: experimental / no-experimental / documental — justified or just declared?
- Población y muestra: defined, sampling method explained, size justified (statistically or by saturation).
- Instrumentos: validated? Reliability reported? If self-built, validation process described?
- Procedimiento: replicable from the description alone.

**Cap. IV — Resultados**

- Do results actually address each objetivo específico? Cross-check explicitly.
- Claims proportional to the evidence? Flag overreach ("se demuestra que…" when data only suggests).
- Tables/figures show what the text claims? Internal contradictions are `[blocking]`.
- Statistical / analytical method appropriate for the data type.
- Discussion: results contextualized against the marco teórico.

**Cap. V — Propuesta (if present)**

- Derived from the results, not pre-decided.
- Feasibility addressed (resources, time, constraints).
- Validation plan: how would adoption be measured?

**Conclusiones**

- One conclusion per objetivo específico (URU expects this alignment).
- Each conclusion supported by results — no new claims introduced.
- No overreach beyond the studied population/scope.

**Recomendaciones**

- Actionable, not platitudes ("se recomienda seguir investigando").
- Addressed to identifiable audiences.

**Cross-chapter coherence (highest-value check)**

- The chain `problema → objetivos → marco → metodología → resultados → conclusiones` must be intact.
- Verify: every objetivo específico has a corresponding methodological step, a results subsection, and a conclusion.
- Verify: every conclusion traces back to a result, which traces back to a method, which addresses an objective.

### 6.3 Formal & linguistic dimensions

Formal aspects (URU §IV), redacción (URU §III), grammar/RAE, semantics & clarity, citations (URU §V), bibliography (URU §VI) — full per-dimension checklists in [CHECKS.md](CHECKS.md).

## 7. Workflow

1. **Carry forward.** If a prior session exists, read its `01-index.md` Seguimiento de issues table (§4.2) before doing anything else. This seeds the current session's tracking table.
2. **Ingest.** `.docx` → reviewable text via §3. Identify section boundaries.
3. **Inventory.** List every section found. Compare against URU expected structure (§6.1). Flag missing/extra sections as `[blocking]`.
4. **Scope.** If the user specified a filter, restrict to those sections.
5. **Substantive pass first.** Walk §6.1 then §6.2 across all chapters before touching prose. Substantive `[blocking]` issues reshape downstream work — surface them early.
6. **Per-section formal/linguistic pass.** Walk [CHECKS.md](CHECKS.md) §1–5 in order. Skip deep prose review on any section flagged with a substantive `[blocking]` — note "prose review deferred pending substantive revision" in INDEX.
7. **Bibliography pass.** Run [CHECKS § 6](CHECKS.md#6-bibliography-uru-vi) at the end — needs the full source list and may require web searches.
8. **Write files.** Create `YYYY-MM-DD/` folder. Write section files in order. Write `01-index.md` last, including the carried-forward + updated Seguimiento de issues table. The `Resumen ejecutivo` leads with substantive impression before formal observations. If the session hands off open work, write it as `00-handoff.md` — always that name, never a variant.
9. **Report.** Brief message to user: session path, severity totals, recommended starting point. Do NOT dump the diffs into chat — point to the files.

## 8. Reference

- **URU norms (authoritative source):** [NORMAS_URU_2020.md](NORMAS_URU_2020.md) in this skill's folder. Read it on first invocation of a session and keep it in working context.
- **RAE** for orthography & grammar.
- **APA 7th** where URU norms are silent (URU is APA-derived but Spanish-localized).

## 9. Out of scope

- Editing the `.docx` directly. Author always applies changes.
- Rewriting entire sections from scratch — propose targeted diffs, not redrafts. If a section needs total rewrite, say so in `[blocking]` and explain why.
- Plagiarism detection — flag suspicious unattributed phrasing as `[suggest] verificar fuente`, don't claim plagiarism.
- Defense/jury preparation — separate skill.
- Translating Resumen ↔ Abstract — flag mismatches, don't translate.
