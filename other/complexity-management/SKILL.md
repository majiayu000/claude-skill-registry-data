---
name: complexity-management
description: Maintain and improve code quality with PHPInsights by refactoring code instead of relaxing configuration, keeping every score at or above the profile's quality.phpinsights.* floors. Use when PHPInsights fails, cyclomatic complexity is too high, a quality/architecture/style score drops, or when refactoring for better maintainability.
---

# Code Complexity Management

## Profile keys consumed

- `make.phpinsights`
- `make.deptrac`
- `make.tests`
- `make.ci`
- `quality.phpinsights.quality`
- `quality.phpinsights.complexity`
- `quality.phpinsights.architecture`
- `quality.phpinsights.style`
- `architecture.source_root`

## Context (Input)

- PHPInsights checks fail (the target mapped by `make.phpinsights` returns errors)
- Cyclomatic complexity exceeds thresholds
- Code quality, architecture, or style score drops below `quality.phpinsights.quality` / `quality.phpinsights.architecture` / `quality.phpinsights.style`
- Complexity score falls below `quality.phpinsights.complexity`
- Adding new features that increase complexity
- Refactoring existing code for better maintainability

## Task (Function)

Maintain the profile's code-quality bar using PHPInsights while preserving the repository's layered architecture (hexagonal/DDD/CQRS where applicable).

**Success criteria** — the target mapped by `make.phpinsights` passes with every score at or above its profile floor:

- Quality ≥ `quality.phpinsights.quality`
- Complexity ≥ `quality.phpinsights.complexity`
- Architecture ≥ `quality.phpinsights.architecture`
- Style ≥ `quality.phpinsights.style`

---

## Protected Quality Thresholds (raise-only)

Thresholds come from the profile's `quality.phpinsights.*` keys. Canonical
shipped defaults: quality `100`, architecture `100`, style `100`,
complexity `94`. **Raise-only rule**: a profile may tighten these floors
above the defaults, never relax them — and the repository's PHPInsights
config must satisfy them:

```php
// phpinsights.php — 'requirements' must be >= the profile floors
'requirements' => [
    'min-quality'      => 100, // >= quality.phpinsights.quality
    'min-complexity'   => 94,  // >= quality.phpinsights.complexity
    'min-architecture' => 100, // >= quality.phpinsights.architecture
    'min-style'        => 100, // >= quality.phpinsights.style
],
```

The same protection applies to any per-suite PHPInsights config the
repository ships (e.g. a tests-only config file).

**Policy**: if PHPInsights fails, fix the code — NEVER lower these
thresholds, in the config or in the profile.

```text
When PHPInsights fails, you MUST FIX THE CODE.
FORBIDDEN: changing config (or the profile) to pass checks.
REQUIRED:  refactoring code to meet the standards.
```

---

## Quick Start Workflow

### Step 1: Identify complex classes

Read the complexity section of the PHPInsights failure output — it names
the offending classes and methods. If the repository wraps a dedicated
hotspot analyzer in a `make` target, prefer it; otherwise run PHPMD's
codesize ruleset through the containerized toolchain (never bare on the
host):

```bash
docker compose exec <php-service> vendor/bin/phpmd <architecture.source_root> text codesize
```

```bash # profile-example
# The upstream reference repo wraps hotspot analysis in make targets:
make analyze-complexity N=10                          # top 10 complex classes
make analyze-complexity-json N=20 > complexity.json   # export for tracking
```

**Metrics to read**:

- **CCN (Cyclomatic Complexity)**: > 15 is critical
- **WMC (Weighted Method Count)**: sum of all method complexities
- **Avg Complexity**: CCN ÷ methods (target: < 5)
- **Max Complexity**: highest complexity of any single method
- **Maintainability Index**: 0–100 (target: > 65)

### Step 2: Run PHPInsights

Run the target mapped by `make.phpinsights`. If the mapping is `null`,
the capability is absent — note it and degrade instead of inventing a
target.

### Step 3: Identify the failing metric

```text
[COMPLEXITY] 93.5 pts (target: <quality.phpinsights.complexity>)
Method `SomeCommandHandler::handle` has cyclomatic complexity of 12
```

### Step 4: Apply a refactoring strategy

- **Extract methods**: break a complex method into smaller private methods, each with a single decision
- **Strategy pattern**: replace conditional chains (if/elseif/switch over a type) with polymorphism
- **Early returns**: replace nested conditionals with guard clauses
- **Functional composition**: replace loop-with-conditional accumulation with `array_map`/`array_filter`/`array_reduce` pipelines
- **Command pattern**: separate command-handling logic into dedicated handlers

