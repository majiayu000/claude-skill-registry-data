---
name: telestudy
description: Create a telescopic HTML study guide from any book, PDF, epub, paper, or article — skimmable key ideas that expand into depth, an interactive ideas-dependency graph, a chapter map, and deep links back to the source. Use when the user asks to "telestudy" something, wants a study guide / distillation / ideas map of a book or document, or wants to add a guide to their Reading Room library.
---

# Telestudy — telescopic study guides from anything

A Telestudy guide lets a reader skim a source's key ideas in ~2 minutes, telescope into any idea
(one-liner → summary → deep dive), browse the **ideas graph** (what builds on what), and jump from
any idea into the actual chapter/section of the source. One shared CSS/JS template renders
everything from a single JSON block per guide, so all guides look and behave identically.

This skill folder is the toolkit:

- `assets/guide.css`, `assets/guide.js` — the renderer (copy, never regenerate or inline)
- `reference/SPEC.md` — the authoring spec: JSON schema, quality bar, graph rules **(read it before writing)**
- `reference/exemplar.html` — a complete finished guide (The Psychology of Money)
- `scripts/extract_structure.py` — TOC/outline extraction from epub (file or unpacked dir) and PDF
- `scripts/validate.py <guide.html>` — structural validation (run before declaring done)
- `scripts/build_index.py <library-root>` — regenerates the library index page

## Workflow

### 1. Ingest the source

Identify what you're distilling and pull its real structure — never invent chapter titles.

- **epub**: `python3 scripts/extract_structure.py <path>` (handles zip epubs and unpacked dirs).
  Read actual chapter text via `zipfile`/`unzip -p`, or the xhtml files directly.
- **PDF**: same script (uses `pypdf`; `pip install pypdf` into a venv if missing). Extract page text
  with `pypdf` when you need to ground content.
- **Article / web page**: fetch it; sections (headings) play the chapter role.
- **Apple Books library item**: look up the asset id and file path:
  `sqlite3 ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/BKLibrary-*.sqlite "SELECT ZASSETID, ZTITLE, ZPATH FROM ZBKLIBRARYASSET WHERE ZTITLE LIKE '%<title>%';"`
  (copy the db to a scratch dir first if it's locked). `assetId` gives the guide an
  `ibooks://assetid/<id>` deep link.

If you know the work deeply, write from knowledge and use the extracted TOC for the chapter map.
If not, **skim the actual text first** — accuracy beats speed; grounding is non-negotiable.

### 2. Choose the destination

- **Adding to an existing library** (a folder with `assets/guide.css` + `books/`): write the guide
  to `books/<slug>.html` with asset hrefs `../assets/…`, then rerun
  `scripts/build_index.py <library-root>`. If the user has a Reading Room library already, prefer it.
- **Standalone guide**: create `<slug>-guide/` next to the source (or where asked) containing
  `assets/` (copied from this skill), and `<slug>.html` at the top with asset hrefs `assets/…`
  and `"library": false` in the JSON.

Always COPY `assets/guide.css` + `assets/guide.js` from this skill folder — do not re-author them.
If the destination library's assets differ from the skill's, the skill's are newer; sync them.

### 3. Author the guide

Read `reference/SPEC.md` in full, study `reference/exemplar.html`, then write the single HTML file:
shell + one `<script id="book-data" type="application/json">` block. Scale idea count to the source
(book 9–15, paper 5–8, article 4–6). Give the `dependsOn` graph real care — edges mean "you must
grasp X to fully get Y", and the set must be a connected acyclic DAG.

For the source link, set `assetId` (Apple Books) or `sourceUrl` (article URL, or `file:///…` for a
local PDF) and optionally `sourceLabel`.

### 4. Validate and verify

- `python3 scripts/validate.py <guide.html>` — fix every failure (including disconnected graph
  nodes: wire them with semantically honest edges).
- Open the result in a browser when feasible and confirm the cards telescope and the graph renders.

### 5. Batch mode

For many sources at once, fan out one subagent per source: each agent gets this skill folder's
SPEC + exemplar paths, its source's path/TOC/assetId, and the output path — then validate all
results centrally and rebuild the index once at the end.
