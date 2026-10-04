---
name: ci-workflow
description: Run the full local frontend CI suite through the profile's make target map and drive every check to green before committing. Use when the user asks to run CI, run quality checks, validate frontend code quality, or before finishing any task that touches React/TypeScript/MUI code.
---

# CI Workflow Skill

## Profile keys consumed

- `make.ci`, `make.format`, `make.lint`, `make.lint_eslint`, `make.lint_tsc`, `make.lint_md`, `make.lint_dup`, `make.lint_metrics`, `make.lint_deps`
- `make.test_unit_client`, `make.test_unit_server`, `make.test_integration`, `make.test_e2e`, `make.test_visual`, `make.test_mutation`, `make.merge_mutation_reports`, `make.lighthouse_desktop`, `make.lighthouse_mobile`
- `quality.coverage_statements`, `quality.coverage_branches`, `quality.coverage_functions`, `quality.coverage_lines`, `quality.mutation_msi`, `quality.jscpd_clones`, `quality.eslint_errors`, `quality.eslint_warnings`, `quality.tsc_errors`, `quality.markdownlint_errors`, `quality.depcruise_violations`, `quality.metrics_enforced`, `quality.visual_diffs`, `quality.lighthouse_desktop`, `quality.lighthouse_mobile`
- `capabilities.visual_testing`, `capabilities.mutation_testing`, `capabilities.lighthouse`

## Context (Input)

- Code changes exist in the working directory
- Ready to validate code quality before commit/PR
- Profile loaded from `.claude/react-sdlc.yml` (run `/fe-sdlc-setup` if missing)

When run under `/fe-sdlc-finish-pr`, the `ci-fixer` agent drives this loop to green; invoked
directly, follow the same steps yourself.

## Task (Function)

Execute the target mapped by `make.ci` and ensure ALL quality checks pass.

**Success Criteria**: the `make.ci` target exits `0`. Some repositories also print a success banner — treat exit status as the contract, the banner as confirmation:

```bash # profile-example
make ci
# ...
# ✅ CI checks successfully passed!
```

**Degrade rule (capability absent)**: if `make.ci` is `null` in the profile, run the individually mapped targets instead, in order — `make.format` first (mutating), then `make.lint_eslint`, `make.lint_tsc`, `make.lint_md`, `make.lint_dup`, `make.lint_metrics`, `make.lint_deps`, `make.test_unit_client`, `make.test_unit_server`, `make.test_integration`, `make.test_e2e`, `make.test_visual`, `make.test_mutation`, `make.merge_mutation_reports`, `make.lighthouse_desktop`, `make.lighthouse_mobile` — skipping any `null` entries with an explicit capability-absent note. The capability-paired lanes only run when their capability is enabled, otherwise note the skip:

- `SKIPPED: make.test_visual` when `capabilities.visual_testing` is false (or `make.test_visual` is `null`).
- `SKIPPED: make.test_mutation` + `make.merge_mutation_reports` when `capabilities.mutation_testing` is false.
- `SKIPPED: make.lighthouse_desktop` / `make.lighthouse_mobile` when `capabilities.lighthouse` is false.

## Parallel Execution

Full-CI targets group their work into a mutating preflight followed by parallel read-only checks; no external tools beyond the repository's CI runner are required. Checks run in stages:

1. **Preflight (sequential, mutating)**: the formatter (Prettier + qlty) that rewrites files runs first, alone, before any verification — never in parallel with a read-only gate.
2. **Parallel stage (read-only)**: ESLint, TypeScript, markdownlint, jscpd, rust-code-analysis metrics, and dependency-cruiser, then the unit/integration/E2E/visual/Lighthouse lanes.

Reference layout of the parallel groups:

```text # profile-example
Format (preflight) | prettier, qlty fmt                                              | sequential, mutating — runs first
Lint               | eslint, tsc, markdownlint, jscpd, rca-metrics, dependency-cruiser | fully parallel, read-only
Unit + Integration | client (jsdom), server (node), integration (100% over source)  | parallel after dev env ready
Mutation           | stryker (sharded matrix) + merge-and-enforce gate              | heavy, isolated, not parallelized
Prod-side          | e2e, visual, lighthouse-desktop, lighthouse-mobile             | prod build + Chromium first
```

