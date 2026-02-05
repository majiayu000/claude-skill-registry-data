---
name: web-search
description: Search the web for up-to-date information using GPT-5.2 with web search and high reasoning. Prefer this over webfetch when you need to research complex queries, find current info across multiple sources, get recent news, up-to-date documentation, or verify facts that may have changed since your training cutoff. Returns cited sources.
---

## What this skill does

Searches the web using a reasoning model with web search capabilities. Returns current, cited information from the internet rather than relying on potentially outdated training data.

## When to use this

- When you need current/recent information (news, updates, releases, etc.)
- When verifying facts that may have changed since training cutoff
- When researching topics that require up-to-date sources
- When the user asks about recent events or developments
- When handling complex queries that require reasoning and multiple searches

## How to use

Run the search script with your query as an argument.

**Query format:** Use full sentences, paragraphs, or lists of questions - not keyword searches. The model handles detailed, multi-part prompts well.

```bash
uv run ~/.config/opencode/skill/web-search/search.py "your detailed query here"
```

**Examples:**
```bash
uv run ~/.config/opencode/skill/web-search/search.py "What are the latest features in Python 3.13? I'm particularly interested in the new REPL improvements and any performance enhancements."
```

```bash
uv run ~/.config/opencode/skill/web-search/search.py "I need to understand how Font Awesome licenses their icons. Can I use their Pro icons in an open source project? What are the restrictions for SVG downloads versus the web font?"
```

## Important notes

- **Slow**: This typically takes 1-3 minutes due to web searching and reasoning. Set an appropriate timeout (180000ms+ recommended).
- **Requires OPENAI_API_KEY**: Must be set in environment.
- **Cost**: ~$0.10-0.20 per query (depends on response length and number of searches).

## Output format

The script outputs:
1. Cost breakdown (tokens, searches, total cost)
2. The response text with inline citations
3. A list of all sources with titles and URLs
