---
name: complexity-management
description: Maintain and improve React/TypeScript code quality with the rust-code-analysis metrics gate by refactoring code instead of relaxing configuration, keeping every metric at or under its policy ceiling (and Maintainability Index at or above its floor). Use when the metrics gate fails, a component body or hook exceeds cyclomatic/cognitive/ABC complexity, a file or function exceeds its LLOC/PLOC/SLOC or Halstead budget, the Maintainability Index drops, or when refactoring MUI/Emotion components, Zustand stores, or tsyringe collaborators for better maintainability.
---

# Complexity Management

## Profile keys consumed

- `make.lint_metrics`
- `make.lint`
- `make.format`
- `make.lint_deps`
- `make.test_unit_client`
- `make.ci`
- `quality.metrics_enforced`
- `quality.jscpd_clones`
- `quality.eslint_errors`
- `quality.tsc_errors`
- `architecture.source_root`

## Context (Input)

- The metrics gate fails (the target mapped by `make.lint_metrics` returns hard-fail rows)
- A component body, hook, closure, or helper exceeds cyclomatic (`>10`), cognitive (`>15`), or ABC magnitude (`>17`)
- A function or file exceeds its LLOC / PLOC / SLOC budget, or its Halstead volume / bugs
- A function takes more than 3 arguments or has more than 3 exit points
- Maintainability Index (Visual Studio) drops below the policy floor (`<20`)
- A class or interface exceeds its WMC / NPM / NPA / COA / CDA limits
- Adding new MUI/Emotion components, Zustand state, or tsyringe collaborators that increase complexity
- Refactoring existing React/TypeScript code for better maintainability

## Task (Function)

Maintain the profile's code-quality bar using rust-code-analysis while preserving the repository's modular bulletproof-react architecture (feature modules under `architecture.source_root`, `UI*` components, services/config/DI seams).

**Success criteria** — the target mapped by `make.lint_metrics` passes with every hard-fail metric at or under its policy ceiling (and every Maintainability Index value at or above its floor):

- Cyclomatic Complexity ≤ `10`, Cognitive ≤ `15`, ABC magnitude ≤ `17`
- Function / closure arguments ≤ `3`, exit points ≤ `3`
- Function LLOC / PLOC / SLOC ≤ `10 / 40 / 45`; file LLOC / PLOC / SLOC ≤ `120 / 300 / 350`
- Halstead volume / bugs ≤ function `1000 / 0.35`, file `8000 / 1.58`
- Maintainability Index (Visual Studio) ≥ `20`
- Class WMC / NPM / NPA / COA / CDA and interface NPM / NPA within policy

---

## Protected Quality Thresholds (raise-only)

The gate is governed by `quality.metrics_enforced` (a boolean, `true` by
default — the rca hard-fail gate is on). The authoritative limits live in the
repository's rust-code-analysis policy (`config/metrics-policy.json`) under its
`hard` block, and `make lint-metrics` enforces exactly those numbers. **Raise-only
rule**: a profile may tighten these limits (lower a ceiling, raise the MI floor),
never relax them — and the repository's policy file must satisfy the profile:

```json
// config/metrics-policy.json — the "hard" block must be >= as strict as the profile
"hard": {
  "cyclomatic_max": 10,
  "cognitive_max": 15,
  "abc_magnitude_max": 17,
  "nargs_function_max": 3,
  "nexits_max": 3,
  "mi_visual_studio_min": 20
}
```

The `review` block in the same policy file (Maintainability Index original/SEI,
comment/blank ratios, the remaining Halstead submetrics) is kept for calibration
but is **not** printed by `make lint-metrics` and does not fail CI by itself.

**Policy**: if the metrics gate fails, fix the code — NEVER lower these
thresholds, in the policy file or in the profile.

```text
When the metrics gate fails, you MUST FIX THE CODE.
FORBIDDEN: changing the policy (or the profile) to pass checks.
REQUIRED:  refactoring code to meet the standards.
```

---

## Quick Start Workflow

### Step 1: Identify the complex subjects

Read the violation table printed by the metrics gate — it names the offending
file, scope, subject, and line. Each row has eight columns:

```text
GATE     FILE                         SCOPE     SUBJECT          LINE  METRIC          VALUE  LIMIT
----------------------------------------------------------------------------------------------------
FAIL     <source-root>/.../foo.ts     function  processResponse    96  cognitive          28  <=15
```

Only hard failures are printed. Use search to locate the related component, hook,
and style definitions before moving any code:

```bash
rg "function ComponentName|const ComponentName" "<architecture.source_root>"
rg "use[A-Z].*=" "<architecture.source_root>"
rg "sx=|styled\\(" "<architecture.source_root>"
```

