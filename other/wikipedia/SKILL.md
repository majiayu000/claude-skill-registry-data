---
name: Wikipedia
description: Search Wikipedia and fetch article summaries or extracts.
requires:
  bins: []
  env: []
---

# Wikipedia

Look up encyclopedia articles. Backed by the `wikipedia` extension hitting the
public MediaWiki + REST APIs. No key.

## Use when

- "Who / what is X?" — factual lookup with a canonical source
- "Summarize the Wikipedia article on Y"
- "Search Wikipedia for Z"
- Grounding for long-form answers before calling `summarize`

## Do not use when

- Real-time / breaking news — use `brave-search`
- Non-encyclopedic web content — use `fetch-url`

## Tools

- `status` — default language
- `search` — `query` + optional `limit` (≤20), `lang`
- `summary` — REST summary (one paragraph + page URL + thumbnail)
- `extract` — plaintext intro (`sentences`, default 10; `0` = full article)

## Language

Default via `WIKIPEDIA_LANG` env (fallback `en`). Override per-call with `lang`.
Common: `en`, `es`, `fr`, `de`, `pt`.
