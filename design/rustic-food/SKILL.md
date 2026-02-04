---
name: rustic-food
description: Create web pages and UI components using the Rustic Food design system—a warm, organic aesthetic inspired by farm-to-table restaurants, artisanal bakeries, and food blogs. Features appetizing color palettes (warm oranges, creams, sage greens), natural textures, serif/script typography, and inviting imagery. Use when the user requests rustic/organic/farm-to-table styling, food website design, restaurant pages, recipe cards, menu layouts, or any food-related web content. Framework-agnostic (works with vanilla HTML/CSS, React, Vue, Tailwind, etc.).
license: MIT
---

# Rustic Food Design System

A warm, organic design system evoking artisanal kitchens, farmers markets, and handcrafted cuisine. Creates UI that feels **handmade and inviting**.

## Core Aesthetic

Rustic Food creates interfaces that feel:
- **Warm & Appetizing**: Colors that evoke fresh ingredients and cozy kitchens
- **Organic & Natural**: Hand-drawn elements, natural textures, soft edges
- **Artisanal & Crafted**: Typography suggesting tradition and care
- **Inviting & Comfortable**: Generous spacing, approachable layouts

## Quick Reference

### Color Palette

| Token | Value | Purpose |
|-------|-------|---------|
| cream | `#FDF6E3` | Primary background |
| warm-white | `#FFFBF5` | Cards, containers |
| terracotta | `#C75B39` | Primary accent, CTAs |
| sage | `#7A9E7E` | Secondary accent, fresh/healthy |
| olive | `#6B7B3C` | Tertiary accent, organic feel |
| espresso | `#3D2B1F` | Primary text, headings |
| charcoal | `#4A4A4A` | Body text |
| honey | `#D4A84B` | Highlights, ratings, warmth |
| paprika | `#A63D2E` | Hover states, emphasis |
| linen | `#E8E0D5` | Borders, dividers |

### Typography

```css
/* Headings - Warm serif with character */
font-family: 'Playfair Display', 'Libre Baskerville', Georgia, serif;

/* Body - Clean, readable */
font-family: 'Source Sans 3', 'Lato', -apple-system, sans-serif;

/* Accent/Script - Handwritten feel for special elements */
font-family: 'Dancing Script', 'Pacifico', cursive;
```

**Scale**:
- Hero: `3.5rem` / `4rem` (56px-64px)
- H1: `2.5rem` (40px)
- H2: `1.875rem` (30px)
- H3: `1.5rem` (24px)
- Body: `1rem` / `1.125rem` (16-18px)
- Small: `0.875rem` (14px)

### Shadows & Depth

```css
/* Soft, warm shadows */
--shadow-sm: 0 2px 8px rgba(61, 43, 31, 0.08);
--shadow-md: 0 4px 16px rgba(61, 43, 31, 0.1);
--shadow-lg: 0 8px 32px rgba(61, 43, 31, 0.12);
--shadow-hover: 0 12px 40px rgba(61, 43, 31, 0.15);
```

### Border Radius

- Small: `4px` (inputs, tags)
- Medium: `8px` (buttons, small cards)
- Large: `16px` (cards, containers)
- Organic: `40% 60% 55% 45% / 55% 45% 60% 40%` (blob shapes)

### Spacing Scale

`4px` → `8px` → `16px` → `24px` → `32px` → `48px` → `64px` → `96px` → `128px`

## Implementation Patterns

### Pattern 1: CSS Variables

```css
:root {
  /* Colors */
  --rf-cream: #FDF6E3;
  --rf-warm-white: #FFFBF5;
  --rf-terracotta: #C75B39;
  --rf-sage: #7A9E7E;
  --rf-olive: #6B7B3C;
  --rf-espresso: #3D2B1F;
  --rf-charcoal: #4A4A4A;
  --rf-honey: #D4A84B;
  --rf-paprika: #A63D2E;
  --rf-linen: #E8E0D5;
  
  /* Typography */
  --rf-font-heading: 'Playfair Display', Georgia, serif;
  --rf-font-body: 'Source Sans 3', -apple-system, sans-serif;
  --rf-font-accent: 'Dancing Script', cursive;
  
  /* Shadows */
  --rf-shadow-sm: 0 2px 8px rgba(61, 43, 31, 0.08);
  --rf-shadow-md: 0 4px 16px rgba(61, 43, 31, 0.1);
  --rf-shadow-lg: 0 8px 32px rgba(61, 43, 31, 0.12);
  
  /* Radius */
  --rf-radius-sm: 4px;
  --rf-radius-md: 8px;
  --rf-radius-lg: 16px;
}
```

