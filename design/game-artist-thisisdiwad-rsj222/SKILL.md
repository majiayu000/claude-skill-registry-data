---
name: game-artist
description: "Visual style, rendering techniques, and animation for web games. Invoked by game-orchestra when code works but needs visual polish. Covers CSS/canvas art, color palettes, animation, responsive design, and game juice."
---

<!-- EXPECTED GATES: 5 -->

# Game Artist

Guides visual design and polish for web games — no external assets required.

## When Invoked

By game-orchestra when gameplay works but needs visual improvement.

## STEP 1 — Review Current State

Examine the game's current visual state. Identify what exists and what needs work.

All visuals are generated in code. No image files, no CDN dependencies.

### Techniques Available
- **Emoji sprites:** Use emoji characters as game objects
- **CSS gradients:** Backgrounds, skies, ground, water
- **Canvas drawing:** Circles, rectangles, paths for custom shapes
- **CSS shapes:** Borders, transforms, clip-path for UI elements
- **Procedural art:** Algorithmically generated patterns, terrain, particles

### GATE 1 OUTPUT
> STEP 1 COMPLETE: Current visual state: [description]. Needs work: [list elements needing visual improvement].

## STEP 2 — Color Palette

Pick 4-6 colors that work together:
- **Background:** 1 color (usually dark or soft)
- **Primary:** 1 color (player, important items)
- **Secondary:** 1 color (environment, UI)
- **Accent:** 1-2 colors (score, highlights, effects)
- **Danger/success:** Red/green for feedback

### GATE 2 OUTPUT
> STEP 2 COMPLETE: Palette — Background: [hex], Primary: [hex], Secondary: [hex], Accent: [hex], Danger: [hex], Success: [hex].

## STEP 3 — Apply Visual Style

Apply styling to all game elements. Use CSS and/or canvas techniques as appropriate.

### Typography
- Sans-serif fonts for readability (Nunito, Inter, system-ui)
- Score/HUD: Bold, large, high contrast
- Instructions: Clear, short, positioned near relevant elements
- Avoid text walls — icons and visual cues preferred

### GATE 3 OUTPUT
> STEP 3 COMPLETE: Elements styled: [list each element and technique used].

## STEP 4 — Add Animation and Game Juice

### CSS Animations (DOM Games)
```css
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
.item { animation: bounce 0.5s ease-in-out; }
```

### Canvas Animation
- Use `requestAnimationFrame` (see game-patterns.md)
- Easing functions: ease-in-out for natural motion
- Interpolation: lerp for smooth transitions

### Game Juice
Small details that make games feel alive:

- **Screen shake:** Brief camera offset on impact/collision
- **Particles:** Small dots/shapes on explosions, collections, completions
- **Scale bounce:** Items briefly grow/shrink when collected
- **Glow effects:** CSS box-shadow or canvas radial gradients
- **Trail effects:** Fading copies of moving objects
- **Sound cues:** (future) Audio feedback on key actions

### GATE 4 OUTPUT
> STEP 4 COMPLETE: Animations added: [list animations with techniques — e.g., "bounce on collect (CSS keyframes)", "particle burst (canvas)"].

## STEP 5 — Responsive Design

- Game canvas/container: `max-width: 100vw; max-height: 100vh`
- Touch targets: minimum 48px x 48px
- Fullscreen: Toggle with `f` key, allow `Esc` to exit
- Aspect ratio: Maintain with `aspect-ratio` CSS or JS calculation

Test at 375px, 768px, and 1024px widths.

### GATE 5 OUTPUT
> STEP 5 COMPLETE: Breakpoints tested: 375px [pass/fail], 768px [pass/fail], 1024px [pass/fail]. Touch targets: [confirmed/fixed]. Aspect ratio: [maintained/fixed].
