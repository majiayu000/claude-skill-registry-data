---
name: ztx4-design-to-code
description: "Deep implementation master for Design-to-Code Pipeline (offline) with 16 targeted Codex skills, code, tests and no MCP. Additive to all existing Perfect_AI versions."
---

# Design-to-Code Pipeline (offline)

Convert permitted local Figma exports/reference assets to structured, accessible, maintainable UI without MCP.

## Mandatory sequence
1. Require a local export, screenshot, token file or SVG with known rights and source.
2. Normalize layers, bounds, parent-child containment, auto-layout, token aliases and typography.
3. Derive semantic components and flex/grid constraints rather than absolute positioned pixel replica.
4. Generate framework-specific code with logical properties and available assets only.
5. Compare screenshots by viewport; validate interactions not represented in static files separately.

## Skill routing
Choose only technique files needed for this project from `DEEP-IMPLEMENTATION-v2/references/design-to-code.md`. Never indiscriminately load all 300+ skills into context.

## Runbook
Inputs: local Figma JSON or exported images/SVG, tokens and rights; no MCP.

Implementation: normalize local layers, reconstruct auto layout as Flex/Grid, map semantics and tokens, generate TSX/CSS with responsive/RTL constraints.

Tests: parse invalid exports safely, no executable unsafe SVG, no absolute-layout dependence, screenshot comparison and keyboard affordances.

## Acceptance gates
1. No MCP required; only local files are read.
2. Exported code uses semantic layout and responds beyond design artboard size.
3. Sanitize imported SVG and verify licensing.

## Runnable assets
`extensions/DEEP-IMPLEMENTATION-v2/examples` and `tools` (installed main package). See `RUNBOOK-FA.md`.

## Sources
- [tailwind](https://tailwindcss.com/docs/theme)
- [bootstrap](https://getbootstrap.com/docs/5.3/customize/color-modes/)
- [storybook](https://storybook.js.org/docs)
