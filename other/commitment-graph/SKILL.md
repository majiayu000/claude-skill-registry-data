---
name: commitment-graph
description: |-
  Turns data/commitments.jsonl (flat list) into a who-owes-what-to-whom graph.
  Surfaces overdue chains and cross-PA dependencies that the flat list hides.
  Triggers: "what's overdue", "what did X promise", "commitment graph", "who's blocking whom".
---

# Commitment Graph

A graph view over commitments.jsonl — surfaces overdue chains, cross-PA dependencies, and blockers.

## When to use
- Daily morning check (overdue chains)
- When asked "what's blocking X?" or "who owes me what?"
- Weekly retro (highlight repeat-offender commitments)

## Process
1. Load `data/commitments.jsonl`
2. Build directed graph: `requester → committed_by → action → due_date`
3. Output:
   - **Overdue** (due_date < today, status != done) — sorted by age
   - **Chains** (A waits on B waits on C) — flag any cycles
   - **Repeat offenders** — names appearing in 3+ overdue items in 30 days

## Script
`python skills/commitment-graph/scripts/graph.py [--overdue|--offenders]`
