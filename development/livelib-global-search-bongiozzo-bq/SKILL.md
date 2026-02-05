---
name: livelib-global-search
description: Use LiveLib global search to find the first/best book result and return its canonical book URL.
compatibility: Requires network access to livelib.ru.
---

## Goal
Given a `book_title` (and optionally author), return the first/best matching `https://www.livelib.ru/book/...` URL from LiveLib search.

## Inputs
- `book_title` (string)

## Output
- `book_url` (string | null)
- `candidates` (list)

## Notes
- Use as fallback when the reading list search fails.
- If no book is found, return `book_url = null`.

See references in `references/`.
