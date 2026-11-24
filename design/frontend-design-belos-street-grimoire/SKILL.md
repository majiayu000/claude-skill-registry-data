---
name: frontend-design
title: Frontend Design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when building web components, pages, artifacts, or applications (websites, landing pages, dashboards, React/Vue components, HTML/CSS layouts). Generates creative, polished code and UI design that avoids generic aesthetics. Complete terms in LICENSE.txt.
tags: frontend, ui-design, css, html, layout, typography, color-theory, animation, accessibility, design-system
---

# Frontend Design

> A guide to creating distinctive, production-grade frontend interfaces with exceptional aesthetic quality and attention to detail.

## Preferences

- Prefer distinctive, characterful typography over generic fonts
- Commit to cohesive aesthetic direction (bold minimalism OR refined maximalism)
- Use CSS variables for theming and consistency
- Prioritize CSS-only solutions where possible
- Focus on high-impact moments with orchestrated animations
- Create atmosphere with backgrounds and visual details

## Core

| Topic | Description | Reference |
|-------|-------------|-----------|
| Design Systems | Component libraries, design tokens, theming, design principles | [design-systems](references/design-systems.md) |
| Typography | Font selection, scale, line-height, readability, vertical rhythm | [typography](references/typography.md) |
| Color Theory | Color palettes, contrast, semantic colors, dark mode | [color-theory](references/color-theory.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Layout & Spacing | Grid, flexbox, spacing scales, responsive breakpoints | [layout-spacing](references/layout-spacing.md) |
| Accessibility | ARIA, keyboard navigation, screen readers, WCAG guidelines | [accessibility](references/accessibility.md) |
| Motion & Animation | Transitions, animations, micro-interactions, performance | [motion-animation](references/motion-animation.md) |

## Design Thinking

Before coding, understand the context and commit to a bold aesthetic direction:

### Purpose
- What problem does this interface solve?
- Who is the target audience?

### Tone
Pick an extreme and commit fully:
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

### Constraints
- Technical requirements (framework, performance, accessibility)

### Differentiation
- What makes this UNFORGETTABLE?
- What's the one thing someone will remember?

> **CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

## Frontend Aesthetics Guidelines

### Typography

Choose fonts that are beautiful, unique, and interesting:

- Avoid generic fonts: Arial, Inter, Roboto, system fonts
- Opt for distinctive choices that elevate the frontend's aesthetics
- Pair a distinctive display font with a refined body font

### Color & Theme

- Commit to a cohesive aesthetic
- Use CSS variables for consistency
- Dominant colors with sharp accents outperform timid, evenly-distributed palettes

### Motion

- Use animations for effects and micro-interactions
- Prioritize CSS-only solutions for HTML
- Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions
- Use scroll-triggering and hover states that surprise

### Spatial Composition

- Unexpected layouts
- Asymmetry
- Overlap
- Diagonal flow
- Grid-breaking elements
- Generous negative space OR controlled density

### Backgrounds & Visual Details

Create atmosphere and depth rather than defaulting to solid colors:
- Gradient meshes
- Noise textures
- Geometric patterns
- Layered transparencies
- Dramatic shadows
- Decorative borders
- Custom cursors
- Grain overlays

## What to Avoid

**NEVER use generic AI-generated aesthetics:**

- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (purple gradients on white)
- Predictable layouts and component patterns
- Cookie-cutter design lacking context-specific character

**NEVER converge on common choices** - each design should be unique.

## Implementation Tips

Match implementation complexity to the aesthetic vision:
- Maximalist designs need elaborate code with extensive animations and effects
- Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details
- Elegance comes from executing the vision well

## Quick Reference

### Distinctive Font Pairing

```css
/* ❌ Generic */
font-family: 'Inter', system-ui, sans-serif;

/* ✅ Distinctive */
font-family: 'Playfair Display', serif;
font-family: 'JetBrains Mono', monospace;
```

### Cohesive Color System

```css
:root {
  /* Dominant with sharp accent */
  --color-bg: #0a0a0a;
  --color-surface: #1a1a1a;
  --color-primary: #f97316;  /* sharp orange accent */
  --color-text: #fafafa;
}
```

### High-Impact Animation

```css
.hero-title {
  animation: fadeInUp 600ms cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.hero-title:nth-child(1) { animation-delay: 0ms; }
.hero-title:nth-child(2) { animation-delay: 100ms; }
.hero-title:nth-child(3) { animation-delay: 200ms; }
```

### Atmospheric Background

```css
.hero {
  background: 
    radial-gradient(ellipse at 20% 80%, rgba(120, 50, 255, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(255, 50, 150, 0.1) 0%, transparent 50%),
    linear-gradient(180deg, #0a0a0a 0%, #1a1a2e 100%);
}
```
