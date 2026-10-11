---
name: refactor-without-behavior-change
description: Improve code structure while preserving current application behavior. Use when Codex needs to clean messy, duplicated, long, hard-to-read, hard-to-maintain, unclear, deeply nested, or overly coupled code across frontend, backend, API, database access, utilities, tests, configuration, or documentation-adjacent code without changing user-facing behavior, API contracts, database schema, business rules, validation, permissions, UI layout, text, navigation, state, side effects, error handling, calculations, status transitions, or external integration behavior.
---

# Refactor Without Behavior Change

Use this skill when the goal is cleaner code, not new behavior.

## Core Rule

A refactor changes how code is organized or expressed, not what the application does. Preserve public behavior and treat any desired behavior change as a separate follow-up unless the user explicitly requests it.

## Workflow

1. Understand current behavior:
   - feature/module, inputs, outputs, user behavior, API behavior, database behavior, business rules, tests, side effects, and edge cases
2. Define behavior that must not change:
   - endpoint paths/methods, request payloads, response structures, validation, permissions, UI text/layout, loading/error/empty states, database writes, calculations, navigation, state, sorting/filtering, and external integrations
3. Identify safe refactor targets:
   - duplicate code, long functions/components, repeated constants, repeated conditionals, unclear names, mixed UI/business logic, repeated API logic, error parsing, formatting, nested branches, dead code, unused imports, and inconsistent file organization
4. Avoid behavior-changing work:
   - do not change business rules, API contracts, database schema, permission rules, validation rules, UI layout, text, navigation, status transitions, error messages, data filters, sorting, pricing, calculations, or integration behavior
5. Keep changes small and reviewable:
   - refactor one module or flow at a time and avoid unrelated cleanup
6. Preserve public interfaces:
   - exported functions, component props, endpoint contracts, model fields, service signatures, utility behavior, events, route names, shared types, and environment variable names
7. Extract helpers when useful:
   - formatting, validation predicates, status mapping, payload builders, response parsers, filters, sorters, summaries, and permission checks
8. Extract components, hooks, services, or utilities only when they improve clarity or remove real duplication.
9. Simplify conditionals with guard clauses, named booleans, predicate helpers, lookup maps, or clearer branching.
10. Remove duplication only after confirming inputs, outputs, edge cases, error behavior, and permissions are truly identical.
11. Improve names carefully:
   - prefer local/private renames; avoid public interface renames unless necessary and approved
12. Improve file organization only when it follows project conventions and keeps the change focused.
13. Preserve error handling:
   - caught errors, user messages, fallback behavior, logging, retries, validation mapping, and unauthorized behavior
14. Preserve state and side effects:
   - API calls, database writes, cache invalidation, navigation, toasts, storage updates, auth tokens, event tracking, file uploads, WebSocket events, jobs, and notifications
15. Add or recommend tests before risky refactors when behavior is not covered.
16. Run relevant checks discovered from project scripts or docs.
17. Compare before/after behavior through tests, build/lint, manual checks, API shapes, UI state review, public exports, business rules, and changed-file scope.
18. Document behavior-changing ideas as follow-up recommendations instead of silently including them.
19. Summarize target, original problem, behavior preservation, changes made, public interfaces, files, checks, risks, and follow-up recommendations.

Read `references/refactor-safety-checklist.md` for behavior preservation boundaries, safe extraction guidance, side-effect checks, verification options, and the final report format.

## Non-Negotiable Rules

- Do not change behavior unless explicitly requested.
- Do not mix feature work with refactoring.
- Do not change API contracts.
- Do not change database schema.
- Do not change business rules.
- Do not change permission behavior.
- Do not redesign UI unless requested.
- Do not rename public interfaces unless necessary and approved.
- Do not remove code unless it is clearly unused or safely replaced.
- Do not merge similar code unless behavior is truly identical.
- Do not introduce new dependencies unless approved.
- Do not make massive unrelated changes in one refactor.
- Do not skip verification when tests or checks are available.
- Do not claim behavior was preserved without explaining how it was checked.

## Output Contract

When using this skill, provide:

1. Refactor target and original maintainability issue.
2. Behavior preservation statement.
3. Specific behavior preserved.
4. Refactor changes made.
5. Public interfaces preserved.
6. Files changed.
7. Tests/checks or manual verification.
8. Risks and limitations.
9. Follow-up recommendations for behavior-changing improvements.