**Metrics to read**:

- **Cyclomatic Complexity**: `>10` is a hard fail (branch-count of one function)
- **Cognitive Complexity**: `>15` is a hard fail (nesting-weighted difficulty)
- **ABC magnitude**: `>17` (assignments + branches + conditions)
- **Function LLOC / PLOC / SLOC**: `>10 / 40 / 45`
- **Halstead volume / bugs**: dense expressions and repeated operators
- **Maintainability Index (Visual Studio)**: `<20` means split responsibilities

### Step 2: Run the metrics gate

Run the target mapped by `make.lint_metrics`. If the mapping is `null`, the
capability is absent — note it and degrade instead of inventing a target. (The
`code-quality-reviewer` agent surfaces the same MI/complexity regressions during
`/fe-sdlc-review`.)

### Step 3: Identify the failing metric

```text
FAIL  <source-root>/modules/.../use-foo.ts  function  useFoo  42  cyclomatic  13  <=10
```

### Step 4: Apply a refactoring strategy

- **Split container and view**: keep data fetching, mutation, routing, and Zustand
  reads in a container or hook; pass plain props to a presentational `UI*` component
- **Extract decision/data-shaping helpers**: move dense boolean logic and mapping
  out of JSX and hooks into **instance methods on a class** (a singleton, or an
  `@injectable()` tsyringe collaborator) — never a free function or `static` member,
  which the ESLint convention gate rejects
- **Replace branches with typed lookup maps**: swap if/else or switch chains over a
  union type for a `Record<Status, …>` defined outside render
- **Guard clauses**: replace nested conditionals with early returns, but consolidate
  early returns so a function stays at or under 3 exit points
- **Group arguments**: fold a `>3`-argument signature into a single typed options object
- **Move repeated state transitions into a hook or the Zustand store** instead of
  re-deriving them per render
- **Reduce Halstead weight**: simplify dense expressions, repeated operators, and
  mixed concerns; keep stable Emotion style objects outside render work
- **Split oversized files by ownership, not by arbitrary line count**

```typescript
// Extracted decision helper as an instance method (no free function, no static)
class RetryPolicy {
  public shouldShowRetry(status: Status, attempts: number): boolean {
    return status === 'failed' && attempts < 3;
  }
}
const retryPolicy = new RetryPolicy();
export default retryPolicy;
```

```typescript
// Stable variant map, defined once outside render
const variantTitleByStatus: Record<Status, string> = {
  idle: 'profile.idle',
  loading: 'profile.loading',
  failed: 'profile.failed',
  saved: 'profile.saved',
};
```

Watch the per-file function/closure budget while extracting: the gate caps
functions-per-file at `10` (and total functions+closures at `15`), so a new hook or
class often belongs in its own file. Type-level constructs move to a dedicated
type-only file, not alongside the logic.

### Step 5: Verify improvements

Re-run the target mapped by `make.lint_metrics`. Splitting files also moves ESLint,
TypeScript, and jscpd, so run the target mapped by `make.format` then the target
mapped by `make.lint`. Repeat steps 3–5 until all hard-fail metrics pass.

---

## Quick Fix Guide by Issue Type

### Complexity / cognitive / ABC magnitude too high

**Problem**: a function, hook, closure, or component body has too many decision
points or too much nesting-weighted difficulty.

**Fix**: locate the hotspot (Step 1), then apply split-container/view, extract a
decision helper, replace branches with a lookup map, or consolidate exit points
(Step 4). Keep each extracted unit's complexity low rather than relocating the
whole blob. Route the actual edit through the `react-implementer` agent during
`/fe-sdlc-implement`.

### Architecture / dependency-cruiser violations

**Problem**: a split reaches across a bulletproof-react boundary (e.g. a component
importing a repository directly, or a cross-feature deep relative chain).

**Fixes**:

1. Respect the layering: components/hooks → feature stores/services → repositories
2. Keep behavioral collaborators behind a tsyringe token (`@injectable()`, resolved
   via the DI container), not reached for at the call site
3. Use the configured path aliases (`@/`, `@auth/`) instead of `../../../` chains
4. Keep types in dedicated type-only files imported with `import type`

**See**: [architecture](../architecture/SKILL.md) for fixing dependency-cruiser
boundaries — always fix the code, never edit the dependency-cruiser config.

### Halstead, line-count, or Maintainability Index out of band

**Problem**: a function or file exceeds its LLOC/PLOC/SLOC or Halstead budget, or
MI drops below `20`.

**Fix**: split the function or file into smaller units by responsibility; reduce
dense expressions and repeated operators; reuse identical Emotion style fragments
(also satisfies the jscpd DRY gate, `quality.jscpd_clones` ceiling `0`). Do **not**
split a component by line count alone when the pieces still share the same state and
side effects — split by responsibility.

