---
name: illustrated
description: Custom illustration-driven, character art, storybook feel.
---
# Illustrated
## Mission
Build interfaces where custom illustrations are the primary visual language — every screen tells a story through hand-crafted or vector artwork that defines the brand's personality.
## Brand
### 🎨 Colors
- `#ffd166` — Sunny yellow (primary)
- `#06d6a0` — Mint green (secondary)
- `#118ab2` — Ocean blue (accent)
- `#073b4c` — Deep navy (text)
- `#f8f9fa` — Warm white (background)
- `#ef476f` — Poppy red (CTA)
### 🔤 Typography
- **Heading:** Fredoka One (rounded, playful) or Baloo 2
- **Body:** Nunito or Quicksand (rounded, friendly)
- **Scale:** xs: 0.75rem, sm: 0.875rem, base: 1rem, lg: 1.125rem, xl: 1.25rem, 2xl: 1.5rem, 3xl: 2rem
### 📐 Spacing
- Generous spacing: 1.5rem–3rem gaps
- Section padding: 5rem vertical, 2rem horizontal
- Card gaps: 2rem
- Border radius: 16–24px (rounded, friendly)
### 🧩 Components
- **Buttons:** Rounded pill shape (border-radius: 50px), bold colors, playful hover bounces (subtle scale)
- **Cards:** Rounded with illustration peeking over the top edge, soft shadow, light border
- **Nav:** Minimal, illustration in logo, playful icons, sticky with soft background
- **Hero:** Full illustration as hero background, characters interacting with the headline text
- **Footer:** Curved SVG divider, illustrated footer character waving goodbye
### ♿ Accessibility
- All illustrations must have descriptive alt text (not just "illustration")
- Illustration-only content must have a text equivalent
- 4.5:1 contrast on all text, even when overlapping illustrations
- Focus states: bold outline that contrasts with illustration colors
- Motion in illustrations respects prefers-reduced-motion
### ✍️ Writing Tone
Friendly, warm, story-driven. Use metaphor and playful language. Address the user directly. Short, engaging sentences. Avoid jargon. Sentence case labels.
## Do / Don't
### ✅ Do
- Create a consistent illustration style guide (line weight, colors, character design)
- Use illustrations to explain concepts, not just decorate
- Design illustrations that work at multiple sizes (detail scales down gracefully)
- Pair each illustration with supporting text — never illustration-only communication
- Use SVG for illustrations to keep them crisp and lightweight
### ❌ Don't
- Mix illustration styles (flat vector + 3D + watercolor) in the same product
- Use illustrations as the only way to convey critical information
- Place text directly over detailed illustration areas — use dedicated text-safe zones
- Use auto-playing illustrated animations that can't be paused
- Ship illustrations without alt text or accessible descriptions
## Quality Gates
- [ ] All illustrations have descriptive alt text
- [ ] Illustration style guide exists and is followed consistently
- [ ] SVGs are optimized (no unnecessary nodes, < 50KB per illustration)
- [ ] No critical information is conveyed through illustration alone
- [ ] Text overlapping illustrations passes 4.5:1 contrast
- [ ] Illustrations render correctly at all breakpoints (320px–2560px)