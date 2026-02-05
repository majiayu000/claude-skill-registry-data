---
name: vibecode-brand-design
description: Vibecode brand design system with colors, typography, spacing, and component guidelines. Use when designing UI, styling components, or ensuring brand consistency in the Vibecode app.
---

# Vibecode Brand Design Guide

This skill provides the official Vibecode brand design system. Follow these guidelines when creating or styling UI components.

## Core Design Philosophy

Vibecode is a modern, tech-forward brand emphasizing clarity, accessibility, and innovation. Focus on creating intuitive digital experiences while maintaining visual consistency.

## Color System

### Background Colors
- **Primary Background:** Clean whites (`#FFFFFF`) and light neutrals (`#F8FAFC`, `#F1F5F9`)
- **Secondary Background:** Soft grays for depth and hierarchy (`#E2E8F0`, `#CBD5E1`)

### Text Colors
- **Primary Text:** Dark charcoal for readability (`#1E293B`, `#0F172A`)
- **Secondary Text:** Medium grays for supporting information (`#64748B`, `#94A3B8`)

### Accent Colors (Kiwi/Teal Scale)
The primary accent palette - vibrant, modern, suggesting growth and technology:
- `#14B8A6` - Teal 500 (Primary accent)
- `#0D9488` - Teal 600 (Hover states)
- `#0F766E` - Teal 700 (Active states)
- `#2DD4BF` - Teal 400 (Light accent)
- `#5EEAD4` - Teal 300 (Backgrounds)

### Secondary Accent (Blueberry)
Deep blue tones for contrast and professional grounding:
- `#3B82F6` - Blue 500
- `#2563EB` - Blue 600
- `#1D4ED8` - Blue 700

## Typography

### Font Family
**Primary Typeface:** `Play` (Google Fonts) - Modern, clean aesthetic
```css
font-family: 'Play', sans-serif;
```

### Type Scale
| Level | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| Display | 48px | 700 | 1.1 | Hero headings |
| H1 | 36px | 700 | 1.2 | Page titles |
| H2 | 28px | 600 | 1.25 | Section headings |
| H3 | 22px | 600 | 1.3 | Subsections |
| H4 | 18px | 500 | 1.4 | Card titles |
| Body | 16px | 400 | 1.5 | Main content |
| Small | 14px | 400 | 1.5 | Captions, labels |
| Tiny | 12px | 400 | 1.4 | Fine print |

### Typography Rules
- Use weight variation for emphasis rather than size alone
- Maintain consistent line-height for readability
- Apply color strategically to guide user attention

## Spacing System

Use an 8px base unit for consistent spacing:
| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Tight spacing, inline elements |
| sm | 8px | Between related elements |
| md | 16px | Standard padding |
| lg | 24px | Section spacing |
| xl | 32px | Large gaps |
| 2xl | 48px | Major sections |
| 3xl | 64px | Page-level spacing |

## Border Radius

Subtle rounded corners for professionalism:
- **Small:** 4px - Buttons, inputs, tags
- **Medium:** 8px - Cards, panels
- **Large:** 12px - Modals, large containers
- **Full:** 9999px - Pills, avatars

## Component Guidelines

### Buttons
```css
/* Primary Button */
.btn-primary {
  background: #14B8A6;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
}
.btn-primary:hover {
  background: #0D9488;
}

/* Secondary Button */
.btn-secondary {
  background: transparent;
  border: 1px solid #E2E8F0;
  color: #1E293B;
  padding: 12px 24px;
  border-radius: 8px;
}
```

### Input Fields
```css
.input {
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: 12px 16px;
  background: #FFFFFF;
}
.input:focus {
  border-color: #14B8A6;
  outline: none;
  box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.1);
}
```

### Cards
```css
.card {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
```

## Effects

### Glassmorphism
For overlay elements and floating panels:
```css
.glass {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
```

### Shadows
| Level | Value | Usage |
|-------|-------|-------|
| sm | `0 1px 2px rgba(0,0,0,0.05)` | Subtle elevation |
| md | `0 4px 6px rgba(0,0,0,0.1)` | Cards, dropdowns |
| lg | `0 10px 15px rgba(0,0,0,0.1)` | Modals, popovers |
| xl | `0 20px 25px rgba(0,0,0,0.15)` | Major floating elements |

## Interaction States

### Hover
- Subtle color darkening (10-15%)
- Optional slight elevation increase

### Focus
- Clear outline using accent color
- `box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.2)`

### Active/Pressed
- Slightly darker than hover
- Scale down subtly if appropriate (`transform: scale(0.98)`)

### Disabled
- Opacity: 50%
- Cursor: not-allowed

## Tailwind CSS Variables

Add to your Tailwind config:
```js
colors: {
  vibecode: {
    kiwi: {
      50: '#F0FDFA',
      100: '#CCFBF1',
      200: '#99F6E4',
      300: '#5EEAD4',
      400: '#2DD4BF',
      500: '#14B8A6',
      600: '#0D9488',
      700: '#0F766E',
      800: '#115E59',
      900: '#134E4A',
    },
    blueberry: {
      500: '#3B82F6',
      600: '#2563EB',
      700: '#1D4ED8',
    }
  }
}
```

## Do's and Don'ts

### Do's
- Maintain grid consistency
- Use accent colors purposefully and sparingly
- Ensure accessible contrast ratios (WCAG AA minimum)
- Apply effects subtly
- Keep layouts clean and organized

### Don'ts
- Avoid overusing accent colors - they should highlight, not dominate
- Don't break grid systems arbitrarily
- Avoid excessive shadows that clutter the interface
- Don't compromise readability for aesthetics
- Avoid generic AI-generated aesthetics (purple gradients, Inter font)