### Line length over the soft limit

**Problem**: lines exceed the configured limit (commonly the 100-character soft line
limit).

**Fixes**:

1. Break long JSX props or method calls across multiple lines
2. Extract complex expressions into named `const`s
3. Use a path alias (`@/`, `@auth/`) instead of a long relative import
4. Refactor long prop lists into a typed options object

Before presenting changes, check changed files for lines longer than 100 characters
and disclose each `path:line` with its measured count — treat this as disclosure, not
failure, unless a project gate fails.

---

## Constraints (Parameters)

### NEVER

- Lower limits in `config/metrics-policy.json` (or any per-suite metrics config)
- Flip `quality.metrics_enforced` to `false`, or relax any profile floor (raise-only)
- Skip the metrics gate to "save time"
- Add `eslint-disable` / `@ts-ignore` / suppression directives to silence a finding
- Edit the dependency-cruiser config to accommodate a boundary violation
- Introduce a free function or `static` member when extracting a helper (the ESLint
  convention gate rejects both outside React components)
- Add a `data-testid` to make a split component testable — locate it by semantics
- Split a component by line count alone when the pieces still share state and effects

### ALWAYS

- Fix code to meet standards (not config to meet code)
- Re-run the target mapped by `make.lint_metrics` after refactoring
- Preserve the bulletproof-react module boundaries while reducing complexity
- Keep extracted logic as instance methods on classes (singleton or `@injectable()`),
  with types in dedicated type-only files
- Run the target mapped by `make.format`, then the target mapped by `make.lint`, after
  a refactor (splitting files moves ESLint, TypeScript, and jscpd)
- Run the target mapped by `make.ci` before finishing
- Preserve unit coverage while refactoring (target mapped by `make.test_unit_client`);
  the coverage floors stay fixed at `100`

---

## Format (Output)

Expected metrics-gate output — every hard-fail metric at or under its ceiling, with
no FAIL rows:

```text
GATE     FILE   SCOPE   SUBJECT   LINE   METRIC   VALUE   LIMIT
----------------------------------------------------------------
(no hard failures)
```

Expected CI output: the target mapped by `make.ci` passes.

---

## Verification Checklist

After refactoring:

- [ ] Target mapped by `make.lint_metrics` passes without hard-fail rows
- [ ] Cyclomatic ≤ `10`, Cognitive ≤ `15`, ABC magnitude ≤ `17`
- [ ] Function / file LLOC / PLOC / SLOC and Halstead within policy
- [ ] Maintainability Index (Visual Studio) ≥ `20`
- [ ] No dependency-cruiser boundary violations (target mapped by `make.lint_deps` passes)
- [ ] No new jscpd clones (`quality.jscpd_clones` ceiling `0`)
- [ ] ESLint and TypeScript clean (`quality.eslint_errors` / `quality.tsc_errors` ceiling `0`)
- [ ] All client unit tests still pass (target mapped by `make.test_unit_client`)
- [ ] Unit coverage maintained at `100`
- [ ] Code remains aligned with the bulletproof-react architecture

---

## Priority Order for Fixes

When facing multiple issues:

1. **CRITICAL (cyclomatic > 10, cognitive > 15, or MI < 20)**: immediate refactoring required
2. **HIGH (architecture / dependency-cruiser violations)**: breaks bulletproof-react boundaries
3. **MEDIUM (file LLOC/PLOC/SLOC or Halstead volume near ceiling)**: plan a split
4. **LOW (line length, comment/blank ratios)**: quick fixes, often local

If UI behavior changes while reducing complexity, also run the focused client, E2E,
or visual test that covers the changed path; if the changed module is mutation-gated,
re-run mutation testing so the refactor does not leave surviving mutants.

---

## Related Skills

- [quality-standards](../quality-standards/SKILL.md) — overview of all protected quality thresholds
- [architecture](../architecture/SKILL.md) — bulletproof-react layering and dependency-cruiser boundaries
- [code-organization](../code-organization/SKILL.md) — structural refactoring, file placement, naming, splitting
- [frontend-component-development](../frontend-component-development/SKILL.md) — splitting components, hooks, and forms
- [frontend-quality-workflow](../frontend-quality-workflow/SKILL.md) — format, lint, TypeScript, markdown, and metrics gates
- [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md) — preserve Jest/Testing Library coverage during refactoring
- [ci-workflow](../ci-workflow/SKILL.md) — run comprehensive CI checks

---

## External Resources

- **rust-code-analysis**: <https://github.com/mozilla/rust-code-analysis>
- **bulletproof-react**: inspiration for the modular architecture and layering
