---
name: data2story
description: "Data Journalist Agent (Data2Story) — orchestrator: turn a dataset into a blog. Runs detective → analyst → editor → designer → programmer → auditor → inspector in sequence. Creates a versioned project folder for each run."
argument-hint: [data path]
allowed-tools: Bash(*), Read, Write, Glob, Grep, Skill, Agent, WebSearch, WebFetch
---

# Data Journalist Agent (Data2Story)

Turn **$ARGUMENTS** into a blog. Orchestrates the roles below in sequence.

## Setup

Resolve paths before doing anything:

- Never hard-code machine-local paths and never ask the user to export path variables.
- Resolve `SKILL_DIR` = the directory containing this `SKILL.md` (`.../skills/data2story`)
- Resolve `ARCHIVE_DIR` = the ancestor directory that contains `skills/` (two levels up from `SKILL_DIR`, i.e. `SKILL_DIR/../..`)
- Resolve `DATA2STORY_ROOT` = parent of `ARCHIVE_DIR`
- Commands below use symbolic placeholders such as `ARCHIVE_DIR`; replace them with resolved, quoted paths before running Bash.
- `DATA_NAME` = the dataset folder name (e.g. `pick_a_card`)
- `DATA_DIR` = if `$ARGUMENTS` is an existing path, use that path; otherwise use `DATA2STORY_ROOT/data/{DATA_NAME}`
- `TIMESTAMP` = current time formatted as `MMDD_HHMM` (e.g. `0401_1618`): `date +%m%d_%H%M` (run in bash)
- `PROJECT_DIR` = `DATA2STORY_ROOT/project/{DATA_NAME}/blog_{MODEL}_{TIMESTAMP}`
- Create `PROJECT_DIR/`, `PROJECT_DIR/assets/`, `PROJECT_DIR/code/`

## Archival

Immediately after creating `PROJECT_DIR`, snapshot the current skills:

```bash
mkdir -p PROJECT_DIR/archival
cp -r ARCHIVE_DIR/skills PROJECT_DIR/archival/skills
```

This preserves the exact skill versions used for this run.

## Tools available

All media tools route through OpenRouter. Set `OPENROUTER_API_KEY` before any generation call.

Media generation is the Designer's job, so the media tools (text2image, text2video, image2video, text2music, embeddings) live under `SKILL_DIR/designer/scripts/openrouter-*/`. The full list — default models and exact `python3 ...` invocations — is in **[`designer/references/tools.json`](designer/references/tools.json)**; full per-tool docs are each tool's own `SKILL.md` under `SKILL_DIR/designer/scripts/openrouter-*/`.

## Pipeline Overview

The pipeline is a single linear sequence that produces a traceable HTML blog from raw data:

```
DATA → Detective → Analyst → Editor → Designer → Programmer → Auditor → Inspector → final index.html + viewer.html
```

Run each stage in order. Each stage reads the previous artifact(s) before starting. Do not proceed to the next stage until the current artifact is complete.

### Stage 1 — Detective
Input: `DATA_DIR`
Output: `PROJECT_DIR/detective.json`
What: Researches external context — background knowledge, domain history, related findings, why this data matters. Each finding gets a `det_xx` ID.

### Stage 2 — Analyst
Input: `DATA_DIR`, `PROJECT_DIR/detective.json`
Output: `PROJECT_DIR/code/*.py`, `PROJECT_DIR/analyst.json`
What: Exhaustive quantitative analysis of the data, informed by detective's context. All code saved to `code/` as runnable scripts. Each finding gets an `ana_xx` ID with `calculation` (file + lines + output) and `data_table` (chart-ready data).

### Stage 3 — Editor
Input: `PROJECT_DIR/detective.json`, `PROJECT_DIR/analyst.json`
Output: `PROJECT_DIR/editor.md`, `PROJECT_DIR/editor.json`
What: Editorial decisions — which findings matter, what the narrative arc is, what the blog argues. Each section gets an `edt_xx` ID with explicit references to `ana_xx` findings and `det_xx` context. No visual design.

