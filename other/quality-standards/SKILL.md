---
name: quality-standards
description: Overview of the protected quality thresholds and a quick-reference router that maps every failing quality check to its command and specialized fixing skill. Use when you need to understand quality metrics, run comprehensive quality checks, or learn which specialized skill to use. For specific issues, use dedicated skills (deptrac-fixer for Deptrac, complexity-management for PHPInsights, testing-workflow for coverage and mutation).
---

# Quality Standards Skill

## Profile keys consumed

- `make.ci`, `make.psalm`, `make.deptrac`, `make.phpinsights`, `make.infection`, `make.tests`, `make.e2e`
- `quality.phpinsights.quality`, `quality.phpinsights.complexity`, `quality.phpinsights.architecture`, `quality.phpinsights.style`
- `quality.deptrac_violations`, `quality.psalm_errors`, `quality.infection_msi`
- `architecture.source_root`

Command convention: `make <make.X>` means "run `make` with the target the
profile maps for key `make.X`". A `null` mapping means the capability is
absent in this repository — skip that check with a capability-absent note
instead of failing (NFR-4). Generic tooling (`composer`, `git`, `gh`) is
invoked directly. PHP quality tools without a `make.*` key still run
through the containerized toolchain: prefer a repository `make` target
that wraps the tool, else `docker compose exec <php-service>
vendor/bin/<tool>`; never run them bare on the host, and note the gap if
neither wrapper exists.

## Context (Input)

- Need to understand the protected quality thresholds
- Running comprehensive quality checks before commit
- Determining which specialized skill to use for a specific issue
- Quick reference for quality tool commands

## Task (Function)

Understand quality metrics and route to the appropriate specialized skill
for fixes.

**Success Criteria**: Know which skill to use for your specific quality issue.

## Protected Quality Thresholds

**CRITICAL — raise-only rule (ADR-7)**: the `quality.*` values in the
project profile are floors/ceilings over the shipped defaults. A profile
may tighten the bar (raise score floors), never relax it. Violation-count
ceilings ship at `0` and may not be raised. NEVER lower any threshold in
the profile or in tool config files.

### PHPInsights (source code)

| Metric       | Profile key                        | Shipped floor | Fix With                                                   |
| ------------ | ---------------------------------- | ------------- | ---------------------------------------------------------- |
| Quality      | `quality.phpinsights.quality`      | 100           | [complexity-management](../complexity-management/SKILL.md) |
| Complexity   | `quality.phpinsights.complexity`   | 94            | [complexity-management](../complexity-management/SKILL.md) |
| Architecture | `quality.phpinsights.architecture` | 100           | [deptrac-fixer](../deptrac-fixer/SKILL.md)                 |
| Style        | `quality.phpinsights.style`        | 100           | Containerized style fixer (see the Code style row below)   |

Some repositories configure a second PHPInsights pass with separate
thresholds for test directories in their phpinsights config. Those values
are repository config, not profile keys — the raise-only rule applies to
them identically: tighten if needed, never loosen.

### Other tools

| Tool      | Metric          | Profile key / bound                                                                                                                                                                                              | Fix With                                                                                              |
| --------- | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Deptrac   | Violations      | `quality.deptrac_violations` (ceiling, fixed `0`)                                                                                                                                                                | [deptrac-fixer](../deptrac-fixer/SKILL.md)                                                            |
| Psalm     | Errors          | `quality.psalm_errors` (ceiling, fixed `0`)                                                                                                                                                                      | Fix reported issues                                                                                   |
| Psalm     | ForbiddenCode   | counted in `quality.psalm_errors`                                                                                                                                                                                | Use the framework serializer; follow the guards in [code-organization](../code-organization/SKILL.md) |
| Psalm     | Security issues | `0` (taint analysis)                                                                                                                                                                                             | Fix tainted flows                                                                                     |
| Infection | MSI             | `quality.infection_msi` (floor, shipped `100`)                                                                                                                                                                   | [testing-workflow](../testing-workflow/SKILL.md)                                                      |
| PHPUnit   | Line coverage   | line coverage at the project's enforced target (an independent bar) — Infection MSI is a separate, stronger signal but does NOT by itself guarantee full line coverage (MSI is measured only over mutated lines) | [testing-workflow](../testing-workflow/SKILL.md)                                                      |

