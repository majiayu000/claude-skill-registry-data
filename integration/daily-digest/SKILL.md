---
skill_id: daily-digest
name: Daily Digest — one filtered update on your niche
description: "Daily briefing on a topic — \"give me today's digest on\", \"what's new in\", \"daily digest for\". Pulls from web or a connected news connector, then filters and ranks to only what matters."
version: 1.0.0
category: research
office: cino
lead_agent: innovation-researcher
everyday_skill: true
triggers:
  - "give me today's digest on"
  - "what's new in"
  - "daily digest for"
collaborates_with:
  - innovation-researcher
  - orchestrator         # the unattended every-morning version (ADR-022)
external_tool:
  name: web / news / RSS connector (optional)
  pattern: ADR-018 — consume a connector for live feeds; falls back to web search
references:
  adr_external_tool: documents/ADRs/ADR-018-external-tool-integration-pattern.md
  adr_moat_framing: documents/ADRs/ADR-007-behavioral-moat-framing-doctrine.md
  adr_confidence: documents/ADRs/ADR-010-confidence-tag-technical-educator-rubric.md
confidence_default: 🟢 HIGH
---

# Daily Digest

> **Does:** one filtered update on your niche — only what actually matters.
> **Solves:** checking ten sources a day and missing the one thing.
> **Triggers on:** *"give me today's digest on [topic]"*

## How Maxim does this (signal, not noise)

Pulls from web search (or a connected news/RSS connector — ADR-018, *consume don't rebuild*), then **filters and ranks** to the handful that matter — deduping the same story across outlets and dropping the recycled noise.

## Behavioral overlay

- **Frameworks (cited per ADR-007):** **Signal-vs-noise filtering** · **Diffusion of Innovations** (is this an early signal or already mainstream?) · relevance ranking against *your* stated focus.
- **No-fabrication:** only real, cited items — never a synthesized "probably happened."
- **Confidence tag (ADR-010)** per item.

## The unattended "every morning" version

Wrapped by `mxm-orchestrator` (ADR-022) as a scheduled, **dry-run-default** workflow — same filtering, delivered each morning, bounded + logged. Same pattern as `inbox-triage`: consume a feed connector, govern it with Maxim.

## Output

3–7 ranked items that matter · why each matters · sources · what to ignore today.
