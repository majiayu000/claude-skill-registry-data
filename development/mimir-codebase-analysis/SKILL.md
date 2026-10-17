---
name: mimir-codebase-analysis
description: Explore codebases, analyze system architecture, and assess the impact of proposed changes.
---

# Codebase Analysis

## Purpose

Understand an existing codebase from structure to architecture, and assess how proposed changes would affect the system. Identify how the system is organized, how components interact, evaluate architectural decisions, and determine the blast radius and risk of modifications.

## When to Use

- At the start of a new task involving an unfamiliar codebase.
- Before making architectural recommendations or evaluating trade-offs.
- Before implementing a change that may affect multiple modules or services.
- When assessing the risk of a refactoring, migration, or dependency upgrade.
- When evaluating whether a fix might introduce regressions.

## Workflow

1. **Identify which sub-domain(s) the brief invokes; apply only those subsections.**

### Exploration

2. **Explore the repository structure.**
   - Understand the directory layout, key entry points, and configuration.
   - Identify the language(s), frameworks, and build systems in use.

3. **Map components and relationships.**
   - Identify the major modules, services, or packages.
   - Trace dependencies between them and understand data flow.
   - Document relevant execution paths.

4. **Analyze architecture and patterns.**
   - Identify the architectural style (layered, hexagonal, microservices, etc.).
   - Recognize design patterns and conventions in use.
   - Evaluate component boundaries and cohesion.

5. **Evaluate trade-offs and risks.**
   - Assess scalability, maintainability, and performance concerns.
   - Compare alternative approaches where applicable.
   - Identify technical debt or areas of risk.
   - Explicitly call out architectural risks and trade-offs in findings.

### Impact

6. **Trace dependencies and references.**
   - Find all imports, calls, and references to the affected code.
   - Identify transitive dependencies — code that depends on code that depends on the change.
   - Check for dynamic references (reflection, string-based lookups, dependency injection).

7. **Assess test coverage impact.**
   - Identify existing tests that cover the affected code.
   - Determine which tests need updating and which new tests are needed.
   - Flag areas with no test coverage that would be affected.

8. **Evaluate risk and scope.**
   - Classify the change scope (isolated, module-level, cross-module, system-wide).
   - Identify high-risk areas (shared utilities, public APIs, hot paths).
   - Flag potential breaking changes for consumers.

9. **Summarize findings.**
   - Provide a clear overview of the codebase structure (exploration) or impact assessment (impact).
   - List all affected files grouped by module or service (impact).
   - Highlight key architectural decisions and their implications (exploration).
   - Summarize risk level and recommended approach — incremental vs. big-bang (impact).
   - Make actionable recommendations where possible.

## Quality Criteria

- The report enables informed decisions about downstream work in the codebase.
- All important components and their relationships are documented.
- Architectural risks and trade-offs are explicitly called out.
- Both direct and transitive impacts are identified (impact analysis).
- Dynamic references are considered, not just static imports (impact analysis).
- Test coverage gaps in affected areas are flagged (impact analysis).
- Recommendations are specific, not generic.

## Anti-Patterns

- **Shared**: Applying subsections the brief does not invoke.
- **Surface-level scan**: Only listing directories or direct imports without understanding relationships or synthesis.
- **Over-analysis**: Spending too much time on irrelevant details instead of what matters for the task.
- **No synthesis**: Providing facts without interpretation or recommendations.
- **Prescription without context**: Recommending architectural changes without understanding constraints.
- **Shallow tracing**: Only checking direct imports, missing transitive dependencies (impact analysis).
- **Ignoring dynamic references**: Missing reflection, string-based lookups, or runtime wiring (impact analysis).
- **Scope underestimation**: Assuming a change is isolated without verifying (impact analysis).
