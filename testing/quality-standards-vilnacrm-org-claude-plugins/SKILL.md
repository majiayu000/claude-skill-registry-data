---
name: quality-standards
description: Overview of the protected frontend quality thresholds and a quick-reference router that maps every failing quality check — ESLint, TypeScript, markdownlint, jscpd, rust-code-analysis metrics, dependency-cruiser, Jest/Playwright coverage and visual tests, Stryker mutation, Lighthouse, and accessibility — to its make target and specialized fixing skill. Use when you need to understand quality metrics, run comprehensive quality checks, or learn which specialized skill to use. For specific issues, use dedicated skills (complexity-management for rust-code-analysis or jscpd, architecture for dependency-cruiser, frontend-testing-workflow for coverage and mutation, frontend-performance-accessibility for Lighthouse, accessibility-audit for a11y).
---

# Quality Standards Skill

## Profile keys consumed

- `make.ci`, `make.format`, `make.lint`, `make.lint_eslint`, `make.lint_tsc`, `make.lint_md`, `make.lint_dup`, `make.lint_metrics`, `make.lint_deps`, `make.a11y`
- `make.test_unit_client`, `make.test_unit_server`, `make.test_integration`, `make.test_e2e`, `make.test_visual`, `make.test_mutation`, `make.merge_mutation_reports`, `make.lighthouse_desktop`, `make.lighthouse_mobile`
- `quality.coverage_statements`, `quality.coverage_branches`, `quality.coverage_functions`, `quality.coverage_lines`, `quality.mutation_msi`, `quality.jscpd_clones`, `quality.eslint_errors`, `quality.eslint_warnings`, `quality.tsc_errors`, `quality.markdownlint_errors`, `quality.depcruise_violations`, `quality.metrics_enforced`, `quality.visual_diffs`, `quality.lighthouse_desktop`, `quality.lighthouse_mobile`
- `capabilities.visual_testing`, `capabilities.mutation_testing`, `capabilities.lighthouse`, `capabilities.accessibility_audit`, `capabilities.dynamic_a11y_testing`
- `architecture.source_root`

Command convention: `make <make.X>` means "run `make` with the target the
profile maps for key `make.X`". A `null` mapping means the capability is
absent in this repository — skip that check with a capability-absent note
instead of failing. Generic tooling (`bun`, `git`, `gh`) is invoked
directly. Never run ESLint, `tsc`, markdownlint, jscpd, rust-code-analysis,
dependency-cruiser, Jest, Playwright, Stryker, or Lighthouse bare on the
host: every quality tool runs through its mapped `make` target, which wraps
the containerized toolchain and the bun-managed dependencies. When `make.a11y`
is `null`, the accessibility lane runs through the plugin's bundled a11y check
(see [accessibility-audit](../accessibility-audit/SKILL.md)) — or is skipped
with a capability-absent note when `capabilities.accessibility_audit` is false.

## Context (Input)

- Need to understand the protected quality thresholds
- Running comprehensive quality checks before commit
- Determining which specialized skill to use for a specific issue
- Quick reference for quality tool commands

When run under `/fe-sdlc-finish-pr`, the `ci-fixer` agent drives the CI loop
to green; invoked directly, follow the same steps yourself.

## Task (Function)

Understand the frontend quality metrics and route to the appropriate
specialized skill for fixes.

**Success Criteria**: Know which skill to use for your specific quality issue.

## Protected Quality Thresholds

**CRITICAL — raise-only rule**: the `quality.*` values in the project
profile are floors/ceilings over the shipped defaults. A profile may tighten
the bar (raise score floors), never relax it. Violation-count ceilings ship at
`0` and may not be raised. NEVER lower any threshold in the profile or in the
tool config files (`jest.config.ts`, `stryker.config.mjs`, `.jscpd.json`,
`config/metrics-policy.json`, `lighthouse/lighthouserc.*.js`, `eslint.config.mjs`,
the dependency-cruiser config).

### Lint, types & metrics (source code)

