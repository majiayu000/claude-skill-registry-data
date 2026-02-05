---
name: totalaud-brand
description: Use when building UI for totalaud.io - enforces brand colours, typography, and calm aesthetic
---

# totalaud.io Brand Guidelines

**IMPORTANT**: totalaud.io is SEPARATE from Total Audio Promo (totalaudiopromo.com). Do not mix these brands.

When building frontend for totalaud.io, ALWAYS use these brand constraints:

## Brand Identity

- **Brand Name**: totalaud.io (lowercase, always)
- **Product**: Calm Creative Workspace for Independent Artists
- **Tone**: Calm, minimal, artist-first, experimental
- **Status**: Experimental project (sandbox for new ideas)

## Colour Palette

```css
:root {
  /* Core colours - Dark theme PRIMARY */
  --background: #0F1113;        /* Matte Black */
  --foreground: #FAFAFA;        /* Light Grey/White */
  --accent: #3AA9BE;            /* Slate Cyan */
  --border: rgba(255,255,255,0.1);

  /* Semantic */
  --muted: #71717A;
  --success: #22C55E;
  --warning: #F59E0B;
  --error: #EF4444;
}
```

## Typography

- **Primary**: Geist Sans / Inter (clean, modern)
- **Monospace**: Geist Mono / JetBrains Mono
- **Line Height**: 1.4–1.6
- **Max Width**: 70ch for reading

## Motion Tokens

```typescript
const motion = {
  fast: '120ms cubic-bezier(0.22, 1, 0.36, 1)',    // Micro feedback
  normal: '240ms cubic-bezier(0.22, 1, 0.36, 1)',  // Pane transitions
  slow: '400ms ease-in-out',                        // Calm fades
}
```

## Aesthetic Direction

**totalaud.io is CALM, not chaotic.**

- Minimal, not overwhelming
- Soft motion, not jarring
- Dark theme by default
- Generous whitespace
- No visual clutter
- Subtle glow effects on accent colour

## Four Core Modes

1. **Ideas Mode** — capture & organise creative/marketing ideas
2. **Scout Mode** — discover real opportunities (playlists, blogs, radio, press)
3. **Timeline Mode** — plan release actions visually
4. **Pitch Mode** — craft narratives and bios with AI coaching

## Visual Elements

- **Subtle glows**: `text-shadow: 0 0 40px rgba(58, 169, 190, 0.15)`
- **Soft borders**: `rgba(255,255,255,0.1)`
- **Rounded corners**: Consistent border-radius
- **Depth**: Subtle layering, not flat

## What to AVOID

- ❌ Bright/loud colours
- ❌ Complex animations
- ❌ Cluttered layouts
- ❌ Generic AI aesthetics
- ❌ Purple gradients
- ❌ Aggressive CTAs
- ❌ Light/white backgrounds (that's Total Audio Promo's style)
- ❌ Blue accent colour (that's Total Audio Promo's accent)

## What to EMBRACE

- ✅ Calm, dark backgrounds (#0F1113)
- ✅ Slate cyan accents (#3AA9BE) - sparingly
- ✅ Soft shadows and glows
- ✅ Clean typography
- ✅ Mobile-first responsive
- ✅ Framer Motion for animations
- ✅ Generous negative space
- ✅ Progressive disclosure

## Brand Comparison

| Aspect | totalaud.io | Total Audio Promo |
|--------|-------------|-------------------|
| Theme | Dark (#0F1113) | Light (#FFFFFF) |
| Accent | Slate Cyan (#3AA9BE) | Blue (#3B82F6) |
| Feel | Calm, experimental | Professional, SaaS |
| Tone | Artist-first, creative | Founder-led, credible |
| Purpose | Creative workspace | Promotion tools |
