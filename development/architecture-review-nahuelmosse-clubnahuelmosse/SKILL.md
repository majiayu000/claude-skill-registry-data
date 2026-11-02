---
name: architecture-review
description: Review codebase architecture for SOLID violations, dependency health, module boundaries, and structural issues. Use when assessing whole-system structure or coupling.
user-invocable: true
allowed-tools: Read, Grep, Glob
---

# Architecture Review

## Core Rule

Critique module boundaries and dependency health against documented intent. Don't propose rewrites — suggest the smallest seam-cutting change.

## When to Use

Invoke with `/architecture-review` when:

- Evaluating overall project structure and organization
- Planning a major refactoring or migration
- Assessing whether the architecture can support planned features
- Onboarding to a codebase and building a mental model
- Due diligence on an inherited or acquired codebase

## Default Behavior

When the user asks to audit, scan, review, or "give me a report" for architecture / module health, produce the full architecture-review report automatically using the Process and Output Format sections below. Do not require the user to specify fields.

Only modify files when the user explicitly requests implement / fix / apply / refactor. By default, this skill is **report-only**.

## Process

### Phase 1: Inventory (first-pass leads)

This pass produces **candidates**, not findings. Treat counts as leads for deeper inspection in later phases. Do not report Phase 1 raw output as the final result.

Build a structural overview:

1. **Read project config** — identify framework, language, dependencies
2. **Map directory structure** — identify layers, modules, boundaries
3. **Identify entry points** — servers, CLI handlers, event processors, main functions
4. **Trace data flow** — request → handler → service → data → response
5. **Identify patterns** — MVC, Clean Architecture, hexagonal, microservices, monolith

### Phase 2: SOLID Principles Check

Evaluate adherence to SOLID (adapted for all paradigms):

**Single Responsibility (S)**
- Does each module/class/file have one clear reason to change?
- Are there god modules that do everything? (>500 lines, multiple concerns)
- Is business logic mixed with infrastructure? (DB queries in handlers, HTTP in services)

**Open/Closed (O)**
- Can new features be added without modifying existing code?
- Are extension points available? (plugins, middleware, strategy pattern)
- Is there excessive switch/if-else that grows with each feature?

**Liskov Substitution (L)**
- Do subtypes/implementations honor the contracts of their interfaces?
- Are there interface implementations that throw "not implemented" errors?
- Do overrides change the expected behavior of base methods?

**Interface Segregation (I)**
- Are interfaces/type contracts focused and minimal?
- Do consumers depend on methods they don't use?
- Are there "fat" interfaces that force empty implementations?

**Dependency Inversion (D)**
- Do high-level modules depend on abstractions, not concrete implementations?
- Are external services (DB, cache, API clients) behind interfaces?
- Can infrastructure be swapped without changing business logic?

### Phase 3: Module Boundaries & Dependencies

Analyze module health:

- **Circular dependencies**: modules that import each other (directly or transitively)
- **Dependency direction**: do dependencies flow inward (toward domain) or outward?
- **Coupling**: changing one module requires changes in many others
- **Cohesion**: are related concepts grouped together?
- **Public surface**: are internal details properly encapsulated?
- **Barrel exports**: do index/barrel files re-export the right things?

### Phase 4: Layer Analysis

Check architectural layering:

- **Presentation → Business → Data**: is the layering consistent?
- **Layer violations**: does the presentation layer directly access the database?
- **Shared state**: is mutable state shared across layers?
- **Configuration**: is config centralized or scattered across modules?
- **Cross-cutting concerns**: how are logging, auth, validation handled? (middleware, decorators, aspect-oriented)

### Phase 5: Scalability Assessment

Evaluate growth readiness:

- Can the codebase support 10x the current feature set without restructuring?
- Are there single points of failure in the architecture?
- Is there a clear strategy for splitting modules if they grow too large?
- Are there hard-coded limits (max items, timeouts) that should be configurable?

## Output Format

```markdown
# Architecture Review Report

## Architecture Overview
[Diagram or description of the current architecture]
[Identified pattern: MVC / Clean / Layered / etc.]

## SOLID Compliance
| Principle | Status | Key Findings |
|-----------|--------|-------------|
| Single Responsibility | ✅/⚠️/❌ | ... |
| Open/Closed | ✅/⚠️/❌ | ... |
| Liskov Substitution | ✅/⚠️/❌ | ... |
| Interface Segregation | ✅/⚠️/❌ | ... |
| Dependency Inversion | ✅/⚠️/❌ | ... |

## Module Health
| Module | Coupling | Cohesion | Issues |
|--------|----------|----------|--------|

## Critical Structural Issues
1. [Issue + impact + recommendation]

## Recommendations
### Short-term (can fix now)
- ...

### Medium-term (next sprint)
- ...

### Long-term (architectural evolution)
- ...
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It's just one exception to the architecture" | Exceptions accumulate. Each one makes the next one easier to justify. |
| "We'll refactor when it becomes a problem" | By the time it's a problem, refactoring costs 10x more. Flag it now. |
| "The project is too small for architecture" | Even small projects have structure. Bad habits set early persist at scale. |
| "This coupling is temporary" | Temporary coupling becomes permanent coupling the moment a second feature depends on it. |
| "SOLID is overkill here" | SOLID is a diagnostic tool, not a rulebook. Use it to identify risks, not enforce dogma. |

## Notes

- This review focuses on structural architecture, not code-level quality (see `/simplify` and `/code-review`)
- For small projects (&lt;5 files), a full architecture review may be overkill — suggest `/simplify` or `/code-review` instead
- Architectural recommendations should consider the team size and project phase

## Related Skills

For design decisions **before** writing code, use `clean-architecture`. For the four stack rules that load automatically when touching `apps/**`, see `.claude/rules/arquitectura.md`.

---
Adapted from `claude-code-kit`, MIT, Copyright (c) 2026 Tansu Asici — https://github.com/tansuasici/claude-code-kit