**AI-friendly output**: grouped per-target output (the CI runner emits each target's log together after completion) prevents interleaved lines from parallel tasks — read failures per group, not line by line.

## Execution Steps

### Step 1: Run CI

Run the target mapped by `make.ci` (always through `make` — the targets wrap the containerized toolchain and the bun-managed dependencies; never invoke ESLint, `tsc`, Jest, Playwright, Stryker, or Lighthouse directly on the host).

### Step 2: Check Result

- **Success** (exit `0`): task complete
- **Failure**: identify the failing check from the grouped output → Step 3

### Step 3: Fix Failures

Identify the failing check and apply the fix at the root cause:

| Check                | Re-run via                                           | Fix                                              | Companion Skill                                                                      |
| -------------------- | ---------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------ |
| Formatting           | `make.format` target                                 | Re-run the formatter, inspect changed files      | -                                                                                    |
| ESLint               | `make.lint_eslint` target                            | Fix the reported rule (never `eslint-disable`)   | [code-organization](../code-organization/SKILL.md)                                   |
| TypeScript           | `make.lint_tsc` target                               | Fix the type contract (no `@ts-ignore`)          | -                                                                                    |
| Markdown             | `make.lint_md` target                                | Keep headings, fences, and lines compliant       | -                                                                                    |
| Duplication (jscpd)  | `make.lint_dup` target                               | Deduplicate; extract shared style/const/factory  | [complexity-management](../complexity-management/SKILL.md)                           |
| Metrics (rca)        | `make.lint_metrics` target                           | Split dense functions/files, lower complexity    | [complexity-management](../complexity-management/SKILL.md)                           |
| Dependencies         | `make.lint_deps` target                              | Fix layer/import-boundary violations             | [architecture](../architecture/SKILL.md)                                             |
| Unit (client/server) | `make.test_unit_client` / `make.test_unit_server`    | Debug failing suites, close coverage gaps        | [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md)                   |
| Integration          | `make.test_integration` target                       | Restore 100% coverage over the source root       | [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md)                   |
| E2E                  | `make.test_e2e` target                               | Debug failing user flows                         | [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md)                   |
| Visual               | `make.test_visual` target                            | Inspect the diff; fix the UI or refresh baseline | [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md)                   |
| Mutation             | `make.test_mutation` / `make.merge_mutation_reports` | Add the missing test cases                       | [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md)                   |
| Lighthouse           | `make.lighthouse_desktop` / `make.lighthouse_mobile` | Fix perf/a11y regressions                        | [frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md) |

**Refactoring during fixes**: if CI failures reveal structural issues (wrong directory, vague names, a component or hook in the wrong module, hardcoded config), consult [code-organization](../code-organization/SKILL.md) before applying fixes. Accessibility regressions surfaced by the a11y lane route to [accessibility-audit](../accessibility-audit/SKILL.md).

### Step 4: Re-run

Re-run the `make.ci` target. Repeat Steps 2-4 until it exits `0`, bounded at
**max 5 iterations** (the same cap the `ci-fixer` agent enforces). On
exhaustion, stop and escalate: report the still-failing checks, the fixes
attempted, and the recommended next step instead of looping further.

## Alternative Commands

Only the full suite is profile-mapped (`make.ci`). Repositories often also provide a mutating preflight and the individual phase targets — check the Makefile before assuming they exist:

```bash # profile-example
make ci             # full local CI flow (setup, lint, dev tests, mutation, prod tests)
make format         # mutating preflight only (Prettier + qlty)
make lint           # read-only aggregate lint gate
```

## Constraints (Parameters)

**Thresholds come from `quality.*` in the profile — NEVER decrease them.** Shipped defaults are the minimum bar; a profile may only raise the floors and may never raise the fixed-`0` ceilings (raise-only rule):

| Profile key                                                                                                           | Shipped default              | Direction               |
| --------------------------------------------------------------------------------------------------------------------- | ---------------------------- | ----------------------- |
| `quality.coverage_statements` / `quality.coverage_branches` / `quality.coverage_functions` / `quality.coverage_lines` | 100                          | floor (raise-only)      |
| `quality.mutation_msi`                                                                                                | `stryker.config.mjs` `break` | floor (raise-only)      |
| `quality.lighthouse_desktop`                                                                                          | 95                           | floor (raise-only)      |
| `quality.lighthouse_mobile`                                                                                           | 85                           | floor (raise-only)      |
| `quality.jscpd_clones`                                                                                                | 0                            | ceiling (fixed)         |
| `quality.eslint_errors` / `quality.eslint_warnings`                                                                   | 0                            | ceiling (fixed)         |
| `quality.tsc_errors`                                                                                                  | 0                            | ceiling (fixed)         |
| `quality.markdownlint_errors`                                                                                         | 0                            | ceiling (fixed)         |
| `quality.depcruise_violations`                                                                                        | 0                            | ceiling (fixed)         |
| `quality.visual_diffs`                                                                                                | 0                            | ceiling (fixed)         |
| `quality.metrics_enforced`                                                                                            | true                         | bool (must stay `true`) |

**DO NOT**:

- Lower quality thresholds or relax test-coverage configuration (`jest.config.ts`, `stryker.config.mjs`, `.jscpd.json`, `config/metrics-policy.json`, `lighthouse/lighthouserc.*.js`)
- Skip failing checks
- Commit while the `make.ci` target fails
- Run quality tools outside the mapped `make` targets (they wrap the containerized toolchain and the bun-managed dependencies)
- Add suppression/ignore annotations to silence ESLint, TypeScript, jscpd, rust-code-analysis, Stryker, or dependency-cruiser failures (`eslint-disable`, `@ts-ignore`, `@ts-nocheck`, jscpd/depcruise ignore directives, Stryker disable comments) — fix the code instead
- Edit the dependency-cruiser config, `.jscpd.json`, or the metrics policy to make violations disappear

## Format (Output)

**Required final state**: the `make.ci` target (or, under the degrade rule, every non-`null` mapped target, skipping capability-absent lanes with a note) exits `0`.

## Verification Checklist

- [ ] `make.ci` target executed (mutating `make.format` ran before any read-only gate)
- [ ] All checks passed (format, ESLint, TypeScript, markdown, jscpd, metrics, dependency-cruiser, unit, integration, E2E, visual, mutation, Lighthouse)
- [ ] Exit status `0` (success banner shown where the repo prints one)
- [ ] Zero test failures; coverage at the `quality.coverage_*` floors over the source root
- [ ] Zero escaped mutants above the gate (`quality.mutation_msi` floor met)
- [ ] No quality threshold decreased, no suppression added

## Rollback

If the parallel grouping causes issues (interleaved failures, resource contention):

1. Run the mutating preflight on its own first (`make.format`), then the read-only `make.lint` aggregate.
2. Otherwise run the mapped targets individually in the degrade order: `make.format`, `make.lint_eslint`, `make.lint_tsc`, `make.lint_md`, `make.lint_dup`, `make.lint_metrics`, `make.lint_deps`, `make.test_unit_client`, `make.test_unit_server`, `make.test_integration`, `make.test_e2e`, `make.test_visual`, `make.test_mutation`, `make.merge_mutation_reports`, `make.lighthouse_desktop`, `make.lighthouse_mobile` — skipping capability-absent lanes with a note.

## Related Skills

- [code-organization](../code-organization/SKILL.md) - Consult when CI failures reveal structural/naming issues, misplaced components/hooks, or hardcoded config
- [complexity-management](../complexity-management/SKILL.md) - Reduce complexity and resolve duplication when jscpd or rust-code-analysis fails
- [architecture](../architecture/SKILL.md) - Fix dependency-cruiser layer/import-boundary violations
- [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md) - Debug specific Jest/Playwright/visual/mutation failures
- [frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md) - Recover Lighthouse desktop/mobile floors
- [accessibility-audit](../accessibility-audit/SKILL.md) - Address accessibility findings the a11y lane raises
- [quality-standards](../quality-standards/SKILL.md) - Overview of all protected thresholds
