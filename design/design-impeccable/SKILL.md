---
name: design-impeccable
description: "Anti-pattern detector and design rules for AI coding agents. Catches the specific mistakes AI makes when generating UI: gray text on color, nested cards, broken buttons, missing states. Use before shipping any frontend."
version: 1.0.0
metadata:
  hermes:
    tags: [Design, Frontend, Audit]
  custodian:
    band: L0
    cost_usd: 0.00
    configured: true
---

# Impeccable

Design rules for AI coding agents. Catches the specific tells that mark output as AI-generated.

## The 23 commands (overview)

| Command | What it does |
|---------|--------------|
| `craft` | Full shape-then-build flow with visual iteration |
| `init` | One-time setup: gather design context, write PRODUCT.md and DESIGN.md |
| `document` | Generate root DESIGN.md from existing project code |
| `extract` | Pull reusable components and tokens into the design system |
| `shape` | Plan UX/UI before writing code |
| `critique` | UX design review: hierarchy, clarity, emotional resonance |
| `audit` | Run technical quality checks (a11y, performance, responsive) |
| `polish` | Final pass, design system alignment, and shipping readiness |
| `bolder` | Amplify boring designs |
| `quieter` | Tone down overly bold designs |
| `distill` | Strip to essence |
| `harden` | Error handling, i18n, text overflow, edge cases |
| `onboard` | First-run flows, empty states, activation paths |
| `animate` | Add purposeful motion |
| `colorize` | Introduce strategic color |
| `typeset` | Fix font choices, hierarchy, sizing |
| `layout` | Fix layout, spacing, visual rhythm |
| `delight` | Add moments of joy |
| `overdrive` | Add technically extraordinary effects |
| `clarify` | Improve unclear UX copy |
| `adapt` | Adapt for different devices |
| `optimize` | Performance improvements |
| `live` | Visual variant mode: iterate on elements in the browser |

## 44 deterministic detector rules

These are the most common AI-generated UI mistakes. Check for each before shipping.

### Typography tells

1. **Inter for everything** — replace with a font that has character (Geist, Outfit, Satoshi, Cabinet Grotesk)
2. **Only 400 and 700 weights** — add 500 and 600 for hierarchy
3. **Headlines too small** — display text should feel heavy
4. **No letter-spacing on large text** — use negative tracking
5. **System font fallbacks visible** — explicitly set the font stack
6. **Mixed serif/sans usage** — pick one family for body, one for display
7. **Numbers in proportional font in tables** — use tabular figures
8. **All-caps everything** — sentence case or italics, not all-caps

### Color tells

9. **Pure `#000` or `#fff`** — use off-black (`#0a0a0a`) and off-white (`#fafafa`)
10. **Two accent colors** — pick one, remove the rest
11. **Purple-to-blue gradient** — the most common AI gradient tell
12. **Saturated accent at 100%** — desaturate to 70-80%
13. **Mixing warm and cool grays** — pick one gray family, tint consistently
14. **Gray text on colored backgrounds** — low contrast fails WCAG
15. **Random dark sections in light pages** — commit to one mode
16. **Identical hex values across components** — should be design tokens, not magic numbers

### Layout tells

17. **Three equal card columns** — the #1 AI layout tell
18. **Centered everything** — break symmetry with offsets
19. **`height: 100vh`** — use `min-height: 100dvh`
20. **No max-width on body** — content stretches edge-to-edge
21. **Cards forced to equal height** — allow variable heights
22. **Uniform border-radius** — vary the radius by element type
23. **No overlap or layering** — flat, flat, flat
24. **Top and bottom padding always equal** — adjust optically
25. **Left sidebar on every dashboard** — try top nav, floating menu, collapsible
26. **Dense layouts with no whitespace** — let it breathe

### Interactivity tells

27. **No hover states** — add background shift or transform
28. **No active/pressed feedback** — add `scale(0.98)` on click
29. **Zero-duration transitions** — use 200-300ms
30. **No focus ring** — accessibility blocker, fix with `:focus-visible`
31. **Generic spinners** — use skeleton loaders that match layout shape
32. **No empty states** — design a "getting started" view
33. **`window.alert()` for errors** — use inline error messages
34. **Buttons linking to `#`** — link to real destinations or disable
35. **No current-page indicator in nav** — style the active link differently
36. **Instant scroll on anchor click** — add `scroll-behavior: smooth`
37. **Animating `top`/`left`/`width`/`height`** — use `transform` and `opacity`

### Content tells

38. **"John Doe" or "Jane Smith"** — use diverse, realistic names
39. **Round numbers everywhere** — use messy data: 47.2%, $99.00
40. **Lorem ipsum** — use realistic placeholder content
41. **Buzzword overload** — "synergy", "leverage", "transformative"
42. **Inconsistent date formats** — pick one (ISO 8601 recommended)

### Code quality tells

43. **Magic numbers in CSS** — use design tokens / CSS variables
44. **No `:focus-visible` for keyboard nav** — accessibility requirement

## Anti-patterns (don't do these)

- Don't use overused fonts (Arial, Inter, system defaults)
- Don't use gray text on colored backgrounds
- Don't use pure black/gray (always tint)
- Don't wrap everything in cards or nest cards inside cards
- Don't use bounce/elastic easing (feels dated)
- Don't animate non-transform properties
- Don't use `window.alert()` for inline errors
- Don't link to `#` in production code
- Don't use `Lorem ipsum` in real product copy

## Usage pattern

```
1. Run /impeccable init  — set up PRODUCT.md and DESIGN.md
2. Build the feature
3. Run /impeccable audit  — check this list
4. Run /impeccable polish — final pass
5. Ship
```

## Installation (for reference)

This skill ships inside the `custodian-kernel` package under
`custodian/bundled_skills/design-impeccable/SKILL.md`.

Your AI agent (Hermes, Claude Code, Codex) will load this file when working on frontend tasks. No additional install steps required.
