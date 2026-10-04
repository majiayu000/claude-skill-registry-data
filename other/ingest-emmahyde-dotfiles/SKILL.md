---
name: ingest
description: Ingest web content into Emma's llmwiki vault — scrape a single page or crawl a set of pages, compile them into schema-conformant wiki pages, and refresh the vault's retrieval indexes. Use when the user says /ingest, "add this page/site to the wiki", "scrape X into the vault", "crawl these docs", or wants any external source captured as vault knowledge.
---

# Ingest into the llmwiki vault

Vault root: `/mnt/c/Users/emmaj/llmwiki`. Read the vault's `CLAUDE.md` first — it is the schema authority (page types, frontmatter, folder layout, raw/ immutability). This skill only adds the mechanics.

## Workflow

1. **Fetch** — single page: WebFetch it. A set of pages: enumerate first (sitemap, index page, or link-follow with an explicit budget), confirm the list with the user if it exceeds ~20 pages, then fetch serially. MediaWiki sites: prefer the wikikb skill's pull machinery and respect its access-posture rules (robots.txt, AI-agent blocks, 403 = stop); never stealth-scrape a site that blocks automated clients.
2. **Archive raw** — save fetched markdown under `raw/` (immutable; never edit existing raw files). One file per source page, named after the page.
3. **Compile** — write wiki pages per vault schema: correct type (concept/entity/source), YAML frontmatter matching existing pages (copy the shape of a neighbor page in the target folder), `[[wikilinks]]` to related pages, `sources:` carrying the origin URL. Update `log.md` with one line per ingest session.
4. **Refresh retrieval** — invoke the `retune` skill (owns the index+tune procedure and its failure modes). Until it completes, new pages are findable via `llmwiki search` but not via `llmwiki ask`.
5. **Optional graph** — for topics that benefit from entity/relation traversal, offer `llmwiki graph <vault-relative-path>` (LLM-expensive; scope to the new pages only).

## Hard rules

- Never edit `raw/` after writing; never write memory or state into `wiki/` pages that isn't compiled knowledge.
- Work-related sources: flag to the user instead of filing (vault policy).
- A failed tune leaves `ask` on the previous pipeline — safe; report and continue.
