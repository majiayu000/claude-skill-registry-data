---
name: testing-workflow
description: Run and manage functional tests (unit, integration, E2E, mutation) for a PHP backend service. Use when running tests, debugging test failures, ensuring test coverage, or fixing mutation testing issues. Covers PHPUnit, Behat-style E2E suites, and Infection. For load/performance tests, use the load-testing skill instead.
---

# Testing Workflow Skill

## Profile keys consumed

- `make.tests`
- `make.e2e`
- `make.infection`
- `make.start`
- `make.load_tests`
- `quality.infection_msi`
- `capabilities.load_testing`

All test invocations go through the profile's `make` target map. A `null`
value for a `make.*` key means the capability is absent: skip that suite
with an explicit capability-absent note instead of failing or improvising
a raw command.

## Context (Input)

- Code changes require test validation
- Test failures need debugging
- Coverage/mutation targets must be met

## Task (Function)

Execute the appropriate test suite and ensure a 100% pass rate with the
required coverage and mutation score.

**Note**: For load/performance testing, see the
[load-testing skill](../load-testing/SKILL.md) (gated by
`capabilities.load_testing`).

## Test Commands Quick Reference

| Test Type        | Invocation                        | Goal                          | Typical location                    |
| ---------------- | --------------------------------- | ----------------------------- | ----------------------------------- |
| Unit/Integration | target mapped by `make.tests`     | All pass, full line coverage  | `tests/Unit/`, `tests/Integration/` |
| E2E (BDD)        | target mapped by `make.e2e`       | All scenarios pass            | `features/`                         |
| Mutation         | target mapped by `make.infection` | MSI ≥ `quality.infection_msi` | Driven by unit tests                |

Reference values from the canonical upstream profile:

```bash # profile-example
make tests          # make.tests  → unit + integration suites
make e2e-tests      # make.e2e    → Behat end-to-end scenarios
make infection      # make.infection → mutation testing
```

## Execution Workflow

### Step 1: Run Tests

Run the target mapped by `make.tests` for quick validation; add the
target mapped by `make.e2e` for a comprehensive check before finishing.

### Step 2: Check Results

- **All pass + coverage target met** → Complete
- **Failures detected** → Go to Step 3

### Step 3: Debug Failures

Identify failure type and apply fix:

| Failure Type          | Debug Source                   | Common Fixes                               |
| --------------------- | ------------------------------ | ------------------------------------------ |
| Assertion failure     | PHPUnit output                 | Fix logic, update test expectations        |
| Coverage below target | Coverage report                | Add missing test cases                     |
| Escaped mutants       | `make.infection` target output | Test edge cases, strengthen assertions     |
| E2E scenario          | Feature/scenario output        | Fix application logic or step definitions  |
| Type error            | Stack trace                    | Fix type hints, mock returns               |

### Step 4: Fix and Re-test

Fix the code/tests, then re-run the target mapped by `make.tests` to
verify. Repeat Steps 2–4 until all tests pass with full coverage.

## Mutation Testing (Infection)

**Goal**: MSI ≥ `quality.infection_msi` — canonical default `100`, zero
escaped mutants. This threshold is raise-only (ADR-7): a profile may
tighten it above the default, never relax it. Never lower the configured
MSI to make a run pass — fix the tests instead.

### Run Mutation Tests

Run the target mapped by `make.infection` (skip with a capability-absent
note when `null`).

### Fix Escaped Mutants

1. Review the mutation diff in the output
2. Add a test case for the uncaught mutation
3. Strengthen assertion specificity
4. Consider refactoring for testability

**Example**: If a mutant changes `>` to `>=`, add a boundary test case.
Never silence a mutant with suppression annotations.

## Faker Usage in Tests

**Setup**: Unit tests extend the project's base test case, which exposes
`$this->faker`.

```php
// Good - Dynamic test data
$this->faker->email();
$this->faker->lexify('??');     // 2 random letters
$this->faker->unique()->word();

// Bad - Hardcoded values
'test@example.com'
'AB'
```

All standard Faker methods are available; projects may register custom
providers for domain identifier formats (ULID/UUID etc.) — prefer those
over hand-rolled strings.

## Load Testing

Load tests run through the target mapped by `make.load_tests`, only when
`capabilities.load_testing` is true — see the
[load-testing skill](../load-testing/SKILL.md) for scenarios and
configuration.

**Prerequisites**:

- Service containers running (target mapped by `make.start`)
- Test database seeded per project setup docs

## Constraints (Parameters)

**NEVER**:

- Cancel long-running tests mid-execution
- Commit with failing tests
- Accept coverage below the project's enforced bar
- Allow escaped mutants or lower `quality.infection_msi`
- Add suppression/ignore annotations to dodge a failing check
- Run tests outside the containerized `make` target map (no bare
  `phpunit`/`behat` on the host)

**ALWAYS**:

- Use Faker for dynamic test data
- Mock external dependencies in unit tests
- Use a real database in integration tests
- Ensure deterministic test results

## Format (Output)

**Functional tests success**:

```text
OK (X tests, Y assertions)
Line coverage at the enforced target
```

**Mutation testing success**:

```text
MSI >= quality.infection_msi (default 100)
0 escaped mutants
```

## Verification Checklist

- [ ] All tests pass (targets mapped by `make.tests` and `make.e2e`)
- [ ] Coverage meets the enforced target
- [ ] Zero escaped mutants, MSI ≥ `quality.infection_msi` (if running mutation tests)
- [ ] No hardcoded test values (use Faker)
- [ ] Tests ran through the profile's `make` target map (containerized)
