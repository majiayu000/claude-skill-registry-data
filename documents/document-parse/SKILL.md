---
name: document-parse
description: "Extract text, tables, and layout from an uploaded file (PDF, DOCX, XLSX, PPTX, image). Do NOT use for web scraping or reading level (use reading-level)."
---

# document-parse

Parse raw file bytes into a structured document representation (UDOM tree). Used by document-intelligence to separate file parsing from governance, and reusable by standards-updater or any skill that needs to extract content from uploaded documents.

## Input

```json
{
  "file_path": "/path/to/uploaded.pdf",
  "file_type": "pdf",
  "parser_hints": {"ocr_engine": "pytesseract", "lang": "en"},
  "confidence_threshold": 0.8
}
```

## Output

```json
{
  "tool": "document-parse",
  "udom": {"type": "document", "children": [{"type": "heading", "text": "Chapter 1"}, {"type": "paragraph", "text": "..."}]},
  "confidence": "high",
  "recovery_note": "Full text extraction; no OCR gaps",
  "parser_used": "PyMuPDF",
  "unrecovered_regions": [],
  "human_review_required": true
}
```

## Do NOT use this atom for
- Web page scraping (use feed-discover or feed-validate)
- Reading level estimation (pass extracted text to reading-level)
- Document comparison or diff (this atom extracts, it does not compare)

## Pipeline note
Follows `references/method.md` at the Ingestion step (raw file → UDOM). Output conforms to `references/metadata-schema.md`. Downstream steps (governance, analysis) are handled by the orchestrator. `human_review_required: true` — OCR/layout recovery is imperfect; teacher should verify critical content.
