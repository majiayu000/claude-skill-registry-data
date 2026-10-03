---
name: python-patterns
version: "1.0"
description: Team conventions for Python development — credentials, API clients, LLM response parsing, testing patterns, and data pipeline structure. Covers dotenv loading, retry logic, secret validation, and pipeline anti-patterns.
---

# Python Patterns — Team Conventions

Unified conventions for team Python projects: credential management, API clients, testing discipline, and data pipeline structure. Supplements standard patterns with team-specific rules.

## When to Activate

- Writing credential/secret handling code or `.env` files
- Creating or modifying API clients (GitHub, Stripe, LLM APIs)
- Parsing LLM responses or structured API outputs
- Writing or reviewing tests (TDD workflow, mocking external APIs)
- Building or debugging data pipeline stages
- Reviewing code that handles HTTP responses or LLM output

## Quick Rules

**Credentials:**
- Never hardcode or use real defaults. Fail fast if missing. Always create `.env.example`.

**APIs:**
- Always timeout (30s). Only retry transient errors (429, 5xx). Always validate response structure.

**Tests:**
- Mock external APIs. Set `random_state=42`. Target 80%+ coverage. Test behavior, not internals.

**Pipelines:**
- Each stage is independently runnable. Validate input before processing. Include metadata in every output. Fail fast on invalid data.

## Details

Read `references/credentials.md`, `references/api-clients.md`, `references/testing.md`, and `references/pipelines.md` for full examples and anti-patterns.
