---
name: distinctive-frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
---

# Distinctive Frontend Design

## Overview

Guide Claude to create frontend interfaces with distinctive aesthetics and high design quality, moving beyond generic AI-generated designs. Apply specific design principles across typography, color, motion, and backgrounds to produce polished, creative outputs.

## Core Design Principles

### 1. Typography

**Primary Directive:** Choose unique, interesting fonts that enhance aesthetics and avoid generic defaults.

**Font Selection Guidelines:**
- Avoid: Inter, Roboto, Arial, system fonts, Helvetica
- Prefer: Distinctive typefaces that match the project's character
- Consider: Display fonts for headlines, reader-friendly fonts for body text
- Pairing: Use high-contrast pairs (e.g., geometric sans + humanist serif)

**Font Categories to Explore:**
- Geometric sans-serif for modern, precise aesthetics
- Humanist serif for warmth and readability
- Monospace for technical or retro contexts
- Display fonts for bold statements

**Implementation:**
```css
/* Example of distinctive typography */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&family=Crimson+Text:ital@0;1&display=swap');

:root {
  --font-display: 'Space Grotesk', sans-serif;
  --font-body: 'Crimson Text', serif;
}
```

### 2. Color & Theme

**Primary Directive:** Commit to a cohesive aesthetic with intentional color choices.

**Color Strategy:**
- Use CSS variables for consistency
- Employ dominant colors with sharp, strategic accents
- Avoid: Purple gradients on white, generic blue/gray schemes
- Draw inspiration from: IDE themes, cultural aesthetics, nature

**Theme Development:**
```css
:root {
  /* Define a cohesive palette */
  --color-primary: #2D4A3E;
  --color-accent: #E8B84B;
  --color-background: #F8F6F1;
  --color-surface: #FFFFFF;
  --color-text: #1A1A1A;
  --color-text-secondary: #5A5A5A;
}
```

**Inspiration Sources:**
- IDE themes: Nord, Dracula, Monokai, Solarized
- Cultural aesthetics: Solarpunk, Cyberpunk, Brutalism, Memphis
- Natural palettes: Desert, Ocean, Forest, Sunset

### 3. Motion & Animation

**Primary Directive:** Use animations for effects and micro-interactions, prioritizing CSS-only solutions.

**Animation Guidelines:**
- Focus on high-impact moments (page loads, state changes)
- Use staggered reveals for lists and grids
- Apply easing curves for natural movement
- Keep duration appropriate (150-300ms for micro-interactions)

**Implementation Patterns:**
```css
/* Staggered reveal */
.item {
  opacity: 0;
  animation: fadeInUp 0.5s ease forwards;
}
.item:nth-child(1) { animation-delay: 0.1s; }
.item:nth-child(2) { animation-delay: 0.2s; }
.item:nth-child(3) { animation-delay: 0.3s; }

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Smooth state transitions */
.button {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
```

### 4. Backgrounds

**Primary Directive:** Create atmosphere and depth through layered effects rather than solid colors.

**Background Techniques:**
- Layered CSS gradients for depth
- Geometric patterns and shapes
- Contextual effects (mesh gradients, noise textures)
- Subtle animations on background elements

**Implementation Examples:**
```css
/* Layered gradient background */
.hero {
  background: 
    linear-gradient(135deg, rgba(45, 74, 62, 0.9) 0%, rgba(45, 74, 62, 0.7) 100%),
    linear-gradient(45deg, #2D4A3E 25%, transparent 25%),
    linear-gradient(-45deg, #2D4A3E 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, #2D4A3E 75%),
    linear-gradient(-45deg, transparent 75%, #2D4A3E 75%);
  background-size: 100% 100%, 20px 20px, 20px 20px, 20px 20px, 20px 20px;
  background-position: 0 0, 0 0, 10px 0, 10px -10px, 0 10px;
}

/* Mesh gradient background */
.section {
  background: radial-gradient(at 40% 20%, rgba(232, 184, 75, 0.3) 0px, transparent 50%),
              radial-gradient(at 80% 80%, rgba(45, 74, 62, 0.2) 0px, transparent 50%);
}
```

## Avoiding Generic Defaults

**Explicitly Avoid These Elements:**

**Typography:**
- Inter, Roboto, Arial, system-ui, sans-serif
- Single-weight font usage
- Lack of typographic hierarchy

**Colors:**
- Purple gradients on white backgrounds
- Generic blue/gray corporate schemes
- Flat, unsaturated color palettes
- Lack of color intention or theme

**Layouts:**
- Center-aligned everything without reason
- Predictable grid patterns without variation
- Cookie-cutter component arrangements
- Lack of whitespace strategy

**Overall:**
- Designs lacking context-specific character
- One-size-fits-all approaches
- Over-reliance on component libraries' default styling

## Design Inspiration References

For theme-specific inspiration and detailed examples, see:
- `references/design-themes.md` - Detailed theme examples (Solarpunk, Cyberpunk, Brutalist, etc.)
- `references/design-patterns.md` - Common patterns for different project types

## Workflow

1. **Understand Context:** Analyze the project's purpose and target audience
2. **Choose Theme Direction:** Select or create a cohesive aesthetic approach
3. **Apply Typography:** Select distinctive fonts that match the theme
4. **Define Color System:** Create a cohesive palette using CSS variables
5. **Add Motion:** Implement purposeful animations for key interactions
6. **Craft Backgrounds:** Layer effects to create depth and atmosphere
7. **Verify Distinctiveness:** Check that the design avoids generic defaults

## Quality Checklist

Before finalizing any frontend design, verify:
- [ ] Typography uses distinctive, non-generic fonts
- [ ] Color scheme is cohesive and intentional
- [ ] CSS variables are defined for consistency
- [ ] Animations enhance key interactions
- [ ] Backgrounds create atmosphere (not just solid colors)
- [ ] Design has context-specific character
- [ ] Code is production-ready and polished
