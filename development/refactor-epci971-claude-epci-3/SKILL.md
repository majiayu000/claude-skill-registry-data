---
name: epci:refactor
description: >-
  Restructure code architecture without changing external behavior.
  Supports 4 scopes: Single File, Module, Cross-Module, Architecture.
  Patterns: Extract, Inline, Encapsulate, Rename, Move, Strangler Fig, Branch by Abstraction.
  TDD enforced with revert on test failure. Mikado Method for complex dependencies.
  Auto-detects stack skills (Django, React, Spring, Symfony, Tailwind).
  Use when: restructuring code, improving architecture, reducing technical debt.
  Triggers: refactor, restructure, extract, reorganize code, reduce complexity.
  Not for: adding features (use /implement), fixing bugs (use /debug).
user-invocable: true
argument-hint: "<target> [--scope <scope>] [--pattern <pattern>]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, AskUserQuestion
---

# Refactor

Restructure code without changing external behavior using TDD discipline.

## Quick Start

```
/refactor src/services/auth.py
/refactor src/utils/ --scope module
/refactor "split UserService into smaller services" --scope cross-module
/refactor src/core/ --scope architecture --pattern mikado
```

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER modify behavior (must preserve external API)
- 🔴 NEVER skip tests (TDD Red-Green-Refactor enforced)
- 🔴 NEVER continue if tests fail (revert immediately)
- 🔴 NEVER skip the BREAKPOINT at plan validation (step-03)
- ✅ ALWAYS start with step-00-init.md
- ✅ ALWAYS follow next_step from each step
- ✅ ALWAYS detect stack skills at initialization
- ✅ ALWAYS generate metrics before AND after
- ⛔ FORBIDDEN applying untested changes
- 🔵 YOU ARE A DISCIPLINED REFACTORER following TDD

## EXECUTION PROTOCOLS:

1. **Load** step-00-init.md
2. **Execute** current step protocols completely
3. **Present** breakpoint at step-03 (plan validation)
4. **Evaluate** next step trigger conditions
5. **Proceed** to next_step or conditional_next

## CONTEXT BOUNDARIES:

- IN scope: Code restructuring, architecture improvement, technical debt reduction
- OUT scope: Feature changes (use /implement), bug fixes (use /debug), performance optimization (use /improve)

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    REFACTOR WORKFLOW (TDD)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 00: INIT                                                   │
│  ├─ Parse input (target, scope, pattern)                        │
│  ├─ Auto-detect stack skills                                    │
│  └─ Launch @Explore in background                               │
│                                                                  │
│  Step 01: ANALYSIS                                               │
│  ├─ Metrics BEFORE (CC, LOC, dependencies)                      │
│  ├─ Detect code smells (Claude + rules)                         │
│  └─ Build dependency graph                                      │
│                                                                  │
│  Step 02: PLANNING                                               │
│  ├─ Select refactoring patterns                                 │
│  ├─ Define step-by-step transformations                         │
│  └─ IF Architecture scope → Mikado Method graph                 │
│                                                                  │
│  Step 03: BREAKPOINT                                             │
│  └─ User validates refactoring plan                             │
│     └─ Options: [A] Execute [B] Modify [C] Cancel               │
│                                                                  │
│  Step 04: EXECUTE                                                │
│  ├─ TDD: RED → GREEN → REFACTOR (per transformation)            │
│  ├─ Atomic commits (if requested)                               │
│  └─ Revert on test failure                                      │
│                                                                  │
│  Step 05: REVIEW (conditional)                                   │
│  ├─ @code-reviewer (if Module+ scope)                           │
│  ├─ @security-auditor (if auth/security patterns)               │
│  └─ @qa-reviewer (if 5+ test files modified)                    │
│                                                                  │
│  Step 06: VERIFY                                                 │
│  ├─ Run full test suite                                         │
│  ├─ Metrics AFTER                                               │
│  └─ Compare delta                                               │
│                                                                  │
│  Step 07: REPORT                                                 │
│  ├─ Generate metrics report (delta per file)                    │
│  ├─ Update project-memory                                       │
│  └─ Suggest /commit if changes ready                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Scopes

| Scope | Target | Files | Reviews | Example |
|-------|--------|-------|---------|---------|
| `single` | One file | 1 | Skip | Extract method from large function |
| `module` | Directory/module | 2-5 | Conditional | Split service into smaller files |
| `cross-module` | Multiple modules | 5-15 | Always | Extract shared utilities |
| `architecture` | System-wide | 15+ | Always | Apply Strangler Fig pattern |

**Auto-detection**: If no `--scope` provided, inferred from target path and complexity.

## Patterns

| Pattern | Description | Scope |
|---------|-------------|-------|
| `extract-method` | Pull code into new method | single |
| `extract-class` | Create new class from code | single, module |
| `extract-module` | Create new module/file | module |
| `inline` | Merge small units back | single |
| `encapsulate` | Hide implementation details | single, module |
| `rename` | Consistent naming across codebase | all |
| `move` | Relocate code to better location | module+ |
| `strangler-fig` | Gradual replacement of legacy | architecture |
| `branch-by-abstraction` | Abstract before replace | architecture |
| `mikado` | Dependency-aware transformation | architecture |

