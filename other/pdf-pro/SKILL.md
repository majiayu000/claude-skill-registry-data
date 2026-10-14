---
name: pdf-pro
description: Programmatic PDF work — creating, reading, merging, and filling PDFs — use when automating PDF generation or extraction.
category: document-processing
---

## Overview

PDFs are everywhere in business workflows: invoices, reports, contracts, forms.
Working with them programmatically means three distinct jobs — generating PDFs
from data, extracting text/structure from existing PDFs, and manipulating pages
(merge, split, rotate, watermark). This skill covers the patterns and library
choices for each, in any language ecosystem.

## When to use

- Generating invoices, reports, or certificates from application data
- Extracting text or tables from PDFs for processing or search
- Merging, splitting, rotating, or watermarking PDF pages
- Filling PDF form fields (AcroForms) programmatically
- Choosing between HTML-to-PDF, native libraries, and template engines

## Core concepts

**Generation strategies.** Three main approaches: (1) HTML/CSS → PDF renderers
(great when you already have web templates and want pixel control via CSS);
(2) native PDF libraries (precise, code-driven layout — best for complex
documents like financial statements); (3) template fill (take a designed PDF
and fill fields — best when design is fixed by someone else). Pick by who owns
the design and how dynamic the layout is.

**PDFs are a presentation format, not a data format.** Text extraction is
heuristic: PDFs store positioned glyphs, not paragraphs or tables. "Reading
order" must be reconstructed, and scanned PDFs are images requiring OCR first.
Always validate extraction against the visual document — especially for tables,
multi-column layouts, and numbers.

**Table extraction is its own problem.** Bordered tables extract reasonably via
line detection; borderless tables need whitespace analysis. Dedicated table
extractors beat generic text extraction. For critical data (financial figures),
build a verification step comparing extracted totals against known sums.

**Forms (AcroForms).** PDFs can carry named form fields; filling them
programmatically preserves the original design exactly. Check whether the PDF
has real fields (fillable) vs flat text that merely looks like a form —
the latter needs overlay text placement instead.

**Fonts and encoding.** Embed fonts when generating (viewers substitute
otherwise, breaking layout for non-Latin scripts). When extracting, know that
some PDFs use custom glyph encodings that produce garbage text — a sign to try
a different extractor or OCR.

## Practical workflow

1. **Classify the job:** generate / extract / manipulate / fill — each has
   different best tools.
2. **For generation:** build an HTML template with print CSS (page size,
   margins, page-break rules) if the design is web-friendly; use a native
   library when you need precise control (headers/footers, flowing tables
   across pages, barcodes).
3. **For extraction:** try text extraction first; check quality on tables and
   multi-column pages; fall back to OCR for scanned documents; add a
   sanity-check layer (row counts, checksums, regex validation of key fields).
4. **For manipulation:** use a page-level library for merge/split/rotate/
   watermark — these are byte-level operations that don't require re-rendering.
5. **For forms:** list field names first, then fill by name; flatten the form
   after filling if the result should be non-editable.
6. **Test with real documents,** not just the happy path — PDFs in the wild
   are malformed, huge, password-protected, or scanned; handle each case
   explicitly.

## Common pitfalls

- **Assuming text extraction preserves layout** — it doesn't; columns interleave,
  tables collapse. Verify, don't assume.
- **Generating PDFs without embedded fonts** — renders fine on your machine,
  breaks on the client's (especially CJK, Arabic, or emoji content).
- **Hardcoding coordinates for text overlay** — fragile across PDF versions;
  prefer named form fields or anchor-based placement.
- **Ignoring PDF/A for archival** — if documents must be archivable long-term,
  generate PDF/A (embedded fonts, no encryption) from the start.
- **Loading entire huge PDFs into memory** — stream or page-window large
  documents; a 2GB PDF will OOM a naive process.
- **Forgetting accessibility** — tagged PDFs matter for screen readers in
  regulated contexts; HTML-to-PDF pipelines can preserve semantic structure
  if built with it in mind.
