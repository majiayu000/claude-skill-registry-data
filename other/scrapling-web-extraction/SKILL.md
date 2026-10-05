---
name: scrapling-web-extraction
description: Use Scrapling for lawful, user-directed web scraping, bulk page extraction, AI-targeted page cleanup, screenshots, and dynamic-page fetching.
---

# Scrapling Web Extraction

Use this skill when a task requires extracting content from websites more systematically than ordinary search or manual browser inspection.

## 适用场景

- The user asks to scrape or extract data from one or more webpages.
- A page needs JavaScript rendering before content is available.
- The task needs batch URL extraction.
- The output should be Markdown, plain text, HTML, or structured page content.
- The user wants AI-friendly cleanup of page content.

## 不适用场景

- Simple fact lookup where ordinary web search is enough.
- Local frontend testing where Playwright or the Codex in-app Browser is more direct.
- Bypassing login, paywalls, CAPTCHA, rate limits, robots rules, or access controls.
- Collecting private, sensitive, or personal data without a clear lawful basis.

## 工作流

1. Clarify the extraction target.
   - Identify URL list, desired fields, output format, and whether JavaScript rendering is needed.

2. Choose the lightest fetcher.
   - Use HTTP GET extraction for static pages.
   - Use dynamic fetch for pages that require browser rendering.
   - Use AI-targeted extraction when content will be summarized or fed into an LLM.

3. Respect boundaries.
   - Avoid aggressive rates.
   - Do not attempt to bypass access controls.
   - Stop and ask if the request touches accounts, private data, or restricted content.

4. Verify output.
   - Inspect a small sample before scaling.
   - Check that key fields are present.
   - Mention any pages that failed, timed out, or looked incomplete.

## Example Commands

Static page to Markdown:

```powershell
scrapling extract get https://example.com output.md --ai-targeted
```

Dynamic page to Markdown:

```powershell
scrapling extract fetch https://example.com output.md --ai-targeted --headless
```

Run MCP server:

```powershell
scrapling mcp
```

## Codex MCP Config Example

```toml
[mcp_servers.scrapling]
command = "C:\\path\\to\\scrapling.exe"
args = ["mcp"]
startup_timeout_sec = 120
```

## Safety Notes

Use Scrapling only for lawful, user-directed collection. Prefer official APIs when available. For websites with terms, rate limits, or robots restrictions, respect those boundaries.
