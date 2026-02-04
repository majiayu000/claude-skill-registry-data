---
name: cloudflare-aware-scrape
description: Detect and document Cloudflare or anti-bot challenge responses while scraping. Use when a site returns "Just a moment...", /cdn-cgi/ pages, or requires JS verification; provides detection heuristics, retry steps, and fallback capture methods.
---

# Cloudflare-Aware Scrape

## Overview
Identify when you are seeing a challenge page and apply a consistent fallback and reporting workflow.

## Quick start
1. Fetch or render the target page.
2. Check for challenge signals from `references/challenge-signals.md`.
3. If challenged, retry once with dev-browser and capture evidence.
4. If still blocked, use the fallback playbook and document access notes.

## Workflow

### 1) Detect challenges
- Inspect the page title, HTML, and obvious banners.
- Use `references/challenge-signals.md` to classify as "challenge" vs "normal".

### 2) Retry with dev-browser
- Load the page in a persistent dev-browser context.
- Wait briefly, then re-check `page.title()` and `page.url()`.
- Capture a screenshot if the challenge persists.

### 3) Use fallbacks
- Follow `references/fallbacks.md` in order: dev-browser retry, Jina snapshot, direct fetch.
- Do not rely on fallback content without noting limitations.

### 4) Record access notes
- State which access path succeeded and which failed.
- Include URLs, timestamps (if relevant), and evidence captured.

## Resources
- `references/challenge-signals.md`
- `references/fallbacks.md`
