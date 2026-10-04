---
name: testing-workflow
description: Run and manage functional tests (unit, integration, E2E, visual, mutation) for a React 18 + TypeScript + Material UI v7 + Emotion frontend. Use when running tests, debugging test failures, ensuring coverage, updating visual snapshots, or fixing mutation testing issues. Covers Jest + Testing Library, Apollo server tests, Playwright (E2E + visual regression), and Stryker. For load/performance and Lighthouse, use the load-testing and frontend-performance-accessibility skills instead.
---

# Testing Workflow Skill

## Profile keys consumed

- `make.test_unit_client`
- `make.test_unit_server`
- `make.test_integration`
- `make.test_e2e`
- `make.test_visual`
- `make.test_mutation`
- `make.merge_mutation_reports`
- `make.test_memory_leak`
- `make.start`
- `make.start_prod`
- `quality.coverage_statements`
- `quality.coverage_branches`
- `quality.coverage_functions`
- `quality.coverage_lines`
- `quality.mutation_msi`
- `quality.visual_diffs`
- `capabilities.visual_testing`
- `capabilities.mutation_testing`
- `capabilities.memory_leak_testing`
- `capabilities.load_testing`

All test invocations go through the profile's `make` target map. A `null`
value for a `make.*` key means the capability is absent: skip that suite
with an explicit capability-absent note instead of failing or improvising
a raw command. Generic tooling (`gh`, `bun`, `git`) may be invoked
directly when needed, but every test suite runs through its mapped target.

## Context (Input)

- Code changes require test validation
- Test failures need debugging
- Coverage, mutation score, or visual snapshots must be kept clean

## Task (Function)

Execute the appropriate test suite and ensure a 100% pass rate with the
required coverage, mutation score, and zero unintended visual diffs.

**Note**: For load/performance testing, see the
[load-testing skill](../load-testing/SKILL.md) (gated by
`capabilities.load_testing`). For Lighthouse, web-vitals, and accessibility
audits, see the
[frontend-performance-accessibility skill](../frontend-performance-accessibility/SKILL.md).
For the deeper Jest/Testing Library/Playwright authoring conventions
(jsdom vs. node envs, Mockoon + Apollo mock setup, accessible selectors),
see the
[frontend-testing-workflow skill](../frontend-testing-workflow/SKILL.md).

## Test Commands Quick Reference

| Test Type        | Invocation                               | Goal                                  | Typical location          |
| ---------------- | ---------------------------------------- | ------------------------------------- | ------------------------- |
| Unit (client)    | target mapped by `make.test_unit_client` | All pass, full coverage (jsdom + RTL) | `tests/unit/`             |
| Unit (server)    | target mapped by `make.test_unit_server` | Apollo mock node-env tests pass       | `tests/apollo-server/`    |
| Integration      | target mapped by `make.test_integration` | All pass, global 100% over `src/**`   | `tests/integration/`      |
| E2E (Playwright) | target mapped by `make.test_e2e`         | All flows pass (Mockoon-mocked API)   | `tests/e2e/`              |
| Visual           | target mapped by `make.test_visual`      | Zero unintended diffs                 | `tests/visual/`           |
| Mutation         | target mapped by `make.test_mutation`    | MSI ≥ `quality.mutation_msi`          | `src/components/**/*.tsx` |

Reference values from the canonical upstream profile:

```bash # profile-example
make test-unit-client    # make.test_unit_client → jsdom + Testing Library suite
make test-unit-server    # make.test_unit_server → Apollo mock (node env)
make test-integration    # make.test_integration → integration suite (global 100%)
make test-e2e            # make.test_e2e         → Playwright end-to-end flows
make test-visual         # make.test_visual      → visual regression snapshots
make test-mutation       # make.test_mutation    → Stryker mutation testing
```

Two Jest environments back the unit/integration tiers: client and
integration run under **jsdom**, the Apollo server tier runs under
**node**, selected by the runner's `TEST_ENV`. E2E and visual tiers run
through Playwright inside the test stack; the default `make.test_e2e` path
builds and runs production-parity (target mapped by `make.start_prod`),
while a dev-container fast path is available for a single-spec inner loop.

## Execution Workflow

### Step 1: Run Tests

