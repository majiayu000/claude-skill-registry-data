---
name: database-migration
description: Use when changing review re-RAG schema, repositories, migrations, or PostgreSQL integration behavior.
---

# Database Migration

Follow `AGENTS.md` first.

## Workflow

1. Inspect `pubtator_link/db/review_schema.sql`, existing migrations, and repository tests before editing schema code.
2. Make migrations idempotent and keep bootstrap schema and migrations consistent.
3. Keep SQL mapping logic in repository/mappers, not API or MCP layers.
4. Add or update unit tests for schema text, migration ordering, mapper behavior, and repository edge cases.
5. Add PostgreSQL integration coverage when the behavior depends on database semantics that unit tests cannot prove.
6. Run focused database tests, then `make ci-local` before handoff.
