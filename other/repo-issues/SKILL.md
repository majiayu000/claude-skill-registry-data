---
name: repo-issues
description: >
  Trigger: repo issues, project problems, architecture issue shortlist.
  Rank verified architecture gaps and pair them with proportional guardrails.
license: MIT
metadata:
  author: andresnator
  version: "2.1.1"
  status: testing
---

# Repo Issues

## Contract

Turn a verified `architecture-state` snapshot into a ranked architecture shortlist. Product repositories only; AI-harness analysis belongs to `absorb`, and code-level findings belong to Deep Plan.

Read-only. Each issue needs source/config/wiring evidence plus consequence. Documentation states intent, never proves behavior.

## Flow

1. Confirm target, state snapshot, optional focus.
2. Trace boundaries, dependency edges, CI wiring, operational hazards using imports, manifests, configs, or healthy graph.
3. Contrast claimed versus observed architecture. Record at least one `Holding up` item.
4. Reject preferences, unverified claims, disproportionate fixes, and code-level findings.
5. Rank surviving `FIX` and `CONDITIONAL` items by impact descending, effort ascending.
6. Give each issue smallest automated guardrail. Prefer no-cycles and allowed-dependencies checks; use manual check when automation costs more than value. Tool examples live in `references/fitness-functions.md`.

## Output

| Status | Issue | Evidence | Consequence | Impact | Effort | Fitness function |
|---|---|---|---|---|---|---|

List `Holding up`, rerouted code-level items, unknowns, and report path when written. Maximum seven shortlist items. No edits or speculative cleanup.