Run the target mapped by `make.test_unit_client` for quick validation; add
the targets mapped by `make.test_unit_server`, `make.test_integration`,
`make.test_e2e`, and `make.test_visual` for a comprehensive check before
finishing.

### Step 2: Check Results

- **All pass + coverage and snapshots clean** → Complete
- **Failures detected** → Go to Step 3

### Step 3: Debug Failures

Re-run the smallest failing suite, read the first real failure before
editing, and confirm whether the cause is app logic, test data, mock
state, or snapshot drift. Then fix the cause, not the symptom:

| Failure Type          | Debug Source                       | Common Fixes                                        |
| --------------------- | ---------------------------------- | --------------------------------------------------- |
| Assertion failure     | Jest / Testing Library output      | Fix logic, update expectations to observed behavior |
| Coverage below target | Jest coverage report               | Add missing test cases for the uncovered branch     |
| Escaped mutants       | `make.test_mutation` target output | Test edge cases, strengthen assertion specificity   |
| E2E flow failure      | Playwright trace / report          | Fix app logic, mock state, or accessible locator    |
| Visual diff           | Playwright snapshot diff image     | Fix the regression, or accept only if intentional   |
| Type error            | tsc / stack trace                  | Fix type hints, mock return types                   |
| Mock drift            | Mockoon / Apollo mock setup        | Make the mock response explicit in test setup       |

### Step 4: Fix and Re-test

Fix the code/tests, then re-run the focused target to verify. Repeat Steps
2–4 until all tests pass with full coverage. When done, run the targets
mapped by `make.format` then `make.lint` — see the
[frontend-quality-workflow skill](../frontend-quality-workflow/SKILL.md).
Fixes surfaced during review or QA route back to the `react-implementer`
agent; never silence a check with a suppression directive.

## Mutation Testing (Stryker)

**Goal**: MSI ≥ `quality.mutation_msi` — the canonical default is read
from the project's Stryker config `break` threshold, zero escaped mutants
on the gated scope. This threshold is **raise-only (ADR-7)**: a profile
may tighten it above the default, never relax it. Never lower the
configured `break`/MSI to make a run pass — fix the tests instead.

Mutation runs are gated by `capabilities.mutation_testing`; when it is
`false` or `make.test_mutation` is `null`, record a capability-absent note
and skip. The mutated scope is the component layer
(`src/components/**/*.tsx`), driven by the client unit suite — stories,
`dist`, and coverage output are excluded.

### Run Mutation Tests

Run the target mapped by `make.test_mutation` for the full, gated suite
locally. In CI the suite is **sharded** across a matrix of
`make.test_mutation` shard runs, and a final merge job runs the target
mapped by `make.merge_mutation_reports` to combine the per-shard JSON
reports and **re-enforce the same `break` threshold** read from the
Stryker config — identical gate, faster wall-clock. When
`make.merge_mutation_reports` is `null`, the un-sharded `make.test_mutation`
run is the authoritative gate.

### Fix Escaped Mutants

1. Review the mutation diff in the output
2. Add a test case for the uncaught mutation
3. Strengthen assertion specificity
4. Consider refactoring the component for testability

**Example**: If a mutant changes `>` to `>=`, add a boundary test case.
Never silence a mutant with suppression annotations.

## Visual Regression

Visual tests are gated by `capabilities.visual_testing`; when it is
`false` or `make.test_visual` is `null`, record a capability-absent note
and skip. The bar is `quality.visual_diffs` (ceiling `0`) — zero
unintended pixel diffs.

Run the target mapped by `make.test_visual`. On a diff:

1. Open the diff image and decide whether the change is **intended**.
2. If unintended → it is a regression: fix the component/style.
3. If intended → regenerate the baseline using the snapshot-update variant
   next to the `make.test_visual` target (find it in the repository
   Makefile), but only **after** inspecting the diff. Never update
   snapshots blind to silence a failing run.

Snapshots are environment-sensitive — keep test data deterministic (seeded
Faker, see below) so baselines stay stable across runs. Visual and E2E
verdicts roll up into the `qa-visual-tester` agent's QA gate.

## Faker Builders in Tests

