---
name: determinism-audit
description: "Scan the C# simulation and controller code for non-deterministic patterns that break reproducibility: wall-clock reads, unordered collection iteration, unseeded RNG, order-dependent float accumulation, and Job/thread races. Produces a prioritised report with file:line locations and remediation. Run before any sim/controller merge and before a release gate."
argument-hint: "[full | time | order | random | float | concurrency | quick]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, Task
model: sonnet
agent: determinism-engineer
---

# Determinism Audit

Project Aegis is a deterministic wargame: a given `(scenario, seed)` must produce
the identical order log and end-state on every run and machine (req 03, req 04).
The delegation design spec's core invariant is that controllers are **pure
functions of (observed state, traits, seed)**. This skill systematically scans
the C# codebase for the patterns that silently violate that invariant and
produces a prioritised remediation plan.

The danger of non-determinism is that it is **invisible until it isn't** — every
unit test can pass while replays diverge on a different machine or a different
day. This audit catches the cause before it costs a debugging week.

**Run this skill:**
- Before merging any change to the sim, controller, or policy layers
- Before the Polish → Release gate (alongside `/replay-verify`)
- After adding any new RNG, collection iteration, or Job on the sim path
- When `/replay-verify` reports a divergence and you need to find the source

**Output:** `production/determinism/determinism-audit-[date].md`

---

## Phase 1: Parse Arguments and Scope

**Modes:**
- `full` — all categories (recommended before release)
- `time` — wall-clock / timing reads only
- `order` — collection iteration ordering only
- `random` — RNG seeding only
- `float` — floating-point order sensitivity only
- `concurrency` — Job/thread/async races only
- `quick` — high-severity categories only (time + random + order)
- No argument — run `full`

