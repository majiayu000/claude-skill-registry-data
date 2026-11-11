---
name: precision-pdf-editing
description: "Makes surgical edits to an existing PDF (change every value in one table column, fix a few labels, replace text in fixed cells) while keeping page geometry, fonts, highlights, images, metadata and every unrelated pixel unchanged, then proves it with a mapping CSV, a pixel diff outside the edit masks and rendered before/after checks. Use when someone says 'add 150 to every price in this PDF', 'change these numbers but keep the layout', 'edit the PDF without regenerating it', or when a natural-language PDF editor would be too loose. Needs Python with PyMuPDF; works in Claude Code or any environment that can run Python."
---

# Precision PDF Editing

Change a few values in a PDF without rebuilding it, and prove nothing else moved.

Do not regenerate pages or tables when the user needs everything else untouched:
regeneration changes fonts, wrapping, image encoding and unrelated pixels.

## Requirements

- Python 3 with `pip install pymupdf numpy` (the bundled script uses both).
- Optional but recommended: `qpdf` (structural check) and Poppler (`pdftotext`, `pdftoppm`, `pdfinfo`).
- If PyMuPDF cannot be installed, stop and say so. Do not fall back to an
  "AI PDF editor" or to regenerating the document.

## Inputs to confirm first

1. The source PDF, and an output path (never overwrite the source).
2. Exactly which cells change: column header text, pages, and the transform
   (for example "add 150", "replace X with Y"). Ask if the column is ambiguous.
3. Number format rules: thousands separator, decimals, currency symbol.

## Steps

1. **Preserve and fingerprint the source.** Record SHA-256, page count, page
   rects and rotation, metadata, fonts (`page.get_fonts()`), image list. Run
   `qpdf --check src.pdf` so pre-existing defects are not blamed on you.
2. **Inspect.** Render every page at 150 to 300 dpi (`pdftoppm -r 200 -png`)
   and look at them. Dump `page.get_text("words")` and find the header's x-range.
   Identify the column by header text AND geometry: right-aligned values share a
   right edge. If text extraction order disagrees with the picture, trust the picture.
3. **Enumerate target cells** with the script (character-level boxes, not span boxes):
   ```bash
   python scripts/pdf_cells.py cells src.pdf --x0 250 --x1 360 --add 150 > manifest.json
   ```
   Without `--add`, each cell's `"new"` is null: fill it in yourself. Check the
   printed count against the number of rows you can see on the renders, page by
   page. Every target must appear once, nothing else may appear.
4. **Review the manifest**: old/new values, `fill` (background colour under the
   cell, null = white), font, size, colour. Integer arithmetic only; format to the
   source convention (`--thousands auto|comma|none`; `auto` copies each cell, so
   `980 + 150` gives `1130`, which may break the column's style).
5. **Apply:**
   ```bash
   python scripts/pdf_cells.py apply src.pdf out.pdf manifest.json
   ```
   It redacts only the union of old and new glyph boxes using the cell's own
   fill colour, keeps images and vector graphics, writes the new value on the
   same baseline and right edge, reuses the embedded font (or the same base-14
   font), and restores metadata with `no_new_id`.
6. **Verify** (all must pass, see `references/verification.md`):
   ```bash
   python scripts/pdf_cells.py diff src.pdf out.pdf manifest.json --dpi 150
   ```
   Exit 0 means zero changed pixels outside the edit masks. Then run
   `qpdf --check out.pdf`, `pdftotext -layout out.pdf -` (every new value decodes
   once, at the right row), and compare `pdfinfo` for both files.
7. **Look at it.** Render the full pages and zoom each edited region. Check
   background continuity, gridlines, clipping, leftover old glyphs, baseline and
   weight. A pixel diff of zero outside the masks says nothing about what is
   inside them.

## Decision rules

- **Font fallback reported** (`font_fallbacks` not empty): the embedded font is a
  subset missing a glyph you need (common when a new digit never appeared in the
  original). Tell the user; options are a matching full font file they supply, or
  accepting the substitute. Never ship a fallback silently.
- **Fill not null:** the row is highlighted. The redaction must use that colour.
  A white patch on a coloured row is a defect even when every other check passes.
- **Duplicate or skipped printed row numbers:** keep them as they are; tell rows
  apart by product text and y-position. Do not "fix" source numbering.
- **Count mismatch** between manifest and visible rows: stop and narrow the
  x-range or pattern. Never apply a manifest you have not reconciled.
- **Rotated pages, scanned images or text drawn as vector outlines:** the script
  cannot edit these. Say so; scanned pages need OCR plus an image patch, which is
  a different job.

## Output

Deliver the edited PDF plus an audit folder:

```
out.pdf
audit/mapping.csv          page,row_id,context,old,new,edit_bbox
audit/manifest.json        full geometry and styling per cell
audit/diff.json            output of the diff command
audit/renders/             source and output pages, zooms of edited regions
audit/REPORT.md            counts, hashes, checks run, anything ambiguous
```

Example REPORT.md summary:

```
Edited 111 cells (68 on p1, 43 on p2), Price column, old + 150.
Outside-mask changed pixels: 0 on both pages (150 dpi, 3 px pad).
qpdf --check: OK. Page sizes, rotation, metadata, trailer /ID: unchanged.
Font: embedded Calibri reused, no fallback.
Note: source prints row 97 twice and skips 98; both kept, told apart by product.
```

## Pitfalls

- Span boxes include alignment spaces and produce oversized redactions. Use character boxes (the script does).
- Comparing full word tuples after editing fails because block/line ids renumber. Compare text plus bbox.
- Text-only checks miss white patches; pixel-only checks miss wrong values. Do both.

See `references/worked-example.md` for a full two-page price-list walkthrough.
