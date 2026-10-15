---
name: Summarize
description: Summarize text or local UTF-8 files via OpenAI-compatible chat completions.
requires:
  bins: []
  env:
    - SUMMARIZE_OPENAI_API_KEY
---

# Summarize

Use this skill when the user asks for concise summaries of long text or local
documents. Backed by the `summarize` extension which calls any
OpenAI-compatible chat completions endpoint.

## Use when

- "Summarize this text"
- "Give me a short summary of this file"
- "Extract key points from this note"
- Long input that would otherwise blow the context window

## Do not use when

- User asks for full verbatim rewrite
- User asks for strict legal or medical advice
- Input is binary media (audio/video) without transcript first
- Input fits comfortably in the conversation already (just summarize directly without the tool)

## Tools

### `status`
No arguments. Returns endpoint, model, key presence, size limits.

### `summarize_text`
- `text` (string, required, ≤ 60 000 chars)
- `length` (string, optional) — `short` (1–2 sentences) | `medium` (paragraph, default) | `long` (6–10 sentences)
- `language` (string, optional) — output language hint, e.g. `Spanish`

Returns `{length, language, input_chars, summary}`.

### `summarize_file`
- `path` (string, required) — UTF-8 file, max 1 MB
- `length`, `language` (optional, same)

Returns `{path, bytes, length, language, input_chars, summary}`.

## Execution guidance

- Default to `length: "medium"`. Bump to `short` if the user wants a one-liner; `long` if they ask for an exec summary or report.
- Pass `language` only if it differs from the conversation language.
- If the text is over 60k chars, chunk it before calling: split into ≤ 50k blocks, summarize each, then summarize the summaries.
- If error code is `-32011` (unauthorized) → `SUMMARIZE_OPENAI_API_KEY` missing or invalid; ask the operator.
- If error code is `-32007` (empty completion) → provider returned blank content; retry once or report.
- For binary files (PDF, DOCX) extract text first via another tool; this extension does not parse them.
