---
description: Research user needs, existing patterns, and accessibility requirements before designing a component
---

# Empathize

Research the problem space for "$ARGUMENTS" before any design work begins. Gather user needs, existing patterns, accessibility requirements, and contextual constraints.

## Prerequisites

None — this is the first phase.

## Process

1. **Read the design system** via MCP tools:
   - Call `figma_get_design_system` to fetch existing components, tokens, and styles
   - Call `figma_get_components` to list all published components
   - Identify components that overlap with or relate to "$ARGUMENTS"

2. **Inspect existing components** (if found):
   - Call `figma_get_component` and `figma_get_component_for_dev` for related components
   - Call `figma_export_image` to get visual references
   - Document what exists, what works well, and what's missing

3. **Review accessibility requirements:**
   - Read `plugins/design/shared/wcag-criteria.md` for applicable WCAG criteria
   - Call `figma_a11y_contrast_check` on any existing color pairs used in related components
   - Note specific accessibility requirements for this component type

4. **Synthesize findings** into a research brief covering:
   - User needs and common use cases for this component type
   - Existing patterns found in the design system
   - Accessibility requirements and considerations
   - Contextual constraints (design tokens available, conventions established)
   - Gaps and opportunities

5. **Write the artifact** to `.metapowers/design/$ARGUMENTS/01-empathize.md`

## Output

The research brief written to `.metapowers/design/$ARGUMENTS/01-empathize.md`. Present a summary to the user highlighting:
- Key user needs identified
- Existing components found (if any)
- Critical accessibility requirements
- Recommended approach for the Define phase
