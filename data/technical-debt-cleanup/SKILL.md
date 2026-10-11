---
name: technical-debt-cleanup
description: Identify, prioritize, and safely clean unnecessary complexity in a project while preserving behavior. Use when Codex needs to review or clean duplicate files, unused components, dead code, commented-out code, confusing naming, outdated utilities, unused dependencies, stale comments, broken documentation, inconsistent folder structure, repeated helpers, old feature flags, unused assets, leftover abandoned-feature code, large mixed-responsibility files, or multiple patterns for the same task before feature work, deployment, handover, or maintenance.
---

# Technical Debt Cleanup

Use this skill when the goal is project health: reduce unnecessary complexity, remove obvious clutter, and make future changes easier without accidentally changing working behavior.

## Core Rule

Verify before deleting and preserve behavior by default. Technical debt cleanup is not a rewrite; it should be small, evidence-based, reviewable, and focused on maintainability value.

## Workflow

1. Understand cleanup goal:
   - maintainability, pre-feature cleanup, handover, deployment readiness, post-rush cleanup, legacy stabilization, active project cleanup, deadline pressure, and behavior preservation expectations
2. Inspect project structure:
   - duplicate folders, old feature folders, unused modules, mixed app layers, deprecated directories, stale tests, committed build artifacts, temp folders, backups, and archives
3. Identify duplicate code:
   - components, API clients, utilities, validation, error handling, permission checks, formatting, database queries, test helpers, config, and styling patterns
4. Identify dead code:
   - unused functions, components, routes, endpoints, services, imports, constants, types, assets, scripts, test utilities, feature flags, and commented-out blocks
5. Verify references before removal:
   - imports, route registration, dynamic imports, API usage, tests, build config, docs, scripts, generated code, runtime conventions, and external references
6. Identify confusing naming:
   - vague local variables, helpers, files, components, routes, and modules; prefer private/internal renames before public interface changes
7. Identify inconsistent patterns:
   - API clients, validation, error formats, forms, date formatting, auth storage, state management, folder naming, styling, and casing conventions
8. Identify outdated utilities:
   - replaced helpers, old API wrappers, auth/date/validation/env helpers, duplicate constants, legacy polyfills, and unused service wrappers
9. Identify unused or risky dependencies:
   - unreferenced packages, duplicate libraries, heavy packages for small tasks, deprecated packages, wrong dependency category, multiple package managers, and unused lockfiles
10. Identify stale comments and documentation:
   - inaccurate README commands, old API docs, missing env vars, outdated deployment notes, stale diagrams, completed task markers, and comments describing removed behavior
11. Identify risky technical debt:
   - duplicated permission checks, inconsistent auth logic, repeated raw SQL, duplicated payment/status rules, hardcoded environment values, missing tests, unclear data ownership, public admin routes, and weak external-service error handling
12. Categorize cleanup items by risk:
   - safe, low-risk, medium-risk, high-risk, and do-not-touch-without-tests
13. Prioritize by value:
   - reduce future confusion, remove duplicated business logic, improve safety, improve onboarding, reduce bundle/build cost, remove dead paths, standardize important patterns, or improve testability
14. Decide cleanup timing:
   - before feature work when debt blocks the feature or would cause duplication; after feature work when cleanup is cosmetic or creates merge risk
15. Perform safe cleanup only when requested:
   - remove unused imports/local variables, delete clearly stale comments, rename local variables, extract small helpers, consolidate duplicate constants, remove unreferenced assets after search, and update stale comments/docs
16. Preserve behavior:
   - API contracts, UI behavior, business rules, database schema, permissions, validation, error messages, navigation, build/deploy behavior, and integrations
17. Escalate risky cleanup:
   - recommend tests or approval before dependency removal, route cleanup, API client consolidation, auth/permission cleanup, database query consolidation, payment logic cleanup, or migration cleanup
18. Run available checks:
   - inspect scripts first, then run relevant lint, tests, build, type checks, format checks, or config validation
19. Document cleanup decisions:
   - debt found, cleaned items, removed files, standardized patterns, behavior preservation, checks, remaining debt, and follow-up
20. Produce either a technical debt report or cleanup summary.

Read `references/technical-debt-checklist.md` for debt categories, reference checks, risk levels, cleanup timing, verification commands, and the final report format.

## Non-Negotiable Rules

- Do not delete code without checking whether it is referenced.
- Do not remove strange legacy code without checking whether it contains business rules.
- Do not change behavior during cleanup unless explicitly requested.
- Do not rename public interfaces casually.
- Do not remove dependencies without verifying usage through code, config, scripts, and build references.
- Do not mix cleanup with unrelated feature work.
- Do not turn cleanup into a rewrite.
- Do not remove tests, validation, authorization, or error handling to simplify code.
- Do not over-abstract simple code.
- Do not prioritize cosmetic cleanup over urgent business work.
- Keep cleanup small, safe, reviewable, and documented.
- Run tests/checks when available, or state the verification limitation.

## Output Contract

When using this skill, provide:

1. Cleanup scope and goal.
2. Areas inspected.
3. Technical debt found with risk level and impact.
4. Safe cleanup items.
5. Risky cleanup items needing tests or approval.
6. Recommended timing before/after feature work.
7. Cleanup performed, if any.
8. Behavior preservation statement.
9. Files changed.
10. Tests/checks run and results.
11. Remaining technical debt.
12. Recommended next steps.
