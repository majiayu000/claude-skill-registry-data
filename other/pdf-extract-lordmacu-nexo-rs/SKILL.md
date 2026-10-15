---
name: PDF Extract
description: Extract plain UTF-8 text from local PDF files; pipeline input for summarize.
requires:
  bins: []
  env: []
---

# PDF Extract

Use this skill whenever the user drops a PDF and wants its content read,
quoted, searched, or summarized. The extension decodes PDFs in pure Rust
(no `pdftotext`, no Python), returns plain text, and truncates to keep the
result within a safe LLM window.

## Use when

- "Read this PDF"
- "What does this document say?" (after a PDF attachment)
- Summarizing a PDF — call this first, then pass the output to `summarize_text`
- Searching for specific text inside a PDF

## Do not use when

- The file is an image scan with no embedded text layer (OCR not done here)
- The file is a form with no flowing text (only fields)
- The user wants **editing**, not extraction — this tool is read-only

## Tools

### `status`
No arguments. Returns provider info, file-size limit, default char cap.

### `extract_text`
- `path` (string, required) — absolute or relative path to the PDF (≤ 25 MB)
- `max_chars` (integer, optional, 1..=1 000 000, default 200 000) — truncates output

Returns:

```
{
  "path": "...",
  "bytes": 12345,
  "max_chars": 200000,
  "truncated": false,
  "char_count": 1200,
  "total_char_count": 1200,
  "text": "..."
}
```

## Execution guidance

- Prefer `max_chars: 50000` when chaining into `summarize_text` (summarize
  rejects inputs > 60 000 chars).
- If `truncated: true`, warn the user the summary is based on the first N
  chars; offer to do a second pass on later pages with a different
  `max_chars` + byte offset (not yet supported).
- Error `-32602` on bad path → ask the user to confirm the absolute path.
- Error `-32006` on extraction failure → likely a scanned PDF with no text
  layer, or a corrupted file. Suggest an OCR tool (out of scope).
- For multi-step work (extract → summarize → store decision), wrap the
  chain in a TaskFlow so a restart doesn't lose progress.
