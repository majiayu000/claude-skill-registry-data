---
name: cite-placement
description: >-
  Place pre-screened literature citations into a LaTeX or Word manuscript, or restyle the
  citations already in one. Three modes: (1) inline placement — inline \cite{}/\citet{}/\citep{}
  with a compiled references.bib, for author-date journals (APA, MLA, Harvard, Chicago
  author-date, IEEE, Vancouver); (2) footnote placement — full formatted \footnote{} or OOXML
  footnotes for legal and notes styles (Bluebook, OSCOLA, Chicago, APA, McGill) with Id./supra
  short forms; (3) restyle — convert existing footnote citations from one style to another.
  This skill is manual-invoke ONLY — trigger ONLY when the user explicitly runs /cite-placement
  or explicitly names the "cite-placement" skill. Do NOT auto-trigger on general citation,
  footnote, or reference requests.
version: 1.0.0
metadata:
  author: Claude Code
---

# Citation Placement

Unified router for three citation workflows. A single Tkinter launcher collects
inputs and writes `run_config.json`; the `"pipeline"` value selects one of three
modes, each with its own detailed workflow document.

## Modes and Routing

| Mode | `pipeline` value | What it does | Workflow doc |
|---|---|---|---|
| Inline placement | `inline` | Places screened citations as inline `\cite{}` / `\citet{}` / `\citep{}` commands with a compiled `references.bib`. For economics, finance, and social-science journals (APA, MLA, Harvard, Chicago author-date, IEEE, Vancouver). `.tex` only. | `references/phase-details-inline.md` |
| Footnote placement | `footnotes` | Places screened citations as full formatted `\footnote{}` (LaTeX) or native OOXML footnotes (Word), with one-click legal/notes style selection (Bluebook, OSCOLA, Chicago notes-bib, APA 7th, McGill) and Id./supra short-form post-processing. `.tex` or `.docx`. | `references/phase-details-footnotes.md` |
| Restyle | `restyle` | Converts ALL existing footnote citations (hand-written or pipeline-placed) from one style to another. No spreadsheet required. `.tex` or `.docx`. | Restyle Pipeline section of `references/phase-details-footnotes.md` |

Read the relevant workflow document at the start of each phase.

## Launcher-First Protocol

When the user triggers this skill:

1. Run the launcher with a **10-minute timeout** (the user needs time to browse
   and configure), using the skill's known absolute directory as `[skill-dir]`,
   not the current working directory:
   ```bash
   python "[skill-dir]/scripts/launcher.py"
   ```
   Call it via the Bash tool with `timeout: 600000`.
2. The unified GUI presents the file fields and options for all three modes and
   offers three run buttons — **Inline Placement**, **Footnote Placement**, and
   **Restyle** — plus a **Utilities** area (Strip All Citations; Regenerate /
   Reorder Cross-Refs, with or without an existing registry). On any run button
   the launcher validates inputs and writes `placement/run_config.json` in the
   **output file's parent directory**, then prints machine-readable status lines
   to stdout.
3. Parse the launcher's stdout:
   - `LAUNCHER_STATUS: success` — proceed. If missing or `cancelled`, stop.
   - `LAUNCHER_CONFIG_PATH: <path>` — the absolute path to `run_config.json`.
     Use this path for all subsequent phases. All paths inside the config are
     absolute; do not assume the config lives in the current working directory.
4. Read `run_config.json` and route on `config["pipeline"]`:
   - `"inline"` → run the inline placement pipeline (`references/phase-details-inline.md`).
   - `"footnotes"` → run the footnote placement pipeline (`references/phase-details-footnotes.md`).
   - `"restyle"` → run the restyle pipeline (Restyle Pipeline section of `references/phase-details-footnotes.md`).
5. **Run the selected pipeline end-to-end without asking questions or waiting for
   confirmation between phases.** The only pause is the Phase 4 human-in-the-loop
   gate in the two placement modes, and only when `auto_approve` is `false`.

### `run_config.json` shapes

The config always lives at `<output_parent>/placement/run_config.json`. The
`"pipeline"` key selects the shape:

