---
name: using-pm-os
description: Session guardrails for PM OS - dynamic execution with dependency awareness.
---

# Using PM OS

## Operating Principles

- PM OS is modular. Run only the skill you need for the question at hand.
- Dynamic flow is allowed, but dependency hygiene is required.

## Dependency Hygiene

Before generating any downstream output (charters or PRDs):
1. Read `alerts/stale-outputs.md`
2. If any outputs are stale, report them and ask whether to refresh
3. If a downstream output is newer than its sources, flag potential drift and ask to reconcile

## Evidence Discipline

Follow `CLAUDE.md` rules:
- Never invent metrics, quotes, or roadmap facts
- Tag claims as Evidence, Assumption, or Open Question
- Always include Sources Used and Claims Ledger in outputs
