---
name: web-scraping
description: Extract structured data from websites — list pages, parse DOM, normalize records, and write to CSV / JSON.
category: web
aliases:
- scrape
- extraction
- data-extraction
triggers:
- scrape this site
- extract data from
- pull all the X from this website
- get me a list of
keywords:
- scrape
- extract
- parse
- dom
- html
- data
- web
- crawl
dependencies: []
risk: medium
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- dom
- extract
- parse
- scrape
- scraping
- web
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Web Scraping

## Purpose

Extract structured data from one or more web pages. Discover pages, parse the relevant DOM,
normalize the records, and write to a useful output format.

## When to Use

- User wants data from a site that exposes it (no auth wall)
- User wants a list of records (e.g. product listings, search results)

## When NOT to Use

- The site has an API (use it)
- The site forbids scraping in its TOS
- The user wants login-walled data (ask first)

## Capabilities

- Identify page structure
- Parse HTML / JSON / XML
- Pagination handling
- Output to CSV / JSON / SQLite

## Safety

- Respect robots.txt
- Rate-limit (delay between requests)
- Don't overload servers
- Cite source for the data

## Source

Custom skill, written for this library.

## Notes

Pairs with `browser-automation` (for JS-heavy sites) and `data-analysis` (after extraction).

## Inputs

- The user's goal and desired output.
- Relevant source material, constraints, and environment details.
- Acceptance criteria when available.

## Workflow

1. Confirm the goal, scope, and constraints.
2. Inspect the available context before acting.
3. Apply the skill-specific guidance in this document.
4. Verify the result and report limitations or next steps.

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "scrape this site"; "extract data from"; "pull all the X from this website".
