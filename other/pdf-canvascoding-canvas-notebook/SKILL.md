---
name: pdf
description: "Use this Canvas-owned clean-room skill for PDF work where layout, extraction, generation, forms, page operations, or visual verification matter. Trigger for reading PDFs beyond plain text, creating PDFs, merging, splitting, rotating, watermarking, extracting tables or images, filling forms, OCR handoff, and final PDF QA."
license: "Canvas Notebook Sustainable Use License"
---

# PDF Workflows

This skill covers PDF creation, inspection, extraction, page operations, forms,
and visual QA in Canvas Notebook. It is a clean-room Canvas skill; do not copy
vendor skill material, hidden prompts, or proprietary helper code into this
folder.

## Core Contract

- Use `CANVAS_AGENT_TEMP_DIR` for scripts, working copies, extracted assets,
  page renderings, and validation output. Promote only the requested final PDF
  to the workspace with `copy_path` or `move_path`.
- Treat rendered pages as the source of truth for layout-sensitive tasks.
- Use text extraction for content discovery, not as proof that a PDF looks
  correct.
- Keep source PDFs immutable unless the user explicitly asks to overwrite them.
- Return only the final requested artifact unless the user asks for extracted
  intermediates.
- Use deterministic scripts for repeated operations and keep those scripts in
  scratch unless the user explicitly requests them as deliverables.

## Recommended Tools

- `pypdf` for merge, split, rotate, metadata, encryption, simple form filling,
  and page-level operations.
- `pdfplumber` for text, coordinates, tables, and layout-aware inspection.
- The Canvas PDF gateway, when exposed in the active runtime, for supported PDF
  operations. Discover it with `search`, inspect the selected operation with
  `describe`, then use `call`.
- HTML plus bundled headless Chromium for creating new PDFs when no suitable
  gateway operation exists.
- Poppler tools such as `pdfinfo`, `pdftoppm`, and `pdftocairo` for rendering
  and page diagnostics.
- OCR tools only when available and required; if OCR dependencies are missing,
  explain the blocker instead of pretending scanned text was read.

## Workflow

1. Classify the task: read/review, generate, page operation, form filling,
   extraction, redaction, OCR, or repair.
2. Make a working copy for destructive operations.
3. Use the simplest reliable library for the operation. Avoid manipulating raw
   PDF bytes manually.
4. Render updated pages to PNG and inspect alignment, margins, clipping,
   legibility, form values, signatures/watermarks, and page order.
5. If a visual issue appears, repair the source operation and re-render.

## Common Tasks

- **Extract text:** start with `pdfplumber`; preserve page numbers and note
  extraction uncertainty for scanned or complex PDFs.
- **Extract tables:** use `pdfplumber` table strategies and validate against
  rendered pages.
- **Create a PDF:** use a supported PDF gateway operation or generate structured
  HTML and print it with headless Chromium; define margins, fonts, section
  hierarchy, tables, and pagination explicitly.
- **Merge or split:** use `pypdf`; verify page count and order with `pdfinfo`
  and rendered thumbnails.
- **Fill forms:** inspect AcroForm fields first, write a copy, flatten only if
  requested or necessary, then render filled pages.
- **Redact:** do not cover text with a black rectangle alone. Remove or rewrite
  underlying content where possible, then verify extraction and rendering.

## Final Checks

- Latest rendered pages match the requested content and order.
- Text is readable at normal zoom and no content is clipped.
- Page size, orientation, margins, headers, footers, and numbering are correct.
- Any extraction, OCR, or redaction limitations are stated clearly.
