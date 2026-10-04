---
id: css.selectors.has-content-aware-layout
name: CSS Has Content Aware Layout
description: "Use CSS :has() and :not(:has()) to adapt layout to child content without JavaScript, Angular bindings, or class toggles."
stack:
  - CSS
category: selectors
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - css has
  - content aware layout
  - quantity query
---

# CSS Has Content Aware Layout

Use this skill when CSS can react to the DOM structure on its own.

## Purpose

Create layout rules that respond to child presence or quantity without JavaScript.

## When to Use

Use this skill when layout depends on visible DOM content and the condition is purely visual.

## Do

- keep selectors structural and readable
- use `:has()` as an enhancement
- keep Angular out of purely visual decisions

## Do Not

- move business logic into CSS
- depend on fragile third-party DOM
- hide accessibility behavior inside selectors

## Review Checklist

- [ ] The default layout works without `:has()`.
- [ ] The condition is purely visual.
- [ ] The selector is scoped and readable.
- [ ] Browser support was checked.

## Expected Output

Return:

1. The layout condition being modeled.
2. The CSS selector strategy.
3. The fallback/default layout.
4. Browser support or testing risks.
