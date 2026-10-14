---
name: docx-creation-skill
description: >-
  Create, read, edit Word (.docx) — TOCs, headings, letterheads, tracked
  changes, comments, images; report/memo/letter/template deliverables. Not PDFs,
  spreadsheets, or Google Docs.
license: Apache-2.0
compatibility: opencode
category: Framework
---

## What I do

- Create new .docx via docx-js; read via pandoc or raw XML; edit by unpack → modify XML → repack
- Tracked changes (insertions/deletions), comments, images, tables, TOCs, letterheads
- Convert .doc→.docx, .docx→PDF, .docx→images

**Use for:** "Word doc" / .docx mentions; reports, memos, letters, templates; tracked-changes review.
**NOT for:** PDFs, spreadsheets, Google Docs, unrelated coding.

## Prerequisites

pandoc (extraction) · `npm install -g docx` (creation) · LibreOffice via `scripts/soffice.py` (PDF) · Poppler `pdftoppm` (images)

## House scripts

```bash
python scripts/soffice.py --headless --convert-to docx document.doc   # legacy .doc → .docx
pandoc --track-changes=all document.docx -o output.md                 # read incl. tracked changes
python scripts/unpack.py document.docx unpacked/                      # raw XML access
python scripts/accept_changes.py input.docx output.docx               # accept all tracked changes
python scripts/soffice.py --headless --convert-to pdf document.docx && pdftoppm -jpeg -r 150 document.pdf page
```

## Creating new documents (docx-js) — critical rules

Full code patterns: [`reference.md`](reference.md) (setup, styles, numbering, tables, images, hyperlinks, TOC, headers/footers).

- **Set page size explicitly** — docx-js defaults to A4; US Letter = 12240 × 15840 DXA (1440 DXA = 1″)
- **Never `\n`** — separate `Paragraph` elements
- **Never unicode bullets** — `numbering.config` with `LevelFormat.BULLET`; same reference continues numbering, different reference restarts
- **`PageBreak` must sit inside a `Paragraph`** — standalone is invalid XML
- **`ImageRun` requires `type`** (png/jpg/…) and `altText` with title+description+name
- **Tables: dual widths** — `columnWidths` array AND per-cell `width`, both DXA, summing to table width; `WidthType.DXA` only (percentages break in Google Docs)
- **`ShadingType.CLEAR`**, never SOLID (black backgrounds)
- **TOC requires `HeadingLevel` only** — override built-in styles by exact ID (`"Heading1"`) and include `outlineLevel` (0 for H1), else TOC won't generate

Validate after creation: `python scripts/validate.py doc.docx` — on failure, unpack, fix XML, repack.

## Editing existing documents — 3 steps, in order

1. `python scripts/unpack.py document.docx unpacked/` (pretty-prints, merges runs)
2. Edit `unpacked/word/*.xml` — patterns in [`reference.md`](reference.md) (tracked changes, comments, images, element order)
3. `python scripts/pack.py unpacked/ output.docx --original document.docx` (validates + auto-repairs)

House rules: tracked-change/comment author = **"Claude"** unless the user names another; smart quotes via XML entities (`&#x2019;` `&#x201C;` `&#x201D;`) for new content.

## Design aesthetics — no generic AI slop

Documents must look designed, not generated. Avoid: Word-gallery defaults (blue headings, Calibri-everything), identical cookie-cutter sections, one font size throughout, equal-width thin-bordered tables, default blue/gray, unbroken walls of text, uneven spacing.

Every document gets ≥1 signature element: 3+ levels of typographic hierarchy (title 28–36pt bold / H1 20–24 / H2 16–18 / body 11–12), 1–2 consistent accent colors, styled table headers (fill + white text, horizontal borders only), pull quotes/callout boxes, generous whitespace (1–1.5″ margins), non-blank header/footer.

Before formatting ask: what is this document's visual identity, what should the reader feel, would a designer approve? (Per-type styling table in [`reference.md`](reference.md).)

## Verification

`validate.py` passes · opens in Word/LibreOffice clean · page size correct · tables/images/TOC/headers render · tracked changes visible in review pane.
