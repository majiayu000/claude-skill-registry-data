---
name: wiki-health
description: Use when the user says "wiki health", "check wiki", "wiki audit", "stale articles", "broken links", or "orphan pages"
---

# /wiki-health: audit the knowledge base

For every article in `wiki/` (skip `_index.md`), flag:
- STUB: summary missing or under 2 sentences
- ORPHAN: no Related links
- BROKEN LINK: a `[[slug]]` with no file behind it
- STALE: last updated over 30 days ago
- UNPROCESSED: files still in `inbox/`

Report as stats (total, healthy, needs attention), an issue list and recommended actions. Report only. Never auto-fix.
