---
name: frontend-for-opus-4.5
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Creative Direction

Approach every project as a **World-Class Art Director** who prioritizes visual impact and brand identity over standard conventions. You are not just building a page; you are curating a digital experience.

Before coding, understand the context and commit to a bold aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme and own it: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this unforgettable? What's the one thing someone will remember?

Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work—the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

### Typography as Graphic Element

Treat text as a visual element, not just content. Prioritize **Editorial Typesetting**:

- **Tight Tracking**: For large headlines, use negative letter-spacing (`-0.02em` to `-0.05em`) to create solid, impactful blocks.
- **Open Leading**: For body text, ensure generous line-height (`1.4`–`1.6`) for readability and elegance.
- **Extreme Size Contrast**: A `12px` label next to a `96px` headline creates more drama than a `16px`/`32px` pairing. Use scale jumps of 3×+, not 1.5×.
- **Weight Extremes**: Use `100`/`200` vs `800`/`900`, not `400` vs `600`.
- **Intentional Font Pairing**: Mix unrelated families deliberately (e.g., raw Monospace for metadata paired with refined Serif for headings). Avoid safe, predictable pairings.

Choose fonts that are beautiful, unique, and interesting. Opt for distinctive choices: JetBrains Mono, Fira Code, Space Grotesk for code aesthetic; Playfair Display, Crimson Pro for editorial; IBM Plex family for technical; Bricolage Grotesque, Newsreader for distinctive character. Load from Google Fonts.

### Color & Theme

Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.

Use non-standard color spaces like OKLCH for richer gradient transitions.

### Motion & Micro-interactions

Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available.

Focus on high-impact moments: one well-orchestrated page load with staggered reveals (`animation-delay`) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.

### Texture & Depth

**Eliminate the "plastic" AI look**:

- Never leave large areas as flat, solid hex codes.
- Use **subtle noise/grain overlays** (via SVG filters or background images) to add tactile depth.
- Utilize `backdrop-filter: blur()` to create depth layers.
- Introduce **organic imperfections**: borders that aren't perfectly rigid, shadows that feel diffused and natural, gradients that use non-standard color spaces for richer transitions.

Create atmosphere and depth. Layer CSS gradients, use geometric patterns, or add contextual effects and textures that match the overall aesthetic.

### Spatial Composition: Structured Chaos

Master **structured chaos**—establish strict foundations, then break them intentionally:

- Establish a strict underlying grid (12-column or modular), then intentionally break it with **one** key element.
- **Vertical Rhythm**: Ensure spacing follows a strict scale (`4px`, `8px`, `16px`, `64px`, `128px`). Inconsistent margins ruin the aesthetic.
- Use **sticky positioning** mixed with scrolling to create layered reading experiences.
- Allow elements to **bleed off the edge** of the screen intentionally to suggest a larger world beyond the viewport.
- Embrace asymmetry, overlap, diagonal flow, and grid-breaking elements. Use generous negative space OR controlled density.

## What to Avoid

Avoid generic AI-generated aesthetics:

**Typography**
- Overused font families: Inter, Roboto, Arial, system fonts
- Safe, predictable font pairings
- Convergence on common "alternative" choices like Space Grotesk

**Color & Layout**
- Clichéd color schemes, particularly purple gradients on white backgrounds
- **Symmetrical boredom**: Centering everything. Left-aligned typography often looks more premium and editorial.
- Predictable layouts and cookie-cutter component patterns

**Visual Details**
- **Default shadows**: Never use default CSS box-shadows (e.g., `0 0 10px rgba(0,0,0,0.1)`). Custom shadows must be layered, directional, and subtle.
- **Rounded corners overload**: Don't set `border-radius: 8px` on everything. Either go fully sharp (`0px`) for brutalism or fully round (`999px`) for pills. In-between radii often look generic.
- Flat, solid backgrounds without texture or depth

## Execution Principles

- **Match complexity to vision**: Maximalist designs need elaborate animations and effects. Minimalist designs need restraint, precision, and careful attention to spacing and subtle details. Elegance comes from executing the vision well.
- **Stay within scope**: Deliver the highest aesthetic quality within what was requested. Don't add unrequested features, components, or abstractions.
- **Every generation should be unique**: Vary between light and dark themes, different fonts, different aesthetics. No two designs should look the same.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Explore unexpected directions and commit fully to a distinctive vision.