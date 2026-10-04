---
name: thalarch-typescript
description: >
  Project-aware TypeScript/JavaScript engineering for browser, Node.js, full-stack, libraries,
  and tooling. Use for TS/JS source, framework code, async behavior, typing, package/toolchain
  work, testing, performance, or TypeScript-specific refactoring.
---

# Thalarch TypeScript

Discover the actual runtime, package manager, compiler, framework, module system, and quality
tools. Do not assume Node, React, Next.js, npm, ESM, or strict TypeScript.

## Preflight

Inspect:

- `package.json` scripts and engines;
- lockfile/package manager;
- `tsconfig*` and module resolution;
- framework/build tool versions;
- lint/format/type/test setup;
- browser vs server vs edge/runtime boundaries.

Use repository scripts instead of inventing equivalent commands.

## Type discipline

- Preserve strictness already configured; do not weaken the compiler to make code pass.
- Prefer narrowing from `unknown` to spreading `any` across a boundary.
- Model discriminated unions for real variant states.
- Avoid type assertions that merely silence the compiler; prove the invariant or validate the boundary.
- Keep runtime validation separate from compile-time typing.
- Do not generate duplicate DTO/types when an existing schema/source of truth can produce or define them.

## Async/runtime behavior

Review:

- promise ownership and missing awaits;
- cancellation/`AbortSignal` when the stack supports it;
- race conditions from stale async results;
- unhandled rejections;
- browser/server resource lifetime;
- event listener/subscription cleanup;
- concurrency fan-out and rate limits.

Do not introduce a new state-management or async library to solve a local problem without
clear evidence it is required.

## Frontend/framework overlay

When React/Vue/Svelte/Angular/another framework is present, follow its current project version
and existing patterns.

For React-family code, verify hook lifecycles, effect dependencies, stale closures, state
ownership, server/client boundaries, key stability, accessibility, and unnecessary rerenders.
Do not add `useMemo`/`useCallback` everywhere as ritual optimization.

Combine visual work with `thalarch-web-design`, `thalarch-browser-qa`, and design review.

## Backend/API overlay

For Node/server code, combine with `thalarch-api`, `thalarch-security`, and `thalarch-data-sql`
when relevant. Validate input at external boundaries and preserve error/HTTP semantics.

## Dependencies

Use the existing package manager and lockfile. Confirm package exports and version-specific APIs
before importing them. Avoid installing a package for functionality already covered by the
runtime/framework or a small local implementation.

## Testing and verification

Use configured tools such as Vitest/Jest/Node test/Playwright/Cypress only when actually present.
Typical proof layers are typecheck → focused test → lint → build → browser/runtime evidence as
required by the acceptance contract.

A TypeScript compile does not prove browser interaction or server integration.
