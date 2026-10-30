---
name: research
description: >-
  Research on the open web, in feeds and in notebooks: pick the method that fits
  the question — pulse for what people say right now, deep-research for a
  high-stakes investigation, research-summarizer for one paper or report,
  agent-reach for content behind a platform, searchmcp-research for an
  anti-detect multi-engine Camoufox pass, notebooklm for a NotebookLM notebook,
  llm-wiki for an Obsidian vault, rss-agent-viewer for feeds.
---

# research — choosing a research method

> Home branch in Memora: `root/skill/research`.
>
> Tool priority in Freebuff Desktop: (1) native `researcher_web` (for multi-step
> questions) and `web_search` / `read_url` (for quick lookups), (2) `searchmcp`
> (Camoufox via `call_mcp_tool`) for anti-detect multi-engine digests, (3) `parallel`
> MCP when authenticated.

## Choosing a part

| Question | Part |
|---|---|
| What are people saying *now*, in which direction is the conversation moving | `parts/pulse/` |
| High-stakes decision, comparing N options, validating a hypothesis with adversarial checks | `parts/deep-research/` |
| Digest one paper, article, report, or doc into structured findings | `parts/research-summarizer/` |
| Extract content behind a platform (X, Reddit, YouTube, GitHub, LinkedIn, Bilibili, RSS) | `parts/agent-reach/` |
| One broad anti-detect Camoufox web pass with digest, SIFT evaluation, and hypothesis spiral | `skills/research/parts/searchmcp-research/` |
| Read or drive a Google NotebookLM notebook via `preview_*` or `browsermcp` | `parts/notebooklm/` |
| Maintain an Obsidian knowledge vault on owner request | `parts/llm-wiki/` |
| Follow RSS/Atom feeds, discover feeds, export OPML | `parts/rss-agent-viewer/` |

## Rules

- Walk `root/skill/research` (and the project root) in Memora before starting; record synthesized findings and source verdicts as Memora nodes (large tables go to `_memory/reports/`, not into ad-hoc `sources/` folders).
- Report search telemetry (`queries / received / cited`) directly in the chat response and the Memora node.
- Gather scope/angle clarifications via a single batched `ask_questions` call with one-line consequences.
- Read the actual URL (`read_url` or `searchmcp`) before citing a claim; snippets are leads, not evidence.

## Related

`osint` (`skills/osint/parts/dossier/` for entity due diligence), `browser` (`preview_*` and `browsermcp` engines), `memory` (Memora RSI tree and `rsi_report_search`).