```jsonc
// inline
{"pipeline": "inline", "input_format": "tex", "project_folder": "...",
 "input_tex": "...", "input_xlsx": "...", "output_tex": "...",
 "citation_style": "apa|mla|harvard|chicago_author_date|chicago_notes|ieee|vancouver",
 "replan": false, "auto_approve": false, "citation_mode": "selective|comprehensive",
 "insertion_style": "prose|simple", "verify_citations": false}

// footnotes
{"pipeline": "footnotes", "input_format": "tex|docx", "project_folder": "...",
 "input_tex": "...", "input_xlsx": "...", "output_tex": "...",
 "replan": false, "auto_approve": false,
 "citation_style": "bluebook|oscola|chicago|apa|mcgill",
 "citation_mode": "selective|comprehensive", "verify_citations": false}

// restyle
{"pipeline": "restyle", "input_format": "tex|docx", "project_folder": "...",
 "input_tex": "...", "input_xlsx": null, "output_tex": "...",
 "current_style": "...", "target_style": "..."}
```

## Citation slots (`% CITE:`)

Drafts from the `writing-article-plans` skill mark where citations belong with
typed placeholder slots, and its `assemble_manuscript.py` normalizes
footnote-wrapped slots before handoff. A slot is a `% CITE:` LaTeX comment
carrying a typed hint (e.g. `% CITE: meta-analysis on Y`). Slots are a `.tex`
convention only — footnotes-mode `.docx` input has no slot support.

**Core rule (both placement modes).** If the input manuscript contains `% CITE:`
slots, every slot MUST end the run either filled or explicitly reported as
unfilled with a reason. Silent slot survival is a pipeline failure. Slots are
author-declared citation demands, so `citation_mode: "selective"` governs only
free placements and never skips a slot.

Three slot forms reach this skill:
1. **Bare comment** — `% CITE: <hint>` on its own line or at the end of a line.
2. **Footnote-wrapped, two-line** (`\footnote{%` / `% CITE: <hint>` / `}`) — the
   normal post-assembly form (brace-safe).
3. **Footnote-wrapped, one-line** — `\footnote{% CITE: <hint>}`; compile-unsafe
   (the `%` comments out the closing brace). Recognize it and recommend running
   writing-article-plans' `assemble_manuscript.py` first.

`% RESULT:` slots belong to a different pipeline and MUST never be touched or
removed. The contract lives in the phase docs: Phase 1 enumerates slots into
`citation_slots`, Phase 3a fills each or defers it to `unfilled_slots`, Phase 4
reports the tally, and Phase 5 executes the replacements and runs a
deterministic `grep` closure check. See `references/phase-details-inline.md`
and `references/phase-details-footnotes.md`.

## Inline Mode — Phase Overview (5 phases)

Detailed instructions: `references/phase-details-inline.md`.

- **Phase 1 — Manuscript Mapping.** Read the `.tex`; produce
  `placement/section_map.md` and `placement/existing_citations.json`. Detect the
  citation package (`natbib` → `\citet`/`\citep`; `biblatex` →
  `\textcite`/`\parencite`; else basic `\cite`) and the bibliography backend
  (`bibtex`/`biber`). **Cached** unless `replan` is `true`. Read-only.
- **Phase 1.5 — Existing Citation Verification (optional).** Gated on
  `verify_citations`. Flags dangling `\cite{}` keys, hallucinated `.bib` entries,
  and spreadsheet overlaps into `placement/audit_report.json`.
- **Phase 2 — Citation Ingestion.** `scripts/core/ingest_citations.py` turns the
  `.xlsx` into `citations.json` + `references_new.bib`. Deterministic, no LLM.
- **Phase 3 — Placement Planning (3a → 3b → 3c).** 3a assigns each citation to
  all supporting sections (multi-placement is normal); 3b spawns one
  general-purpose sub-agent per section to draft anchors and cite commands,
  keyed to `insertion_style` (`prose` default — Types 1/2/3 with sentence
  rewriting; `simple` — parenthetical-only, no rewriting); 3c consolidates into
  `placement/placement_plan.md`. **Cached / incremental**: with `replan: false`,
  only cite keys absent from the `planned_keys` header trigger new planning.
- **Phase 4 — HITL Review.** Always print the plan. Pause for corrections when
  `auto_approve` is `false`; otherwise continue immediately.