## Quick Reference Commands

### Comprehensive checks

```bash
# Run the full local CI suite (recommended before commit)
make <make.ci>
```

**Success**: the target exits `0` and every reported score sits at or
above its `quality.*` floor.

### Individual quality checks

| Check               | Command                                                                                             | Purpose                     |
| ------------------- | --------------------------------------------------------------------------------------------------- | --------------------------- |
| Code quality        | `make <make.phpinsights>`                                                                           | All PHPInsights metrics     |
| Complexity hotspots | `docker compose exec <php-service> vendor/bin/phpmd <architecture.source_root> text <repo ruleset>` | Find high-CCN methods       |
| Static analysis     | `make <make.psalm>`                                                                                 | Type checking and errors    |
| Security taint      | `docker compose exec <php-service> vendor/bin/psalm --taint-analysis`                               | Security vulnerability scan |
| Architecture        | `make <make.deptrac>`                                                                               | Layer boundary validation   |
| Code style          | `docker compose exec <php-service> vendor/bin/php-cs-fixer fix`                                     | Auto-fix coding standards   |
| Composer validation | `composer validate --strict`                                                                        | Validate composer.json/lock |

For the rows not backed by a `make.*` key (PHPMD, taint analysis, style
fixer), prefer a repository `make` wrapper target when one exists — the
`docker compose exec` form is the fallback (command convention above).

### Testing commands

| Check                  | Command                                              | Purpose                                           |
| ---------------------- | ---------------------------------------------------- | ------------------------------------------------- |
| Unit/integration tests | `make <make.tests>`                                  | Domain/Application logic + component interactions |
| E2E tests              | `make <make.e2e>`                                    | Full user scenarios                               |
| Test coverage          | see [testing-workflow](../testing-workflow/SKILL.md) | Generate coverage report                          |
| Mutation tests         | `make <make.infection>`                              | Test quality validation                           |

## Routing to Specialized Skills

When quality checks fail, use the appropriate specialized skill:

### Architecture issues

- **Deptrac violations** → [deptrac-fixer](../deptrac-fixer/SKILL.md)
  - Domain depends on Infrastructure
  - Layer boundary violations
  - "must not depend on" errors
- **DDD architecture patterns** → [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md)
  - Creating new entities/value objects
  - Implementing CQRS patterns
  - Understanding layer responsibilities

### Code quality issues

- **High cyclomatic complexity** → [complexity-management](../complexity-management/SKILL.md)
  - PHPInsights complexity below `quality.phpinsights.complexity`
  - PHPMD reports high CCN
  - Methods too complex
- **Structural/naming issues** → [code-organization](../code-organization/SKILL.md)
  - Class in wrong directory for its type
  - Vague variable or class names
  - Hardcoded config values that should be in `.env`
  - Namespace doesn't match directory structure
- **Code style issues** → run the repository's style-fixer `make` target
  if one exists, else `docker compose exec <php-service> vendor/bin/php-cs-fixer fix`
  - Coding-standard violations per the repository's fixer config
  - Formatting and line-length issues

### Testing issues

- **Test failures** → [testing-workflow](../testing-workflow/SKILL.md)
  - Unit/Integration/E2E failures
  - Mutation testing (Infection) below `quality.infection_msi`
  - Coverage gaps

### Workflow integration

- **Before committing** → [ci-workflow](../ci-workflow/SKILL.md)
  - Run all checks systematically
  - Fix failures in priority order
- **PR review feedback** → [code-review](../code-review/SKILL.md)
  - Fetch and address PR comments systematically

