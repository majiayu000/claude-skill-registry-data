---
name: livelib-quote-search
description: Given a LiveLib book URL and a quote fragment, find a matching LiveLib quote URL.
compatibility: Requires network access to livelib.ru.
---

## Goal
Given `book_url` and `quote_text`, locate a matching quote on LiveLib and return a canonical `https://www.livelib.ru/quote/...` URL.

## Inputs
- `book_url` (string)
- `quote_text` (string)

## Output
- `quote_url` (string | null)

## Notes
- Prefer exact/substring matches after normalization.
- If the quote cannot be verified on a quote page, return `quote_url = null`.

See references in `references/`.
