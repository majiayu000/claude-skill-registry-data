---
name: mk:brainstorming
preamble-tier: 3
version: 2.1.0
description: Generate or compare multiple technical approaches for one validated decision. Do not use for product discovery or an existing plan.
allowed-tools:
  - Read
  - Grep
  - Glob
  - AskUserQuestion
  - WebSearch
source: local
keywords:
  - brainstorm
  - explore-solutions
  - compare-approaches
  - trade-off-analysis
  - alternatives
when_to_use: Use for generating or comparing multiple technical approaches to one validated decision. NOT for product validation (mk:office-hours), debugging (mk:investigate), or critique of an existing plan (mk:plan-ceo-review or mk:elicit).
user-invocable: true
owner: research
criticality: medium
status: active
runtime: claude-code
---

# Brainstorming

Use for generating or comparing multiple technical approaches to one validated decision.

**Boundary:** `mk:office-hours` answers “should we build this?”; this skill answers “how should we build it?” A bare “brainstorm” request is ambiguous: ask whether the user wants product discovery/validation or technical approaches. Do not route from that word alone.

## Profiles

- **quick** / `--depth quick` (default) — restate the decision in one line; give 2-4 technically distinct options and one recommendation. If a material fact is missing, state the assumption rather than running discovery. Return inline and stop. Do not load techniques, scout, scoring, challenge, reports, plans, wiki candidates, memory, or handoff.
- **deep** / `--depth deep` — load the needed technique and use the deep workflow below. A report, HTML output, or handoff is optional and only produced when requested or needed by an active plan.

## Routing

| Situation | Route |
| --- | --- |
| New product, feature, or side-project value is unvalidated | `mk:office-hours` |
| Observed failure or root-cause work | `mk:investigate` |
| Existing plan, verdict, or brainstorm needs critique | `mk:plan-ceo-review` or `mk:elicit` |
| Generic Q&A or a single implementation detail | answer directly or use `mk:docs-finder` |

## Defaults

Use at least two alternatives. Quick returns 2-4; deep generates 3-8 and never more than 8. Keep multiple dimensions in one run when they serve one decision or report; split only 3+ independently shippable concerns.

## Quick Workflow

1. Restate the validated decision and any material assumption.
2. Give 2-4 technically distinct options with the key trade-off for each.
3. Recommend one option and return inline. Do not create a report, plan, wiki candidate, or memory entry.

## Deep Workflow

**`--advice` (optional, deep only):** when the flag is present, GUIDE fires after
step 1's frame and REVIEW after step 4's challenge pass, capped at 4 calls per run.
Athena supplies decision criteria and reads the chosen direction; it never generates
the option set, chooses for the user, or adds a gate. Without the flag there are zero
calls and no state. See `references/advice-checkpoints.md`.

1. Confirm the decision, binding constraint, success criterion, and excluded scope. Ask at most three focused questions when needed.
2. If 3+ independently shippable concerns are bundled, ask to choose one. Use a compact scout summary only when current codebase touchpoints change the decision.
3. Load one technique from `references/techniques/`; generate 3-8 technical approaches without scoring while generating.
4. Run one anti-bias pivot, then the challenge pass in `references/challenge-pass.md` before recommending.
5. Load scoring only for deep scoring. Write a report, HTML output, or handoff only when requested or needed by an active plan. For a requested report, an optional `mewkit wiki handoff suggest` follows `.claude/skills/wiki/references/terminal-handoff-advisory.md`; it is fail-open and never runs for quick.

## References

- `references/context-budget.md` — deep clarification, count, pivot, and challenge limits
- `references/techniques/` — choose one technique for a deep run
- `references/challenge-pass.md` and `references/scoring-criteria.md` — deep convergence only
- `references/editorial-html.md` — HTML only for a requested report
- `references/advice-checkpoints.md` — deep `--advice` checkpoints; load only when the flag is present
