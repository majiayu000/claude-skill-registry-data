---
name: pdf
description: Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables/formulas from PDFs (including scanned and photographed documents), OCR, combining or merging multiple PDFs, splitting, rotating, watermarking, creating new PDFs, encrypting/decrypting, and extracting images. Routes between pypdf (fast born-digital text), pdfplumber (tables), opendataloader-pdf (born-digital complex layout with optional Docling hybrid), and LightOnOCR-2-1B (vision-LM OCR for scanned/photographed docs; dolphin v2 fallback). If the user mentions a .pdf file or asks to produce one, use this skill.
license: MIT (repository license)
---

# PDF Skill — Unified Extraction and Manipulation

One auto-triggered entry point for all PDF work. The skill probes the PDF first, then routes to the cheapest sufficient backend. GPU OCR (LightOnOCR-2-1B, ~3 GB VRAM) is reserved for scans; dolphin v2 remains as fallback.

## Step 1 — Probe first (ALWAYS)

Run this before any other PDF action:

```bash
python ~/.claude/skills/pdf/scripts/probe_pdf.py <input.pdf>
```

The probe returns JSON with:
- `classification`: one of `encrypted`, `scanned`, `born_digital_footnotes`, `born_digital_simple`, `born_digital_formulas`, `born_digital_tables`, `born_digital_complex`, `uncertain`, `error`
- `formula_density`: fraction of sampled pages carrying a math signal (math fonts such as CMMI/CMSY/CMEX, or math glyphs). Above `0.2` the PDF is classified `born_digital_formulas` and must be routed to a LaTeX-capable backend.
- `footnote_density`: fraction of sampled pages that look footnote-bearing. At/above `0.5` the PDF is classified `born_digital_footnotes` and routed to Docling-direct, which reconstructs footnotes (and emits formula LaTeX) — opendataloader-pdf discards footnote structure.
- `recommended_backend`: one of `halt_password_required`, `lightonocr`, `docling`, `pypdf`, `pdfplumber`, `opendataloader_hybrid`, `opendataloader_then_lightonocr`, `fallback` (`docling` drives `scripts/docling_extract.py`, the footnote-and-formula-aware path; `lightonocr` drives `scripts/lightonocr_run.py`)
- `reasoning`: one-sentence rationale
- `warnings`: list of strings; non-empty when a density-measurement helper (pdfplumber image/table probes) failed. When present, the classifier will not return `born_digital_simple` even if other signals look clean.

Cost: ~1 second, no GPU. Use the result to pick the next step.

## Step 2 — Route by task

### A. The user wants to READ / EXTRACT content from a PDF

Read `extraction.md`. Follow its decision tree based on the probe's `classification`:

| Classification | Backend |
|---|---|
| `encrypted` | Halt; ask the user for a password; re-probe. |
| `scanned` | `scripts/lightonocr_run.py` (GPU, ~3 GB VRAM, ~1–2 s/page, LaTeX-aware). Fallback: `dolphin` (7.5 GB VRAM, ~10 s/page). |
| `born_digital_footnotes` | `scripts/docling_extract.py` — footnote-aware (inlines each footnote at its reference point as a pandoc inline footnote `^[…]`, and routes any note whose marker cannot be located to an `## Endnotes` section so nothing is dropped) **and** formula-aware (LaTeX). The right path for academic papers (math or not). Then run `sanitize_math.py`. **See `extraction.md` §"Footnotes + academic papers → Docling".** |
| `born_digital_simple` | `pypdf.extract_text()` (instant). |
| `born_digital_formulas` | `opendataloader-pdf --hybrid docling-fast` **with `--enrich-formula`** (emits equations as LaTeX), OR `docling_extract.py` if footnotes also matter. Escalate to `lightonocr` if equations are images. **See `extraction.md` §"Math-heavy → LaTeX".** |
| `born_digital_tables` | `pdfplumber.extract_tables()`. |
| `born_digital_complex` | `opendataloader-pdf --hybrid docling-fast`. |
| `uncertain` | `opendataloader-pdf` first; escalate to `lightonocr` if output is empty or has high `(cid:N)` ratio. |

