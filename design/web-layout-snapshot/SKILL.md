---
name: web-layout-snapshot
description: Capture web page layout summaries and scraping notes from live sites. Use when asked to document page structure, identify sections, or describe how to scrape a site; includes guidance for dev-browser screenshots, ARIA snapshots, and layout writeups.
---

# Web Layout Snapshot

## Overview
Create a concise layout summary and scraping plan for a live web page using dev-browser, a screenshot, and an ARIA snapshot.

## Quick start
1. Start the dev-browser server.
2. Open the target URL in a named page.
3. Capture a full-page screenshot and ARIA snapshot.
4. Write the layout summary using the template in `references/layout-template.md`.

## Workflow

### 1) Open the page in dev-browser
- Run the dev-browser server if it is not already running.
- Use a named page so follow-up scripts reuse the same state.
- Log `page.title()` and `page.url()` after load.

### 2) Capture evidence
- Take a full-page screenshot to anchor the layout description.
- Get an ARIA snapshot to enumerate headings, links, and sections.
- If the page appears to be a Cloudflare/anti-bot challenge, switch to `cloudflare-aware-scrape` before continuing.

### 3) Summarize layout
- Use `references/layout-checklist.md` to verify coverage.
- Write the final notes in Markdown using `references/layout-template.md`.
- Prefer structural descriptions (columns, hero, cards, grids) over CSS class details.

### 4) Describe scraping plan
- List entry points (homepage, category pages, search).
- Identify link patterns for detail pages.
- Identify media/thumbnail hosts and mapping rules.
- Note pagination mechanisms.
- Document access constraints and any fallbacks used.

## Resources
- `references/layout-template.md`
- `references/layout-checklist.md`