| Gate                         | Profile key                    | Shipped bound           | Fix With                                                                                                                |
| ---------------------------- | ------------------------------ | ----------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| ESLint errors                | `quality.eslint_errors`        | `0` (ceiling, fixed)    | [code-organization](../code-organization/SKILL.md) / [frontend-quality-workflow](../frontend-quality-workflow/SKILL.md) |
| ESLint warnings              | `quality.eslint_warnings`      | `0` (ceiling, fixed)    | [frontend-quality-workflow](../frontend-quality-workflow/SKILL.md)                                                      |
| TypeScript errors            | `quality.tsc_errors`           | `0` (ceiling, fixed)    | [frontend-quality-workflow](../frontend-quality-workflow/SKILL.md)                                                      |
| Markdown errors              | `quality.markdownlint_errors`  | `0` (ceiling, fixed)    | [frontend-quality-workflow](../frontend-quality-workflow/SKILL.md)                                                      |
| Duplication (jscpd)          | `quality.jscpd_clones`         | `0` (ceiling, fixed)    | [complexity-management](../complexity-management/SKILL.md)                                                              |
| Metrics (rust-code-analysis) | `quality.metrics_enforced`     | `true` (hard-fail gate) | [complexity-management](../complexity-management/SKILL.md)                                                              |
| Dependency boundaries        | `quality.depcruise_violations` | `0` (ceiling, fixed)    | [architecture](../architecture/SKILL.md)                                                                                |

The ESLint gate enforces the project's `no-restricted-syntax` conventions —
classes-with-instance-methods (no `static`, no free functions) outside React
components, type-only files, and no `data-testid` in `src/**`. The metrics gate
hard-fails on the rust-code-analysis bands in `config/metrics-policy.json`
(cyclomatic > 10, cognitive > 15, ABC magnitude > 17, function/closure args
> 3, exit points > 3, function/file LLOC/PLOC/SLOC and Halstead ceilings, MI
< 20, class WMC/NPM/NPA/COA/CDA limits); those values are repository policy,
not profile keys — the raise-only rule applies to them identically: tighten if
needed, never loosen.

### Tests, mutation & performance

| Tool               | Metric                              | Profile key / bound                                                                                                                                                          | Fix With                                                                             |
| ------------------ | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Jest coverage      | statements/branches/functions/lines | `quality.coverage_statements` / `quality.coverage_branches` / `quality.coverage_functions` / `quality.coverage_lines` (floor, shipped `100` over `architecture.source_root`) | [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md)                   |
| Stryker            | MSI                                 | `quality.mutation_msi` (floor, default = `stryker.config.mjs` `break`, raise-only)                                                                                           | [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md)                   |
| Playwright visual  | Snapshot diffs                      | `quality.visual_diffs` (ceiling, fixed `0`)                                                                                                                                  | [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md)                   |
| Lighthouse desktop | Performance score                   | `quality.lighthouse_desktop` (floor, shipped `95`)                                                                                                                           | [frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md) |
| Lighthouse mobile  | Performance score                   | `quality.lighthouse_mobile` (floor, shipped `85`)                                                                                                                            | [frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md) |
| Accessibility      | a11y findings                       | `0` via `make.a11y` (gated by `capabilities.accessibility_audit` / `capabilities.dynamic_a11y_testing`)                                                                      | [accessibility-audit](../accessibility-audit/SKILL.md)                               |

Jest runs two separate environments (client `jsdom`, server `node`) plus an
integration project that enforces full coverage over the source root; Stryker
mutation is **sharded** across a matrix and re-enforced by the merge gate
(`make.test_mutation` + `make.merge_mutation_reports`). MSI is measured only
over mutated lines, so it is a separate, stronger signal that does NOT by
itself guarantee full line coverage — the `quality.coverage_*` floors are an
independent bar.

## Quick Reference Commands

### Comprehensive checks

```bash
# Run the full local CI suite (recommended before commit)
make <make.ci>
```

**Success**: the target exits `0` and every reported score sits at or
above its `quality.*` floor (and every violation count at `0`). Some
repositories also print a success banner — treat exit status as the contract,
the banner as confirmation.

