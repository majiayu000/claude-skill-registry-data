---
name: dual-theme-spec-board
description: Apply or adapt a complete dual-theme UI specification board for product interfaces. Use when Codex should build or restyle dashboard, admin, workspace, settings, or system UI with both light and dark themes, shared semantic tokens, structured component states, and a full preview board covering foundations, controls, navigation, data display, and feedback patterns.
---

# Dual Theme Spec Board

Use this skill to create or restyle a product interface using the bundled light and dark theme board. Keep one semantic component system across both themes and change visual output through tokens rather than component rewrites.

## Workflow

1. Read `references/usage.md` first.
2. Load only the files needed for the task:
   - `references/DualThemeSpecBoard.tokens.json` for semantic tokens and light/dark values
   - `references/DualThemeSpecBoard.css` for component rules and CSS variable mapping
   - `references/tailwind.preset.cjs` when the host project uses Tailwind
   - `references/preview.html` when you need the full board layout and state matrix
3. Decide whether the task needs:
   - only token mapping
   - component restyling
   - a full-page board or design system preview
4. Preserve shared structure across both themes.
5. Verify that all interactive states remain visually coherent in both light and dark modes.

## Non-Negotiables

- Use semantic tokens instead of hardcoded colors whenever possible.
- Keep the same component semantics in light and dark themes.
- Express hierarchy with elevation, borders, inset states, spacing, and restrained accent usage.
- Use the board as a complete system:
  foundations, controls, navigation, data display, and feedback should feel related.
- Do not mix radically different visual languages such as glassmorphism, flat bootstrap cards, or neon cyber UI into this system.

## Component Rules

### Foundations

- Surfaces should define clear depth levels: base, raised, inset, and pressed.
- Use accent color mainly for active, primary, or highlighted states.
- Keep spacing and radii consistent across modules.

### Controls

- Buttons, fields, switches, radios, and sliders must all belong to the same material family.
- Inputs should visibly communicate default, focus, and error states.
- Disabled states should lose contrast, not change design language.

### Navigation

- Tabs, breadcrumbs, pagination, and steppers should feel compact and operational.
- Active state should use accent and elevation rather than large layout changes.

### Data Display

- Cards, lists, badges, table headers, and tooltips should remain legible in both themes.
- Reuse spacing and token logic from foundations and controls.

### Feedback

- Modal, toast, alert, progress, skeleton, and empty states must follow the same surface rules.
- Error and warning states should be obvious but not louder than the whole interface.

## Deliverables

- If the user asks for a UI kit or template, provide both light and dark theme support.
- If the user asks for a single screen, still preserve the dual-theme token architecture.
- When possible, keep the preview or example page shareable without a build step.
