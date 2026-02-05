---
name: cloodle-design-tokens
description: Cloodle design system tokens for colors, typography, spacing, and components. Use when styling Cloodle interfaces, creating CSS, or implementing consistent visual design across the platform.
---

# Cloodle Design Tokens

Apply consistent visual design across all Cloodle platform interfaces using these design tokens.

## When to Use This Skill

- Creating new UI components for Cloodle
- Styling pages in Kirby CMS or Moodle
- Ensuring brand consistency across platforms
- Implementing responsive, accessible designs

## Quick Reference

See [reference.md](reference.md) for the complete token definitions.

## Key Principles

1. **Warm and Grounding** - Use earth tones (terracotta, forest, sand) as primary palette
2. **Breath-Based Spacing** - Use the 8px breath unit for consistent rhythm
3. **Accessible by Default** - Maintain 4.5:1 contrast minimum
4. **Motion with Purpose** - Animations should feel calm and intentional

## Implementation

### Colors
```css
/* Primary accent */
background: var(--cloodle-coral);

/* Grounded CTA */
background: var(--cloodle-forest);

/* Warm background */
background: var(--cloodle-white); /* #FAF8F5, not stark white */
```

### Typography
```css
/* Headings */
font-family: var(--font-display); /* Outfit */

/* Body text */
font-family: var(--font-body); /* Source Serif Pro */

/* UI elements */
font-family: var(--font-ui); /* Inter */
```

### Spacing
```css
/* Use semantic spacing tokens */
padding: var(--space-rest);      /* 24px - inside cards */
margin-bottom: var(--space-settle); /* 32px - between cards */
```

## Platform-Specific Notes

### Kirby CMS (UIkit)
Map tokens to UIkit variables in SCSS.

### Moodle (Boost Union)
Map tokens to Bootstrap/Boost variables.

### React/Web Components
Use CSS custom properties directly.
