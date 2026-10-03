---
name: liquid-glass-aurora-board
description: Apply or adapt a dual-theme liquid glass UI board for premium dashboards, workspace launchers, settings surfaces, design-system previews, and glossy interface concepts. Use when Codex should build or restyle interface work with frosted translucent panels, aurora glow accents, pill controls, circular glass actions, blurred color blooms, and a polished light-plus-dark material system.
---

# Liquid Glass Aurora Board

Use this skill to build or restyle interfaces in a liquid-glass style with soft translucency, aurora glow, and premium control surfaces. Keep the material luminous and layered, but still structured enough for real product UI.

## Workflow

1. Read `references/usage.md` first.
2. Load only the files needed for the task:
   - `references/LiquidGlassAuroraBoard.tokens.json` for semantic token values
   - `references/LiquidGlassAuroraBoard.css` for glass material, glow, and component behavior
   - `references/tailwind.preset.cjs` when the host project uses Tailwind
   - `references/preview.html` when you need the full board, theme switching, or screenshot-safe capture mode
3. Decide whether the task needs:
   - token remapping
   - component restyling
   - a full preview board or landing-style control surface
4. Keep both themes on the same material logic instead of redesigning dark mode from scratch.
5. Verify that blur, border brightness, and accent glow support hierarchy instead of washing out content.

## Non-Negotiables

- Keep the interface translucent and layered, not flat or border-heavy.
- Use purple and cyan as the main accent pair unless the task explicitly asks for a different palette.
- Maintain large radii, pill controls, circular actions, and bright edge highlights.
- Reserve the strongest glow for primary buttons, active controls, and meaningful hotspots.
- Keep the page background atmospheric with blurred color blooms rather than hard gradients or noisy textures.
- Do not mix this style with industrial admin chrome, hard neumorphism, or dense data-table-first layouts.

## Component Rules

### Foundations

- Panels should feel like frosted glass sheets floating over a soft background.
- Borders should be thin, bright, and slightly more visible than in classic glassmorphism.

### Controls

- Buttons should read as luminous capsules, not flat pills.
- Inputs, segmented tabs, toggles, and chips should share the same glass material family.
- Circular plus buttons and orb actions are part of the language, not decorative extras.

### Layout

- Prefer elegant board compositions, launcher layouts, premium settings surfaces, or polished feature cards.
- Use negative space and blur blooms to create depth before adding more components.

### Motion

- Motion should be slow, floaty, and glow-aware.
- Provide a capture-safe mode when generating screenshots or static previews.

## Deliverables

- Provide both light and dark themes unless the user explicitly asks for one theme only.
- Prefer shareable preview pages that work without a build step when practical.
- Keep the result usable as both inspiration board and frontend handoff reference.
