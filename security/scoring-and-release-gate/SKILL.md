---
name: scoring-and-release-gate
description: "Score a documentation package against the ten-dimension weighted rubric in `references/scorecard-rubric.md` with a cited justification per dimension, then evaluate the nineteen conditions in `references/release-gate-conditions.md` and emit a binary release-ready, conditionally-ready, or not-ready verdict with per-condition evidence. Use when a verification pass is finishing, when reconciliation completes a round, or when CI needs a machine-readable gate result. This skill MUST be consulted because a score is not a gate — a package can average 96 out of 100 and remain unreleasable on a single unsupported public claim, and conflating the two is how audit-ready packages ship with unverified security claims."
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: Explore
---

# Scoring and Release Gate

Two separate judgments that must never be collapsed: how good the package is, and whether it may be released.

## Iron Law

**THE GATE IS BINARY AND CONJUNCTIVE — 19 of 19 or NOT-RELEASABLE. A high score never substitutes for a failed condition.**

The score is a quality signal for the people improving the package. The gate is a release decision. A 98 with one unapproved public claim is `not ready`, and the 98 is irrelevant to that fact.

## Scoring

Ten weighted dimensions summing to 100. Full tests and 0/3/5/8/10 anchors: `references/scorecard-rubric.md`.

| # | Dimension | Weight |
|---:|---|---:|
| 1 | Evidence grounding and freshness | 18 |
| 2 | Coverage and completeness | 12 |
| 3 | Technical correctness | 15 |
| 4 | Cross-document consistency | 10 |
| 5 | Due-diligence decision value | 10 |
| 6 | Onboarding and operability | 10 |
| 7 | Security, privacy, and disclosure safety | 10 |
| 8 | Reliability and verification depth | 5 |
| 9 | Public usefulness and claim integrity | 5 |
| 10 | Clarity and maintainability | 5 |

Two rules:

- **Every deduction cites at least one finding ID.** A deduction with no finding is a mood. If the deduction is real, write the finding.
- **Every dimension must reach `gate.minDimensionPercent` of its available points** (default 80%). This is a gate condition, not a scoring rule — it exists so a package cannot average well while failing one dimension outright.

## Who scores what

Each verification pass scores independently, seeing only its own findings. **Do not calibrate toward the other passes or toward an expected number** — variance across passes is the signal three passes exist to produce, and averaging it away in advance destroys it.

`dossier-scorer` issues the final score and is the **only** issuer of the gate verdict. It sees the final package, the adjudicated findings ledger, and the resolved scope — never the drafting rationale, never the repair rationale, never the author's self-score.

## The mechanical / judgment split

Most of the nineteen conditions are checkable by script; the rest need a model to read the package.

This split is load-bearing. A script that evaluated only the mechanical conditions and emitted `PASS` would make the entire system theater: link-checking and header parsing would certify a package whose security claims were never read. So:

**`bin/dossier-gate.sh` structurally refuses to emit PASS without a `dossier-scorer` verdict file covering the judgment conditions.** Absent that file the result is `NOT-READY` with `reason=no-scorer-verdict`, never a pass. `tests/bin-scripts.test.sh` asserts this specific behaviour.

Per-condition tags and checks: `references/release-gate-conditions.md`.

## The nineteen conditions

`G01` score ≥ `gate.minScore` · `G02` every dimension ≥ `gate.minDimensionPercent` · `G03` no unresolved Critical or High finding · `G04` no unsupported or unapproved public claim · `G05` every required human approval recorded · `G06` no secret, credential, personal data, or prohibited disclosure present · `G07` no known contradiction that could materially mislead · `G08` canonical coverage 100% including justified `N/A` · `G09` every material internal claim has a state and locator · `G10` every public claim maps to `V`/`C` disclosure-approved evidence · `G11` links, paths, and diagram syntax validate · `G12` commands and examples executed or visibly marked not executed · `G13` planned behaviour not presented as implemented · `G14` targets not presented as measured results · `G15` policies not presented as implemented controls · `G16` unresolved uncertainty and source limitations visible · `G17` reviewer-pass independence method disclosed, including model diversity · `G18` no hard-category prose-clarity violation exists in the package · `G19` no unresolved Critical or High dependency vulnerability lacks a recorded disposition.

Conjunctive. All nineteen, or not releasable.

## Verdicts

| Verdict | Condition |
|---|---|
| `release-ready` | All 19 pass |
| `conditionally ready` | Failures are all `needs-owner` or blocked by a stated access limitation — nothing further the run can do |
| `not ready` | Anything else |

Never claim perfection. When a condition cannot pass because evidence does not exist, say exactly that and name the evidence needed. A `conditionally ready` package with three named blockers is a useful deliverable; a `release-ready` package that quietly skipped a condition is a liability.

## Owner-decision items block

An unmade business, legal, or disclosure decision is a real reason a package is not release-ready. `needs-owner` rows block `G05` and `G07`, and overriding a gate condition is a Tier 3 action requiring explicit human confirmation — recorded with who overrode it and why.

## Output Format

```markdown
## Scorecard — round {n}

| # | Dimension | Weight | Score | Weighted | Min required | Meets min | Justification (finding IDs) |
|---:|---|---:|---:|---:|---:|---|---|

TOTAL={n}/100  MIN_DIMENSION_MET={yes|no}

## Release Gate

| ID | Condition | Type | Result | Evidence |
|---|---|---|---|---|
| G01 | {condition} | mechanical | PASS / FAIL | {value or locator} |

GATE_VERDICT={release-ready|conditionally ready|not ready}
GATE_FAILED_CONDITIONS={G04,G10}
SCORER_VERDICT_PRESENT={yes|no}

### Blockers
| Condition | Why it fails | Exact next action | Owner | Evidence required |
|---|---|---|---|---|
```

The blocker table is the most-read output of the whole package. Every row must name a specific artifact or decision — "improve evidence coverage" is not an action; "obtain the approved data-retention record for the analytics store" is.

## Rationalization Prevention

| Excuse | Response |
|--------|----------|
| "96 out of 100 is clearly good enough to release" | The gate is not the score. Which of the nineteen failed? |
| "The mechanical checks all pass, so the gate passes" | Then no one read the security claims. Without a scorer verdict the result is `not ready`. |
| "One public claim is pending approval, everything else is clean" | `G04` and `G10` fail. That is `not ready` or `conditionally ready`, never `release-ready`. |
| "This dimension scores low but it is a small weight" | `G02` applies per dimension regardless of weight. That is why it exists. |
| "I deducted three points for general vagueness" | Cite the finding. If there is no finding, write one or restore the points. |
| "The other passes scored higher, I will adjust" | Then you have destroyed the signal. Report your score. |
| "Owner approval is a formality, mark it approved" | Then approval means nothing. `pending` blocks the gate by design. |
| "We hit max rounds, call it release-ready" | Rounds exhausted with open findings is `conditionally ready` with named blockers. |

## Integration

Loaded by all three verification passes for independent scoring, and by `dossier-scorer`, which alone issues the verdict. `/dossier:gate` runs `bin/dossier-gate.sh` for the mechanical set and dispatches `dossier-scorer` for the judgment set. `finding-reconciliation` supplies the adjudicated ledger. CI reads `GATE_VERDICT` as an exit condition.

References: `references/scorecard-rubric.md`, `references/release-gate-conditions.md`, `references/finding-schema.md`.
