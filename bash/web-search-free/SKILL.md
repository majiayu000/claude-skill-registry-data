---
name: web-search-free
description: Search the public web and fetch readable HTML, JSON, CSV, text, and PDF content with a local-first, zero-paid-API workflow. Use when Codex needs current web evidence, topic discovery, official-source lookup, URL extraction, PDF text, source collection, or a free fallback before Tavily/Firecrawl. Also use when users mention WebSearch, WebFetch, DDGS, SearXNG, Jina Reader, local scraping, web research cost control, or avoiding paid search credits.
---

# Free Web Research

Use the bundled CLI to discover and read public sources without calling paid search or scraping APIs. Preserve evidence quality: prefer primary sources, check dates, and cite the final URLs.

## Locate the CLI

Run the bundled wrapper from this Skill directory:

```bash
python3 scripts/free_web_research.py health
```

If it reports that the CLI is missing, tell the user to run `python3 scripts/install.py` from this Skill directory. The downloaded Skill contains the complete CLI source and creates an isolated environment. Do not install dependencies into the system Python ad hoc.

## Route the request

1. Search local project files and `.web-research-cache/` first.
2. For a known URL, fetch it directly:

   ```bash
   python3 scripts/free_web_research.py fetch 'https://example.com/page'
   ```

3. For an unknown URL, use a zero-cost built-in Web Search available in the current harness when possible. Otherwise run DDGS/SearXNG:

   ```bash
   python3 scripts/free_web_research.py search 'topic official source' --max-results 5
   ```

4. After discovering a URL, return to `fetch`; do not use a paid extractor by habit.
5. If direct extraction is incomplete, explicitly add free fallbacks:

   ```bash
   python3 scripts/free_web_research.py fetch 'https://example.com/page' --fallback jina,browser
   ```

6. Consider Tavily or Firecrawl only when the JSON result contains `escalation.recommended: true`. Record the failed routes and expected paid call count before escalating. Never invoke a paid tool automatically from this Skill.

Read [references/routing-policy.md](references/routing-policy.md) before multi-source research, paid escalation, or changing cache policy. Read [references/cli.md](references/cli.md) for all commands and output fields.

## Search efficiently

- Start with one focused query and 3-5 results.
- Use `--domains` for a strict allowlist and `--prefer-domain` to rank primary domains first.
- Use `--recency d|w|m|y` only when freshness is required.
- Configure `FREE_WEB_RESEARCH_SEARXNG_URL` to use a self-hosted SearXNG instance; otherwise `auto` uses DDGS.
- Treat DDGS/SearXNG results as discovery evidence. Fetch and inspect the source before making material claims.

## Fetch safely

- Keep TLS verification enabled. Never add `--insecure`, `verify=False`, credential harvesting, CAPTCHA bypass, or proxy rotation.
- Do not send private, authenticated, or confidential URLs through Jina Reader.
- Use Playwright only when it was installed with `--with-browser` and direct extraction is inadequate.
- Respect access controls, robots policies, rate limits, copyright, and website terms.
- Keep realtime data TTL short; keep immutable filings and PDFs longer.

## Handle outputs

Use JSON for agent workflows. Check `ok`, `cache_hit`, `backend`, `quality_score`, `attempts`, and `escalation` before relying on `text` or `results`. Use `--format markdown` only for human-readable output.
