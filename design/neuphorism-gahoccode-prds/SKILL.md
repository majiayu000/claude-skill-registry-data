---
name: neuphorism
description: Create web pages and UI components using the Neuphorism design system—a soft, tactile neumorphic aesthetic with extruded/pressed shadows, muted surface colors, and refined typography. Use when the user requests neuphorism/neumorphic styling, soft UI, or references this design system for any web page, component, dashboard, or application. Framework-agnostic (works with vanilla HTML/CSS, React, Vue, Tailwind, etc.).
license: MIT
---

# Neuphorism Design System

A soft, tactile design system featuring extruded shadows, pressed states, and muted color palettes that create depth through light simulation rather than hard borders.

## Core Aesthetic

Neuphorism creates UI that appears **carved from the surface**:
- Elements "extrude" with dual shadows (dark bottom-right, light top-left)
- Interactive elements "press" into the surface on activation
- Soft, muted backgrounds with subtle gradients
- Clean Inter typography at light-to-medium weights
- Generous spacing and rounded corners

## Quick Reference

### Shadows (The Heart of Neuphorism)

```css
/* Extruded - default raised state */
box-shadow: 12px 12px 24px #c5c8ce, -12px -12px 24px #ffffff;

/* Pressed - active/focused state */
box-shadow: inset 6px 6px 12px #c5c8ce, inset -6px -6px 12px #ffffff;

/* Elevated - hover state */
box-shadow: 16px 16px 32px #c5c8ce, -16px -16px 32px #ffffff;
```

### Color Palette

| Token | Light | Dark | Purpose |
|-------|-------|------|---------|
| bg-primary | `#e6e8ed` | `#2d3748` | Main surface |
| shadow-dark | `#c5c8ce` | `#1a202c` | Bottom-right shadow |
| shadow-light | `#ffffff` | `#3d4a5c` | Top-left highlight |
| text-primary | `#4a5568` | `#e2e8f0` | Body text |
| text-heading | `#2d3748` | `#f7fafc` | Headings |
| accent | `#667eea` | `#667eea` | Interactive elements |

### Typography

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
/* Weights: 300 (light), 400 (regular), 500 (medium) */
```

### Spacing Scale

`4px` → `8px` → `12px` → `16px` → `24px` → `32px` → `48px` → `64px`

### Border Radius

- Small: `8px` (inputs, small buttons)
- Medium: `12px` (buttons, cards)
- Large: `20px` (containers, heroes)

## Implementation Patterns

### Pattern 1: CSS Variables (Vanilla/Any Framework)

Include at document root for consistent theming:

```css
:root {
  --neu-bg: #e6e8ed;
  --neu-shadow-dark: #c5c8ce;
  --neu-shadow-light: #ffffff;
  --neu-text: #4a5568;
  --neu-heading: #2d3748;
  --neu-accent: #667eea;
  --neu-radius: 12px;
  --neu-extruded: 12px 12px 24px var(--neu-shadow-dark), -12px -12px 24px var(--neu-shadow-light);
  --neu-pressed: inset 6px 6px 12px var(--neu-shadow-dark), inset -6px -6px 12px var(--neu-shadow-light);
}
```

### Pattern 2: Component States

Every interactive element needs three shadow states:

```css
.neu-element {
  box-shadow: var(--neu-extruded);
  transition: box-shadow 250ms ease, transform 250ms ease;
}
.neu-element:hover {
  box-shadow: 16px 16px 32px var(--neu-shadow-dark), -16px -16px 32px var(--neu-shadow-light);
  transform: translateY(-2px);
}
.neu-element:active, .neu-element:focus {
  box-shadow: var(--neu-pressed);
  transform: translateY(0);
}
```

### Pattern 3: Dark Mode

Toggle via `data-theme="dark"` on root element:

```css
:root[data-theme="dark"] {
  --neu-bg: #2d3748;
  --neu-shadow-dark: #1a202c;
  --neu-shadow-light: #3d4a5c;
  --neu-text: #e2e8f0;
  --neu-heading: #f7fafc;
}
```

## Component Reference

See `references/components.md` for complete component CSS (buttons, cards, inputs, navigation, heroes).

See `references/tailwind-config.md` for Tailwind CSS configuration.

## Accessibility Notes

1. **Focus visibility**: Add visible ring on `:focus-visible`:
   ```css
   .neu-element:focus-visible {
     box-shadow: var(--neu-pressed), 0 0 0 3px rgba(102, 126, 234, 0.3);
   }
   ```

2. **Reduced motion**: Wrap animations in media query:
   ```css
   @media (prefers-reduced-motion: no-preference) {
     .neu-element { transition: all 250ms ease; }
   }
   ```

3. **Touch targets**: Ensure minimum 44×44px for mobile.

4. **Contrast**: All text colors pass WCAG AA against backgrounds.

## Usage Workflow

1. Set background to `#e6e8ed` (light) or `#2d3748` (dark)
2. Apply CSS variables at `:root`
3. Import Inter font (weights 300, 400, 500)
4. Use extruded shadow for raised elements
5. Use pressed shadow for inputs and active states
6. Apply transitions for smooth state changes
