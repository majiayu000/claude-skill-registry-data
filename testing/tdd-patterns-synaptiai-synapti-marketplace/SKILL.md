---
name: tdd-patterns
description: "Guide test-driven development through the mandatory Red-Green-Refactor cycle: a test is RED only when it fails for the intended reason, its expected value has a stated source (spec, reference implementation, hand computation, fixture, or standard — never the implementation's own output), and its input discriminates the right implementation from the plausible wrong one. Also enforces run-mode test runners and the `testing.tddMode` opt-out. Use when implementing features or fixing bugs (with `testing.tddMode='enforce'` blocking implementation without a failing test). This skill MUST be consulted because test-first is the primary quality enforcement point; tests that pass on first write, tests with self-referential expectations, and tests on degenerate inputs are the observed ways agents write tests that cannot fail."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, TaskCreate, TaskList, TaskUpdate
context: fork
agent: general-purpose
paths:
  - "**/*.test.{js,jsx,ts,tsx,mjs,cjs}"
  - "**/*.spec.{js,jsx,ts,tsx,mjs,cjs}"
  - "**/__tests__/**"
  - "**/test_*.py"
  - "**/*_test.py"
  - "**/tests/**.py"
  - "**/spec/**.rb"
  - "**/*_spec.rb"
  - "**/*_test.go"
  - "**/test_*.rs"
---

# TDD Patterns

## Contract

Iron law: if you did not watch the test fail, you do not know it tests the right thing. Invoked by `/flow:start` Phase 3 CODE step 3 (per task, before production code) and by `/flow:address` for behavior-changing fixes; `testing.tddMode` governs enforcement. Returns, per behavior, three tracked tasks: a RED test with a sourced expected value and a non-degenerate input, GREEN code, REFACTOR with all tests passing. Permitted skips: `tddMode=off`; `tddMode=suggest` with `tddModeOptOut=true` plus an explicit user decision; refactors (existing tests suffice); config changes without behavior change.

## Where expected values come from

An expected value is derived from the spec, a reference implementation, hand computation, an existing fixture, or an external standard, and the test states which (test comment; evidence-bundle column `Source of expected`). Never run the implementation and paste its output as the expectation. A literal with no stated source is a finding.

## Inputs must discriminate

Before testing a risky area (the task's `Risk areas:` rows, from the specification's `### Risk map`), state the plausible wrong implementation and choose an input on which right and wrong differ. Degenerate inputs (identical elements, symmetric or palindromic data, zero, one value repeated in every slot, the simplest possible case) are not coverage of order-, position-, or value-sensitive behavior. Bias randomized inputs toward interesting state and code paths rather than one shared rejection path; prefer structured generators over raw bytes.

## Red-Green-Refactor

Three tasks per behavior:

```
TaskCreate("RED: Failing test for {behavior}", "Sourced expectation, discriminating input, fails first.")
TaskCreate("GREEN: Implement {behavior}", "Simplest passing code.")
TaskCreate("REFACTOR: Clean up {behavior}", "All tests still pass.")
```

A test is RED only when (a) it fails on first run for the intended reason, (b) its expected value has a stated source, and (c) its input is not degenerate for the behavior under test. A test that passes on first write is checked by breaking the implementation deliberately and watching it fail. REFACTOR runs ALL tests after each step; new functionality is a new RED. TaskList confirms the cycle before the next behavior.

## Independent re-derivation

After implementing, for each `Risk areas:` row re-derive the expected result without reading the production code (from the spec, by hand, or with a throwaway independent computation) and compare with the test's assertion. Resolve mismatches before completing the task.

These rules are the behavior; never name techniques as instructions ("use property-based testing"): naming yields the surface, not the checks.

## Runner discipline

Run mode only, never watch mode: `vitest run`, `CI=true jest`, `pytest`, `rspec` (not `guard`). Watch mode leaves orphans: `pgrep -f "vitest|jest|pytest"`.

## When TDD applies

Feature or bug fix: always (reproducing test first). Refactor: existing tests before and after. Spike: tests before merging. Config: only if behavior changes. Mock only external boundaries, never the module under test.

## `testing.tddMode`

`enforce` (default): no production code without a RED test. `suggest`: recommend TDD; override needs an explicit user decision. `off`: no TDD guidance; tests still run in verification. Opt-out needs both fields; while `tddModeOptOut` is `false` (default), `tddMode` stays `enforce`:

```json
{ "testing": { "tddMode": "suggest", "tddModeOptOut": true } }
```

## Stop conditions

| Trigger | Action |
|---|---|
| Test passes on first write | Break the code deliberately; if it still passes, rewrite the test. |
| "Skip TDD just this once" | Delete the code; start from RED. |
| Risk area tested only with degenerate inputs, or literal without source | Fix the test before GREEN. |
