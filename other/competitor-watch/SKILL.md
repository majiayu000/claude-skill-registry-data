---
skill_id: competitor-watch
name: Competitor Watch — track a competitor, ping on real moves
description: "Track what a competitor actually shipped — \"watch this competitor\", \"track what they ship\", \"what changed at\". Compares against the last snapshot and reports only real moves: launches, pricing changes, positioning shifts."
version: 1.0.0
category: research
office: cino
lead_agent: innovation-researcher
everyday_skill: true
triggers:
  - "watch this competitor"
  - "track what they ship"
  - "what changed at"
collaborates_with:
  - innovation-researcher
  - competitive-intel-analyst   # the depth this surfaces
  - orchestrator                # the unattended monitor (ADR-022, workflow #2)
references:
  unattended_version: orchestrator/workflows/competitor-watch.mjs
  adr_external_tool: documents/ADRs/ADR-018-external-tool-integration-pattern.md
  adr_workflow_standard: documents/ADRs/ADR-022-autonomous-workflow-standard.md
  adr_moat_framing: documents/ADRs/ADR-007-behavioral-moat-framing-doctrine.md
  adr_confidence: documents/ADRs/ADR-010-confidence-tag-technical-educator-rubric.md
confidence_default: 🟡 MEDIUM
---

# Competitor Watch

> **Does:** tracks what a named competitor is shipping and pings you only on **real** moves.
> **Solves:** finding out about a competitor's launch a month late.
> **Triggers on:** *"watch [competitor] and tell me what changes"*

## How Maxim does this

Routes to `competitive-intel-analyst` + web sources, compares against the last snapshot, and reports **only real moves** since — launches, pricing changes, positioning shifts — not noise. Each move gets a *so-what* (does it threaten your moat?), grounded in Porter / 7 Powers.

## Behavioral overlay

- **Frameworks (cited per ADR-007):** **Porter's Five Forces** · **7 Powers** · **signal detection** (real move vs. PR noise).
- **No-fabrication is load-bearing:** verified moves are stated as fact with the source; anything inferred (e.g. "likely targeting enterprise") is marked **inference**. Default **🟡 MEDIUM** for that reason.

## The unattended "monitor" version

`orchestrator/workflows/competitor-watch.mjs` — the read-only Workflow #2 from the standard: scheduled, **dry-run-default**, idempotent (won't re-report the same move), bounded + logged. Read-only, so it never acts — it only surfaces. Go-live just turns on the morning delivery.

## Output

Moves since last check (launch / pricing / positioning) · significance vs. your moat · sources · *fact vs. inference* marked.
