---
name: pdf
description: Inspect, extract, create, combine, split, rotate, redact, OCR, or fill PDF files with provenance and visual validation. Use whenever PDF is the main input or deliverable; preserve originals, distinguish visual redaction from secure removal, and never break signatures or protections silently.
license: MIT
---

# PDF Workflow

## Inspect first

Record size, page count, version, encryption, permissions, signatures, page boxes/rotation, text-layer quality, fonts, images, attachments, forms, annotations, and whether pages are scanned. Use installed tools such as a PDF parser, renderer, OCR engine, or office converter; do not install dependencies implicitly.

## Route by task

- **Read/summarize:** extract text by page and visually inspect pages containing figures, tables, formulas, or suspicious extraction.
- **Tables:** compare text extraction with rendered layout; do not treat a visually aligned table as reliable rows until validated.
- **Scans/OCR:** preserve the original image, record language and OCR settings, and mark uncertain text.
- **Merge/split/rotate:** preserve page order, boxes, bookmarks, metadata, links, and forms when supported.
- **Create:** use a layout engine appropriate to the source, embed or license fonts correctly, and add document metadata/accessibility structure where supported.
- **Forms:** detect AcroForm versus XFA, preserve field names and appearances, and flatten only when requested.
- **Redaction:** remove underlying text/images and metadata, then verify by extraction and object inspection. Drawing a black rectangle is not secure redaction.

## Safety

- Write to a new output path and keep a backup.
- Do not bypass passwords or permissions without authority.
- Warn before an edit that invalidates a digital signature.
- Do not execute JavaScript, launch actions, attachments, or embedded content.
- Remove hidden metadata/attachments only when requested; they may be evidentiary.
- Do not send private PDFs to external OCR or conversion services without explicit authorization.

## Validation

Reopen the output, verify page count/order/rotation, render all affected pages, inspect text and form fields, check links/bookmarks/attachments, and confirm no corruption. For secure redaction, search extracted text, inspect content streams where possible, and test copy/paste. Report exact pages changed and any unsupported feature.