Tests generate arbitrary user/domain data (emails, names, passwords, ids,
tokens) with `@faker-js/faker` via shared builders under `tests/builders/`
(`buildUser`, `buildCredentials`, `buildEmail`, …), imported through the
`@tests/*` alias. Builders return domain-valid data by construction and
accept an `overrides` object.

```typescript
// Good — generated once, reused across input and assertion
const user = buildUser();
render(<Profile email={user.email} />);
expect(screen.getByText(user.email)).toBeInTheDocument();

// Bad — hardcoded literals that are not the test case
'test@example.com';
'John Doe';
```

Faker is **seeded deterministically** (`seedFaker()` in each runner's
setup; default `DEFAULT_FAKER_SEED`, override with `FAKER_SEED=<integer>`)
so the suite is reproducible and visual snapshots stay stable. Bind a
generated value to a `const` once and reuse it. Keep hardcoded literals
only when the value **is** the test case or a fixed contract
(invalid/edge-case inputs, golden text, config, URLs, error codes/messages,
i18n strings, mock sentinels).

## Load, Performance & Memory

These tiers live outside this skill and are each capability-gated:

- **Load (k6)** — gated by `capabilities.load_testing`; runs through the
  target mapped by `make.test_load`. See the
  [load-testing skill](../load-testing/SKILL.md). Skip with a
  capability-absent note when the capability is `false`.
- **Lighthouse / web-vitals / accessibility** — covered by the
  [frontend-performance-accessibility skill](../frontend-performance-accessibility/SKILL.md)
  (desktop/mobile budgets `quality.lighthouse_desktop` /
  `quality.lighthouse_mobile`, plus the
  [accessibility-audit skill](../accessibility-audit/SKILL.md)).
- **Memory leaks (memlab)** — gated by `capabilities.memory_leak_testing`;
  runs through the target mapped by `make.test_memory_leak`. Skip with a
  capability-absent note when the capability is `false`.

**Prerequisites** for the suites that hit a running app:

- Service containers running (target mapped by `make.start` for the dev
  fast path, or `make.start_prod` for the production-parity E2E/visual stack)
- Mockoon-mocked API responses available per the project's test stack

## Constraints (Parameters)

**NEVER**:

- Cancel long-running tests mid-execution
- Commit with failing tests
- Accept coverage below the enforced floors (`quality.coverage_statements`,
  `quality.coverage_branches`, `quality.coverage_functions`,
  `quality.coverage_lines` — all `100`)
- Allow escaped mutants or lower `quality.mutation_msi` / the Stryker `break`
- Accept an unintended visual diff or update snapshots without inspecting them
- Add `eslint-disable` / `@ts-ignore` / suppression annotations to dodge a check
- Add a `data-testid` so a test can find an element — refactor to a semantic query
- Run tests outside the profile's `make` target map (no bare `jest` /
  `playwright` / `stryker` on the host)

**ALWAYS**:

- Use seeded Faker builders for dynamic test data
- Mock network and service boundaries in unit tests; do not test mock internals
- Use accessible role/label/text locators (Testing Library and Playwright)
  before any `id` fallback — source ships no `data-testid`
- Keep Mockoon and Apollo-mock behavior explicit in test setup
- Add regression coverage for a bug fix before changing behavior
- Ensure deterministic test results

## Format (Output)

**Functional tests success**:

```text
PASS  tests (X suites, Y tests)
Coverage: 100% statements / branches / functions / lines
Visual: 0 unintended diffs
```

**Mutation testing success**:

```text
MSI >= quality.mutation_msi (default = Stryker `break`)
0 escaped mutants on src/components/**/*.tsx
```

## Verification Checklist

- [ ] All client/server/integration unit tests pass with full coverage
      (targets mapped by `make.test_unit_client`, `make.test_unit_server`,
      `make.test_integration`)
- [ ] E2E and visual suites pass with zero unintended diffs (targets mapped
      by `make.test_e2e`, `make.test_visual`)
- [ ] Coverage meets the enforced floors (statements/branches/functions/lines = 100)
- [ ] Zero escaped mutants, MSI ≥ `quality.mutation_msi` (when mutation testing runs)
- [ ] No hardcoded test values where seeded Faker builders apply
- [ ] No `data-testid` added; elements located by accessible queries
- [ ] Tests ran through the profile's `make` target map (containerized)
</content>
