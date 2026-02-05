---
name: svelte-game-visual-design
description: Graphical and UI/UX design improvements for SvelteKit browser games, including layout, typography, color systems, HUD design, visual polish, and dynamic effects. Use when asked to redesign or enhance a Svelte game's visuals, to improve readability or aesthetics, to add motion/animation polish, or to audit/iterate on UI using Playwright MCP snapshots.
---

# Svelte Game Visual Design

## Scope

- Focus on visual polish for SvelteKit games: layout, typography, color, spacing, component styling, HUD, menus, and effects.
- Use Playwright MCP to inspect live UI, compare states, and verify changes.
- Prefer small, targeted changes that improve clarity and vibe without breaking game logic.

## Workflow

1. Clarify the visual goal and constraints.
   - Ask for the desired mood (arcade, neon, retro, minimal), device targets, and any brand or palette constraints.
   - Identify critical game states to evaluate (title, gameplay, pause, game over).

2. Audit the current UI with Playwright MCP.
   - Open the game route and capture snapshots for key states.
   - Note readability, contrast, alignment, spacing, and motion issues.
   - Record concrete UI elements to improve (HUD, score, buttons, canvas frame, background).

3. Plan visual system updates.
   - Define CSS variables for colors, spacing, radii, shadows, and typography.
   - Pick one primary and one accent color; ensure contrast for gameplay legibility.
   - Choose a display font for headers and a readable UI font for numbers and labels.

4. Implement UI improvements in Svelte.
   - Update layout containers and UI components first, then supporting styles.
   - Use Svelte transitions for panels and menus; use CSS keyframes for subtle motion.
   - Keep the canvas unobstructed; use overlays or side panels when needed.

5. Add dynamic visual effects carefully.
   - Prefer lightweight effects: glow pulses, parallax layers, scanlines, gradient drift.
   - Drive effects from game state or time using requestAnimationFrame or tweened stores.
   - Avoid heavy DOM counts; keep effects GPU-friendly (transform/opacity).

6. Validate with Playwright MCP.
   - Re-snapshot the same states to verify improvements and regressions.
   - Check mobile and desktop breakpoints.

## Playwright MCP checklist

- Navigate to the game route and wait for it to render.
- Capture accessibility snapshots for the main states.
- Use before/after snapshots to confirm fixes.

## Implementation tips

- Use CSS variables at `:root` or a top-level layout for consistent theming.
- Use `prefers-reduced-motion` to disable heavier animations.
- Keep game canvas size fixed; adapt UI around it.
- If performance drops, reduce shadow blur and animation duration.

## References

- Use `references/ui-patterns.md` for layout, HUD, and typography patterns.
- Use `references/effects-patterns.md` for safe, lightweight motion and effects.
- Use `references/playwright-audit.md` for a repeatable UI review routine.
- Use `references/free-assets.md` to source relevant free assets and verify licensing.

## Assets

- Use `assets/ui-shell/VisualShell.svelte` as a drop-in layout shell with HUD, panel, and visual tokens.
