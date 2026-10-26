---
name: ocr
description: Use when extracting text and fields from photographed or scanned documents (letters, receipts, forms), including Japanese — choosing and chaining OCR engines (cloud document conversion, Tesseract, Japanese-specialised engines, PaddleOCR, vision LLMs), capture resolution, splitting and stitching large pages, quality gates, field extraction with rules plus a local LLM, and measuring accuracy on an evaluation set. Also use when small print is misread, dates come out wrong, or a vision model takes minutes per page.
---

# OCR pipelines

Default: measure first — build a small evaluation set, compare engines on it, then run a fallback chain (best engine → next → ...) with a quality gate, and extract fields with rules first and a local LLM only for gaps, verifying every LLM value against the OCR text.

## Capture

- Resolution on paper is what matters: aim for roughly 10+ pixels per millimetre for small print. A 12 MP phone photo of an A4 page gives about 13 px/mm; an A3 page about 9–10 px/mm, and "scan document" modes often downscale further.
- For large sheets or tiny print, photograph in 2–3 overlapping strips (overlap two text lines) instead of one wide shot.
- Even lighting, no shadows, page filling the frame; avoid digital zoom.

## Engines (compare on your own documents)

| Engine | Strength | Watch out |
|---|---|---|
| Cloud document conversion (e.g. uploading an image to a document service that OCRs it) | Strong on mixed Japanese/English layouts | Data leaves the machine; quotas |
| Tesseract (`jpn`, `jpn_vert`) | Local, fast, scriptable | Weak on low resolution and complex layouts |
| Japanese-specialised local engines (e.g. NDLOCR-Lite) | Good on Japanese print | Setup effort |
| PaddleOCR | Good detection, many languages | Heavy dependencies |
| Vision LLM on CPU | Reads context, can return structure | Very slow on large images (minutes to tens of minutes); downscale or avoid |

## Stitching strips

Order strips by overlap: match identical text lines between the bottom of one and the top of the next; fall back to fuzzy string overlap. Produce one document record, not one per strip. Ask a model "same document?" only with extracted identifiers (issuer, title, date) compared in code — direct yes/no questions get confident wrong answers.

## Quality gate

Score each result (characters recognised per area, dictionary-word ratio, mean confidence). Below a threshold, mark "possibly too low resolution", notify once, and ask for a retake rather than extracting garbage.

## Field extraction

1. Rules first: regular expressions for dates (including Japanese era years), amounts, due dates, document types.
2. A local LLM fills only fields the rules left empty, returning JSON with the exact supporting text.
3. Verify in code: the quoted text must exist in the OCR output (after normalising full-width/half-width characters and similar glyphs such as `O`/`0`) and contain the value. Unverified values become "candidates" for human confirmation, never silent facts — and never trigger reminders.
4. Store the extractor version with each record so improvements can be replayed on old documents.

## Evaluation

- 5–20 synthetic documents with known fields (safe to commit) plus real documents kept private.
- Metrics: field exact-match rate, character accuracy, time per page, failure count. Re-run whenever an engine, model or rule changes.

## Pitfalls

- **Era years:** models often convert Japanese era years to the wrong Western year (off by years); convert in code.
- **Template text** (example values printed on forms) gets extracted as real data; detect and skip known example strings.
- **Rotations and vertical text** need detection; try both orientations when confidence is low.
- **Personal data:** keep images and OCR text out of repositories and logs; commit only synthetic samples.