**Degrade rule (capability absent)**: if `make.ci` is `null`, run the
individually mapped targets in order — `make.format` first (mutating), then
`make.lint_eslint`, `make.lint_tsc`, `make.lint_md`, `make.lint_dup`,
`make.lint_metrics`, `make.lint_deps`, the unit/integration/E2E lanes, then the
capability-gated lanes — skipping any `null` entry with an explicit
capability-absent note:

- `SKIPPED: make.test_visual` when `capabilities.visual_testing` is false (or `make.test_visual` is `null`).
- `SKIPPED: make.test_mutation` + `make.merge_mutation_reports` when `capabilities.mutation_testing` is false.
- `SKIPPED: make.lighthouse_desktop` / `make.lighthouse_mobile` when `capabilities.lighthouse` is false.
- `SKIPPED: make.a11y` when `capabilities.accessibility_audit` is false.

### Individual quality checks

| Check               | Command                    | Purpose                                              |
| ------------------- | -------------------------- | ---------------------------------------------------- |
| Format (preflight)  | `make <make.format>`       | Prettier + qlty fmt (mutating; runs first, alone)    |
| Aggregate lint      | `make <make.lint>`         | Read-only lint aggregate                             |
| ESLint              | `make <make.lint_eslint>`  | Lint rules incl. `no-restricted-syntax` gates        |
| TypeScript          | `make <make.lint_tsc>`     | Type checking and errors                             |
| Markdown            | `make <make.lint_md>`      | Markdown lint                                        |
| Duplication (jscpd) | `make <make.lint_dup>`     | Copy/paste DRY gate                                  |
| Metrics (rca)       | `make <make.lint_metrics>` | rust-code-analysis complexity gate                   |
| Dependencies        | `make <make.lint_deps>`    | dependency-cruiser layer/import boundaries           |
| Accessibility       | `make <make.a11y>`         | a11y audit (bundled lane when `make.a11y` is `null`) |

### Testing commands

| Check         | Command                                                            | Purpose                                           |
| ------------- | ------------------------------------------------------------------ | ------------------------------------------------- |
| Unit (client) | `make <make.test_unit_client>`                                     | Component/hook tests (jsdom)                      |
| Unit (server) | `make <make.test_unit_server>`                                     | Apollo mock/server tests (node)                   |
| Integration   | `make <make.test_integration>`                                     | Component interactions, 100% over the source root |
| E2E           | `make <make.test_e2e>`                                             | Full user flows (Playwright + Mockoon mocks)      |
| Visual        | `make <make.test_visual>`                                          | Visual regression snapshots                       |
| Mutation      | `make <make.test_mutation>` / `make <make.merge_mutation_reports>` | Test-quality validation (sharded + merge gate)    |
| Lighthouse    | `make <make.lighthouse_desktop>` / `make <make.lighthouse_mobile>` | Perf/a11y budget (desktop + mobile)               |

## Routing to Specialized Skills

When quality checks fail, use the appropriate specialized skill:

### Architecture issues

- **dependency-cruiser violations** → [architecture](../architecture/SKILL.md)
  - "must not depend on" / layer or import-boundary errors
  - A type-only file importing a runtime module
- **Module placement (bulletproof-react)** → [architecture](../architecture/SKILL.md) / [code-organization](../code-organization/SKILL.md)
  - A component, hook, store, repository, or service in the wrong module/directory
  - Cross-feature reach via deep relative paths instead of a path alias (`@/`, `@auth/`)

### Code quality issues

- **High complexity** → [complexity-management](../complexity-management/SKILL.md)
  - rust-code-analysis hard-fail (cyclomatic, cognitive, ABC, exit points, LLOC/PLOC/SLOC, Halstead, MI)
  - Dense functions/files, class metrics out of band
- **Duplication** → [complexity-management](../complexity-management/SKILL.md)
  - jscpd reports a clone at or above `minTokens`/`minLines` — deduplicate (extract a shared style/const/factory), never suppress
- **Structural/naming/convention issues** → [code-organization](../code-organization/SKILL.md)
  - `static` member or free function outside a React component (use an instance method on an injectable class)
  - Type declared in a logic file, or runtime in a type-only file
  - `data-testid` in `src/**` (use a semantic query — `getByRole`/`getByLabelText`/`getByText`)
  - Vague names, hardcoded config that belongs in `.env`/the DI config
