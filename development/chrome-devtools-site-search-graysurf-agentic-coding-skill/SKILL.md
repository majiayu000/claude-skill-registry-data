---
name: chrome-devtools-site-search
description: Validate website parsing and browser automation feasibility by browsing and searching within a user-specified website scope using the chrome-devtools MCP server (mcp_servers.chrome-devtools); summarize results backed by observed page content (real titles/URLs), and open matching pages for review. Use when the user asks you to open a site, find specific content on it, run a site-scoped query, and keep the relevant pages open.
---

# Chrome DevTools Site Search

## Purpose (Parsing + Automation Feasibility)

- This skill’s workflow is primarily for testing whether a site can be reliably parsed (content extraction) and whether automated browsing flows are feasible using a real browser controlled by `mcp_servers.chrome-devtools`.

## Setup

- Use the MCP server `mcp_servers.chrome-devtools` to control a real browser session (tabs, navigation, interaction, and page content extraction).
- If `mcp_servers.chrome-devtools` is not available (missing, cannot start, cannot connect, times out), STOP immediately and report the failure and what needs to be enabled/configured. Do not fall back to non-browser scraping or alternative search methods outside the MCP-controlled browser.

## Inputs

Collect (or infer) these inputs from the user request:

- **Site scope**: a domain, URL prefix, or an explicit allow-list of domains/paths.
- **Query conditions**: keywords and any constraints (title must contain X, language, timeframe, section/category, content type).
- **Open policy**: whether to open a single result (“any one”) or multiple results (“top N”).

Ask at most 1-2 clarifying questions if the request is underspecified. Defaults:

- If the user does not specify a count, open up to 3 results.
- Cap auto-open to 5 pages unless the user requests more.

## Workflow

1. **Confirm scope and intent**
   - Restate the site scope and query conditions in one sentence.
   - If the user’s terms are ambiguous, ask for the exact keyword(s) and the desired count of pages to open.

2. **Navigate to the site**
   - Open the site entry page (home, section page, or known search page).
   - Keep a dedicated “results” tab whenever possible.

3. **Choose a search strategy (prefer in-site search)**
   - Prefer the site’s native search UI or search endpoint.
   - If no native search is discoverable, use a reputable external search engine with a strict site restriction (for example, `site:<domain> <keywords>`), and only open results that match the requested scope.

4. **Collect candidate results with evidence**
   - For each candidate, capture:
     - Title text as displayed on the site
     - Final URL after navigation/redirects (canonical when available)
     - Date/time if visible (otherwise record “date not visible”)
     - A 1-sentence gist from the page’s lede/summary
     - Why it matches the user’s condition(s)
     - (Feasibility) Whether the title/date/lede were extractable via stable DOM selectors, and any automation blockers (e.g., consent wall, login, bot protection, infinite scroll)
   - Do not rely on search snippets alone; open the page and verify the title/lede against the conditions.

5. **Summarize results**
   - Summarize in a compact list (3-6 bullets max unless requested), each containing: `Title — Date (if known) — 1-sentence gist — URL`.
   - If there are no matches, state that clearly and suggest the smallest query refinement (different keyword, broader timeframe, alternate spelling).

6. **Open result pages for the user**
   - Open the number of pages implied by the user’s open policy (or defaults).
   - Prefer opening pages in background tabs so the results list remains available.
   - Leave all opened pages/tabs in place for the user; do not close or “clean up” tabs.

## Quality and safety rules

- Do not fabricate results. Every summarized item must be backed by an observed page and a real URL obtained during the run.
- Stay within the user-provided site scope. If a result is off-scope but highly relevant, ask before opening it.
- If the user request involves disallowed content, refuse that part and offer a safe alternative (for example, summarize high-level workflow without visiting the site).
