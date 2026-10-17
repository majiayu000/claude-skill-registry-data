---
name: tinyfish-search
description: High-speed web search and clean Markdown URL extraction powered by TinyFish AI.
compatibility: Node.js 24+, TINYFISH_API_KEY, and @tiny-fish/sdk package.
---

# TinyFish Search

Exports `tinyfish_search` and `tinyfish_extract` from `dist/index.js`.

All operations validate inputs before network transport and return `{ ok: true, data }` or `{ ok: false, error }`.

Features:
- 30 searches/min and 150 fetches/min process-isolated token-bucket rate limiting.
- 3-attempt exponential backoff with jitter on HTTP 429 status codes.
- 10-second per-request hard timeout failing closed with `TINYFISH_API_ERROR`.
- Sanitized error returns preventing raw provider exception leakage.

See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md) for Toolforge conventions.
