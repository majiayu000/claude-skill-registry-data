---
name: test-first-discipline
version: "1.0.0"
user-invocable: false
description: "Hard discipline for behavior-changing work: write a failing test first, observe the failure, then write minimal production code; delete production code written before a failing test was observed. Distinct from test-suite-ensure (post-hoc coverage/scaffold). Referenced by PDCA execution stages. Triggers — 「测试先行」「先写失败测试」「红绿重构」「TDD 铁律」「test-first」 / test-first discipline, failing test first. Do NOT use as a name alias for tdd or test-driven-development."
---

# Test-First Discipline

> Internal shared skill. Single source of truth for **failing-test-first** implementation order. Hosts declare it in `dependencies` and abort if missing — no silent fallback.
>
> **Name note:** intentionally **not** named `tdd` or `test-driven-development` (external skills repos). Use this name only.

## Iron Law

**NO PRODUCTION BEHAVIOR CODE WITHOUT A FAILING TEST OBSERVED FIRST.**

1. Write the failing test (or equivalent automated failing check).
2. Run it and **observe** the failure in the current session.
3. Write the **minimal** production code to pass.
4. Re-run; then refactor if needed while staying green.

If production behavior code was written before step 2: **delete it** and restart from the failing test. Do not keep it as "reference" or "adapt while writing tests".

## When it applies

**Applies:** new features, bug fixes, behavior-affecting refactors.

**Exceptions** (unless the user asks otherwise):
- Throwaway prototypes
- Generated code
- Pure configuration with no behavior under test
- Pure documentation
- **User-explicit skip** with a short recorded reason

Rationalizing "skip just this once" without an exception or user skip is forbidden.

## Distinct from `test-suite-ensure`

| Skill | Owns |
|-------|------|
| `test-first-discipline` | **Order** — red before production behavior code |
| `test-suite-ensure` | **Post-hoc** — stack detect, scaffold, generate/run coverage for existing logic |

A green `test-suite-ensure` run **MUST NOT** be reported as compliance with this skill. Hosts that use both: follow test-first during behavior implementation; call test-suite-ensure afterward for gaps/scaffold (advisory or mandatory per host).

## Forbidden

- Claiming test-first compliance after only post-hoc test-suite-ensure
- Renaming or aliasing this skill to `tdd` / `test-driven-development` inside this repository
- Skipping the observed-red step for normal behavior changes without an exception or user skip

## Integration guide

- Hosts: one-line pointer in the execution stage — load this skill for behavior changes; keep test-suite-ensure as the separate post-task ensure step.
- Prefer `user-invocable: false`; users reach it through PDCA hosts.
- Compose with `completion-evidence-discipline`: the observed failing (and later passing) run must be fresh evidence when claiming red/green.