- **Code style / formatting** → [frontend-quality-workflow](../frontend-quality-workflow/SKILL.md)
  - Prettier/qlty formatting, ESLint rule, TypeScript, or markdownlint failures
  - Run the `make.format` target first, then re-run the read-only gate

### Testing issues

- **Test failures, coverage gaps, escaped mutants, visual diffs** → [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md)
  - Jest client/server/integration failures or coverage below the `quality.coverage_*` floors
  - Playwright E2E failures or visual snapshot diffs above `quality.visual_diffs`
  - Stryker mutants below `quality.mutation_msi`
  - General testing strategy → [testing-workflow](../testing-workflow/SKILL.md)

### Performance & accessibility issues

- **Lighthouse below floor** → [frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md)
  - Desktop below `quality.lighthouse_desktop` or mobile below `quality.lighthouse_mobile`
  - Bundle/runtime-performance regressions on the paint path
- **Accessibility findings** → [accessibility-audit](../accessibility-audit/SKILL.md)
  - Failures from the `make.a11y` lane; a11y is non-negotiable, fixes route to [frontend-component-development](../frontend-component-development/SKILL.md)
  - Design-fidelity questions on a Figma-backed component → [figma-design-check](../figma-design-check/SKILL.md) (gated by `capabilities.figma`)

### Workflow integration

- **Before committing** → [ci-workflow](../ci-workflow/SKILL.md)
  - Run all checks systematically through `make.ci`, fix failures in priority order
- **PR review feedback** → [code-review](../code-review/SKILL.md)
  - Fetch and address PR comments systematically

## Quality Improvement Workflow

### Step 1: Run comprehensive checks

```bash
make <make.ci>
```

### Step 2: Identify the failing check

Read the grouped per-target output for the specific failure, e.g. a
rust-code-analysis cognitive-complexity value reported above its
`config/metrics-policy.json` limit, or a Jest coverage number below the
`quality.coverage_*` floor.

### Step 3: Use the specialized skill

| Failure Pattern                                                     | Skill to Use                       |
| ------------------------------------------------------------------- | ---------------------------------- |
| "cyclomatic/cognitive/ABC over limit"                               | complexity-management              |
| jscpd clone found                                                   | complexity-management              |
| dependency-cruiser violation / "must not depend on"                 | architecture                       |
| component/hook/store in the wrong module                            | code-organization                  |
| `no-restricted-syntax` (static/free function/data-testid/type-only) | code-organization                  |
| ESLint rule error / TypeScript error / markdownlint                 | frontend-quality-workflow          |
| test failed / coverage gap                                          | frontend-testing-workflow          |
| escaped mutants                                                     | frontend-testing-workflow          |
| visual snapshot diff                                                | frontend-testing-workflow          |
| Lighthouse below floor                                              | frontend-performance-accessibility |
| accessibility violation                                             | accessibility-audit                |

### Step 4: Re-run CI

```bash
make <make.ci>
```

Repeat until the target exits `0` with every score at or above its floor
and every violation count at `0`.

## Constraints (Parameters)

### NEVER

- Lower quality thresholds in the profile or tool config files
  (`jest.config.ts`, `stryker.config.mjs`, `.jscpd.json`,
  `config/metrics-policy.json`, `lighthouse/lighthouserc.*.js`,
  `eslint.config.mjs`, the dependency-cruiser config)
- Skip failing checks to "save time"
- Commit code while the `make.ci` target fails
- Edit the dependency-cruiser config, `.jscpd.json`, or the metrics policy to
  make violations disappear (fix the code, not the config)
- Commit generated visual snapshots unless the UI change is intentional
- Add suppression/ignore annotations to hide quality issues (`eslint-disable`,
  `// @ts-ignore`, `// @ts-nocheck`, `prettier-ignore`,
  `editorconfig-checker-disable`, `markdownlint-disable`, jscpd or
  dependency-cruiser ignore directives, Stryker disable comments,
  `/* istanbul ignore */`)

### ALWAYS

