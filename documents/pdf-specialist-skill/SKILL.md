---
name: pdf-specialist-skill
description: >-
  Create, read, edit, analyze PDFs — forms, OCR, merge, split, convert,
  watermark, encryption, image extraction. Any PDF/.pdf mention. Not Word or
  spreadsheets.
license: Apache-2.0
compatibility: opencode
category: Framework
---

## What I do

- Extract text and tables (pdfplumber / `pdftotext`); merge, split, rotate, watermark, encrypt (pypdf / qpdf)
- Fill forms — fillable AcroForm fields via pypdf; non-fillable via text annotations with validated coordinates
- Create PDFs from scratch (reportlab); convert pages to/from images (poppler-utils); OCR scanned PDFs (pytesseract)

**Routing:** tier 4 of the office-doc extraction ladder — structured PDF data (forms, fillable fields, OCR-as-purpose) escalates here after markitdown/docling/image-analyzer prove insufficient.
**Use for:** any PDF/.pdf mention.
**NOT for:** Word documents (.docx → docx-creation-skill), spreadsheets (Excel/CSV), coding unrelated to PDFs.

## Prerequisites

`pip install pypdf pdfplumber reportlab pdf2image pytesseract` · poppler-utils + qpdf (`sudo apt-get install poppler-utils qpdf`; macOS `brew install poppler qpdf`; Windows `winget install` or WSL) · LibreOffice via `scripts/soffice.py` (auto-configured on first run)

## Tool chain — house rules

| Task | Tool | House rule |
|------|------|------------|
| Merge/split/rotate/metadata/encrypt | pypdf (or qpdf CLI) | pypdf page indices are **0-based** |
| Text/table extraction | pdfplumber | preserves layout; coordinates `(x0, top, x1, bottom)` with **y=0 at TOP** of page |
| Create from scratch | reportlab | platypus flowables, not raw canvas, for multi-page docs |
| Batch CLI ops | qpdf, poppler-utils | `pdftotext -layout` preserves layout; `pdfimages` beats page rendering for image extraction |
| OCR | pytesseract + pdf2image | first resort when extraction returns garbage, `(cid:X)`, or empty text |
| Forms | house scripts below | never fill with unvalidated coordinates |

Per-task code recipes, JSON schemas, and CLI option catalogs: [`reference.md`](reference.md).

## House scripts

```bash
python scripts/check_fillable_fields.py <file.pdf>                    # branch point for form filling
python scripts/extract_form_field_info.py <in.pdf> <field_info.json>  # fillable-PDF field inventory
python scripts/extract_form_structure.py <in.pdf> form_structure.json # non-fillable structure (labels/lines/boxes)
python scripts/convert_pdf_to_images.py <file.pdf> <outdir/>          # also the verification pass
python scripts/check_bounding_boxes.py fields.json                    # validate boxes BEFORE filling
python scripts/fill_fillable_fields.py <in.pdf> <values.json> <out.pdf>
python scripts/fill_pdf_form_with_annotations.py <in.pdf> fields.json <out.pdf>
python scripts/soffice.py --headless --convert-to pdf document.docx    # LibreOffice conversions
```

## Reading / extraction workflow

1. Try `pdftotext -layout` (fastest plain text) or pdfplumber (coordinates, tables).
2. Garbage / `(cid:X)` / empty output → scanned PDF → OCR via pytesseract + pdf2image.
3. Tables → pdfplumber `extract_tables()` → DataFrames; adjust `snap_tolerance` / `intersection_tolerance` for complex layouts.

Gotchas: pypdf `extract_text()` loses layout — prefer pdfplumber when structure matters. Encrypted: `reader.is_encrypted` → `reader.decrypt(pw)`, or `qpdf --password=… --decrypt`. Corrupted: `qpdf --check` / `qpdf --fix-qdf`. Large files: process pages individually. Code patterns: [`reference.md`](reference.md).

## Creation workflow (reportlab)

- Use platypus (`SimpleDocTemplate` + `Paragraph` story) for anything multi-page; raw `canvas` only for one-off drawing.
- **Never Unicode sub/superscript characters (₀₁₂…, ⁰¹²…) — built-in fonts lack the glyphs and render as solid black boxes.** Use `<sub>`/`<super>` markup tags inside `Paragraph`; for canvas-drawn text, adjust font size and position manually.

Setup, styles, and multi-page patterns: [`reference.md`](reference.md).

## Form filling — complete these steps in order, do not skip ahead

1. `python scripts/check_fillable_fields.py <file.pdf>` — its output branches the workflow:
   - Fillable → **2A** · Non-fillable → **2B**

### 2A Fillable fields

1. `extract_form_field_info.py` → `field_info.json`: `field_id`, 1-based `page`, `rect` ([left, bottom, right, top]), `type` (text/checkbox/radio_group/choice); checkboxes carry `checked_value`/`unchecked_value`, radios `radio_options`, choices `choice_options`.
2. `convert_pdf_to_images.py` → analyze images to determine each field's purpose (convert PDF rects to image coords as needed).
3. Author `field_values.json` — `field_id` and `page` must match field_info exactly; checkboxes use `checked_value`, radios one of `radio_options` values. Schema: reference.md.
4. `fill_fillable_fields.py` — fix any reported field errors and re-run.

### 2B Non-fillable (text annotations)

1. `extract_form_structure.py` → labels (with coordinates), lines, checkboxes, row_boundaries.
2. Meaningful labels → **Approach A (structure-based, preferred)**: entry x0 = label x1 + 5; entry x1 = next label's x0 or row boundary; top = label top; bottom = row boundary line below. Use `pdf_width`/`pdf_height` and coordinates directly from form_structure.json.
3. Scanned / no usable labels → **Approach B (visual estimation)**: convert to images, identify fields roughly, then **zoom-refine** — `magick page.png -crop <W>x<H>+<X>+<Y> +repage crop.png` (~50px padding; use `convert` if `magick` is absent). **Add crop offsets back**: full_x = crop_x + offset_x, full_y = crop_y + offset_y. Author fields.json with `image_width`/`image_height` pixel coordinates.
4. `check_bounding_boxes.py fields.json` — fix ALL intersecting boxes and too-small-for-font boxes before filling.
5. `fill_pdf_form_with_annotations.py` — auto-detects PDF-vs-image coordinate system.
6. **Verify:** `convert_pdf_to_images.py` on the filled output; check placement visually. Mispositioned → Approach A: PDF-point origin check; Approach B: image-dimension/pixel match.

## Verification

- Forms: `check_bounding_boxes.py` passes pre-fill; filled PDF re-imaged and visually checked
- Extraction: `pdftotext` round-trip returns expected text
- Creation: output opens clean; page count/size as specified

> Removed 2026-09: per-task Python/CLI recipe dumps, form-JSON schema examples, option catalogs, duplicated library-selection prose, LibreOffice install walkthrough, and common-issue restatements — moved to reference.md or deleted.
