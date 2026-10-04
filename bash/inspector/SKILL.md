---
name: inspector
description: "Run sentence-level traceability verification on a Data2Story blog (verify.py -> verifier.json), then emit the in-page Inspector panel (the reader-facing runnable verifier) + the verify/ artifacts (verify_map.json, run_cells.json, the reproducible notebook, cell_registry.json). Mostly Python; the runnable layer recomputes each computation in-browser from its inlined data and grades it against the published output, while the bundled notebook re-executes from raw data. Use verify.py at Stage 6.4 (after validate.py, before the Critic) and generate_viewer.py at Stage 7 after the Programmer authors the verify/ files and pastes the panel shell. Triggers: a built index.html plus the role JSONs exist, or you need the traceability map / the in-page runnable verifier."
argument-hint: [PROJECT_DIR]
allowed-tools: Bash(*), Read, Write
---

# Inspector

Your job is **traceability verification** plus standing up the **runnable verify layer** — a reader can recompute each computation in-browser (from its inlined data), and the bundled notebook re-executes the headline numbers from raw data (that notebook is the paper's coding verifier). You parse the blog HTML, link each visible sentence back to its evidence in the role JSONs (`verify.py → verifier.json`), and then build the **in-page Inspector panel**: a click-any-claim drawer embedded in `index.html` whose evidence is byte-identical to the on-disk `verify/` artifacts, backed by a reproducible notebook that re-runs the headline numbers from raw data.

**This whole layer is MANDATORY on every blog.** A blog without a working Inspector panel, the `verify/` artifacts, and a clean reproducible notebook is incomplete.

## Setup

- `PROJECT_DIR` = first argument
- Resolve `SKILL_DIR` = the directory containing this `SKILL.md` (`.../skills/data2story-pro/inspector`). Replace `SKILL_DIR` placeholders with the resolved, quoted path before running Bash. Do not hard-code machine-local paths.
- Required files in PROJECT_DIR: `index.html`, `analyst.json`, `detective.json`, `designer.json`, `editor.json`

## Step 1: Run verify.py (sentence → evidence map) — early, at Stage 6.4

```bash
python3 SKILL_DIR/scripts/verify.py PROJECT_DIR
```

Produces `PROJECT_DIR/verifier.json` (the sentence→evidence mapping — the upstream traceability index). The output shape (format v3: `stats`, `sentences`, `unused_ids`) is in **[`references/inspector_schema.json`](references/inspector_schema.json)**.

**Ordering (important):** `verify.py` runs **early** — at **Stage 6.4**, after the contract gate (`validate.py`) and **before the Critic** — so `verifier.json` already exists when the Critic reads it. Re-run `verify.py` inside the Critic loop each round. The panel-injection (Step 2, `generate_viewer.py`) happens later, at **Stage 7**.

## Step 2: Emit the Inspector panel + verify/ artifacts

The Inspector no longer ships a standalone reader-viewer. It now emits the **in-page verify panel** (the reader-facing front-end) plus the auditable `verify/` artifacts that back it — including the reproducible notebook, which is the paper's from-raw-data coding verifier:

1. **The in-page Inspector panel (lives in `index.html`).** The Programmer copies `references/inspector_panel_reference.html` **VERBATIM** into `index.html` (the `.v-*` `<style>`, the `#verifyToggle` button, the drawer/backdrop/toast markup, and the `window.__verify` IIFE — see the programmer's `inspector_panel` family). The `.v-*` CSS must stay **inside a `<style>` element in `<head>`** — if it lands after the document's own `</style>` the rules render as visible text (conspicuous on mobile). The Inspector fills the panel's two inline JSON islands:
   - `<script type="application/json" id="verifyMap">` — per-element provenance, **byte-identical** to `verify/verify_map.json`
   - `<script type="application/json" id="runCells">` — in-browser-runnable snippets, **byte-identical** to `verify/run_cells.json`
   Clicking any element carrying a `data-{ana,det,des,sct,cin}` id opens the drawer for that id and renders the matching kind. A `computation` whose snippet is runnable gets a **Run** button that re-executes the statement in-browser (lazy Pyodide) and grades stdout against `expected_stdout` — recomputing the figure from the snippet's inlined data (the reproducible notebook performs the paper's from-raw-data re-execution; the panel makes that reproduction one-click for the reader).

2. **The `verify/` artifacts (on-disk source of truth).**
   - `verify/verify_map.json` — the per-element provenance map (the same bytes inlined as `verifyMap`). Schema: **[`references/verify_map.schema.json`](references/verify_map.schema.json)**.
   - `verify/run_cells.json` — the parallel runnable-snippet map (the same bytes inlined as `runCells`). Schema: **[`references/run_cells.schema.json`](references/run_cells.schema.json)**.
   - `verify/<topic>_forecast.ipynb` — the **reproducible notebook** that re-runs the pipeline from raw data and `assert`s the reproduced figures match the published ones (the notebook is a *proof*). Recipe: **[`references/reproducible_notebook.md`](references/reproducible_notebook.md)** (+ `references/notebook_template.ipynb` skeleton).
   - `verify/cell_registry.json` — maps each notebook `cell_id` to the atomic claim ids it backs (the inverse of `verify_map[id].cell_id`). Schema: **[`references/cell_registry.schema.json`](references/cell_registry.schema.json)**.
   - `verify/data/` — the dataset inputs the notebook reads (bundled at publish; see `reproducible_notebook.md` §7).

```bash
python3 SKILL_DIR/scripts/generate_viewer.py PROJECT_DIR
```

`generate_viewer.py` is the **deterministic panel + redirect emitter** — pure Python, no LLM. It runs at **Stage 7** and **requires** that the upstream authoring is already in place: the Programmer must have authored `verify/verify_map.json` + `verify/run_cells.json` (per their schemas) and copied `references/inspector_panel_reference.html` **VERBATIM** into `index.html` (the two **empty** `<script type="application/json" id="verifyMap">` and `id="runCells">` islands plus the IIFE's `var NB_PATH`). Given that, the script:

1. **Validates** the authored `verify/*.json` against the schemas, and checks every page `data-*` id resolves to a `verify_map` key (and vice-versa).
2. **Injects** the two payloads byte-identically into the empty islands in `index.html` — the rule is `inline == file_text.rstrip("\n")`, raw UTF-8, escaping a literal `</script>` only if present (never re-serialised). The on-disk `verify/*.json` files stay the source of truth; the inline copies are what the panel reads at runtime.
3. **Derives** `verify/cell_registry.json` — the mechanical inverse of `verify_map[id].cell_id` (plus the analyst `calculation.file → cell_<stem>` tag) — written only if absent, or refreshed with `--refresh` (so hand-attached `backs[]` are preserved).
4. **Wires** `NB_PATH` in the IIFE (the Download-notebook target — run locally; there is no Colab branch).

You run the script; you do not reimplement it. Its behaviour — the no-reflow overlay drawer, the kinds→renderers, the byte-identical-inline rule, the `data-*` contract, the lazy-Pyodide grading, and the publish wiring — is documented in the LIVE internals doc **[`references/inspector_panel_internals.json`](references/inspector_panel_internals.json)**; the verbatim UI build it copies is **[`references/inspector_panel_reference.html`](references/inspector_panel_reference.html)**. (An earlier margin-shift evidence viewer was retired and **superseded** by this layer — do not follow that old design.)

### Kinds the panel renders

`verify_map[id].kind` selects the drawer renderer (matching `verify_map.schema.json`):

- **computation** — claim + code slice (`code_file` + `code_lines`) + `data_preview` + `expected_output` + a Run panel. Runnable snippets execute in-browser and grade; stochastic ones run a reduced-N sample graded "≈ within noise" (never a hard PASS); `needs_network:true ⇒ runnable:false` (shown read-only, pointing at the notebook cell in `full_ref`).
- **media** — real (fetched) asset preview + `source_url` + `license` + `author` + `identity`; multi-asset elements render a gallery (`flags || assets || photos`, first non-empty wins).
- **generated** — AI-asset preview + `tool`/`model`/`prompt`/`disclosure` + the `real_default` publish-safe fallback (the real asset is the default; the AI asset is opt-in).
- **fact** — claim + category + categorised `sources[]`, each with its own `facts[]`.
- **credits** — a fact-shaped license/source aggregator (e.g. a card-deck's data + photo licences) rendered with a **Credits** badge (same renderer as `fact`).

### Byte-identical inline rule (hard)

The `verifyMap` / `runCells` islands inlined into `index.html` MUST be byte-identical to `verify/verify_map.json` / `verify/run_cells.json`. The on-disk files are the auditable source of truth and the publish artifacts (they are also the inputs the downloaded notebook reproduces from); the inline copies are what the panel reads at runtime. If they drift, the audited provenance no longer matches what readers see. When inlining, escape any literal `</script>` as `<\/script>` and serialise with `ensure_ascii` (see `inspector_panel_internals.json` → `inline_byte_identical`).

### data-* contract (no new attribute)

Elements bind to provenance via `data-{ana,det,des,sct,cin}` — one per producing role; the value is the atomic id (e.g. `data-ana="ana_01"`). Reuse these five only; do **not** introduce a new `data-*` attribute. Decorative wrappers carry no id and are skipped; the innermost tagged element wins. Every `data-*` id on the page MUST exist as a key in `verify_map.json` (a dangling id is an auditor failure; a `verify_map` id with no element is an unused-entry report, not fatal).

## Scripts

| Script | Role |
|---|---|
| `scripts/verify.py` | sentence→evidence pass → `verifier.json`. Runs **early, at Stage 6.4** (before the Critic). |
| `scripts/generate_viewer.py` | the deterministic **panel + redirect emitter** (Stage 7): validates the authored `verify/verify_map.json` + `verify/run_cells.json` against the schemas + page `data-*` ids, injects them byte-identically into the panel shell already in `index.html`, derives `verify/cell_registry.json` (write-if-absent / `--refresh`), wires `NB_PATH` (the Download-notebook target — run locally). |
| `scripts/validate.py` | the contract gate (run before `verify.py`; not modified here). |

Where the `verify/` payloads come from: `verify/verify_map.json`, `verify/run_cells.json`, and the reproducible notebook are **authored upstream by the Programmer** (the `claim` is the Editor's published sentence; `data_preview` is curated; the `run_cells` snippets are self-contained, pre-tested Pyodide code with real `expected_stdout`). They are not producible by a pure `analyst.json → islands` transform, so they are not emitted by the Inspector. `generate_viewer.py` only **validates, injects, derives, and wires** what the Programmer authored — it never invents provenance, which is why no LLM enters the Inspector. `cell_registry.json` is the one artifact the script derives (mechanical inversion of `verify_map[id].cell_id`).

## Running the steps

```bash
python3 SKILL_DIR/scripts/verify.py PROJECT_DIR
python3 SKILL_DIR/scripts/generate_viewer.py PROJECT_DIR
```

## Output

- `PROJECT_DIR/verifier.json` — full traceability data (with `raw_evidence`) — the upstream sentence→evidence map.
- `PROJECT_DIR/index.html` — now carrying the **in-page Inspector panel** (verbatim UI + the two byte-identical JSON islands).
- `PROJECT_DIR/verify/verify_map.json`, `PROJECT_DIR/verify/run_cells.json`, `PROJECT_DIR/verify/<topic>_forecast.ipynb`, `PROJECT_DIR/verify/cell_registry.json` (+ `verify/data/` at publish) — the auditable coding-verifier artifacts.

Done when: `index.html` opens directly in a browser (no server) and the 🔍 Inspector toggle opens a no-reflow drawer for every traced `data-*` element; a `computation` with a runnable snippet executes in-browser and grades against `expected_stdout`; the inline `verifyMap`/`runCells` islands are byte-identical to the `verify/` files; the reproducible notebook runs clean (every cell's `assert` passes).
