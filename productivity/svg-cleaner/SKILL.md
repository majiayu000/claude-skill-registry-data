---
name: svg-cleaner
description: Clean SVG files for UI usage. Use when asked to remove SVG comments, simplify SVG markup, or make icon color follow CSS via currentColor.
disable-model-invocation: true
allowed-tools: Read Edit MultiEdit Write Grep
model: sonnet
---

# SVG Cleaner

Use this skill when the user wants an SVG cleaned up for application use, especially for icons that should inherit color from CSS.

Arguments:

- `$ARGUMENTS` may contain one or more SVG file paths, or a short instruction about the target SVGs.
- If no arguments are provided, inspect the current task context and ask for the SVG path only if it cannot be inferred safely.

Goals:

1. Remove SVG comments such as `<!-- ... -->`.
2. Make icon color follow CSS with `currentColor` where it is safe to do so.
3. Preserve rendering unless the user explicitly asks for a more aggressive cleanup.

Workflow:

1. Read the SVG file or files first.
2. Remove comments and obvious editor noise only when it is safe.
3. Inspect how color is applied:
   - If the SVG is effectively single-color, convert hardcoded `fill` and/or `stroke` colors to `currentColor`.
   - Keep `fill="none"` and `stroke="none"` unchanged.
   - Preserve `url(#...)` paints, gradients, masks, clip paths, filters, and other structural features.
   - Preserve multi-color artwork unless the user explicitly asks to flatten it into a single CSS-controlled color.
4. Prefer the smallest safe change:
   - If one shared color is used throughout, replacing repeated hardcoded colors with `currentColor` is preferred.
   - If a root-level `fill` or `stroke` can safely express the same result, that is acceptable.
   - Update inline `style` attributes when they are the only place color is defined.
5. Keep important SVG behavior intact:
   - Preserve `viewBox`.
   - Preserve geometry, transforms, `fill-rule`, `clip-rule`, and opacity-related attributes unless cleanup requires a targeted rewrite.
6. After editing, quickly re-read the result and check that no hardcoded color remains on elements that should now inherit from CSS.

Decision rules:

- Treat monochrome icons as good candidates for `currentColor`.
- Treat logos, illustrations, flags, gradients, and intentionally multi-color assets as not safe for automatic color unification.
- If safety is unclear, make the conservative cleanup only: remove comments and report why color conversion was skipped.

Output:

- Briefly state which SVG files were updated.
- State whether `currentColor` conversion was applied or intentionally skipped.
- Call out any remaining manual follow-up only if the SVG structure makes safe automation ambiguous.
