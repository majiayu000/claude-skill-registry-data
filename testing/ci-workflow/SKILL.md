---
name: ci-workflow
description: Run the full local CI suite through the profile's make target map and drive every check to green before committing. Use when the user asks to run CI, run quality checks, validate code quality, or before finishing any task that involves code changes.
---

# CI Workflow Skill

## Profile keys consumed

- `make.ci`, `make.tests`, `make.e2e`, `make.psalm`, `make.deptrac`, `make.phpinsights`, `make.infection`
- `quality.phpinsights.quality`, `quality.phpinsights.architecture`, `quality.phpinsights.style`, `quality.phpinsights.complexity`
- `quality.deptrac_violations`, `quality.psalm_errors`, `quality.infection_msi`

## Context (Input)

- Code changes exist in the working directory
- Ready to validate code quality before commit/PR
- Profile loaded from `.claude/php-sdlc.yml` (run `/sdlc-setup` if missing)

## Task (Function)

Execute the target mapped by `make.ci` and ensure ALL quality checks pass.

**Success Criteria**: the `make.ci` target exits `0`. Many repositories also print a success banner — treat exit status as the contract, the banner as confirmation:

```bash # profile-example
make ci
# ...
# ✅ CI checks successfully passed!
```

**Degrade rule (capability absent)**: if `make.ci` is `null` in the profile, run the individually mapped targets instead, in order — `make.psalm`, `make.deptrac`, `make.phpinsights`, `make.tests`, `make.e2e`, `make.infection` — skipping any `null` entries with an explicit capability-absent note.

## Parallel Execution

Full-CI targets typically use GNU Make's built-in parallelism (`make -j4 --output-sync=target`); no external tools beyond GNU Make. Checks run in two stages:

1. **Preflight (sequential, mutating)**: auto-fixers and quality scoring that rewrite files must run first, one at a time
2. **Parallel stage (read-only)**: static analysis, architecture check, tests + API-contract checks, mutation testing

Reference layout of the parallel groups:

```text # profile-example
Static Analysis | composer-validate, check-requirements, check-security, psalm, psalm-security | fully parallel
Architecture    | deptrac                                                                      | none
Tests + OpenAPI | unit-tests, integration-tests, behat, openapi-diff, spectral, schemathesis  | setup-test-db first
Mutation        | infection                                                                    | none
```

**AI-friendly output**: `--output-sync=target` groups each target's output together after completion, preventing interleaved output from parallel tasks — read failures per group, not line by line.

## Execution Steps

### Step 1: Run CI

Run the target mapped by `make.ci` (always through `make` — the targets wrap the containerized toolchain; never invoke the underlying tools directly on the host).

### Step 2: Check Result

- **Success** (exit `0`): task complete
- **Failure**: identify the failing check from the grouped output → Step 3

### Step 3: Fix Failures

Identify the failing check and apply the fix at the root cause:

| Check           | Re-run via                | Fix                                 | Companion Skill                                            |
| --------------- | ------------------------- | ----------------------------------- | ---------------------------------------------------------- |
| Code style      | repo's style auto-fixer   | Apply auto-fixes, re-score style    | -                                                          |
| Static analysis | `make.psalm` target       | Fix type errors                     | -                                                          |
| Quality metrics | `make.phpinsights` target | Reduce complexity, fix architecture | [complexity-management](../complexity-management/SKILL.md) |
| Architecture    | `make.deptrac` target     | Fix layer boundary violations       | [deptrac-fixer](../deptrac-fixer/SKILL.md)                 |
| Organization    | `make.psalm` target       | Fix naming, directory placement     | [code-organization](../code-organization/SKILL.md)         |
| Tests           | `make.tests` target       | Debug failing tests                 | [testing-workflow](../testing-workflow/SKILL.md)           |
| E2E             | `make.e2e` target         | Debug failing scenarios             | [testing-workflow](../testing-workflow/SKILL.md)           |
| Mutations       | `make.infection` target   | Add missing test cases              | [testing-workflow](../testing-workflow/SKILL.md)           |

**Refactoring during fixes**: if CI failures reveal structural issues (wrong directory, vague names, hardcoded config), consult [code-organization](../code-organization/SKILL.md) before applying fixes.

### Step 4: Re-run

Re-run the `make.ci` target. Repeat Steps 2-4 until it exits `0`.

## Alternative Commands

Only the full suite is profile-mapped (`make.ci`). Repositories often also provide sequential and preflight-only variants — check the Makefile before assuming they exist:

```bash # profile-example
make ci             # parallel CI (default, faster)
make ci-sequential  # sequential CI (fallback)
make ci-preflight   # mutating preflight checks only
```

## Constraints (Parameters)

**Thresholds come from `quality.*` in the profile — NEVER decrease them.** Shipped defaults are the minimum bar; a profile may only raise the floors, never lower them (raise-only rule):

| Profile key                         | Shipped default | Direction          |
| ----------------------------------- | --------------- | ------------------ |
| `quality.phpinsights.quality`       | 100             | floor (raise-only) |
| `quality.phpinsights.architecture`  | 100             | floor (raise-only) |
| `quality.phpinsights.style`         | 100             | floor (raise-only) |
| `quality.phpinsights.complexity`    | 94              | floor (raise-only) |
| `quality.infection_msi`             | 100             | floor (raise-only) |
| `quality.deptrac_violations`        | 0               | ceiling (fixed)    |
| `quality.psalm_errors`              | 0               | ceiling (fixed)    |

**DO NOT**:

- Lower quality thresholds or relax test-coverage configuration
- Skip failing checks
- Commit while the `make.ci` target fails
- Run quality tools outside the mapped `make` targets (they wrap the containerized toolchain)
- Add suppression/ignore annotations to silence PHPMD/PHPInsights/Infection/Psalm/PHPStan/PHPCS failures — fix the code instead
- Edit `deptrac.yaml` to make violations disappear

## Format (Output)

**Required final state**: the `make.ci` target (or, under the degrade rule, every non-`null` mapped target) exits `0`.

## Verification Checklist

- [ ] `make.ci` target executed
- [ ] All checks passed (composer validation, security, style, static analysis, architecture, tests, mutations)
- [ ] Exit status `0` (success banner shown where the repo prints one)
- [ ] Zero test failures
- [ ] Zero escaped mutants (`quality.infection_msi` floor met)
- [ ] No quality threshold decreased, no suppression added

## Rollback

If parallel execution causes issues (interleaved failures, resource contention):

1. Use the repository's sequential CI variant if one exists
2. Otherwise run the mapped targets individually: `make.psalm`, `make.deptrac`, `make.phpinsights`, `make.tests`, `make.e2e`, `make.infection`

## Related Skills

- [code-organization](../code-organization/SKILL.md) - Consult when CI failures reveal structural/naming issues or hardcoded configs
- [complexity-management](../complexity-management/SKILL.md) - Reduce cyclomatic complexity when PHPInsights fails
- [deptrac-fixer](../deptrac-fixer/SKILL.md) - Fix architectural boundary violations
- [testing-workflow](../testing-workflow/SKILL.md) - Debug specific test failures or mutation issues
- [quality-standards](../quality-standards/SKILL.md) - Overview of all protected thresholds
