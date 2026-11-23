---
name: pid-to-kg
description: Converts P&IDs (piping and instrumentation diagrams) and PFDs in PDF form, either vector or scanned, into a process knowledge graph covering equipment connectivity (upstream/downstream), instrument locations and measured variables, and control loops. Output is JSON plus a DuckDB file plus an LLM-ready Markdown summary. Use when the user wants to digitize, extract, analyze or build a knowledge graph or context layer from P&IDs, or asks what is upstream/downstream of a piece of equipment, which sensors measure what, or how a plant's control loops are structured.
---

# P&ID to knowledge graph

Work is split between deterministic scripts and you:

- **Scripts** classify pages (vector vs scanned), render them into readable tiles, collect OCR/text hints, then build, check, store and query the graph.
- **You** read the drawings and write one structured extraction file per sheet. Symbol recognition and line tracing are visual reasoning, and that is the part scripts cannot do well.

All scripts are in `scripts/` next to this file. Call them by their full path (the commands below abbreviate it as `scripts/`), and keep the work directory in the user's current folder, e.g. `work/<plant>`.

**Setup.** Many users are engineers, not programmers, so handle setup yourself. The scripts need Python 3.10+. Before the first run, install the dependencies with `pip install -r <skill dir>/scripts/requirements.txt` (use a virtual environment if the user's Python is shared with other work). If Python is missing, tell the user to install it from python.org and stop there.

## Ground rules

- **Only the P&ID pages.** Drawings often sit inside a long permit or design report. If the user names the pages, pass them with `--pages`. If not, and the PDF has more than a few pages, probe it, look at the page overviews or ask the user, then re-run the probe with `--pages` so later steps skip reports, legends and non-P&ID drawings.
- **One plant, one work directory, one graph.** Never put sheets from different plants in the same work directory: tags would merge across unrelated plants. If the user supplies several plants, run the whole workflow separately for each.
- **One configuration per graph.** If the PDF contains two revisions of the same drawing (same title or area, overlapping tags, e.g. an as-built and an older draft), do not merge them. Ask the user which revision to use, extract only that one, and record the excluded pages and the reason in the report. QA flags likely duplicates as `possible_duplicate_revision`. Record each sheet's `issue_status` from the title block or stamps.
- **Record only what is drawn.** Never invent tags, connections or loops to make the graph look complete. Anything unclear goes in with a lower `confidence`, or into `unreadable`.
- **The QA loop is not optional.** Rebuild until there are no errors, and re-check every warning on the drawing.

## Workflow

Copy this checklist into your notes and tick it off:

```
- [ ] 1. Probe:    python scripts/probe_pdf.py <pdf> --work <work> --plant-name "<name>" [--pages 47-60]
- [ ] 2. Render:   python scripts/render_pages.py <work>
- [ ] 3. Orient:   open each pages/page_NN/overview_grid.png; fix rotation if text is not upright
- [ ] 4. Hints:    python scripts/make_hints.py <work>
- [ ] 5. Extract:  for each sheet, write <work>/extract/page_NN.json (references/extraction_procedure.md)
- [ ] 6. Build:    python scripts/build_kg.py <work>
- [ ] 7. QA loop:  fix every error, re-check every warning, rebuild (repeat)
- [ ] 8. Report:   summarize the results and open issues for the user
```

### 1. Probe
`probe_pdf.py` assigns each page a class and an extraction route, and writes `<work>/manifest.json`. With `--pages`, the later steps render and read only those pages.

| Class | What it means | Route |
|---|---|---|
| `vector_text` | Vector drawing with a text layer | Render from vectors; exact text from the text layer as hints |
| `vector_outlined` | Vector drawing, text drawn as outlines (no text layer) | High-resolution vector render; OCR hints |
| `raster` | Scanned image | Native-resolution render, upscaled and contrast-enhanced; OCR hints |
| `raster_with_text` | Scan with an OCR text layer | As raster; text layer as (untrusted) hints |
| `hybrid` | Vectors plus large images | Both routes |

Report the probe result to the user in one line, e.g. "14 vector sheets with outlined text."

Low scan resolution is flagged in the notes. Expect to record more items in `unreadable` on those sheets.

### 2–3. Render and check orientation
`render_pages.py` writes the following for each page:

- `overview.png`
- `overview_grid.png`, which shows the tile names
- overlapping tiles in `tiles/`
- `tiles.json`, which records which tiles are blank

Orientation is detected with OCR when it is installed. Always confirm it on `overview_grid.png`. If the main drawing text is not upright, re-render that page with an explicit rotation, given clockwise: `render_pages.py <work> --pages N --rotation 90`.

Title blocks are sometimes rotated differently from the drawing. Orient by the drawing labels, not by the title block.

### 4. Hints
`make_hints.py` writes `hints/page_NN.json`. Each file holds candidate tags with page positions, taken from the text layer or from OCR. They are only hints: OCR misreads, and it misses things. You don't need to read the hint files during extraction. QA uses them to flag tags you may have missed. If OCR is not installed the step is skipped; note this in the final report.

### 5. Extract each sheet
This is the core of the job. Follow **[references/extraction_procedure.md](references/extraction_procedure.md)** exactly. It covers:

- the reading order: overview, then every non-blank tile, then zoomed crops
- how to model pipe runs, tees, taps, signals and off-page connectors
- confidence calibration
- a self-check list to run before saving

Reference material, to read when needed:

- [references/isa_5_1.md](references/isa_5_1.md): instrument letter codes, bubble symbols, signal line types
- [references/symbol_guide.md](references/symbol_guide.md): how equipment and valve symbols map to `kind` values
- [references/ontology.md](references/ontology.md): the graph's node and edge types and how they are derived
- `references/schema/extraction.schema.json`: the exact JSON schema of a page file

Write `extract/page_NN.json` and save it before starting the next sheet, so a long job never holds more than one sheet in context. With many sheets, and if your environment supports subagents, you can extract sheets in parallel. Give each subagent the procedure file and its own page directory.

### 6–7. Build and the QA loop
`build_kg.py` validates every page file and stops with a precise message on schema errors. It then writes these files to `<work>/kg/`:

- `graph.json`
- `graph.duckdb`
- `summary.md`
- `qa_report.md`

Work through `qa_report.md`:

- **Errors**, such as `unresolved_reference`, are mistakes in the page files. Fix them and rebuild.
- **Warnings** name the tiles to re-check. Look at those tiles again, or use `crop.py` for a zoomed view, and correct the extraction if the drawing shows something different. Common warnings:
  - `instrument_not_located`: a sensor with no `measures`
  - `equipment_not_connected`
  - `unmatched_off_page`
  - `possible_missed_tags`: an OCR tag that is not in your extraction
  - `tiles_not_reviewed`
- A warning that turns out correct on the drawing is fine to leave. Examples: an off-page connector whose other drawing was not supplied, or an OCR misread. List these in your report.

Stop when there are no errors and every warning has been checked.

```bash
python scripts/crop.py <work> --page 5 --bbox 0.40 0.20 0.55 0.35   # zoomed view of a region
```

### 8. Report
Tell the user:

- where the outputs are
- the headline counts (equipment, instruments, loops)
- two or three example flow paths and loops taken from `summary.md`
- what remains uncertain

Point to `qa_report.md` for the details. State plainly that the graph is machine-extracted and needs engineering review before it is used for design, operations or safety.

## Using the graph

- `summary.md` is the compact, token-efficient context for an LLM: equipment-level flow, an instrument table with locations, and a loop table.
- `graph.json` is the canonical graph, which any tool can read.
- `graph.duckdb` is for SQL. Its views are `equipment`, `equipment_flow`, `instruments`, `loops` and `signals`, and its table macros are `upstream(id)` and `downstream(id)`.

Use `kg_query.py` to answer questions; add `--json` when another tool will consume the output:

```bash
python scripts/kg_query.py <work>/kg downstream 660-TK-001 --equipment
python scripts/kg_query.py <work>/kg upstream FV-0502
python scripts/kg_query.py <work>/kg path 660-TK-001 660-TK-004
python scripts/kg_query.py <work>/kg instruments --on 660-PP-011
python scripts/kg_query.py <work>/kg loop FIC-0502
python scripts/kg_query.py <work>/kg sql "SELECT * FROM equipment_flow"
```

To measure extraction quality on a sheet, hand-check it into a small gold file (format in `scripts/eval_kg.py`) and run `python scripts/eval_kg.py <work>/kg gold.json`: it reports tag, flow and loop precision/recall and instrument placement.

To move a graph into other tools: `python scripts/export.py <work>/kg graphml` produces a file for yEd, Gephi or NetworkX, and `python scripts/export.py <work>/kg neo4j` produces CSVs plus a Cypher import script.
