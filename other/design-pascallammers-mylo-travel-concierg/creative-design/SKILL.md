---
name: creative-design
description: Create distinctive, memorable UI for landing pages, portfolios, marketing sites, and one-off creative work. Use when the user explicitly wants something "distinctive", "creative", "memorable", or "unique" - NOT for standard app components where consistency matters.
---

# Creative Design

> Adapted from [Anthropic's frontend-design skill](https://github.com/anthropics/skills/tree/main/skills/frontend-design)

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Use for **creative one-offs**, not standard app components.

## When to Use This vs. Standard Patterns

| Use `creative-design` | Use standard patterns |
|-----------------------|-----------------------|
| Landing pages | App dashboards |
| Portfolio pieces | CRUD interfaces |
| Marketing sites | Admin panels |
| One-off demos | Reusable components |
| "Make it memorable" | "Make it consistent" |

If working on a Next.js app with shadcn/ui, prefer theme tokens and consistent patterns unless explicitly asked for something distinctive.

## Design Thinking

Before coding, commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this solve? Who uses it?
- **Tone**: Pick an extreme:
  - Brutally minimal
  - Maximalist chaos
  - Retro-futuristic
  - Organic/natural
  - Luxury/refined
  - Playful/toy-like
  - Editorial/magazine
  - Brutalist/raw
  - Art deco/geometric
  - Soft/pastel
  - Industrial/utilitarian
- **Differentiation**: What's the ONE thing someone will remember?

**CRITICAL**: Choose a clear direction and execute with precision. Bold maximalism and refined minimalism both work - the key is intentionality.

## Aesthetics Guidelines

### Typography

Choose fonts that are beautiful, unique, and interesting. Avoid:
- Arial, Inter, Roboto, system fonts
- Space Grotesk (overused in AI outputs)

Instead: pair a distinctive display font with a refined body font. Character over safety.

### Color & Theme

- Commit to a cohesive aesthetic
- Use CSS variables for consistency
- Dominant colors with sharp accents > timid, evenly-distributed palettes
- AVOID: purple gradients on white (cliched AI aesthetic)

### Motion

Focus on high-impact moments:
- One well-orchestrated page load with staggered reveals (`animation-delay`)
- Scroll-triggered effects
- Hover states that surprise

Prioritize CSS-only for HTML. Use Motion library for React when available.

### Spatial Composition

- Unexpected layouts
- Asymmetry, overlap, diagonal flow
- Grid-breaking elements
- Generous negative space OR controlled density

### Backgrounds & Texture

Create atmosphere rather than solid colors:
- Gradient meshes
- Noise textures
- Geometric patterns
- Layered transparencies
- Dramatic shadows
- Grain overlays

## Anti-Patterns

NEVER produce:
- Generic font families (Inter, Roboto, Arial)
- Purple gradients on white
- Predictable layouts
- Cookie-cutter components
- Same design twice

## Implementation

Match complexity to vision:
- Maximalist = elaborate animations, effects, layers
- Minimalist = restraint, precision, spacing, typography

Always produce working code (HTML/CSS/JS, React, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with clear aesthetic point-of-view
