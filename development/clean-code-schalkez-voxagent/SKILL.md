---
name: clean-code
description: Enforces Clean Code and SOLID principles during code generation or refactoring in VoxAgent. Use when writing new modules, refactoring existing code, reviewing PRs, or optimizing Python/TypeScript code for maintainability and testability. Triggers on tasks involving new skills, providers, platform modules, or React dashboard components.
---

# Clean Code & SOLID Standards for VoxAgent

Comprehensive guidelines for writing maintainable, testable code across VoxAgent's Python backend and TypeScript dashboard. Contains rules organized by priority to guide automated code generation and refactoring.

## When to Apply

Reference these guidelines when:
- Writing new skills, providers, or core modules (Python)
- Building dashboard components (TypeScript/React)
- Refactoring existing code for readability or performance
- Reviewing code for architectural violations
- Resolving code smells or test failures

## Rule Categories by Priority

| Priority | Category | Impact | Applies to |
|----------|----------|--------|------------|
| 1 | SOLID Principles | CRITICAL | Python + TS |
| 2 | Naming & Readability | HIGH | Python + TS |
| 3 | Error Handling | HIGH | Python |
| 4 | Function Design | MEDIUM | Python + TS |
| 5 | React Patterns | MEDIUM | TS (dashboard) |
| 6 | Dependency Management | LOW-MEDIUM | Python + TS |

## Quick Reference

### 1. SOLID Principles (CRITICAL)

- `solid-srp` — One class/function = one responsibility. If description uses "and", split it.
- `solid-ocp` — Extend via interfaces (BaseSkill, LLMProvider), don't modify existing classes.
- `solid-lsp` — All provider implementations must be drop-in replacements for their base class.
- `solid-isp` — Keep interfaces focused. Don't add vision methods to STTProvider.
- `solid-dip` — Core modules depend on abstractions (ABC), never import concrete providers.

### 2. Naming & Readability (HIGH)

- `naming-intention` — Names reveal intent: `get_active_window()` not `get_aw()`
- `naming-consistency` — Python: `snake_case`. TS components: `PascalCase`. TS files: `kebab-case.tsx`
- `naming-no-abbreviations` — `configuration` not `cfg`, `provider` not `prov`
- `naming-constants` — Extract magic values: `CONFIDENCE_THRESHOLD = 0.85` not inline `0.85`
- `naming-boolean` — Booleans read as questions: `is_active`, `has_permission`, `can_execute`

### 3. Error Handling (HIGH)

- `error-specific` — Catch specific exceptions, never bare `except:` or `except Exception:`
- `error-early-return` — Guard clauses at top, happy path below
- `error-custom-types` — Use custom exceptions: `ProviderUnavailableError`, `SkillPermissionDenied`
- `error-graceful-fallback` — Providers must fallback gracefully per fallback chain in config
- `error-no-silent-fail` — Always log errors, never swallow with empty except blocks

### 4. Function Design (MEDIUM)

- `func-small` — Functions should do one thing well. If scrolling to read, it's too long.
- `func-flat` — Max 2 levels of nesting. Extract inner logic to helper functions.
- `func-pure` — Prefer pure functions. Side effects only at boundaries (I/O, database).
- `func-params` — Max 3 positional params. Use dataclass/TypedDict for more.
- `func-async` — All I/O operations must be async. Never block the event loop.

### 5. React Patterns — Dashboard (MEDIUM)

- `react-composition` — Composition over prop drilling. Use context or custom hooks.
- `react-hooks-extract` — Business logic in custom hooks, components only render.
- `react-memo-expensive` — Memoize computed values, not trivial expressions.
- `react-types-first` — Define Props interface above component, export for reuse.
- `react-no-inline-components` — Never define components inside other components.

### 6. Dependency Management (LOW-MEDIUM)

- `deps-import-order` — stdlib → third-party → local, separated by blank lines
- `deps-no-circular` — No circular imports. If A imports B and B imports A, refactor.
- `deps-lazy-load` — Heavy imports (torch, vision models) lazy-loaded at use site.
- `deps-registry` — All providers accessed through ProviderRegistry, never direct import.

## Operational Procedure

### Before coding
1. Check if similar code/pattern already exists in the codebase
2. Identify which module boundary the change belongs to (core/providers/skills/platform)

### During coding
1. Write types/interfaces first, implementation second
2. Apply the rules above by priority (SOLID first, then naming, etc.)
3. Keep the execution tier priority in mind (Shell → API → UI → Mouse)

### After coding
1. Self-check: does every new public function have type hints and a docstring?
2. Self-check: are there any magic values or bare except blocks?
3. Verify tests exist for new functionality

## Detailed Rules

For expanded examples with before/after code, see `references/` folder:
- `references/solid-examples.md` — SOLID violations and fixes
- `references/python-patterns.md` — Python-specific patterns
- `references/react-patterns.md` — React dashboard patterns