User override hints take precedence over the probe:
- `"OCR this"` / `"scanned"` → force lightonocr; `"use dolphin"` → force dolphin (legacy backend, still installed)
- `"tables only"` / `"extract rows"` → force pdfplumber + opendataloader
- `"formulas"` / `"equations"` / `"math"` / `"keep the LaTeX"` → `born_digital_formulas` path: opendataloader `--enrich-formula` (always add `--restart-backend` so the flag actually applies), or lightonocr if scanned. Do NOT use pypdf/pdfplumber — they drop equations.
- `"footnotes"` / `"keep the footnotes"` / `"academic paper"` / `"law review"` / `"journal article"` → `scripts/docling_extract.py` (footnote + formula aware). Do NOT use opendataloader/pypdf — they jumble or drop footnotes.
- `"fast"` / `"quick text"` → force pypdf
- `"light mode"` / `"no hand repair"` / `"just the raw extraction"` → run the probe-selected backend plus the deterministic post-processors (`clean_garbled_fragments.py`, `sanitize_math.py`), then run `verify_extraction.py` **report-only** (see Verification) and stop. Do NOT run the §4C render-and-rewrite repair loop.

### B. The user wants to MANIPULATE a PDF

(merge / split / rotate / watermark / encrypt / extract images / create new)

Read `manipulation.md`. Uses pypdf, qpdf, pdfimages, reportlab.

### C. The user wants to FILL a PDF FORM

Form filling is not included in this distribution. Anthropic's own document-skills `pdf` plugin ships a form-filling toolchain; install and use that instead.

### D. The user needs JavaScript libs, pypdfium2, or performance optimization

Not covered in this distribution. Anthropic's document-skills `pdf` plugin carries the detailed pypdf/pypdfium2/JavaScript reference; consult that, or the libraries' own documentation.

### E. The user wants ANNOTATIONS (reviewer comments, highlights, sticky notes)

Skip the content-extraction backends entirely — comments live in the PDF annotation layer, which none of them read. Run:

```bash
python ~/.claude/skills/pdf/scripts/extract_annotations.py <input.pdf> [output.md]
```

Emits one Markdown entry per annotation: page, type, author, comment text, the marked (highlighted) span, and the full surrounding paragraph as context. Link/Popup/Widget annotations are filtered out (hyperref PDFs otherwise yield hundreds of junk entries). The marked-span text is noisy by nature (overlapping quadpoints); quote from the clean `Context` field.

## Quick reference

| Task | Backend | When |
| ---- | ------- | ---- |
| Quick text dump | pypdf | Born-digital, no tables |
| Tables | pdfplumber | Born-digital, table-heavy |
| Markdown with structure | opendataloader-pdf hybrid | Complex born-digital layouts |
| Scanned / photographed | `scripts/lightonocr_run.py` | GPU, ~3 GB VRAM, LaTeX-aware |
| OCR fallback (GPU) | dolphin | LightOnOCR unavailable, or element/layout modes needed |
| Merge / split / rotate | pypdf or qpdf | Manipulation |
| Reviewer comments / highlights | `scripts/extract_annotations.py` (PyMuPDF) | Annotated manuscripts |
| Create from scratch | reportlab | Generation |
| OCR fallback (no GPU available) | pytesseract + pdf2image | When dolphin unavailable |

## Verification (run after every extraction)

**Run the executable gate first** — it catches the silent failures the manual checks below rely on you noticing:

```
python ~/.claude/skills/pdf/scripts/verify_extraction.py <out.md> --probe <probe.json>
```

It flags, with line numbers, the three failure modes that look plausible but are wrong on born-digital academic papers (finance/econ articles especially): Docling **merging dense table rows** into one cell, the formula model **flattening or garbling equations** (including `\intertext` debris from multi-line/cases equations), and **stray private-use glyphs**. Exit 1 = issues to fix before shipping. The repair for a flagged table or equation is the same: render that page region (`render_region.py`), read it, and rewrite the block from the image (`extraction.md` §4C), then re-run the gate until clean. A clean report plus the checks below = done.

**Light mode** (user said "light mode" / "no hand repair"): still run the gate — it is a ~1 s deterministic script — but treat it as **report-only**. Surface the flagged line numbers to the user as known defects and ship the output as-is; do not enter the render-and-rewrite loop. The user can then ask for repair of just the blocks they care about.