- Fix code to meet standards (not config to meet code)
- Run `make <make.ci>` before creating commits
- Use specialized skills for specific quality issues
- Keep coverage at the `quality.coverage_*` floors and MSI at the
  `quality.mutation_msi` floor over `architecture.source_root`
- Keep cyclomatic complexity low (well under the policy limit) and components,
  hooks, and helpers small
- Respect the bulletproof-react module boundaries and the `@/` / `@auth/`
  path-alias convention
- Treat accessibility as non-negotiable — clear the `make.a11y` lane
- Before presenting changes, disclose any changed-file lines over 100
  characters as `path:line` with the measured count (disclosure, not failure,
  unless a gate fails)
- Skip-with-note when a `make.*` key is `null` (capability absent)

## Format (Output)

Generalized pass criteria, against the profile values:

- `make <make.ci>` exits `0`
- ESLint: errors ≤ `quality.eslint_errors`, warnings ≤ `quality.eslint_warnings` (both `0`)
- TypeScript: errors ≤ `quality.tsc_errors` (i.e. `0`)
- Markdown: errors ≤ `quality.markdownlint_errors` (i.e. `0`)
- jscpd: clones ≤ `quality.jscpd_clones` (i.e. `0`); rust-code-analysis: `0` hard-fail violations (`quality.metrics_enforced` stays `true`)
- dependency-cruiser: violations ≤ `quality.depcruise_violations` (i.e. `0`)
- Coverage: each of statements/branches/functions/lines ≥ its `quality.coverage_*` floor
- Stryker: MSI ≥ `quality.mutation_msi`; Playwright visual: diffs ≤ `quality.visual_diffs` (i.e. `0`)
- Lighthouse: desktop ≥ `quality.lighthouse_desktop`, mobile ≥ `quality.lighthouse_mobile`

```text # profile-example
# Template output at the shipped floors:
✅ CI checks successfully passed!
ESLint: 0 errors, 0 warnings   tsc: 0 errors   markdownlint: 0 errors
jscpd: 0 clones                rust-code-analysis: 0 hard-fail violations
dependency-cruiser: 0 violations
Coverage: 100% statements / branches / functions / lines
Mutation Score Indicator (MSI): >= break threshold   Visual: 0 diffs
Lighthouse  desktop >= 95   mobile >= 85
```

## Verification Checklist

After using this skill:

- [ ] Identified which quality check is failing
- [ ] Selected the appropriate specialized skill for the issue
- [ ] Ready to execute the specialized skill workflow
- [ ] Understand which `quality.*` threshold applies to the failure
- [ ] Know the command (via the `make.*` map) to re-run the check after fixes
- [ ] Capability-absent lanes (visual / mutation / Lighthouse / a11y) noted, not silently dropped

## Related Skills

- [ci-workflow](../ci-workflow/SKILL.md) — run comprehensive CI validation through `make.ci`
- [frontend-quality-workflow](../frontend-quality-workflow/SKILL.md) — fix formatting, ESLint, TypeScript, markdown, and metrics failures
- [complexity-management](../complexity-management/SKILL.md) — reduce rust-code-analysis complexity and resolve jscpd duplication
- [code-organization](../code-organization/SKILL.md) — fix structural/naming issues, class-only and type-only conventions, semantic selectors
- [architecture](../architecture/SKILL.md) — fix dependency-cruiser layer/import-boundary violations
- [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md) — debug Jest/Playwright/visual/mutation failures and close coverage gaps
- [testing-workflow](../testing-workflow/SKILL.md) — general testing strategy across unit, E2E, visual, and mutation
- [frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md) — recover the Lighthouse desktop/mobile floors
- [accessibility-audit](../accessibility-audit/SKILL.md) — address accessibility findings the a11y lane raises
- [code-review](../code-review/SKILL.md) — address PR review feedback

## Reference Documentation

For detailed examples and patterns, see:

- **Refactoring & duplication patterns** → complexity-management skill
- **Module boundaries & import aliases** → architecture skill
- **Class-only / type-only / semantic-selector conventions** → code-organization skill
- **Testing strategies (coverage, mutation, visual)** → frontend-testing-workflow skill
- **Lighthouse & accessibility recovery** → frontend-performance-accessibility and accessibility-audit skills