## Quality Improvement Workflow

### Step 1: Run comprehensive checks

```bash
make <make.ci>
```

### Step 2: Identify the failing check

Read the output for the specific failure, e.g. a PHPInsights complexity
score reported below the `quality.phpinsights.complexity` floor.

### Step 3: Use the specialized skill

| Failure Pattern            | Skill to Use             |
| -------------------------- | ------------------------ |
| "Complexity score too low" | complexity-management    |
| Deptrac violations         | deptrac-fixer            |
| "must not depend on"       | deptrac-fixer            |
| "Class not found"          | code-organization        |
| Namespace mismatch         | code-organization        |
| tests failed               | testing-workflow         |
| "Psalm found errors"       | Fix type errors directly |
| escaped mutants            | testing-workflow         |

### Step 4: Re-run CI

```bash
make <make.ci>
```

Repeat until the target exits `0` with every score at or above its floor.

## Constraints (Parameters)

### NEVER

- Lower quality thresholds in the profile or tool config files
  (`phpinsights.php`, `infection.json5`, etc.)
- Skip failing checks to "save time"
- Commit code without all CI checks passing
- Modify `deptrac.yaml` to allow violations (fix code, not config)
- Disable security checks
- Add suppression/ignore annotations to hide quality issues
  (`@SuppressWarnings`, `@infection-ignore*`, `@codeCoverageIgnore*`,
  `@psalm-suppress`, `@phpstan-ignore*`, `phpcs:ignore`,
  `@phpinsights-ignore*`)

### ALWAYS

- Fix code to meet standards (not config to meet code)
- Run `make <make.ci>` before creating commits
- Use specialized skills for specific quality issues
- Keep coverage and MSI at the `quality.infection_msi` floor
- Keep cyclomatic complexity low (target: < 5 per method)
- Respect the layered architecture boundaries
- Skip-with-note when a `make.*` key is `null` (capability absent, NFR-4)

## Format (Output)

Generalized pass criteria, against the profile values:

- `make <make.ci>` exits `0`
- PHPInsights: each of the four scores ≥ its `quality.phpinsights.*` floor
- Deptrac: violations ≤ `quality.deptrac_violations` (i.e. zero)
- Psalm: errors ≤ `quality.psalm_errors` (i.e. zero)
- Infection: MSI ≥ `quality.infection_msi`

```text # profile-example
# Reference-service output at the shipped floors:
✅ CI checks successfully passed!
[CODE] 100.0 pts  [COMPLEXITY] 94.0 pts  [ARCHITECTURE] 100 pts  [STYLE] 100.0 pts
✅ No violations found            # deptrac
Mutation Score Indicator (MSI): 100%
```

## Verification Checklist

After using this skill:

- [ ] Identified which quality check is failing
- [ ] Selected the appropriate specialized skill for the issue
- [ ] Ready to execute the specialized skill workflow
- [ ] Understand which `quality.*` threshold applies to the failure
- [ ] Know the command (via the `make.*` map) to re-run the check after fixes

## Related Skills

- [ci-workflow](../ci-workflow/SKILL.md) — run comprehensive CI validation
- [complexity-management](../complexity-management/SKILL.md) — reduce complexity, improve quality
- [code-organization](../code-organization/SKILL.md) — fix structural/naming issues, extract hardcoded configs
- [code-review](../code-review/SKILL.md) — address PR review feedback
- [deptrac-fixer](../deptrac-fixer/SKILL.md) — fix architectural violations
- [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) — understand DDD patterns
- [testing-workflow](../testing-workflow/SKILL.md) — fix test failures, improve coverage

## Reference Documentation

For detailed examples and patterns, see:

- **Refactoring patterns** → complexity-management skill
- **Architecture rules** → implementing-ddd-architecture skill
- **Layer boundaries** → deptrac-fixer skill
- **Testing strategies** → testing-workflow skill