- Output length sane (proportional to page count).
- No high `(cid:N)` ratio in the result.
- Tables (if any) preserved as structure, not flattened text.
- Special characters (Greek, math symbols) extracted, not replaced with `?`.
- For `born_digital_formulas`: the output actually contains LaTeX (`$$…$$`, `\frac`, `\sum`, `\alpha`, …). If `formula_density` was high but no LaTeX appears, the `--enrich-formula` flag did not apply — re-run the converter with `--restart-backend`, or escalate to lightonocr.
- For lightonocr and dolphin: confirm `VRAM released: X MB remaining` line in the run output. If missing, find the orphaned OCR process and kill ONLY that PID — never blanket-kill python (other GPU jobs and pipelines may be running):

  **PowerShell variant** (Windows native):
  ```powershell
  nvidia-smi --query-compute-apps=pid,process_name --format=csv,noheader
  Get-CimInstance Win32_Process -Filter "ProcessId = <pid>" | Select-Object CommandLine  # confirm it's the OCR worker
  Stop-Process -Id <pid> -Force
  nvidia-smi --query-gpu=memory.used,memory.free --format=csv
  ```

  **Bash variant** (Git Bash / WSL / Linux):
  ```bash
  nvidia-smi --query-compute-apps=pid,name --format=csv,noheader
  ps -p <pid> -o args=   # confirm it's the OCR worker, not another GPU job
  kill -9 <pid>
  nvidia-smi --query-gpu=memory.used,memory.free --format=csv
  ```

## Scripts directory

All scripts live in `scripts/`:

- `probe_pdf.py` — classifier (run first)
- `render_region.py` — render a page or `--bbox` region to PNG so a gate-flagged table or equation can be read back and rewritten by hand. The general repair for any mangled table (numeric grid, multi-panel, or prose+math definitions) and any broken equation — one approach, no per-table tuning. Auto-suggested by the gate; see `extraction.md` §4C
- `verify_extraction.py` — post-extraction quality gate (run last). Flags merged/spilled table rows, broken/flattened equations (`\intertext` debris, empty `$$`, display math left as plain text), and stray private-use glyphs, each with a line number and a fix pointer. `--probe probe.json` enables the formula-density-aware equation check. Exit 1 = issues. See `extraction.md` §8
- `opendataloader_convert.py` — wrapper with tqdm progress bar + probe integration. Post-processes the Markdown: strips garbled figure text (`--no-clean-fragments`) and makes math KaTeX-safe (`--no-sanitize-math`)
- `clean_garbled_fragments.py` — removes leaked vector-figure label fragments from extracted Markdown, and strips whole lines that are only private-use glyphs (e.g. a leaked `cases`-environment brace stranded above a `$$` block), protecting LaTeX/tables/prose (run standalone on any `.md`)
- `sanitize_math.py` — wraps leaked equation alignment in `\begin{aligned}` and suppresses blocks the KaTeX engine can't render, so no parse-error string reaches a renderer (run standalone on any `.md`)
- `katex_validate.js` — Node helper that batch-validates LaTeX with the real KaTeX engine (oracle behind `sanitize_math.py`)
- `vendor/katex.min.js` — single-file KaTeX bundle vendored with the skill so math validation works across machines (with Node) without an npm install or a `node_modules` directory in a synced config folder
- `docling_extract.py` — Docling-direct extraction for academic papers: inlines each footnote at its reference point as a pandoc inline footnote (`text^[note body]`), routes notes whose marker cannot be located to an `## Endnotes` section (preserved through pandoc), and emits formula LaTeX. Used for `born_digital_footnotes`; run `sanitize_math.py` on its output
- `extract_figures.py` — recovers vector/raster figures Docling drops (it only detects embedded-raster pictures) by rendering each figure page to a cropped PNG; with `--link-md` inserts them at their captions and de-duplicates Docling's doubled caption lines. See `extraction.md` §4C
- `lightonocr_run.py` — LightOnOCR-2-1B OCR: scanned PDF (or image) → Markdown with LaTeX math. Primary OCR backend; re-execs itself under the `~/LightOnOCR/venv` (override: `LIGHTONOCR_DIR`), VRAM pre-check + release marker
- `dolphin_run.py` — wrapper that activates the Dolphin venv and runs demo scripts (fallback OCR; element/layout modes)

## Related skills

- `markdown-to-pdf` — converting a Markdown (`.md`) file INTO a PDF (pandoc → HTML + print CSS → headless Chrome, images preserved and scaled). Route "save this markdown as a PDF" requests there, not through reportlab.
- `latex-from-mixed-sources` — patterns for combining extracted PDF text with LLM-generated text into a `.tex` document. Read this AFTER extracting text if you're building a LaTeX manuscript.
- `manuscript-editing-template-latex` — docx ↔ LaTeX round-tripping pipeline.
