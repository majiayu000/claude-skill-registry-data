---
name: neo-glow-control-board
description: Apply or adapt a dual-theme neo-glow control board for UI kits, design-system previews, settings surfaces, admin panels, control rooms, and dense operational interfaces. Use when Codex should build or restyle interface work with bright white or dark control surfaces, compact neumorphic cards, vertical icon rails, blue/cyan halo accents, glowing active states, luminous toggles, and a board focused on control states, inputs, and specification details.
---

# Neo Glow Control Board

Use this skill to build or restyle interfaces in a luminous control-board style derived from soft-neumorphic surfaces plus bright blue glow states. Keep the system dense, technical, tactile, and state-driven.

## Workflow

1. Read `references/usage.md` first.
2. Load only the files needed for the task:
   - `references/NeoGlowControlBoard.tokens.json` for semantic token values
   - `references/NeoGlowControlBoard.css` for component and glow behavior
   - `references/tailwind.preset.cjs` when the host project uses Tailwind
   - `references/preview.html` when you need the full board or screenshot-safe capture behavior
3. Decide whether the task needs:
   - token remapping
   - component restyling
   - a full control-board or design-system preview
4. Keep active states luminous and neutral states quiet.
5. Verify that glow is concentrated on meaningful controls instead of flooding the whole screen.

## Non-Negotiables

- Keep the base interface calm and pale or dark-neutral; reserve blue/cyan glow for active and highlighted states.
- Use glow as an intentional signal, not background decoration.
- Maintain compact, control-heavy layout with clear component groupings.
- Keep rails, cards, inputs, toggles, and chips within the same material family.
- Do not mix this style with colorful dashboard mosaics, glassmorphism, or heavy gradient backgrounds.

## Component Rules

### Foundations

- Surfaces should feel soft, compact, and slightly technical.
- Border radius should stay generous but not overly playful.

### Controls

- Buttons, toggles, sliders, selects, and focused inputs should carry the strongest glow behavior.
- Focus rings should remain visible and deliberate.

### Rails and Navigation

- Side icon rails should feel like control strips, not consumer app sidebars.
- Active rail items may glow more strongly than secondary items.

### Specs and States

- The board should document behavior as much as appearance.
- Include checklists, state chips, and grouped control samples when useful.

## Deliverables

- Provide both light and dark themes unless the user explicitly asks for one theme only.
- Prefer shareable preview pages with screenshot-safe capture mode.
- Keep the resulting kit suitable for handoff to frontend developers or designers.
