---
name: frontend-change
description: Build or refine Next.js pages, features, forms, client state, BFF routes or shared UI in frontend/. Use when implementing, fixing or refactoring frontend behavior or interaction after its scope is known. Backend-only work and read-only reviews (review-change) belong elsewhere.
---

# frontend-change

Read `frontend/AGENTS.md` (the frontend constitution), the affected contract,
a matching feature and relevant tests. Use the profile for active capabilities
or shared contracts. Read PRODUCT.md and DESIGN.md before building or
restyling UI. Functional work uses one OpenSpec change and incremental
[TDD](../tdd/SKILL.md); reuse an already defined scope.

## Architecture references

`frontend/AGENTS.md` owns the binding rules. Read only the relevant sections of
`docs/content/docs/conceptos/arquitectura-frontend.md` (paths there are relative
to `frontend/`):

| Change | Sections |
| --- | --- |
| Feature placement, facades or import boundaries | §§3–4 |
| Server/client boundary, Server Functions, proxy, BFF, session or errors | §§5–7 |
| Query/cache scope, client state, forms, i18n, themes or shell | §§8–11 |
| Test location and browser coverage | §12 |

Use the matching installed feature for code shape. Load the installed Next.js
documentation for an unresolved framework API question, not for routine edits.

## Build mode

1. Pick one vertical interaction and write its failing test under
   `tests/{api,models,components}/features/<feature>/`, `tests/unit/` or
   `tests/end-to-end/` (layout in the architecture doc).
2. Implement it, checking zod/forms, loading/empty/success/error/recovery
   states, i18n and themes.
3. Run it to green, then repeat for the next interaction.

Load a library only for its question: vercel-react-best-practices for measured performance, vercel-composition-patterns
for composition, typescript-advanced-types for a difficult type contract,
impeccable for visual design with the project's tokens/components,
tailwind-design-system for token or primitive plumbing, and
[webapp-testing](../webapp-testing/SKILL.md) (driving playwright-cli or the
Playwright MCP) to observe behavior in a browser.

## Refinement mode

1. Take a concrete finding or objective and preserve behavior.
2. Improve composition, state, hierarchy, copy or accessibility in a small step.
3. Check keyboard, focus, labels, narrow viewport and error recovery in the
   browser, then renew affected evidence.

## Verify and hand off

`just frontend new-feature <name>` scaffolds a feature and refuses existing ones.
Run `just frontend verify` for functional work, `just spec-check <id>`, and the
browser/BFF tests that `docs/content/docs/equipo/verificacion.md` selects. Pass results to
[validate-change](../validate-change/SKILL.md).

## Gotchas

- A shared contract needs a real browser -> BFF -> API journey; a screenshot or
  mocked backend does not prove integration.
- Do not load every frontend library by default.
- Performance improvements require measurement.
- New behavior discovered while refining returns to define-change.
