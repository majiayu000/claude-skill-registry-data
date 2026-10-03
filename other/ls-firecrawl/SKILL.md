---
name: ls-firecrawl
description: Guide Firecrawl-powered scraping and research workflows. Use for crawl,
  scrape, search, extraction, indexing, and API-key handling.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: adapted-import
    source_url: https://github.com/firecrawl/skills
    source_path: skills/firecrawl-build/SKILL.md
    source_commit: 7ad43730e76913c4d1e9f94bf6fa6f82e38fc12b
    source_ref: main
    source_sha256: f6b1d4c2f9f014390095e09a10ecdfe1c6f3c8f66e01d5da4df87952a9e0945f
    license: ISC
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Firecrawl

Use this skill when working on Firecrawl tasks.

## Workflow

- Confirm the target site's terms, robots expectations, rate limits, and data sensitivity before scraping.
- Keep Firecrawl API keys out of source; use narrow extraction schemas and bounded crawl scopes.
- Validate output quality, retry behavior, deduplication, and downstream storage before automating large crawls.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source: `https://github.com/firecrawl/skills`
- Ref: `main` at `7ad43730e76913c4d1e9f94bf6fa6f82e38fc12b`
- Source path: `skills/firecrawl-build/SKILL.md`
- License classification: `ISC`
- Source SHA-256: `f6b1d4c2f9f014390095e09a10ecdfe1c6f3c8f66e01d5da4df87952a9e0945f`
