---
name: verification-contract
user-invocable: false
version: 1.3.0
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
description: >
  Internal contract: one compact frozen ACCEPTANCE.md per delivery unit, its
  validation ladder, anti-weakening rules, and blob-bound execution receipt.
  Consumed by planners, execute-phase, and review-change.
---

# Verification Contract (internal)

Single owner of the delivery finish line. Planning freezes it; executors may
strengthen coverage but cannot move it; review checks the same bytes.

## Artifact

Every new feature/fix carries `ACCEPTANCE.md` beside its SPEC. Copy the matching
repository template. Required parts: `Status: frozen`; one stable ID per SPEC
criterion; `Required outcome`; named `Validator`; literal quality floor; project
commands. Prefer commands, otherwise use `read-verified: <evidence>` or
`manual: <exact observation>`. Unlabelled prose is invalid. A planned test may
name its future project runner; it cannot substitute a narrower runner later.

**Validator stability.** A validator must never gate on a surface other workflow
actors mutate — the branch diff as a whole, the session log, progress entries,
review ledgers, or forge state — because any out-of-unit commit (a session-log
append, another unit's fold) then re-fails a frozen criterion on a finished unit
and re-opens its review loop. Grep the unit's own files and outputs; a
diff-based validator enumerates the unit's paths or excludes the
workflow-mutated surfaces explicitly (docs/LOGS.md, the unit's own docs
directory, harness/toolstate).

## Freeze and receipt

At first execution run `git hash-object <unit>/ACCEPTANCE.md` and append to the
unit progress file:

```text
## Acceptance receipt v1
- Manifest: <path> · Blob: <sha> · Status: frozen · Verified: <date>
```

Before every phase and final review, recompute it. Exact match continues;
missing/mismatched evidence stops before edits:

```text
ACCEPTANCE GATE — <unit> BLOCKED
Expected blob: <sha|missing> · Actual: <sha|missing>
Reason: the frozen finish line is missing or changed.

→ Next: restore the frozen manifest, or obtain explicit user approval for a
  SPEC amendment and replacement manifest; then write a fresh receipt
  · never edit tests, commands, or acceptance to make the current candidate pass
```

A legitimate change requires, in order: explicit user approval; dated SPEC
`## Amendments` row; replacement manifest; committed fresh receipt. The
executor never self-authorizes it.

Legacy unit with no manifest mention: fingerprint committed `SPEC.md` and record
`Manifest: legacy SPEC.md`. A new plan or any plan naming the manifest fails
closed when it is missing.

## Validation ladder

Evaluate every row plus the normal project gate:

- `PASS`: commands green; read evidence present; manual checks named.
- `FAIL`: validator disproves the candidate; include compact failure evidence.
- `NEEDS-DECISION`: missing product/architecture choice.
- `BLOCKED`: command/input/environment unavailable; name it.

## Anti-gaming rules

Forbidden: deleting, skipping, narrowing, or loosening a validator; suppression,
stub, hard-coded answer, or no-op fix used to manufacture green. A command cannot
prove an untested read/manual row. Stronger regression tests are allowed. Repair
test setup only when assertions stay at least as strong and the reason is logged.

## Test immutability

A test, once written, is **immutable**. The executor fixes code until green,
never the test — editing an expectation to match behaviour is not a fix, it is
a cover-up. The sole legitimate amendment is a **proven mis-encoding of external semantics**: the test's expectation contradicts the actual
documented semantics of the platform/library/language, cited from authoritative documentation — not a product decision change. Even that surfaces as a
**finding plus a SPEC amendment**, never a silent edit to go green.

The deterministic backstop for this rule is the feature 60 path-protection
checkpoint (`path-protection@1` in the turn contract): the Tier 1 gate fails a
protected-path change with no recorded justification/approval, and the pi guard
blocks the write before it lands. This manifest is the finish line those
recorded escapes are checked against.

Prevention rides the research gate (**research-before-encode**): platform
semantics are verified against authoritative documentation **before a test encodes them**, so **adding stronger tests stays allowed**; **editing expectations never** (except the proven-mis-encoding path above).

## Done when

Frozen manifest + current blob receipt + named validators + literal quality
floor; executor and reviewer evaluate identical bytes.