- **Phase 5 — Execution.** Copy the `.tex` to a versioned output, insert cites
  (parenthetical = insert after anchor; prose/textual = replace anchor), merge
  `references_new.bib`, ensure `\bibliographystyle{}`/`\bibliography{}` (or
  `\addbibresource`/`\printbibliography` for `biblatex`), then compile with
  `pdflatex` + `bibtex`/`biber` + two more `pdflatex` passes.

## Footnote Mode — Phase Overview (6 phases)

Detailed instructions: `references/phase-details-footnotes.md`. Accepts `.tex`
(LaTeX `\footnote{}`, compiled with `xelatex`) or `.docx` (native OOXML
footnotes via `scripts/core/docx_support/`); for `.docx`, skip every
LaTeX-specific step (no `xelatex`, no `%CITE-PLACED`, no `\bibliography{}`).

- **Phase 1 — Manuscript Mapping.** Produce `placement/section_map.md` and
  `placement/existing_footnotes.json`, classifying each footnote
  (`article`/`book`/`working_paper`/`case`/`legislation`/`cross_reference`/`discursive`/`mixed`).
  **Cached** unless `replan`.
- **Phase 1.5 — Existing Citation Audit (optional).** Gated on
  `verify_citations`; verification cascade (OpenAlex → CrossRef → Google Scholar)
  into `placement/audit_report.json`.
- **Phase 2 — Citation Ingestion.** `scripts/core/ingest_citations.py` →
  `citations.json` + `references_new.bib`. Deterministic.
- **Phase 3 — Placement Planning (3a → 3b → 3c).** Style-specific rules are read
  from `references/styles/<citation_style>.md` and injected into the 3b sub-agent
  prompts; every placement carries the **full** citation string (Phase 6 handles
  repeats). 3c merges same-anchor placements into single multi-citation
  footnotes. **Cached / incremental** on the `planned_keys` header.
- **Phase 4 — HITL Review.** Pause when `auto_approve` is `false`.
- **Phase 5 — Execution.** Copy the manuscript; insert each `\footnote{` with an
  invisible `%CITE-PLACED` marker immediately after the opening brace; apply
  Phase 1.5 audit fixes; tag any pre-existing footnotes with `%CITE-PLACED`; run
  `merge_adjacent_footnotes.py`; then Phase 6; then `xelatex` (one pass, no
  `bibtex`/`biber`).
- **Phase 6 — Short-Form Post-Processing.** `short_form.py` converts repeat
  citations to the style's short form (Id./ibid/supra/shortened title/author-date)
  and writes `placement/footnote_registry.json` for later cross-reference
  reordering. Runs automatically after Phase 5; compile `xelatex` twice to settle
  footnote numbers.

### `%CITE-PLACED` marker rule

Every `\footnote{}` in a `.tex` output carries `%CITE-PLACED` immediately after
the opening brace (a LaTeX comment `pdflatex` ignores, so the PDF is unchanged).
The marker lets `strip_citations.py` cleanly remove all pipeline footnotes for a
clean re-run, and it is preserved through merge and short-form rewrites.

## Restyle Mode — Overview

Detailed instructions: Restyle Pipeline section of
`references/phase-details-footnotes.md`. Converts every existing footnote
citation from `current_style` to `target_style`, correcting Id./ibid/supra
cross-references and symbol-footnote numbering. The `.tex` path spawns one
sub-agent per section and finishes with `merge_adjacent_footnotes.py` +
`short_form.py`; the `.docx` path extracts footnotes via
`scripts/core/docx_support/`, restyles them, and writes back via
`replace_footnote_text`. Standalone drivers: `scripts/docx_restyle.py` and
`scripts/tex_restyle.py` (each takes `--config placement/run_config.json`). Case
citations, legislation, and discursive footnotes pass through unchanged.

## Utilities

The launcher's Utilities area (and the corresponding scripts) support
maintenance outside a full run:

- **Strip All Citations** — `strip_citations.py` removes every `%CITE-PLACED`
  footnote, yielding a clean manuscript for a from-scratch re-run.
- **Regenerate / Reorder Cross-Refs** — `reorder_crossrefs.py` reverses all
  short forms to full citations and re-applies them with correct footnote
  numbering after manual footnotes shift the numbering. Uses
  `placement/footnote_registry.json` (created by Phase 6); when the registry is
  absent it reconstructs from the current full citations.
