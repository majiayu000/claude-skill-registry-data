---
name: typescript-monorepo-clean-code
description: Apply clean code principles to TypeScript monorepos. Use when a repo needs package boundaries, import discipline, shared type ownership, error handling conventions, module sizing, naming, refactoring, or clean implementation review.
---

# TypeScript Monorepo Clean Code

## Purpose

Turn broad clean-code preferences into concrete TypeScript and monorepo rules agents can follow and reviewers can enforce.

## Inspect First

- workspace packages, app/package boundaries, `tsconfig` references, aliases, exports, lint rules, architecture docs, and golden patterns
- source files with repeated patterns, oversized modules, cross-package imports, and duplicated type definitions

## Procedure

1. Define package responsibilities.
   - Apps compose features and runtime wiring.
   - API packages own contracts, routers, validation, and service orchestration.
   - DB packages own schema, migrations, seed data, and typed persistence.
   - UI packages own reusable primitives and shared composition pieces.

2. Set TypeScript rules.
   - Prefer explicit domain types at package boundaries.
   - Keep validation schemas close to ingress points and exported when reused.
   - Avoid broad `any`, ambient globals, hidden side effects, and circular imports.
   - Keep error handling typed and observable.

3. Keep modules small enough to review.
   - Split by responsibility, not by arbitrary layers.
   - Extract only when duplication or complexity is real.
   - Keep generated code and hand-written code clearly separated.

4. Document local rules.
   - Create or update `docs/quality/typescript-clean-code.md` from `assets/templates/typescript-clean-code.md.tmpl`.
   - Feed canonical examples into `golden-pattern-extractor`.
   - Feed boundary risks into `architecture-boundary-enforcer`.

## Validation

- Run lint, typecheck, tests, and boundary checks.
- Confirm examples cite real local files.
- Confirm new rules do not contradict existing architecture docs.

## Completion Criteria

- Agents have concrete TypeScript monorepo rules for imports, types, errors, modules, and ownership.
- Clean-code guidance is repo-specific enough to review against.
- Follow-up refactors are separated from feature work unless they block the task.

