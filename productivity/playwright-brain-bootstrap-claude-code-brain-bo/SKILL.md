---
name: playwright
description: Browser automation — navigate, click, fill, snapshot web pages. Use for UI testing, documentation scraping, OAuth flows, web research.
user-invocable: true
disable-model-invocation: true
---

# Browser Automation with Playwright MCP

**Use when:** you need to interact with a web page — test a UI, scrape docs, verify a login flow, research a live API.

**MCP server key:** `playwright` — tools: `mcp__playwright__*`

**Token cost:** 🟡 LOW-MEDIUM — accessibility snapshots are structured text (no pixel cost); large pages produce verbose trees.

## Decision matrix — when to use playwright vs other tools

| Task                              | Use                                    |
| --------------------------------- | -------------------------------------- |
| "Test this login form end-to-end" | playwright                             |
| "Scrape this documentation page"  | playwright                             |
| "Verify OAuth redirect works"     | playwright                             |
| "Find code about auth"            | cocoindex-code (semantic search)       |
| "What does AuthService call?"     | codebase-memory-mcp (structural graph) |
| "Is this PR safe to ship?"        | code-review-graph                      |

## Core tools

```
mcp__playwright__browser_navigate(url)           — go to URL
mcp__playwright__browser_snapshot()              — accessibility tree (PREFER over screenshot)
mcp__playwright__browser_click(element, ref)     — click by accessibility label
mcp__playwright__browser_fill(element, ref, val) — fill an input
mcp__playwright__browser_screenshot()            — visual capture (only when structure is insufficient)
mcp__playwright__browser_evaluate(script)        — run JS in page context
mcp__playwright__browser_wait_for_url(url)       — wait for navigation
mcp__playwright__browser_close()                 — clean up when done
```

## Standard workflow — snapshot first, screenshot never (unless needed)

```
1. browser_navigate(url)
2. browser_snapshot()              ← read the accessibility tree
3. browser_click / browser_fill    ← interact by element label or ref
4. browser_snapshot()              ← verify the new state
5. browser_close()                 ← always clean up
```

**Never use `browser_screenshot` as the first action** — accessibility snapshots give the same structural information at a fraction of the token cost.

## Token efficiency tips

- `browser_snapshot` returns a structured accessibility tree — use `element` labels for clicking/filling
- Prefer `browser_evaluate` for data extraction over reading the full snapshot repeatedly
- Always `browser_close` when done — open tabs accumulate context
- For long pages, use `browser_evaluate("document.querySelector('selector').textContent")` to extract specific content without loading the full tree

## Manual install (if browsers not pre-installed)

```bash
# Pre-install Chromium browsers (avoids download delay on first use)
npx playwright install chromium

# Full install with system dependencies (Linux CI)
npx playwright install chromium --with-deps
```

The MCP server (`npx @playwright/mcp@latest`) lazy-installs on first invocation — no manual setup required if Chromium is already installed.
