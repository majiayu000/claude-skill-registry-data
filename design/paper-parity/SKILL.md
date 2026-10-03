---
name: paper-parity
description: Use when comparing or recreating this repo's UI in Paper MCP and fixing parity issues against the live rendered site.
---

# paper-parity

Use this skill whenever working with Paper MCP to recreate, compare, or audit UI from this repo.

## Goal

Match the live rendered website in Paper as closely as possible. The live DOM is the source of truth for visual output. Source files are secondary references for ownership, structure, and intent.

## Workflow

1. Inspect the live rendered page first.
2. Use `agent-browser eval` to capture `getComputedStyle()` for the actual visible element.
3. Check the parent chain and rendered wrappers before inferring where a style comes from.
4. Use `outerHTML` when needed to confirm final DOM structure.
5. Recreate the final rendered values in Paper, not guessed source-level values.
6. Use `*.astro`, `*.tsx`, and `*.ts` files only after the DOM check to clarify ownership and structure.
7. After each meaningful Paper change, take a screenshot and compare again.

## DOM Rules

- Do not infer selector paths from Astro or React source alone when layout or styling depends on the final DOM.
- Parent-driven selectors, arbitrary variants, descendant combinators, `astro-island` wrappers, slots, and scoped styles can all change where a style is actually applied.
- If a style appears to belong to a component, verify whether it is really coming from a parent wrapper in the rendered DOM.

## Color Rules

- For Tailwind utilities, use the computed color from the browser, not the utility name.
- Utilities like `bg-*-100` may resolve to generated tints and not the base theme token.
- Do not collapse a utility name to a guessed token value without checking computed styles first.

## Verification

- Before declaring parity, confirm spacing, typography, alignment, clipping, and color against the live render.
- Screenshots show what is wrong; computed styles explain why.
