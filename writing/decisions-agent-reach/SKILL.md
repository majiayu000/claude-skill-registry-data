---
name: decisions-agent-reach
description: Use with DecisionsAI when a ticket or workflow needs internet research — social posts, articles, video subtitles, GitHub, RSS, or competitor scans. Routes through Agent Reach upstream tools; run agent-reach doctor first.
---

# Decisions + Agent Reach

**I am fetching external sources so the user can decide or ship with evidence — not inventing citations.**

Agent Reach installs and routes upstream CLIs. Decisions adds workflow discipline: scope, evidence packets, and harness reporting.

## When to invoke

- Ticket asks to research, compare competitors, read tweets/Reddit threads, summarize a YouTube/Bilibili video
- User pastes a URL from Twitter, GitHub, a blog, or RSS
- Content workflows (`content-engine`, `article-writing`) need primary sources
- **Not** for: writing the final doc (use content skills), UI mockups (use `decisions-ui-ideation`), or posting/commenting on social platforms

## Workflow

1. Run `agent-reach doctor --json` — use each platform's `active_backend`.
2. Fetch in parallel when useful (Exa + Twitter + Reddit + web via Jina).
3. Save raw extracts under `/tmp/` or cite URLs — **never** write fetch artifacts into the project repo unless the ticket asks for committed research notes.
4. In the Decisions result packet include:
   - `Sources:` bullet list with URLs
   - `Method:` platform + backend used
   - `Summary:` what matters for the ticket decision

## Install / repair

If `agent-reach` is missing:

```
Install Agent Reach: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
```

Or from Decisions reference clone (after `bin/setup.py`):

```bash
pip install -e ../reference/agent-reach
agent-reach install --env=auto
```

Safe mode on shared servers: `agent-reach install --env=auto --safe`

## Skill pairing

| Task | Also use |
|------|----------|
| UI informed by trends | `decisions-ui-ideation`, `decisions-design-references` |
| Article from research | `content-engine`, `article-writing` |
| Verify a shipped page | `browser-qa`, `decisions-playwright` |
| Minimal implementation | `ponytail` |

## Full routing table

Read the projected **`agent-reach`** skill (`references/*.md`) — it is the source of truth for per-platform commands and retry chains.

Reference repo (local): `../reference/agent-reach` from DecisionsAI parent folder.
