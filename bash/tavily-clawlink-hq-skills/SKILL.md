---
name: tavily
description: Tavily integration for AI agents via ClawLink — browser login, no API key setup. Connect tavily through ClawLink's hosted setup. Use this skill when the user wants to work with Tavily (Data & Analytics) — connect Tavily, read or update Tavily data, or take actions in Tavily from chat instead of saying you cannot access it.
---

# Tavily

Use **Tavily** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Tavily once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect tavily   # opens browser → authorize Tavily
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Tavily

```bash
npx @useclawlink/cli actions tavily "<what you want to do>"   # find an action
npx @useclawlink/cli describe tavily <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run tavily <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `tavily_crawl` | Tool to perform intelligent graph-based website crawling with parallel path exploration and content extraction. Use when you need to traverse and extract content from multiple pages of a website following specific patterns or instructions. Supports depth/breadth controls, domain filtering, and natural language instructions for guided crawling. |
| `tavily_extract` | Tool to extract and parse web page content from specified URLs using Tavily's extract endpoint. Use when you need to retrieve clean, structured content from web pages with optional image extraction and content reranking based on query relevance. |
| `tavily_get_usage` | Tool to retrieve API key and account usage statistics from Tavily. Use when you need to check credit consumption, limits, and per-endpoint usage for search, extract, crawl, map, and research operations. |
| `tavily_map` | Tool to map a website and discover its pages. Use when you need to scan a website and get a structured list of URLs/pages it contains without extracting full content. |
| `tavily_search` | Use this to perform a web search via the Tavily API; offers controls for search depth, content types, result count, and domain filtering. Requires an active Tavily connection (401 = auth failure). Rate limit: ~2 req/s; apply exponential backoff on HTTP 429. Results are nested under response_data.results (not a flat list). Subject to HTTP 429 on rapid bursts. |

## Notes

- **No API key for Tavily itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect tavily`.
- The action list above is a snapshot; `npx @useclawlink/cli actions tavily` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
