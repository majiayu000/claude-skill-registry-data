---
name: Tesseract OCR
description: Extract text from images and scanned PDFs via the local Tesseract binary.
requires:
  bins:
    - tesseract
  env: []
---

# Tesseract OCR

Local, offline OCR. Wraps the `tesseract` CLI. No API key, no upload.

## Use when

- "Read the text in this screenshot / photo"
- Extracting text from scanned documents (PDF images)
- Processing receipts / handwritten notes (low confidence, but tries)
- Pre-processing an image before feeding text into `summarize` / `translate`

## Do not use when

- Digital PDFs with embedded text — use `pdf-extract` (faster, exact)
- Handwriting-heavy or complex layouts — results will be poor
- You need bounding boxes or structured output — use a vision LLM

## Tools

- `status` — Tesseract version
- `languages` — installed language packs (`eng`, `spa`, `fra`, ...)
- `ocr` — `image_path`; optional `lang` (default `eng`), `psm` (page seg mode, default 3), `oem` (engine mode, default 3)

## Language packs

Install on Debian/Ubuntu: `apt install tesseract-ocr-spa` (etc.). Check
installed with `languages`. Combine with `+`: `lang: "eng+spa"`.

## Common PSM values

| PSM | Meaning |
|-----|---------|
| 3 | Fully automatic (default) |
| 6 | Single uniform block of text |
| 7 | Single line |
| 11 | Sparse text — find as much as possible, no order |
| 13 | Raw line — single text line, no preprocessing |
