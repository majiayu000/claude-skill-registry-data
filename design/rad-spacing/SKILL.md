---
name: rad-spacing
description: Use for Figma layout work when creating new screens, refactoring spacing, standardizing hierarchy, or spacing nested components. Apply hierarchical spacing using the Gestalt principle of proximity so outer containers get proportionally more spacing than inner elements, using 8px/4px increments from the file's library variables.
---

# Rad Spacing

## When to use
- You're creating new screens or layouts and need intentional, consistent spacing that communicates visual hierarchy.
- You're refactoring spacing in an existing Figma design to improve readability and grouping.
- You're building components that will nest inside larger containers and need spacing that scales with depth.
- You're standardizing spacing across a file to align with the Gestalt principle of proximity — related items close together, separate groups further apart.

## Instructions
1. Identify the nesting depth of the design. Map out the hierarchy levels from outermost to innermost (e.g., page → section → card → card content → inline elements).
2. Check the Figma file's library for existing spacing variables:
   - Look for number variables in 4px or 8px increments (e.g., `spacing/4`, `spacing/8`, `spacing/16`, `spacing/24`).
   - If the library already has spacing variables, use them. Adapt to whatever naming convention is in place.
3. If no spacing variables exist, create semantic number variables using this default convention:
   - `spacing/xs` → 4px
   - `spacing/sm` → 8px
   - `spacing/md` → 12px
   - `spacing/lg` → 16px
   - `spacing/xl` → 24px
   - `spacing/2xl` → 32px
   - `spacing/3xl` → 48px
   - Adapt the naming if the library already has a pattern for other variable types.
4. Calculate spacing per hierarchy level using the ~40% rule:
   - Each parent level gets approximately 1.4× the spacing of its child level.
   - Snap the result to the nearest 8px increment. If the 0.6 ratio (child = parent × 0.6) lands closer to a 4px increment than an 8px increment, use the 4px value instead.
   - Work from the innermost elements outward, or from a known base value (commonly 8px for the tightest grouping).
5. Apply spacing using the `use_figma` MCP tool:
   - Use **padding** on auto-layout frames for container-level spacing (pages, sections, cards).
   - Use **gap** (itemSpacing) on auto-layout frames for spacing between sibling elements.
   - Bind spacing values to the library's number variables wherever possible.
6. Validate the visual hierarchy:
   - Outer groups should feel clearly separated from one another.
   - Inner items within a group should feel cohesive and related.
   - Check that the spacing progression is perceptible at each level — if two adjacent levels look the same, increase the ratio or adjust the snap.
7. Summarize what was applied:
   - List the spacing values used at each hierarchy level.
   - Note any new variables created and any exceptions or deviations from the 40% rule.

## Examples

**Input request:** "Create a settings page with a sidebar and content area containing form sections."

**Hierarchy and spacing calculation (base = 8px, working outward):**

| Level | Element | Spacing | Calculation |
|-------|---------|---------|-------------|
| 4 (innermost) | Form field labels and inputs | 8px gap | Base value |
| 3 | Fields within a form section | 12px gap | 8 × 1.4 = 11.2 → snaps to 12px (4px increment) |
| 2 | Form sections within content area | 16px gap | 12 × 1.4 = 16.8 → snaps to 16px |
| 1 | Content area padding | 24px padding | 16 × 1.4 = 22.4 → snaps to 24px |
| 0 (outermost) | Page padding | 32px padding | 24 × 1.4 = 33.6 → snaps to 32px |

**Result:** A settings page where the tightest spacing (8px) groups labels with their inputs, slightly wider spacing (12px) separates fields, wider still (16px) distinguishes form sections, and the largest spacing (24–32px) frames the overall page and content area. The eye naturally parses the groupings without explicit dividers.

## Common edge cases
- **No library variables exist:** Create the semantic spacing variables as described in step 3. Confirm the naming convention with the designer or adapt to any existing variable patterns in the file.
- **Deeply nested structures (4+ levels):** The 40% rule may push the outermost spacing very large. Cap the maximum at a reasonable value (e.g., 48px or 64px) and compress the inner levels to fit, maintaining the relative progression.
- **Hitting the 4px minimum:** If the innermost level calculates below 4px, floor it at 4px and recalculate outward from there.
- **Ambiguous nesting depth:** When it's unclear whether elements are siblings or parent-child, default to treating visually distinct groups as separate hierarchy levels.
- **Mixed component reuse:** A component used at different nesting depths may need spacing overrides via instance properties. Apply the spacing appropriate to its context, not its definition.
- **Existing designs with inconsistent spacing:** Audit the current values first, then remap systematically from the innermost level outward rather than adjusting individual values in isolation.