See [references/refactoring-patterns.md](references/refactoring-patterns.md) for details.

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--scope <scope>` | auto | Force scope: single, module, cross-module, architecture |
| `--pattern <pattern>` | auto | Suggest pattern: extract, inline, rename, strangler-fig, mikado |
| `--turbo` | off | Use @implementer, skip reviews, minimal breakpoints |
| `--dry-run` | off | Generate plan only, no execution |
| `--atomic` | off | Create atomic commits per transformation |
| `--no-metrics` | off | Skip metrics collection |

## Steps

| Step | Name | Description | Skippable |
|------|------|-------------|-----------|
| 00 | init | Parse input, detect stack, launch @Explore | No |
| 01 | analysis | Metrics before, code smells, dependency graph | No |
| 02 | planning | Pattern selection, transformation plan | No |
| 03 | breakpoint | User validation of plan | No |
| 04 | execute | TDD cycle per transformation | No |
| 05 | review | Conditional code/security/qa reviews | Conditional |
| 06 | verify | Tests, metrics after, delta | No |
| 07 | report | Final report, memory update | No |

## Step Files

- [steps/step-00-init.md](steps/step-00-init.md) — Initialization
- [steps/step-01-analysis.md](steps/step-01-analysis.md) — Analysis
- [steps/step-02-planning.md](steps/step-02-planning.md) — Planning
- [steps/step-03-breakpoint.md](steps/step-03-breakpoint.md) — Plan validation
- [steps/step-04-execute.md](steps/step-04-execute.md) — Execution
- [steps/step-05-review.md](steps/step-05-review.md) — Review
- [steps/step-06-verify.md](steps/step-06-verify.md) — Verification
- [steps/step-07-report.md](steps/step-07-report.md) — Report

## Reference Files

- [references/refactoring-patterns.md](references/refactoring-patterns.md) — Pattern catalog
- [references/code-smells-catalog.md](references/code-smells-catalog.md) — Code smell detection
- [references/metrics-formulas.md](references/metrics-formulas.md) — CC, LOC, MI formulas
- [references/mikado-method.md](references/mikado-method.md) — Mikado Method guide

## Templates

- [templates/metrics-report.md](templates/metrics-report.md) — Delta report template

## Shared Components Used

- `epci:complexity-calculator` — Scope estimation
- `epci:tdd-enforcer` — TDD Red-Green-Refactor cycle
- `epci:breakpoint-system` — Plan validation (step-03)
- `epci:state-manager` — Track multi-session refactors
- `epci:project-memory` — Store refactoring patterns

## Subagents

| Agent | Model | Trigger |
|-------|-------|---------|
| `@Explore` | - | Always at init (background) |
| `@implementer` | Sonnet | --turbo mode or Single scope |
| `@code-reviewer` | Opus | Module+ scope, >5 files |
| `@security-auditor` | Opus | Files match `**/auth/**`, `**/security/**` |
| `@qa-reviewer` | Sonnet | >= 5 test files modified |

### Subagent Invocation Matrix

| Subagent | Single | Module | Cross-Module | Architecture |
|----------|--------|--------|--------------|--------------|
| @Explore | Yes | Yes | Yes | Yes |
| @implementer | turbo | turbo | turbo | Skip |
| @code-reviewer | Skip | >5 files | Always | Always |
| @security-auditor | patterns | patterns | patterns | Always |
| @qa-reviewer | Skip | >5 tests | Always | Always |

## Stack Skills (Auto-detected)

| Stack | Trigger Files | Refactoring Context |
|-------|---------------|---------------------|
| `python-django` | manage.py, django in deps | Service layer patterns, pytest |
| `javascript-react` | react in package.json | Component patterns, Jest |
| `java-springboot` | spring-boot in pom/gradle | Bean patterns, JUnit |
| `php-symfony` | symfony in composer.json | Service patterns, PHPUnit |
| `frontend-editor` | tailwind.config.* | Component extraction |

## Metrics Tools (Adaptive)

| Stack | Tool | Fallback |
|-------|------|----------|
| Python | radon, xenon, lizard | Claude estimation |
| PHP | phploc | Claude estimation |
| JavaScript | lizard, eslint-complexity | Claude estimation |
| Java | lizard, checkstyle | Claude estimation |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Tests fail | Behavior changed | Revert, adjust transformation |
| No tests exist | Missing coverage | Warn user, proceed cautiously |
| Circular dependency | Architecture issue | Use Mikado Method |
| Metrics tool missing | Not installed | Use Claude estimation |
| Scope too large | Underestimated | Split into phases |

## Limitations

This skill does NOT:
- Add new features (use /implement)
- Fix bugs (use /debug)
- Optimize performance (use /improve)
- Generate tests from scratch (expects existing tests)
- Modify external API contracts
- Handle database migrations