### Step 5: Verify improvements

Re-run the target mapped by `make.phpinsights`. Repeat steps 3–5 until
all scores meet the profile floors.

---

## Quick Fix Guide by Issue Type

### Cyclomatic complexity too high

**Problem**: method has too many decision points (if/else/switch/loops).

**Fix**: locate the hotspot (Step 1), then apply extract-methods,
strategy pattern, early returns, or command pattern (Step 4). Keep each
extracted method's complexity low rather than relocating the whole blob.

### Architecture violations

**Problem**: layer dependencies violated (e.g. Domain depending on
Infrastructure).

**Fixes**:

1. Review layer boundaries: Domain → Application → Infrastructure
2. Define interfaces in Domain, implement them in Infrastructure
3. Inject dependencies through constructors
4. Keep data access behind repository implementations in Infrastructure

**See**: [deptrac-fixer](../deptrac-fixer/SKILL.md) for fixing
architectural violations — always fix the code, never edit `deptrac.yaml`.

### Style issues

**Problem**: code doesn't meet PSR-12 / framework coding standards.

**Fix**: run the repository's style auto-fixer `make` target if one
exists, else `docker compose exec <php-service> vendor/bin/php-cs-fixer fix`,
then re-run the target mapped by `make.phpinsights` to verify.

### Line length over the configured limit

**Problem**: lines exceed the configured limit (commonly 100–120 chars).

**Fixes**:

1. Break long method calls into multiple lines
2. Extract complex expressions into variables
3. Use named parameters (PHP 8+)
4. Refactor long argument lists into DTOs

---

## Constraints (Parameters)

### NEVER

- Lower thresholds in `phpinsights.php` (or any per-suite PHPInsights config)
- Lower `quality.phpinsights.*` values in the profile (raise-only)
- Skip PHPInsights checks to "save time"
- Add suppression annotations or disable sniffs to silence a finding
- Edit `deptrac.yaml` to accommodate a violation
- Ignore architecture violations
- Put business logic in the Application layer (it belongs in Domain)

### ALWAYS

- Fix code to meet standards (not config to meet code)
- Re-run the target mapped by `make.phpinsights` after refactoring
- Maintain the layered architecture while reducing complexity
- Keep the Domain layer pure (no framework dependencies)
- Run the target mapped by `make.ci` before finishing
- Preserve test coverage while refactoring (target mapped by `make.tests`)

---

## Format (Output)

Expected PHPInsights output — each score at or above its profile floor:

```text
[CODE]         >= quality.phpinsights.quality       (default 100)
[COMPLEXITY]   >= quality.phpinsights.complexity    (default 94)
[ARCHITECTURE] >= quality.phpinsights.architecture  (default 100)
[STYLE]        >= quality.phpinsights.style         (default 100)
```

Expected CI output: the target mapped by `make.ci` passes.

---

## Verification Checklist

After refactoring:

- [ ] Target mapped by `make.phpinsights` passes without errors
- [ ] Quality ≥ `quality.phpinsights.quality`
- [ ] Complexity ≥ `quality.phpinsights.complexity`
- [ ] Architecture ≥ `quality.phpinsights.architecture`
- [ ] Style ≥ `quality.phpinsights.style`
- [ ] No layer-boundary violations (target mapped by `make.deptrac` passes)
- [ ] All tests still pass (target mapped by `make.tests`)
- [ ] Test coverage maintained
- [ ] Code remains aligned with the layered architecture

---

## Priority Order for Fixes

When facing multiple issues:

1. **CRITICAL (complexity > 15)**: immediate refactoring required
2. **HIGH (architecture violations)**: breaks hexagonal/DDD boundaries
3. **MEDIUM (complexity 10–15)**: plan refactoring
4. **LOW (style issues)**: quick fixes, often auto-fixable

---

## Related Skills

- [quality-standards](../quality-standards/SKILL.md) — overview of all protected quality thresholds
- [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) — proper layer separation and patterns
- [deptrac-fixer](../deptrac-fixer/SKILL.md) — fix architectural violations
- [code-organization](../code-organization/SKILL.md) — structural refactoring, directory placement, naming
- [ci-workflow](../ci-workflow/SKILL.md) — run comprehensive CI checks
- [testing-workflow](../testing-workflow/SKILL.md) — maintain test coverage during refactoring

---

## External Resources

- **PHPInsights documentation**: <https://phpinsights.com/>
- **CodelyTV DDD**: inspiration for architecture patterns
