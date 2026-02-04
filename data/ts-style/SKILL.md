---
name: ts-style
description: TypeScript style standards for AIRBot reviewers
license: MIT
---

## Mission
- Enforce readable, maintainable TypeScript that matches AIRBot conventions.
- Prioritize issues that break builds, lose type safety, or harm long-term maintainability.

## Quick Triage
- Block PRs for TypeScript compile errors, missing exports, or obvious runtime crashes.
- Flag high-churn files with risky refactors unless tests or migration notes exist.
- Praise meaningful improvements to typing, structure, or docs.

## Style Heuristics
- Prefer explicit `type` aliases or interfaces when exporting shared shapes; avoid anonymous object literals.
- Require strict null handling: guard `undefined` and `null`, avoid non-null assertions unless justified.
- Ensure `async` functions propagate errors or handle them locally; reject swallowed `catch` blocks.
- Favor pure utilities in `src/*` modules; move orchestration or side effects to `src/index.ts`.
- Keep imports sorted by module path and remove unused imports, enums, and helper functions.
- Encourage `const` over `let` unless mutation is necessary; avoid `var`.
- Recommend descriptive naming: PascalCase for types, camelCase for variables, kebab-case for files.

## Type Safety
- Reject usage of `any` or `unknown` without runtime guards; suggest narrower generics or refinements.
- Require exhaustive `switch`/`if` chains on discriminated unions; enforce `never` exhaustiveness checks where practical.
- Verify third-party library calls have appropriate typings, especially for Octokit and Claude SDK interactions.
- Check that new utility functions declare return types explicitly when exported.

## Documentation & Comments
- Accept concise comments that explain non-obvious control flow; remove comments that restate code.
- Encourage README/CLAUDE rubric updates alongside behavior changes.

## Tooling Tips
- Use `Read` to inspect files, `Grep` for patterns like `any`, and `Glob` for locating related modules or tests.
