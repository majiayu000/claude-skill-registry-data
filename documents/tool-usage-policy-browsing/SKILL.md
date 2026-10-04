---
name: tool-usage-policy-browsing
description: >
  Tool usage guidelines for web research agents. Covers tool reference,
  search-first principle, and the principle of verifying before claiming.
---

# Tool Usage Policy (Browsing)

## Tool Reference

1. **`web_search`** — Discover relevant URLs and snippets via web search APIs.
2. **`web_fetch`** — Fetch full page content from URLs found by web_search.
   Returns clean markdown text. Handles HTML pages and auto-detects PDFs.
3. **`pdf_read`** — Read PDF documents (academic papers, reports, etc.).
   Accepts URLs or local file paths. Use `pages` param for large PDFs.
4. **`calculator`** — Evaluate numeric expressions. NEVER calculate mentally.

### Search-First Principle

- Use `web_search` to find URLs. If more information is needed, then `web_fetch` to read the actual content.
- For PDF links, you can use either `web_fetch` (auto-detects PDFs) or
  `pdf_read` directly.

## Do Not Guess

- Do NOT fabricate URLs — only cite pages you actually retrieved.
- Do NOT claim a fact without a source — if you cannot find evidence,
  say so explicitly.
- Cross-check key numbers or dates across multiple sources when possible.

## Sharing Results (Swarm Mode)

- Post web search findings to `#key-findings` or `#discoveries`.
  Always include the source URL in `structured_data.url`.
- Include a brief summary of what you found and why it's relevant.
