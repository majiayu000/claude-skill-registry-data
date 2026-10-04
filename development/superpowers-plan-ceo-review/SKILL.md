---
name: superpowers-plan-ceo-review
description: >
  Use when asked to "think bigger", "expand scope", "strategy review", "rethink this",
  "is this ambitious enough", "CEO review", or "founder review". CEO/founder-mode review
  of an implementation plan — finds the 10-star product, challenges premises, expands scope.
  Requires a plan file as input.
---

> **DEPRECATED** — use `/plan-ceo-review` instead. This skill is a legacy alias and will be removed in a future cleanup.
# Plan CEO Review

**Purpose:** Rethink the problem, find the 10-star product, challenge premises. CEO/founder posture — strategy over tactics.

**Input:** An implementation plan file. Read it first.

---

## Trigger Detection

Run when the user says:
- "think bigger"
- "expand scope"
- "strategy review"
- "rethink this"
- "is this ambitious enough"
- "CEO review"
- "founder review"

Or proactively suggest when:
- The plan is significantly smaller than the stated ambition
- The plan solves a narrow version of a broader problem
- The user expresses dissatisfaction with the scope

---

## Four Review Modes

Detect mode from user intent:

| Mode | Posture | Trigger |
|------|---------|---------|
| **SCOPE EXPANSION** | Enthusiastic — push UP | Greenfield features, "go big" requests |
| **SELECTIVE EXPANSION** | Neutral — hold scope, cherry-pick | "Show me options" |
| **HOLD SCOPE** | Rigorous — make bulletproof | Bug fixes, refactors, hotfixes |
| **SCOPE REDUCTION** | Surgical — cut to essentials | Overbuilt plans, >15 files touched |

---

## Read the Plan

```bash
ls docs/superpowers/plans/*.md 2>/dev/null | head -5
cat docs/superpowers/plans/*.md 2>/dev/null | head -100 || echo "No plan found"
```

Extract:
- Goal and stated scope
- Architecture approach
- Key decisions
- What's explicitly NOT in scope
- Files to be created/modified

---

## Section 1: Architecture Review

Draw the current system as ASCII:

```
CURRENT SYSTEM
════════════════════════════════
[Component diagram]

What it does:
- [Point 1]
- [Point 2]

What's missing:
- [Gap 1]
- [Gap 2]
```

Challenge: Is this the right architecture? What does this look like at 10x scale? At 100x?

---

## Section 2: Error & Rescue Map

For every function/module:

| Function | Happy path | Nil path | Empty path | Upstream error |
|----------|-----------|---------|-----------|----------------|
| `process()` | ✓ | ? | ? | ? |
| `validate()` | ✓ | ? | ? | ? |

Every failure mode must have a name. "Handle errors" is not a name. "Missing user session returns 401" is a name.

Flag: catch-all error handlers, silent failures, error messages that don't help.

---

## Section 3: Security & Threat Model

- What can go wrong?
- What's the blast radius of a breach?
- What's the most valuable asset this system protects?
- Where are the trust boundaries?

---

## Section 4: Data Flow & Edge Cases

Trace every data path:

- Happy path
- Nil/null inputs
- Empty inputs
- Upstream service failures
- Concurrent access
- Large inputs (scale testing)

For each: what happens? What should happen? What's the gap?

---

## Section 5: Scope Expansion Proposals

For each section, ask: "What would the 10-star version of this look like?"

Generate expansion proposals:

```
SCOPE EXPANSION PROPOSALS
════════════════════════════════════════

[Section]: [Current scope] → [10-star scope]

Expansion A: [Name]
- What: [Description]
- Why it matters: [Impact]
- Risk: Low/Medium/High
- Effort: human: ~X / AI: ~Y
- RECOMMENDATION: [Include / defer / cut]

[Repeat for each section]
```

---

## Section 6: Error & Rescue Registry

Compile all named error cases from Section 2:

```
ERROR & RESCUE REGISTRY
════════════════════════════════
| Error name | Cause | Rescue | Owner |
|-----------|-------|--------|-------|
| Missing user session | No auth token | Return 401 | auth/ |
| Upstream timeout | External API down | Retry 3x + circuit break | http/ |
```

Every error gets a name. Every name gets a rescue path.

---

## Section 7: NOT in Scope

Explicitly list what the plan does NOT cover:

- Features that were considered and deferred
- Edge cases that are out of scope
- Future considerations

This prevents scope creep and grounds the review.

---

## Section 8: Completion Summary

```
PLAN CEO REVIEW
════════════════════════════════
Scope mode: [SCOPE EXPANSION / SELECTIVE / HOLD / REDUCTION]
Plan file: [path]
Findings: N sections reviewed
Expansions proposed: N
Expansions accepted: N
Errors named: N
Errors with rescues: N
════════════════════════════════
```

---

## Key Principles

- **Zero silent failures** — every error gets a name
- **Completeness first** — recommend the full version over shortcuts (see Boil the Lake)
- **Data flows have 4 paths** — happy, nil, empty, upstream-error
- **User is in control** — every scope change is an explicit opt-in via AskUserQuestion
- **ASCII diagrams mandatory** — if you can't draw it, you don't understand it

---

## Anti-Patterns Flagged

- Catch-all error handling
- Deferring tests
- "Shortcut vs complete" when complete costs minutes more
- Silent scope drift
- Vague TODOs
- "Handle errors" as an error name

---

## Completion Status

- **DONE** — All 8 sections complete, registry populated, expansion proposals generated
- **DONE_WITH_CONCERNS** — Review done but some expansions weren't accepted
- **BLOCKED** — No plan file provided
- **NEEDS_CONTEXT** — Need more context about the product/market to do CEO review
