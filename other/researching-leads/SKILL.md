---
name: researching-leads
description: Research each lead to find five specific facts with sources — funding, launches, hires, expansions, awards — so outreach can reference a real trigger event instead of being generic. Use after scraping leads and before writing outreach.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Researching Leads

## Goal
Find five true, sourced facts about each prospect — especially something that changed recently. That trigger event is what the outreach opener is built from.

## Why this step exists
An opener that says "I came across your website" gets deleted. One that says "I noticed you opened a second location" gets read. The difference is entirely this step. Everything downstream depends on it, so if research is thin, fix it here rather than letting the writer invent something.

## Prerequisites
- `ANTHROPIC_API_KEY` (research agent)
- `TAVILY_API_KEY` (web search — free tier is 1,000/month, plenty)

## Process

```bash
python -X utf8 scripts/01_b2b_contacts/research_lead.py \
    --input output/leads.json \
    --output output/researched.json \
    --limit 10 --workers 3
```

Run `--limit 10` first and read the facts. If they're generic ("they have a website", "they are located in Alabama"), the leads lack a findable web presence — reconsider the ICP rather than pushing on.

## What it does
An agent loop with two tools: Tavily web search, and a page fetcher. It searches for the person and company, reads the company site, and returns `fact1`..`fact5` with `explanation1`..`explanation5` (the source for each). The system prompt is the course's, unchanged, in `prompts/research_agent.md`.

## Guardrails worth knowing

- `--max-tool-calls` (default 8) caps tool calls **per lead**. An agent on a canvas can loop until your search quota is gone; this one stops.
- Checkpoints save every 5 leads. Ctrl-C at lead 400 of 1,000, then `--resume`, and it starts at 401 rather than re-paying for the first 400.
- Tavily keys rotate automatically — add `TAVILY_API_KEY_2`, `_3` and it moves on when one hits its monthly cap.

## Reading the output

| Field | Meaning |
|---|---|
| `facts_found` | 0–5 |
| `needs_research: true` | Nothing found. The outreach step will skip this lead rather than invent an opener. |
| `_tool_calls` | How hard it worked. Consistently hitting the cap means the leads are hard to research. |

A run where most leads come back `needs_research: true` is a signal about the list, not the script — the businesses have no findable web presence.

## Edge cases
- **"No Tavily API key configured"** — free at tavily.com, no card.
- **All keys exhausted** — add `TAVILY_API_KEY_2`; the free tier resets monthly.
- **Slow** — normal, several searches per lead. Raise `--workers` to 5, not higher; you'll hit rate limits.

## Cost
About $0.01–0.03 per lead. Tavily is free at this volume.
