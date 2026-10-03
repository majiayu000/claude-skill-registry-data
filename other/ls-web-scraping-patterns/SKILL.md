---
name: ls-web-scraping-patterns
description: Guide ethical web scraping patterns. Use for crawl scope, extraction,
  anti-abuse limits, browser scraping, structured data, and integration with Scrapling/Firecrawl.
metadata:
  version: '1.0'
---

# Web Scraping Patterns

Use this skill when working on web scraping patterns tasks.

## Workflow

- Check authorization, terms, robots expectations, rate limits, privacy, and data retention before scraping.
- Prefer official APIs or exports when available; otherwise bound crawl depth, concurrency, and retries.
- Use `ls-scrapling` or `ls-firecrawl` for implementation-specific scraping guidance.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source classification: `localsetup-native`
- This is a LocalSetup-native skill written from project workflow requirements and public/official documentation routing.
