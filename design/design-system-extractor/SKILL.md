---
name: design-system-extractor
description: "Extracts tokens, typography, spacing, component states, assets, layout, responsive rules, and interactions from a UI reference."
---

# Design System Extractor

Turn a visual reference into implementable constraints.

## Workflow

1. Identify the authoritative reference: Figma, screenshot, concept, codebase,
   Storybook, or existing design system.
2. Extract color tokens, type scale, spacing, radii, borders, shadows, icons,
   assets, layout grid, and responsive behavior.
3. Map repeated elements to components and variants.
4. Record intentional deviations and unknowns.
5. Feed the result into `ui-build`, `figma-to-code`, or `playwright-visual-qa`.

## Output

- tokens
- typography
- components and variants
- layout/responsive rules
- asset inventory
- interaction states
- unresolved gaps
