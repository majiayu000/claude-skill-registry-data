---
name: surya-ocr
description: Recognize and extract text from images or PDFs using Surya OCR (datalab-to/surya). Use when a user uploads a document, screenshot, scan, or photo and wants the text extracted or analyzed. Surya supports 90+ languages and works on both images and PDFs without an internet connection.
origin: "github.com/datalab-to/surya (Apache 2.0)"
---

# Surya OCR

## Overview

Surya is a local VLM-based OCR engine that extracts text from images and PDFs with high accuracy across 90+ languages. When a user attaches a file in Yana's chat, Yana sends it to `/api/ocr`, which runs `ocr_worker.py` using Surya, and injects the extracted text into the message draft — ready for the user to add their question.

Surya runs entirely on-device. No data leaves the machine during OCR.

## When to Use

- User uploads a screenshot, photo, or scanned document and says "đọc cái này", "phân tích ảnh này", "trích xuất văn bản", "extract text", "what does this say", "summarize this document"
- User attaches a PDF and asks questions about its content
- User sends an image with handwriting, receipts, contracts, or printed text

## Installation

```bash
pip install surya-ocr

# For PDF support (converts pages to images before OCR)
pip install pdf2image
# Also need poppler (renders PDF pages):
# Ubuntu/Debian: apt install poppler-utils
# macOS:         brew install poppler

# Alternative: pypdf (extracts text from text-based PDFs — no image conversion needed)
pip install pypdf
```

First run downloads ~1 GB of model weights to `~/.cache/huggingface/`. Subsequent runs use the cache.

## How Yana Uses It

1. User taps the paperclip (📎) button in chat
2. Selects an image or PDF from their device
3. Yana encodes it to base64 and sends it to `POST /api/ocr`
4. Server calls `python3 tools/yana-web/ocr_worker.py <tmpfile> [lang]`
5. Surya extracts the text, worker prints JSON: `{"ok": true, "text": "...", "pages": N}`
6. Extracted text is injected into the draft input
7. User adds their question and sends — Yana analyzes the content with full context

## Supported File Types

| Extension | Notes |
|-----------|-------|
| jpg/jpeg/png/gif/webp/bmp/tiff | Direct OCR |
| pdf | Requires pdf2image + poppler, or pypdf for text-based PDFs |

## Supported Languages

90+ languages including English, Vietnamese (vi), Chinese (zh), Japanese (ja), Korean (ko), Arabic (ar), and more. Pass a 2–5 character ISO 639-1 code as the `lang` field in the request body.

## API Contract

**Request** `POST /api/ocr`
```json
{
  "fileBase64": "<base64-encoded file data>",
  "filename": "scan.pdf",
  "lang": "en"
}
```

**Response (success)**
```json
{
  "ok": true,
  "text": "Extracted text content...",
  "pages": 3
}
```

**Response (failure)**
```json
{
  "ok": false,
  "error": "surya not installed. Run: pip install surya-ocr"
}
```

## Troubleshooting

| Error | Fix |
|-------|-----|
| `surya not installed` | `pip install surya-ocr` |
| `Pillow not installed` | `pip install Pillow` |
| PDF: `pdf2image or pypdf not installed` | `pip install pdf2image pypdf` + `apt install poppler-utils` |
| Slow first run | Model weights downloading (~1 GB), normal |
| Wrong language | Set `lang` to correct ISO code (e.g. `vi` for Vietnamese) |

## Anti-Patterns

- Do NOT call `/api/ocr` for files larger than 20 MB — use chunked uploads or compress the image first
- Do NOT pass user-constructed filenames directly to the filesystem — the server sanitizes extensions and uses a random temp name
- Do NOT assume OCR is 100% accurate — always let the user verify extracted text before acting on it
- Do NOT log extracted text if it might contain CONFIDENTIAL content (rule 68 applies)

## References

- `tools/yana-web/ocr_worker.py` — Python worker script
- `tools/yana-web/server.js` — `/api/ocr` endpoint (`handleApiOcr`)
- `tools/yana-web/desktop/chat.jsx` — desktop attach button + `handleOcr`
- `tools/yana-web/mobile/m-chat.jsx` — mobile attach button + `handleOcr`
- `github.com/datalab-to/surya` — upstream Surya OCR library
