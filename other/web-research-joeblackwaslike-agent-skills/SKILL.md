---
name: web-research
description: Expert web research router. Automatically selects the best search and page-fetch tool for any research task. Invoke whenever performing web search, fetching documentation, looking up library APIs, or retrieving any external web content. The user never needs to specify which tool to use — routing is handled invisibly.
license: MIT
compatibility: Requires MCP servers for optimal routing (Exa, Context7, Ref, Tavily, Perplexity). Falls back gracefully to built-in webSearch and webFetch when specialized tools are unavailable.
metadata:
  last_updated: "2026-09-07"
---

## Web Research Routing Rules

Apply these rules automatically — never ask the user which search or fetch tool to use.
Never explain the routing unless the user explicitly asks. If routing fails, surface the
failure clearly; never silently return inferior results.

### Search Tool Selection

Classify the query intent first, then route to the appropriate tool.

**Library / framework documentation (known library, version-specific API)**

1. Try Context7 first: `mcp__context7__query-docs`
2. If Context7 doesn't have the library, or prose/explanation is needed: `mcp__Ref__ref_search_documentation`

**Niche technical query (library internals, obscure bugs, RFCs, edge cases, implementation patterns)**

- Default: `mcp__exa__web_search_exa`
- For finding code examples in OSS specifically: `mcp__exa__get_code_context_exa`

**Synthesis query ("what is the current state of X", "compare A vs B", "explain how X works in 2025/2026")**

- If Perplexity Sonar is connected: use it
- Otherwise: `mcp__exa__web_search_exa` and synthesize the results yourself

**Exhaustive research task (deep investigation, literature review, comprehensive comparison)**

- Use `mcp__exa__deep_researcher_start`, then poll `mcp__exa__deep_researcher_check` until complete
- Only when the task explicitly requires comprehensive multi-source synthesis — it is slow (~45–90s) and expensive

**News / announcements / time-sensitive information**

- If Tavily is connected: use it
- Otherwise: `mcp__exa__web_search_exa` with a recency filter

**Company or product research**

- Use `mcp__exa__company_research_exa`

**General / broad web lookup**

- `mcp__exa__web_search_exa`, or Tavily if connected

**Last resort** (no specialized tool is available for the query type):

- Use built-in `webSearch`
- Always emit a visible note to the user: "(using fallback search — results may be less targeted than usual)"

### Page Fetch / Rendering Escalation

Apply in order. Stop at the first step that returns sufficient content.

1. **`webFetch`** — always try first. Zero overhead, instant.
   - **Skip to step 3** if the URL hostname is on the known-blocking list (see `references/browserless.md`).

2. **Detect unhydrated SPA** — if the response body meets any of these conditions, escalate:
   - Total body text content < ~200 characters
   - Body contains `<div id="root">`, `<div id="app">`, or `<div id="__next">` with no meaningful content inside
   - Body is dominated by `<script>` tags with little visible text

3. **Browserless (bot-blocked sites)** — self-hosted headless Chrome for sites that actively block agents. Trigger when:
   - URL is on the known-blocking domain list (`references/browserless.md`), OR
   - `webFetch` returned HTTP 403 / 429, a CAPTCHA page, or near-empty content from a page that is clearly server-rendered (not an SPA)

   ```bash
   source ~/creds.zsh
   curl -sS -X POST "$BROWSERLESS_URL/content" \
     -H "Authorization: Bearer $BROWSERLESS_TOKEN" \
     -H 'Content-Type: application/json' \
     -d '{"url":"<target-url>","waitForTimeout":3000}' | head -c 200000
   ```

   `waitForTimeout` shown here (3000 ms) is the default for standard server-rendered pages. Increase to 5000–10000 ms for JS-heavy, lazy-loaded, or infinite-scroll content — see timeout tuning table in `references/browserless.md`. Response is rendered HTML — parse the same way as any `webFetch` result.

4. **`superpowers-chrome`** — lower token cost than headless browser:
   `mcp__plugin_superpowers-chrome_chrome__use_browser`

5. **Playwright MCP** — full headless Chromium if superpowers-chrome was insufficient:
   `mcp__playwright__browser_navigate` + `mcp__playwright__browser_snapshot`

6. **Chrome DevTools MCP** — alternative to Playwright:
   `mcp__chrome-devtools__navigate_page` + `mcp__chrome-devtools__take_snapshot`

7. **Firecrawl** — only when structured JSON extraction or browser interaction (login, forms, pagination) is required. Never use Firecrawl for general search queries.

### Fallback Behavior

- If a preferred tool is unavailable (not connected): skip silently, use the next option in routing order
- If a tool returns an error: log the tool name and error, escalate to the next option
- Never retry the same tool + query combination more than twice
- Never fabricate citations — only cite URLs actually returned by a tool

## Reference Files

Load the relevant reference when deep tool-specific details are needed:

| Tool | Reference | When to load |
|------|-----------|--------------|
| Context7 (library docs) | `references/context7.md` | Resolving library IDs, version-specific queries, quota errors |
| Exa (search + deep research) | `references/exa-research.md` | Deep researcher workflow, date handling, citation format |
| Brave Search | `references/brave-web-search.md` | Brave MCP unavailable, REST API fallback needed |
| Tavily CLI | `references/tavily-cli.md` | `tvly` commands, crawl/extract/map/research workflows |
| Browserless (bot-blocked sites) | `references/browserless.md` | Known-blocking domains, credential sourcing, timeout tuning |
