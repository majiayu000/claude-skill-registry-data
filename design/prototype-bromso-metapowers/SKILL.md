---
description: Build the component in Figma using the chosen design approach from ideation
---

# Prototype

Build "$ARGUMENTS" in Figma as a component with all variants and states specified in the component contract.

## Prerequisites

Read `.metapowers/design/$ARGUMENTS/02-define.md` (required — hard gate enforced by hook).
Read `.metapowers/design/$ARGUMENTS/03-ideate.md`. If this file does not exist, tell the user:

> Phase 3 (Ideate) has not been completed for "$ARGUMENTS". Run `/design:ideate $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip the ideation check and log to `.metapowers/design/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context files:**
   - Read `.metapowers/design/$ARGUMENTS/02-define.md` for the component contract (props, variants, states, tokens)
   - Read `.metapowers/design/$ARGUMENTS/03-ideate.md` for the chosen design approach (if exists)
   - Read `plugins/design/shared/component-contract-template.md` for reference

2. **Read the design system** via MCP tools:
   - Call `figma_get_variables` to get current token values for fills, spacing, typography
   - Call `figma_get_design_system_summary` to understand the system structure

3. **Build the base component:**
   - Call `figma_create_component` with the component name and base dimensions
   - Call `figma_set_auto_layout` to establish layout structure
   - Call `figma_create_text` for text elements
   - Call `figma_create_shape` for visual elements
   - Call `figma_apply_styles` to apply token-based fills, strokes, and effects

4. **Build variant components** for each variant dimension:
   - Create a component for each variant value
   - Call `figma_arrange_component_set` to combine as a variant set

5. **Apply states** to each variant:
   - Modify fills, opacity, and effects for hover, focus, active, disabled, error, loading states

6. **Verify the prototype:**
   - Call `figma_export_image` to capture a visual of the built component
   - Compare against the component contract requirements

7. **Write the artifact** to `.metapowers/design/$ARGUMENTS/04-prototype.md` with implementation notes

## Output

The Figma component built on the canvas and notes written to `.metapowers/design/$ARGUMENTS/04-prototype.md`. Present to the user:
- Component node ID for reference
- Visual export of the component
- Any deviations from the contract and why
- Notes for the Test phase
