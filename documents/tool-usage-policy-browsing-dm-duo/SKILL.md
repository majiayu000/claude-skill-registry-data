---
name: tool-usage-policy-browsing-dm-duo
description: >
  Tool usage guidelines for web research agents in DM/Duo mode (no BBS).
  Covers tool reference, search-first principle, and the principle of
  verifying before claiming. Sharing happens via direct messaging and
  task-completion summaries — there is no Bulletin Board System.
---

# Tool Usage Policy (Browsing — DM/Duo)

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

## Sharing Results (DM/Duo Mode)

There is no Bulletin Board System in this run. Do NOT call `post_to_bbs`
(it is not registered) and do NOT reference `#discoveries`,
`#key-findings`, or any BBS channel — they do not exist here.

Share findings through the two channels you actually have:

- **`complete_task` summary** — your primary output. Include the answer,
  the exact source URLs you fetched, key quoted facts, and any caveats.
  This is the ONLY signal the orchestrator (DM mode) or the main worker
  (Duo mode) is guaranteed to read.
- **`send_message` to a specific peer** — use when a teammate needs your
  finding to do their work, when you spot an error in their result, or
  when your conclusion rests on a non-obvious assumption a peer should
  know about. Include the source URL inline in the message body, since
  there is no shared `structured_data.url` field.

Do NOT broadcast (`to='all'`) unless your finding affects every
teammate's work.
