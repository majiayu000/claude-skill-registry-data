---
name: explore-docs
description: Retrieve authoritative library documentation and code examples.
---

## Intent
Use when the task depends on library/framework usage details.

## Steps
1. Prefer Context7: resolve library ID, then fetch targeted docs.
2. If Context7 is unavailable or insufficient, use web.run with search_query and open official docs.
3. Extract APIs, examples, configuration, and pitfalls.

## Output format
- Library name/version (if known)
- Key concepts
- Code examples
- API reference (short list)
- URLs (official docs)
