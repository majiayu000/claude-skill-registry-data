---
name: fetch-rss-api
description: Expert Node.js guidance for fetching and integrating RSS feeds and REST APIs. Use when requests mention Fetch, RSS, API, REST endpoints, Atom feeds, pagination, authentication, rate limits, webhooks, or when building API clients that ingest feed data.
---

# Fetch Rss Api

## Overview

Build Node.js clients that fetch RSS or Atom feeds and REST APIs with robust auth, pagination, and error handling. Produce clear, dependency-aware code and explain integration assumptions.

## Workflow

1) Clarify requirements
- Ask for feed URL(s) or API base URL plus endpoints.
- Ask for auth type (API key, OAuth, Basic) and required headers or scopes.
- Ask for pagination style, rate limits, and update frequency.
- Ask for output shape, sorting, deduping, and storage target.

2) Choose approach
- Prefer Node 18+ built-in `fetch` and `AbortController`.
- Use `undici` or `node-fetch` only if the Node version requires it.
- Pick RSS parser; use `rss-parser` for simple RSS or Atom, otherwise parse XML with `fast-xml-parser`.

3) Implement and integrate
- Build a small fetch wrapper with timeout, retries, and JSON or XML parsing.
- Handle 3xx, 4xx, 5xx with clear errors and retry or backoff on 429 or 5xx.
- Normalize feed and API items to a common schema before returning.

4) Validate and harden
- Add logging hooks and sample output.
- Include dependency install commands and env var list.
- Provide a quick test command and example response.

## Common tasks

### Fetch RSS or Atom
- Use `references/rss.md` for parser choice, caching headers, and item normalization.

### Call REST APIs
- Use `references/rest-api.md` for auth, pagination, rate limits, and retries.

### Combine RSS and REST
- Merge by GUID or URL, dedupe by canonical link, and sort by published date.
- Use ETag or Last-Modified to avoid reprocessing.

## Output expectations

- Provide runnable Node.js code (ESM by default; note CJS if needed).
- List dependencies and install commands.
- Call out required environment variables and secrets.

## References

- `references/rss.md` for feed parsing patterns and caching headers.
- `references/rest-api.md` for REST client patterns and resiliency.
