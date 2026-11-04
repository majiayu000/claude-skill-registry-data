---
name: testing
description: >
  Use this skill when writing, reviewing, or deciding where to place tests
  in the Next.js frontend package. Covers which project (unit / integration /
  storybook) to use for a given scenario, what NOT to duplicate across
  projects, and file placement conventions for this package.
---

# Testing skill

See `guidelines.md` for the full decision rules and examples.

## Quick reference

| Project     | Pattern                    | Environment | Purpose                                        |
|-------------|----------------------------|-------------|------------------------------------------------|
| unit        | `*.unit.test.ts(x)`        | happy-dom   | Pure logic: utils, hooks, data transforms      |
| integration | `*.integration.test.tsx`   | happy-dom   | User flows across components with MSW          |
| storybook   | `*.stories.tsx`            | browser     | Visual states, a11y, interaction per component |

## One-line decision rule

> "If this test fails, do I tell the **designer** or the **engineer**?"
> - Designer → **storybook**
> - Engineer → **unit** or **integration**

## File placement in this package

- Unit / integration tests → co-located with the component:
  `src/components/Button/Button.unit.test.tsx`
- Stories → co-located with the component:
  `src/components/Button/Button.stories.tsx`
- MSW handlers → `src/mocks/handlers/`
- Storybook config → `apps/nextjs/.storybook/`
- `vitest.config.ts` → monorepo root (not in this package)

For the full decision guide, do-not-duplicate rules, and code examples,
read `guidelines.md` in this directory.
