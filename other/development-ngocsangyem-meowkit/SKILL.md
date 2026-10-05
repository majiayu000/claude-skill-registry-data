---
name: mk:development
description: Use when implementing features or writing code. TDD enforcement is opt-in via --tdd / MEOWKIT_TDD=1. Provides code patterns, skill loading, and coding standards.
keywords:
  - development
  - feature-implementation
  - tdd-optional
  - coding-standards
  - skill-loading
when_to_use: Use when implementing features or writing code. TDD opt-in via --tdd. NOT for orchestrated pipelines (see mk:cook).
user-invocable: true
owner: utility
criticality: medium
status: active
runtime: claude-code
---

# Development Toolkit

Reference guides for implementation: code patterns, TDD enforcement (opt-in), and skill lazy-loading.

## When to Use

- During Phase 3 (Build) for implementation guidance
- When the `developer` agent needs coding pattern references
- For TDD enforcement rules during red/green/refactor cycle (TDD mode only)

## Workflow Integration

Operates in **Phase 2 (Test)** and **Phase 3 (Build)**. Output supports the `developer` and `tester` agents.

TDD enforcement (`tdd-enforcement.md` reference) is OPT-IN as of the TDD-optional migration. Default mode skips RED-phase enforcement; enable with `--tdd` or `MEOWKIT_TDD=1`.

## References

| Reference | When to load | Content |
|-----------|-------------|---------|
| **[code-patterns.md](./references/code-patterns.md)** | During implementation | Coding patterns, architecture patterns, file organization |
| **[tdd-enforcement.md](./references/tdd-enforcement.md)** | Phase 2-3 | RED/GREEN/REFACTOR cycle, test-first rules, coverage requirements |
| **[skill-loader.md](./references/skill-loader.md)** | Skill activation | How to load skills on-demand, lazy loading patterns |

## Gotchas

- **TDD enforcement blocking exploratory prototyping**: Strict red-green cycle slows rapid iteration → Default mode (TDD off) is now the right choice for prototypes; opt into `--tdd` only when shipping production-quality work
- **200-line file rule on generated code**: Auto-generated files (migrations, schemas) exceed limit by design → Exempt generated files explicitly in plan constraints
