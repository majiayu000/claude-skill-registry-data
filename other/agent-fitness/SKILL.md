---
name: agent-fitness
agent: none
description: Track and surface sub-agent dispatch calibration ratios. Extract from JSONL transcript or read existing ledger. Per-agent clean/blocked/errored/partial trends.
allowed-tools: Bash, Read
user-invocable: true
triggers:
  - agent fitness
  - agent calibration
  - agent stats
  - sub-agent stats
  - which agents work
  - /agent-fitness
  - agent dispatch trends
---

# /agent-fitness

Three modes:

**`/agent-fitness extract`** — runs `python3 daemons/agent-fitness-extract.py` to scan the latest JSONL transcript and append new dispatch rows to `memory/AGENT_FITNESS.md`. Idempotent (dedup by session_id + tool_use_id).

**`/agent-fitness`** (no args) — runs `python3 daemons/agent-fitness-report.py`. Surfaces:
- Total dispatches (all-time, last 30d, last 7d)
- Per-agent calibration table (Total / Clean / Blocked / Errored / Partial / Ratio)
- Per-agent recent outcome trend (last 10 dispatches encoded as `c7 b1 e0 p0`)
- ⚠ Repeat-blocker callouts (any agent with >=2 blocks in window)
- Top 3 failing (agent, task) pairs

**`/agent-fitness --days 7`** — same as above but windowed to last N days. Useful for "is this agent failing more lately?"

## Computation

Calibration ratio per agent: `clean / (total − errored)`. The denominator excludes hard errors (infrastructure/tool failures) and only counts agent-level outcomes.

Trend signal: any agent with >=2 blocks in the window surfaces a repeat-blocker callout. The classifier was hardened in v0.5.1 to catch real Lyra-style block patterns ("BLOCKED:", "are denied", "blocker-found" etc).

## When to run

- After major sessions where multiple sub-agents fired (today S30d had ~7 dispatches)
- Periodically (weekly?) to spot trends
- Before relying on a sub-agent for something heavy ("am I about to dispatch an agent that's been failing?")

## What it does NOT do

- Does not auto-reroute dispatches based on calibration. Surfaces data; principal decides.
- Does not LLM-classify failures — heuristic only (keyword matching on result content).
- Does not pool across sessions for cluster analysis. Future v0.5.x.
- Does not include task-type clustering. All tasks pooled per agent.

## Cross-links

- [[concepts/Somatic v0.5.0 Agent Fitness]] — spec
- [[memory/AGENT_FITNESS]] — the data
- [[concepts/Somatic Roadmap]]
- [[memory/TRUST_DECAY]] — sibling claim → outcome ledger
