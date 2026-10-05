---
name: citation-monitor
version: 0.1.0
license: MIT
description: |
  Track brand mention citations across 4 LLMs (Claude, ChatGPT, Perplexity, Gemini)
  for a configurable list of brand keywords. Daily cron pulls write to local sqlite.
  Weekly markdown report shows mention counts, position, and citation deltas.
  Powers citelift.app SaaS upgrade path. Local-first; Supabase + n8n optional later.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
triggers:
  - /citation-monitor
  - "track brand mentions"
  - "AEO citations"
  - "monitor LLM citations"
  - "citation tracking"
  - "AEO scoring"
---

# citation-monitor v0.1.0

## Purpose

Answer the question: **"Is my brand showing up when buyers ask LLMs for recommendations?"**

Daily, query 4 LLMs with a fixed prompt set per tracked brand. Score each response for
brand mention, list position, and citation URL presence. Store in sqlite. Render a
weekly markdown report with deltas.

## Architecture (v0.1.0 — local-first)

| Layer       | Implementation                                      |
|-------------|-----------------------------------------------------|
| Inputs      | `tracked-brands.json` (brand + keywords + niche)    |
| Engines     | Claude (full), OpenAI (full), Perplexity (stub), Gemini (stub) |
| Storage     | sqlite at `data/citations.db`                       |
| Schedule    | cron-friendly entry point `scripts/run_daily.py`    |
| Reports     | `reports/<yyyy-ww>.md` markdown with deltas         |

Upgrade path (v0.2+): Supabase Postgres + n8n cron + multi-tenant brand list.

## Schema (sqlite)

```
citations(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  brand TEXT NOT NULL,
  keyword TEXT NOT NULL,
  engine TEXT NOT NULL,
  query TEXT NOT NULL,
  response_excerpt TEXT,
  mention_count INTEGER DEFAULT 0,
  position INTEGER,           -- 1-indexed list position; NULL if not mentioned
  citation_url TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Execution Flow

1. **Init (one-time)** — `python scripts/init_db.py` creates `data/citations.db`.
2. **Daily run** — `python scripts/run_daily.py` reads `tracked-brands.json`, loops
   brand x keyword x engine x prompt-template, calls each engine, scores response,
   inserts row.
3. **Weekly report** — `python scripts/weekly_report.py` reads sqlite, computes
   week-over-week deltas, writes `reports/<yyyy-ww>.md`.

## Triggers in conversation

When the user says any of:

- "track citations for SkynetLabs"
- "run citation monitor"
- "weekly AEO report"
- `/citation-monitor`

Read `tracked-brands.json`, run `scripts/run_daily.py`, then offer to render the
weekly report.

## Cost guardrails

- Default model IDs: `claude-haiku-4-5` and `gpt-4o-mini`. Cheapest tier per provider.
- Anthropic prompt caching enabled (5-min ephemeral) on the system prompt — every
  brand+keyword tuple shares the system prompt, so cache hit rate is high.
- One run = ~24 API calls (3 brands x 2 engines x 4 prompts). At Haiku + Mini pricing,
  approximately $0.01-0.03/day.

## Constraints

- No fake-claims content. No em-dashes in any output.
- v0.1 ships Claude + OpenAI fully. Perplexity + Gemini raise `NotImplementedError`
  with a clear `v0.2 — needs <KEY>` message.
- Python 3.11+. Pinned deps in `requirements.txt`.

## Files

- `SKILL.md` — this file
- `README.md` — quick start
- `requirements.txt` — pinned deps
- `.env.example` — required env vars
- `tracked-brands.example.json` — input shape
- `scripts/init_db.py` — sqlite schema
- `scripts/run_daily.py` — main loop
- `scripts/query_engines.py` — engine abstractions
- `scripts/weekly_report.py` — markdown report
- `references/prompt-templates.md` — exact prompts
- `references/aeo-scoring-rubric.md` — scoring math
- `data/.gitkeep`, `reports/.gitkeep`
