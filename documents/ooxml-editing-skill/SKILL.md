---
name: ooxml-editing-skill
description: >-
  Surgical OOXML edits — unpack DOCX/PPTX/XLSX to XML, edit elements, validate,
  repack ('fix typo on slide 4'); houses the html2pptx escape hatch. Not
  template slide generation.
license: Apache-2.0
compatibility: opencode
category: Office Utilities
---

## What I do

I provide **surgical OOXML editing** for any Office file (`.docx`, `.pptx`, `.xlsx`). Rather than regenerating an entire document, I unpack the zip, edit specific XML elements, validate the structure, and repack — preserving everything else exactly.

- **Unpack** any Office file to its XML parts (`unpack.py`)
- **Edit** individual XML elements (slide XML, document XML, workbook XML)
- **Validate** structural integrity before repacking (`validate.py` + `validators/`)
- **Clean** unreferenced files from unpacked dirs (`clean.py`)
- **Pack** the edited XML back into a valid Office file (`pack.py`)

I also house the **html2pptx escape hatch** — explicit "convert HTML to PPTX" requests only. This path is undocumented in the orchestrator's default routing and is surfaced only when the user explicitly says "convert HTML to PowerPoint".

## When to use me

Use this skill when the user wants:
- "Fix typo on slide 4" / "change this specific text" — surgical edits
- "Update this chart's data" — targeted XML modification
- "Remove slide 3" — structural edit
- "Change this shape's fill color" — property edit
- "Convert HTML to PPTX" (explicit escape hatch — follows the hidden-JSON approach: html2pptx → generate-template → generate-slide)

Do NOT use me for:
- Template-based slide generation → `pptx-generate-slide-skill`
- Template extraction/embedding → `pptx-generate-template-skill`
- Template extension (cloning layouts) → `pptx-template-modifier-skill`
- Visual analysis / thumbnails → `office-thumbnail-skill`

## Prerequisites

- **Python 3.9+** with `defusedxml` for secure XML parsing
- **LibreOffice** (`soffice`) — only needed by some validators for render-checking; not required for basic unpack/pack
- For the html2pptx escape hatch only: **Node.js** + `pptxgenjs` + `playwright` + `sharp` (not needed for pure OOXML editing)

## Workflow

1. **Unpack** the Office file to a working directory:
   ```bash
   python scripts/unpack.py presentation.pptx unpacked/
   ```

2. **Edit** the XML files in `unpacked/` (primarily `ppt/slides/slide{N}.xml`, `word/document.xml`, or `xl/worksheets/sheet{N}.xml`)

3. **Validate** after each edit:
   ```bash
   python scripts/validate.py unpacked/ --original presentation.pptx
   ```

4. **Clean** unreferenced files (optional):
   ```bash
   python scripts/clean.py unpacked/
   ```

5. **Pack** back to an Office file:
   ```bash
   python scripts/pack.py unpacked/ new_presentation.pptx
   ```

## Scripts

| Script | Purpose |
|--------|---------|
| `unpack.py` | Extract Office zip → pretty-printed XML files |
| `pack.py` | Validate + condense XML → create Office zip |
| `validate.py` | Validate XML structure against OOXML rules |
| `clean.py` | Remove unreferenced files from unpacked dir |
| `validators/base.py` | Shared validation logic |
| `validators/pptx.py` | PPTX-specific OOXML rules |

## html2pptx Escape Hatch

For explicit "convert HTML to PPTX" requests only. The Node-based html2pptx toolchain (`pptxgenjs` + `playwright`) produces a basic PPTX from HTML slides. Per BT-142, this output then flows through `pptx-generate-template-skill` (extract + embed hidden JSON) → `pptx-generate-slide-skill` (final render against Slide Master) to ensure the hidden-JSON-template approach is followed.

This path is intentionally undocumented in the orchestrator's default routing — it's surfaced only when the user explicitly says "convert HTML to PowerPoint" or similar.
