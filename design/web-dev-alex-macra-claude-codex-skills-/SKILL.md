---
name: web-dev
description: "TypeScript and Python web development: React, Vue or Svelte UI, Node and Python backends, accessibility audits, CI, deploy and rollback. Use for components, forms, API routes, migrations, WCAG, Dockerfiles, GitHub Actions."
license: MIT
metadata:
  display-name: "Web Dev"
  version: "2.0"
  platforms: "claude-code codex"
  tags: "web frontend backend accessibility ci deploy typescript python"
---

# Web dev

Load the reference that matches the work; a change spanning layers loads each one it touches.

| Work | Reference |
|---|---|
| Components, pages, hooks, state, styling, performance | `references/frontend.md` |
| Routes, middleware, data, async, logging, CI, deploy, rollback | `references/backend.md` |
| Accessibility audit of a page or flow against WCAG 2.2 AA | `references/a11y.md` |

## Rules for every layer

- **Types are not negotiable.** TypeScript `strict`, Python annotated and checked (`mypy --strict` or `pyright`). No `any`, `@ts-ignore`, `# type: ignore` or `as unknown as T` to silence a checker; fix the type.
- **Validate at every boundary** (request, response, storage, URL, env) with a schema (`zod`, `pydantic`); inferred types come from the schema, not the reverse.
- **Match the project.** Use its styling system, framework data layer, package manager and conventions; do not introduce a second one.
- **Reuse before writing.** Search for the existing component, hook, util or route first.
- **Idempotent, loud, reproducible.** Scripts fail on any unhandled error, run twice with the same result, and work from a clean checkout.
- **Measure before optimizing.** Profile, Lighthouse, `EXPLAIN ANALYZE`; never cargo-cult memoization or indexes.

## Hand-offs

- Auth, tokens, sessions, uploads, SSRF: `security-review` before wiring them.
- Writing or fixing tests: `qa-automation`. Browser, HTTP or CLI journeys live in its `references/e2e.md`.
- Launching the app to prove a change: `see-it-live`.
- Design and boundary critique of the result: `architect-review`.

## Done means

Type-check, lint and tests pass; the feature was exercised in the running app on the golden path and the error states; for services, the endpoint was hit with a real payload and the response matches the schema; for migrations, forward and rollback ran against a real database copy; for UI, axe or Lighthouse ran on the changed pages. Type-check passing is not feature-correctness.