### Pattern 2: Natural Textures

Add warmth with subtle background textures:

```css
/* Paper/Linen texture overlay */
.rf-texture-paper {
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  background-blend-mode: soft-light;
  opacity: 0.03;
}

/* Wood grain suggestion */
.rf-texture-wood {
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(61, 43, 31, 0.02) 50%,
    transparent 100%
  );
  background-size: 8px 100%;
}
```

### Pattern 3: Organic Shapes

```css
/* Blob/organic border radius */
.rf-organic-shape {
  border-radius: 40% 60% 55% 45% / 55% 45% 60% 40%;
}

/* Wavy divider */
.rf-divider-wavy {
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120'%3E%3Cpath d='M0,60 C200,120 400,0 600,60 C800,120 1000,0 1200,60 L1200,120 L0,120 Z' fill='%23FDF6E3'/%3E%3C/svg%3E");
  background-size: 100% 100%;
  height: 60px;
}
```

### Pattern 4: Hover States

```css
.rf-card {
  background: var(--rf-warm-white);
  box-shadow: var(--rf-shadow-sm);
  border-radius: var(--rf-radius-lg);
  transition: transform 300ms ease, box-shadow 300ms ease;
}

.rf-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--rf-shadow-hover);
}

.rf-button {
  background: var(--rf-terracotta);
  color: white;
  transition: background 200ms ease, transform 200ms ease;
}

.rf-button:hover {
  background: var(--rf-paprika);
  transform: scale(1.02);
}
```

### Pattern 5: Dark Mode (Evening/Bistro)

```css
:root[data-theme="dark"] {
  --rf-cream: #1A1410;
  --rf-warm-white: #2A2420;
  --rf-terracotta: #E07B5B;
  --rf-sage: #8AB88E;
  --rf-espresso: #F5EDE5;
  --rf-charcoal: #D4CBC2;
  --rf-linen: #3A3430;
}
```

## Component Reference

See `references/components.md` for complete component patterns:
- Hero sections with full-bleed imagery
- Recipe cards with ingredient tags
- Menu layouts and pricing
- Navigation with scroll effects
- Footer with newsletter signup
- Image galleries
- Testimonial/review sections

See `references/tailwind-config.md` for Tailwind CSS configuration.

## Page Structure Patterns

### Restaurant/Cafe
1. Full-bleed hero with signature dish
2. Story/about section with imagery
3. Featured menu items grid
4. Location/hours callout
5. Reservation CTA
6. Instagram feed / reviews

### Recipe Blog
1. Hero with recipe image
2. Quick info bar (time, servings, difficulty)
3. Ingredient list (sticky on scroll)
4. Step-by-step instructions
5. Related recipes grid
6. Comment section

### Food Product
1. Product hero with large imagery
2. Ingredient story / sourcing
3. Features/benefits grid
4. Reviews/ratings
5. Add to cart section
6. Related products

## Accessibility Notes

1. **Contrast**: All text passes WCAG AA (espresso on cream = 9.5:1)
2. **Focus states**: Add visible ring with terracotta accent
3. **Image alt text**: Describe dishes appetizingly for screen readers
4. **Motion**: Respect `prefers-reduced-motion`

## Usage Workflow

1. Set page background to `#FDF6E3` (cream)
2. Import fonts: Playfair Display (400, 700), Source Sans 3 (400, 600), Dancing Script (400)
3. Apply CSS variables at `:root`
4. Use full-bleed hero images with text overlays
5. Apply warm shadows to cards and containers
6. Use terracotta for primary CTAs, sage for secondary
7. Add subtle texture overlays for warmth
8. Include organic shapes and hand-drawn decorative elements
