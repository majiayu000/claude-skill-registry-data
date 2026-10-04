---
name: query-review
description: Review an authorized codebase for ORM misuse, N+1 query patterns, authorization-after-fetch bugs, raw SQL risks, cache key collisions, and missing tenant scopes. Use for data-access layers and security-adjacent performance pitfalls.
---

# Query Review

## Focus

- missing tenant scopes
- authorization after broad fetches
- raw SQL without parameter binding
- N+1 patterns that become availability or side-channel issues
- eager loads that overexpose sensitive associations
- cache keys missing tenant or role context

## Heuristic

Treat data-access issues as security-relevant when they change scope, leak metadata, or undermine availability controls.