- **Migrate markers** — `migrate_markers.py` retroactively adds `%CITE-PLACED`
  to footnotes in manuscripts produced before the marker convention.

## Commands

`[skill-dir]` is the absolute path to this skill's directory. All paths shown as
`placement/...` are relative to the output file's parent directory.

| Command | Purpose | Invocation |
|---|---|---|
| Launcher | Collect inputs, write `run_config.json` | `python "[skill-dir]/scripts/launcher.py"` (Bash `timeout: 600000`) |
| Ingest | `.xlsx` → `citations.json` + `references_new.bib` (deterministic) | `python "[skill-dir]/scripts/core/ingest_citations.py" --input citations.xlsx --output-json citations.json --output-bib references_new.bib [--existing-bib references.bib] [--min-score N]` |
| Verify (inline) | Audit existing `\cite{}` keys vs `.bib` + APIs | `python "[skill-dir]/scripts/core/verify_citations.py" --mode inline --citations placement/existing_citations.json --bib references.bib --output placement/audit_report.json [--spreadsheet cites.xlsx]` |
| Verify (footnotes) | Audit existing footnote citations vs APIs | `python "[skill-dir]/scripts/core/verify_citations.py" --mode footnotes --footnotes placement/existing_footnotes.json --output placement/audit_report.json [--spreadsheet cites.xlsx]` |
| Merge adjacent footnotes | Combine adjacent `\footnote{}...\footnote{}` (Phase 5 post-proc) | `python "[skill-dir]/scripts/merge_adjacent_footnotes.py" --input OUT.tex --output OUT.tex --style <id> --skill-dir "[skill-dir]"` |
| Short form | Style-aware Id./supra/ibid substitution (Phase 6) | `python "[skill-dir]/scripts/short_form.py" --input OUT.tex --output OUT.tex --style <id> --skill-dir "[skill-dir]" [--plan-dir placement/]` |
| Reorder cross-refs | Fix supra/Id. after manual footnote edits | `python "[skill-dir]/scripts/reorder_crossrefs.py" --input OUT.tex [--plan-dir placement/]` |
| Strip citations | Remove all `%CITE-PLACED` footnotes | `python "[skill-dir]/scripts/strip_citations.py" input.tex [output.tex]` |
| Migrate markers | Add `%CITE-PLACED` to legacy footnotes | `python "[skill-dir]/scripts/migrate_markers.py" input.tex [output.tex]` |
| Restyle (`.docx`) | Standalone restyle driver | `python "[skill-dir]/scripts/docx_restyle.py" --config placement/run_config.json` |
| Restyle (`.tex`) | Standalone restyle driver | `python "[skill-dir]/scripts/tex_restyle.py" --config placement/run_config.json` |

The verification report schema is unchanged from the source pipelines: inline
mode reports dangling references, per-`.bib`-entry verification, and spreadsheet
overlaps; footnotes mode reports per-citation verification status, Bluebook
format issues with corrected strings, and spreadsheet overlaps.

## Inline vs. Footnote Mode

The two placement modes differ in output form, compilation, and style set:

| Aspect | Inline mode | Footnote mode |
|---|---|---|
| Citation command | `\cite{key}`, `\citep{key}`, `\citet{key}` | `\footnote{Full formatted citation}` (or OOXML footnote) |
| `.bib` file | **Essential** — compiled by LaTeX into the bibliography | Vestigial record only; not compiled |
| Compilation | `pdflatex` + `bibtex`/`biber` | `xelatex` only (footnotes are self-contained) |
| Citation styles | APA, MLA, Harvard, Chicago author-date, IEEE, Vancouver | Bluebook, OSCOLA, Chicago notes-bib, APA 7th, McGill |
| Short forms (Id./supra) | Not applicable — the bibliography style handles repeats | Phase 6 post-processing (`short_form.py`) |
| Phase count | 5 phases (1–5) | 6 phases (1–6) |
| Input format | `.tex` only | `.tex` or `.docx` |

Chicago **notes-bib** and legal styles belong to footnote mode; the inline mode's
`chicago_notes` option warns and points to footnote mode instead.
