---
name: frontend-design
description: "Create distinctive, production-grade frontend interfaces."
allowed-tools:
  - bash
  - write_file
  - read_file
enabled: true
related-skills: []
license: MIT
author: Adapted from deer-flow (Bytedance, MIT)
---

# Frontend Design

## Overview

Create distinctive, production-grade frontend interfaces that avoid generic
"AI slop" aesthetics. Implement real working code with exceptional attention
to aesthetic details and creative choices.

## Output Requirements

**MANDATORY**: The entry HTML file MUST be named `index.html`.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos,
  retro-futuristic, organic/natural, luxury/refined, playful/toy-like,
  editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel,
  industrial/utilitarian, etc.
- **Constraints**: Technical requirements (framework, performance, accessibility)
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing
  someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision.
Bold maximalism and refined minimalism both work — the key is intentionality.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

### Typography
- Choose fonts that are beautiful, unique, and interesting
- Avoid generic fonts (Arial, Inter, Roboto, system fonts)
- Pair a distinctive display font with a refined body font
- Use Google Fonts or local font files

### Color & Theme
- Commit to a cohesive aesthetic
- Use CSS variables for consistency
- Dominant colors with sharp accents outperform timid, evenly-distributed palettes
- Avoid cliched purple gradients on white backgrounds

### Motion
- Use animations for effects and micro-interactions
- Prioritize CSS-only solutions for HTML
- Focus on high-impact moments: one well-orchestrated page load with staggered
  reveals creates more delight than scattered micro-interactions
- Use scroll-triggering and hover states that surprise

### Spatial Composition
- Unexpected layouts. Asymmetry. Overlap. Diagonal flow
- Grid-breaking elements
- Generous negative space OR controlled density

### Backgrounds & Visual Details
- Create atmosphere and depth rather than defaulting to solid colors
- Add contextual effects and textures: gradient meshes, noise textures,
  geometric patterns, layered transparencies, dramatic shadows, decorative
  borders, custom cursors, grain overlays

**NEVER use generic AI-generated aesthetics:**
- Overused font families (Inter, Roboto, Arial)
- Cliched color schemes (purple gradients on white)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

**Match implementation complexity to the aesthetic vision.** Maximalist designs
need elaborate code. Minimalist designs need restraint, precision, and careful
attention to spacing, typography, and subtle details.

## Workflow

1. Understand the user's frontend requirements
2. Choose an aesthetic direction (tone, fonts, colors, motion)
3. Generate the HTML/CSS/JS code:
   ```
   write_file("index.html", "<full HTML content>")
   write_file("styles.css", "<full CSS content>")
   write_file("script.js", "<full JS content>")
   ```
4. Present the file path so the user can open it in a browser

## Pitfalls

- **Generic aesthetics**: the #1 failure mode. If it looks like every other
  AI-generated page, redo it with a bolder direction.
- **Font convergence**: don't use the same fonts across every project. Vary.
- **Over-animation**: too many animations overwhelm. One well-orchestrated
  moment beats ten scattered micro-interactions.
- **No dark mode**: consider whether the design should support dark mode.
- **Accessibility**: bold aesthetics must not sacrifice readability. Check
  contrast ratios, font sizes, focus states.
