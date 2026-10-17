---
name: research-store
description: Index local research exports into Supabase and retrieve project-scoped research over MCP.
compatibility: Node.js >=24; Supabase PostgreSQL >=15 with pgvector
---

# Research store

## Trigger

Use for explicit one-way research indexing or authorized research retrieval. Candidate status; production rollout requires evidence gates in implementation plan.

## Input schema

- Sync: `RESEARCH_ROOT` absolute local export directory; optional `--project` in `CIC`, `RewriteLabs`, or `other`; optional `--dry-run` boolean flag.
- `match_research_items`: required query string (1..8000 characters); optional project/status, threshold (0..1, default 0.7), and count (1..50, default 10).
- `fetch_document`: required document UUID; optional include_claims boolean (default false).
- `list_by_status`: required status; optional project, limit (1..100, default 20), and offset (0..2147483547, default 0).
- Status enum: `VERIFIED`, `INFERRED`, `UNKNOWN`, `NEEDS_REVIEW`.

## Output schema

- Sync stderr JSON: `{processed: integer, skipped: integer, failed: integer}`; exit 1 when any file fails.
- MCP: text content containing JSON results; failed calls return `isError: true` with sanitized error text.
- Search: array of chunks with similarity, project, document_id, status, and provenance metadata.
- Fetch: document and ordered research_items; claims included only when requested.
- List: array of matching authorized research items.

[Skill Operator Guide](../../docs/meta/skill-operator-guide.md) defines standard setup and documentation conventions.
