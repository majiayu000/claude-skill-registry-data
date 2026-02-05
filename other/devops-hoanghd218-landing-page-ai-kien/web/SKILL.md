---
name: web
description: Use to browse or verify external info—run web searches, open pages, drive Chrome via CDP tools, and cite sources when facts may be outdated, niche, or user-requested.
---

# Web (search + browse + cite + CDP)

## Overview
Default to web search when info may have changed, is niche, or the user asks. Use `web.run` for queries; follow citation rules and prefer authoritative sources. If interaction with a live page is needed, start Chrome with the bundled CDP helpers (`tools/start.js`, `nav.js`, `eval.js`, `pick.js`, `screenshot.js`, `click-link.js`).

## When to Use
- User says search/browse/look up/verify.
- Topics likely to change: news, prices, releases, schedules, policies, versions, CEOs, rankings, travel, recommendations.
- Niche/uncertain terms or potential typos.
- Need direct quotes/links/citations.
- Need to click, navigate, or extract structured data from a live site (use CDP tools).

## Core Pattern
1) Clarify intent + recency if not given.
2) Issue 1–3 targeted `search_query` calls (diverse terms/domains as needed).  
3) Open promising results; skim with `find` for key patterns (names, dates, numbers).  
4) Extract 3–5 load-bearing facts; ensure dates are explicit.  
5) Cite each non-obvious fact with citeturnX… immediately after the sentence.  
6) State assumptions; if data missing, say so briefly.
7) If interaction is required, start Chrome and use CDP helpers (below) to click/navigate/screenshot.

## Query Tips
- Add qualifiers: `site:docs.example.com`, version numbers, region.
- For names with ambiguity, include org or role.
- For recency: set `recency` days on `search_query` when asking “today/latest”.
- Run multiple queries in one `search_query` array to save turns.

## Reading & Validation
- Check publish date vs event date; prefer the latest credible source.
- Cross-check at least two domains for important claims.
- Avoid low-trust domains unless only source; if used, flag confidence.

## CDP Browser Controls (Chrome DevTools Protocol)
- Start Chrome with remote debugging on :9222  
  ```bash
  ./tools/start.js          # fresh profile
  ./tools/start.js --profile # reuse your profile/cookies
  ```
- Navigate current tab or open new tab  
  ```bash
  ./tools/nav.js https://example.com
  ./tools/nav.js https://example.com --new
  ```
- Evaluate JS in active tab  
  ```bash
  ./tools/eval.js 'document.title'
  ./tools/eval.js 'document.querySelectorAll(\"a\").length'
  ```
- Screenshot current viewport  
  ```bash
  ./tools/screenshot.js
  ```
- Pick elements interactively  
  ```bash
  ./tools/pick.js "Click the submit button"
  ```
- Click a known link/text  
  ```bash
  ./tools/click-link.js "Submit"
  ```
- All CDP scripts live in `skills/web/tools/`; ensure they’re executable.

## Citations
- Place after punctuation; avoid bold/italics/code fences.  
- Group multiple sources: citeturn2search1turn2open0  
- Cite every fact that isn’t obvious or could have changed since 2024.  
- Don’t paste raw URLs; citations render as links.

## Output Style
- Be concise; surface the answer first, then short context.  
- Include exact dates (e.g., “as of 2025-12-12”).  
- If unresolved, say what you tried and what’s missing.

## Red Flags
- Answering from memory when the topic is time-sensitive.  
- No dates on “latest/new/current”.  
- Failing to cite or citing irrelevant pages.  
- Over-long quotes; keep ≤25 words per source.  
- Ignoring conflicting sources—mention disagreement briefly.
- Using CDP without starting Chrome on :9222 via `tools/start.js`.
- Forgetting to give citations when summarizing CDP-derived content.