### Stage 4 — Designer
Input: `PROJECT_DIR/editor.md`, `PROJECT_DIR/editor.json`, `PROJECT_DIR/analyst.json`
Output: `PROJECT_DIR/designer.json`, `PROJECT_DIR/assets/*`
What: Data-driven creative visual decisions — how to present each point using charts, images, video, audio, maps, interactives, stat callouts, instances, or text-only treatment when appropriate. The media mix should emerge from the dataset's properties, not from a fixed checklist. The page should be **multimedia-rich by default**: borrow the visual language from the shared [`frontend-design`](../frontend-design/) skill and use all five channels (chart, image, video, audio, interactive/map) unless a channel's documented fallback would be fabricated or purely decorative. Each visual gets a `des_xx` ID with `data_source` pointing to `ana_xx` data_tables when data-driven. Generates selected assets. No HTML.

### Stage 5 — Programmer
Input: `PROJECT_DIR/editor.md`, `PROJECT_DIR/editor.json`, `PROJECT_DIR/analyst.json`, `PROJECT_DIR/designer.json`
Output: `PROJECT_DIR/index.html`
What: Implements the final blog in HTML. Applies the theme/accent recorded in `designer.json` `page_rhythm` and borrows component + token recipes from the [`frontend-design`](../frontend-design/) skill. Resolves chart data from analyst.json data_tables (NO raw data access). Tags every element with `data-edt`, `data-ana`, `data-det`, `data-des` attributes for traceability.

### Stage 6 — Auditor
Input: `PROJECT_DIR/index.html`
Output: `PROJECT_DIR/index.html` (modified), `PROJECT_DIR/auditor.json`
What: Detects and fixes layout issues (overlap, spacing, alignment) without changing content or design intent. Runs automatically after Programmer to ensure visual elements are properly wrapped and spaced.

Call: `Skill auditor PROJECT_DIR`

### Stage 7 — Inspector
Input: `PROJECT_DIR/index.html`, all JSON files
Output: `PROJECT_DIR/inspector.json`, `PROJECT_DIR/viewer.html`
What: Runs sentence-level traceability verification and generates an interactive viewer. Two steps:
```bash
python3 SKILL_DIR/inspector/scripts/verify.py PROJECT_DIR --log-errors
python3 SKILL_DIR/inspector/scripts/generate_viewer.py PROJECT_DIR
```
Step 1 produces `inspector.json` (sentence→evidence mapping). Step 2 produces `viewer.html` (self-contained, works on `file://` — no server needed). See `inspector/SKILL.md` for details.

## Traceability: ID flow through the pipeline

```
det_01 ──┐
det_02 ──┤
         ├──▶ ana_01 (based_on: [det_02]) ──┐
         │    ana_02 (based_on: [])          ├──▶ edt_01 (findings: [ana_01, ana_02], context: [det_01]) ──▶ des_01 (section: edt_01, data_source: ana_01)
         │    ana_03 (based_on: [det_01])    │    edt_02 (findings: [ana_03], context: [det_02])         ──▶ des_02 (section: edt_02, data_source: ana_03)
         └────────────────────────────────────┘
```

Every value in the final HTML can be traced: `HTML data-des="des_01"` → `designer.json des_01.data_source="ana_01"` → `analyst.json ana_01.calculation.code` → verifiable.

## Handoff rules

- Each artifact must be complete before the next stage starts.
- If an artifact is missing required sections, fix it before proceeding.
- **Media-richness gate (after Designer, before Programmer):** `designer.json` should exercise all five channels (chart, image, video, audio, interactive_or_map). For any channel marked `used:false`, confirm its documented fallback was genuinely tried and a data-grounded reason recorded in `meta.media_decisions`. If a channel was skipped for convenience rather than because the data can't support it, send it back to the Designer before the Programmer runs.
- All generated assets go into `PROJECT_DIR/assets/` only.
- Final deliverables: `PROJECT_DIR/index.html`, `PROJECT_DIR/detective.json`, `PROJECT_DIR/analyst.json`, `PROJECT_DIR/code/*.py`, `PROJECT_DIR/editor.md`, `PROJECT_DIR/editor.json`, `PROJECT_DIR/designer.json`, `PROJECT_DIR/inspector.json`, `PROJECT_DIR/viewer.html`.
