---
name: web-search
description: Search the web via DuckDuckGo. Use when you need to find current information, discover URLs for deeper reading, or research a topic beyond your training data.
---

# Web Search

Your knowledge has a cutoff. The world does not. When a question requires current information — prices, events, announcements, regulations, people — search before answering.

Search finds URLs. It does not read them. When a result looks relevant, follow up with WebFetch to read the full page. Search and read are separate acts — keep them separate.

## Usage

```bash
.agents/skills/web-search/search "query"
```

| Flag | Effect |
|------|--------|
| `--max N` | Number of results (default: 5) |
| `--news` | Search news instead of web (includes source and date) |
| `--region xx-xx` | Region bias (e.g. `cn-zh`, `us-en`, `hk-tzh`) |

### Examples

```bash
.agents/skills/web-search/search "TSMC N2 production timeline 2025"
.agents/skills/web-search/search "semiconductor export controls" --news
.agents/skills/web-search/search "美联储利率决议" --max 10 --region cn-zh
```

## When to search

- User asks about something that changes (prices, policies, people, events)
- You need to verify a claim or find a primary source
- You are building a view and need current evidence
- The heartbeat flags a thread worth following

## When not to search

- The answer is in the workspace (check WORLDVIEW.md, views/, journal.jsonl first)
- The question is conceptual or analytical — search adds noise, not signal
- You already have a URL — use WebFetch directly
