---
name: ocr-pipeline
description: Use when extracting text from PDFs or images before document classification ג€” Hebrew OCR, layout-aware parsing, scanned vs digital PDF detection. Feeds into `classify_document`.
---

# OCR Pipeline skill

## When to invoke

- Touching `src/integrations/ocr/` or `src/tools/extract-text.ts`
- Incoming attachment is a PDF, JPG, PNG, or scanned image
- Before calling `classify_document` on non-text input
- Debugging classification failures that may stem from bad text extraction

## Pipeline stages

```
Raw file (PDF/image)
  1. detect: digital PDF vs scanned PDF vs image
  2. if digital PDF ג†’ text layer extract (fast path)
  3. if scanned/image ג†’ OCR (Hebrew + English, RTL-aware)
  4. layout cleanup (tables, columns, headers)
  5. confidence score per page
  6. handoff to classify_document
```

## Hard rules

1. **Hebrew + English** are both required ג€” most Israeli financial docs mix them (provider names in English, content in Hebrew)
2. **RTL handling**: post-OCR text must preserve reading order ג€” verify on multi-column layouts
3. **Confidence threshold**: pages below 0.7 confidence ג†’ flag for human review, do NOT pass to classification
4. **Page limit**: documents over 50 pages ג†’ split, process in parallel, recombine
5. **Never store raw OCR output as the customer record** ג€” always pair with original file in Drive
6. **PII redaction** before logging ג€” never log full extracted text in plaintext (log first 100 chars + hash)

## Provider abstraction

OCR provider sits behind `src/integrations/ocr/client.ts` interface. Default: Google Document AI. Mock for tests in `mock.ts`. Switching providers must not change the interface ג€” `extract(file): Promise<ExtractedDoc>`.

## Common document types (Israeli financial)

- ׳“׳•׳— ׳©׳ ׳×׳™ ׳©׳ ׳§׳¨׳ ׳₪׳ ׳¡׳™׳”
- ׳×׳׳•׳© ׳׳©׳›׳•׳¨׳×
- ׳©׳•׳׳× ׳׳¡
- ׳₪׳•׳׳™׳¡׳× ׳‘׳™׳˜׳•׳— ׳—׳™׳™׳
- ׳׳™׳©׳•׳¨ ׳”׳₪׳§׳“׳” ׳׳§׳•׳₪׳× ׳’׳׳
- ׳×׳¢׳•׳“׳× ׳–׳”׳•׳× / ׳¡׳₪׳—

## Error handling

OCR failure ג†’ retry once with different engine ג†’ fall back to manual queue ג†’ notify operations agent.