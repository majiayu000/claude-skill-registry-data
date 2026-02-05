---
name: livelib-reading-list-search
description: Search https://www.livelib.ru/reader/<username>/reading for a mentioned book and return the best matching LiveLib book URL.
compatibility: Requires network access to livelib.ru; public profile/reading page.
---

## Goal
Given a `username` and `book_title`, find the best matching book in the user's LiveLib reading list and return a canonical `https://www.livelib.ru/book/...` URL.

## Inputs
- `username` (string)
- `book_title` (string)

## Output
- `book_url` (string | null)
- `candidates` (list)

## Notes
- Prefer exact title matches; otherwise choose the closest candidate.
- If no candidate is found, return `book_url = null`.

See references in `references/`.
