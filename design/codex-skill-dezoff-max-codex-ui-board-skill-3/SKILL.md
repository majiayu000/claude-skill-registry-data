---
name: soft-neumorphic-dual-theme-board
description: Apply or adapt a dual-theme soft-neumorphic UI board for dashboards, workspaces, settings panels, admin tools, and design-system previews. Use when Codex should build or restyle interface work in a tactile soft-neumorphic style with both light and dark themes, shared semantic tokens, large radii, raised surfaces, inset fields, restrained accent states, and a complete preview board covering foundations, controls, navigation, data display, and feedback.
---

# Soft Neumorphic Dual Theme Board

Use this skill to build or restyle UI in a soft-neumorphic style that supports both light and dark themes. Preserve the tactile material logic across themes: same-tone surfaces, large radii, raised cards and buttons, inset fields, and restrained accent usage.

## Workflow

1. Read `references/usage.md` first.
2. Load only the files needed for the task:
   - `references/SoftNeumorphicDualThemeBoard.tokens.json` for semantic tokens and light/dark values
   - `references/SoftNeumorphicDualThemeBoard.css` for CSS variables and component semantics
   - `references/tailwind.preset.cjs` when the host project uses Tailwind
   - `references/preview.html` when you need the complete system board
3. Decide whether the task needs:
   - token mapping only
   - component restyling
   - a full preview board or design-system page
4. Keep both themes aligned through tokens rather than duplicating component logic.
5. Verify that depth, input treatment, and button behavior feel coherent in both themes.

## Non-Negotiables

- Keep surfaces close in tone to the page background.
- Create hierarchy through soft shadows, inset surfaces, spacing, and radii rather than harsh borders.
- Use large radii consistently.
- Keep buttons raised by default and fields inset by default.
- Use accent color selectively for active, primary, or highlighted states.
- Do not mix this style with glassmorphism, flat border-heavy cards, or hard industrial panels.

## Component Rules

### Foundations

- Use base, raised, inset, and pressed surfaces as a unified system.
- Treat light and dark as the same design language with different tokens.

### Controls

- Buttons, inputs, selection controls, and sliders must all feel tactile and physically related.
- Focus and error should be clear without breaking the soft-neumorphic material.

### Navigation

- Tabs, breadcrumbs, pagination, and steppers should remain compact and quiet.
- Active state should rely on accent and surface behavior rather than heavy outlines.

### Data Display

- Cards, list items, badges, and compact table surfaces should remain readable and soft in both themes.

### Feedback

- Modal, toast, progress, alert, skeleton, and empty states must keep the same shadow and radius logic as the rest of the system.

## Deliverables

- When asked for a theme or kit, provide both light and dark support unless the user explicitly asks for only one theme.
- When asked for a page, keep the underlying dual-theme token architecture.
- Prefer shareable preview pages that work without a build step when practical.