Read `.claude/docs/technical-preferences.md` for engine/language (expected: Unity
+ C# / DOTS). The audit targets C# source.

---

## Phase 2: Establish the Deterministic Boundary

Not all code must be deterministic — only the sim path. Classify directories
before scanning so presentation code is not flagged as a false positive.

**Must be deterministic (scan these):**
- `src/**/Sim/`, `src/**/Core/`
- `src/**/Controllers/`, `src/**/Policy/`, `src/**/Decision/`
- `src/**/Traits/`, `src/**/Attention/`, `src/**/Roe/`, `src/**/Targets/`, `src/**/Trust/`
- `src/**/Orchestration/`, `src/**/Groups/`

**Presentation-only (exempt — note but do not flag):**
- `src/ProjectAegis.Delegation.UnityAdapter/**` rendering / UI / audio glue
- Anything purely visual

If the directory layout differs, glob `src/**/*.cs` and infer the boundary from
namespaces and `using UnityEngine` usage; report the boundary you used.

---

## Phase 3: Spawn Determinism Engineer

Spawn `determinism-engineer` via Task. Pass:
- The audit scope/mode
- The deterministic boundary established in Phase 2
- A manifest of the in-scope source files

The agent runs the scan across the categories below and returns findings with
`file:line` locations. Collect the full findings before proceeding.

---

## Phase 4: Audit Categories

Each finding records the offending `file:line`, the pattern, and whether it sits
on the deterministic path (findings on presentation-only code are informational).

### Category 1: Time and Timing
Grep (in-scope dirs): `DateTime.Now`, `DateTime.UtcNow`, `DateTime.Today`,
`Stopwatch`, `Environment.TickCount`, `Time.deltaTime`, `Time.time`,
`Time.realtimeSinceStartup`.
Flag any use inside controller/sim logic. The sim must advance on its **fixed
tick**, never wall-clock.

### Category 2: Collection Ordering
Grep: `Dictionary<`, `HashSet<`, `.Keys`, `.Values`, `foreach` over a dictionary,
`GroupBy`, `ToLookup`, `Distinct`, `OrderBy` without a total-order key.
Flag any case where iteration order affects a result or an emitted order. Prefer
`SortedDictionary`/`SortedSet`, or sort a `List` by a stable key before iterating.

### Category 3: Randomness
Grep: `new Random(` (check for an explicit seed argument), `System.Random`,
`UnityEngine.Random`, `Random.Range`, `Random.value`, `Guid.NewGuid(`.
Flag: unseeded `System.Random`, any `UnityEngine.Random` on the sim path, and
`Guid.NewGuid()` used as logical identity. All sim randomness must derive from
the sim seed via reproducible sub-streams.

### Category 4: Floating-Point Order Sensitivity
Grep: `Sum(`, `Aggregate(`, `Average(`, `+=` on `float`/`double` inside loops
over collections, `Math.Sin`/`Cos`/`Sqrt`/`Pow` and `Mathf.*` on the sim path.
Flag order-dependent reductions across entities and inconsistent `float`/`double`
mixing. Recommend stable reduction order, a pinned math path, or fixed-point for
values that feed branches.

### Category 5: Concurrency
Grep: `Parallel.For`, `Parallel.Invoke`, `Task.Run`, `async`/`await` on the sim
path, `[BurstCompile]`, `IJobParallelFor`, `.Schedule(`, shared mutable statics.
Flag any parallel write whose interleaving or scheduling order can affect results.
Job results feeding a shared accumulator must be combined in a deterministic order.

### Category 6: Hidden Global State
Grep: `static` mutable fields on the sim path, singletons holding mutable state,
`DateTime`/culture-dependent parsing (`float.Parse` without `InvariantCulture`).
Flag culture-dependent parsing/formatting and mutable statics that leak between
runs.

---

## Phase 5: Classify Findings

**Severity:**
| Level | Definition |
|-------|-----------|
| **CRITICAL** | On the deterministic path and certain to cause replay divergence (unseeded RNG, wall-clock in controller logic, ordered action over an unordered dictionary) |
| **HIGH** | On the deterministic path and likely to diverge across runs/machines (order-dependent float reduction, Job race) |
| **MEDIUM** | On the deterministic path but divergence is conditional or hard to trigger (culture-dependent parse, latent mutable static) |
| **LOW** | Defence-in-depth / clarity — e.g., presentation code that should be explicitly marked exempt to prevent future confusion |

**Status:** Open / Accepted Risk / Off Deterministic Path (informational)

---

## Phase 6: Generate Report

```markdown
# Determinism Audit Report

**Date**: [date]
**Scope**: [full | time | order | random | float | concurrency | quick]
**Engine**: [engine + version]
**Deterministic boundary**: [list of dirs scanned as must-be-deterministic]
**Audited by**: determinism-engineer via /determinism-audit
**Files scanned**: [N C# files on the deterministic path]

---

## Executive Summary

| Severity | Count | Must Fix Before Merge/Release |
|----------|-------|------------------------------|
| CRITICAL | [N] | Yes — all |
| HIGH | [N] | Yes — all |
| MEDIUM | [N] | Recommended |
| LOW | [N] | Optional |

**Reproducibility recommendation**: [DETERMINISTIC — SAFE TO MERGE /
FIX CRITICALS FIRST / DO NOT MERGE]

---

## CRITICAL Findings

### DET-001: [Title]
**Category**: [Time / Order / Random / Float / Concurrency / Global State]
**File**: `[path]` line [N]
**Pattern**: `[the offending code/pattern]`
**Why it diverges**: [how this breaks reproducibility]
**Remediation**: [specific change — e.g., "derive a seeded sub-stream", "replace
Dictionary iteration with a List sorted by EntityId"]
**Effort**: [Low / Medium / High]

[repeat per finding]

---

## HIGH Findings
[same format]

## MEDIUM Findings
[same format]

## LOW Findings
[same format]

---

## Off Deterministic Path (informational)

Patterns found in presentation-only code (UnityAdapter rendering/UI/audio). These
are acceptable but should be explicitly fenced from the sim path.

| File:line | Pattern | Note |
|-----------|---------|------|

---

## Accepted Risk

[Any findings explicitly accepted by the team with rationale.]

---

## Remediation Priority Order

1. [DET-NNN] — [1-line description] — Est. effort: [Low/Medium/High]
2. ...

---

## Next Step

After remediating CRITICAL/HIGH findings, run `/replay-verify` to confirm the
fixes actually restore byte-identical reproduction. A clean audit is necessary
but not sufficient — only a passing golden replay proves determinism.
```

---

## Phase 7: Write Report

Present the executive summary plus CRITICAL/HIGH findings in conversation.

Ask: "May I write the full determinism audit report to `production/determinism/determinism-audit-[date].md`?"

Write only after approval.

---

## Phase 8: Gate Integration

This report pairs with `/replay-verify` for the **sim merge gate** and the
**Polish → Release gate**.

**If CRITICAL findings exist:**
> "⛔ CRITICAL determinism findings will break replay. Resolve them, then run
> `/determinism-audit quick` to confirm, and `/replay-verify` to prove
> reproducibility, before merging sim/controller changes."

**If no CRITICAL/HIGH findings:**
> "✅ No blocking determinism findings on the deterministic path. Report written
> to `production/determinism/`. Run `/replay-verify` to confirm byte-identical
> reproduction before merge."

---

## Collaborative Protocol

- **Never auto-fix findings** — report `file:line` and the remediation; let the
  developer (or `determinism-engineer` in a follow-up task) apply changes.
- **Respect the boundary** — patterns in presentation-only code are informational,
  not failures. Always report which boundary you used.
- **A clean audit is not proof** — only `/replay-verify` proves determinism. State
  this in the verdict.
- **Accepted risk is valid** — but on the deterministic path it must be justified
  (e.g., "this `float` reduction is over a single element, order-independent").
