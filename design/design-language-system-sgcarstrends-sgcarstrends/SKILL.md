---
name: design-language-system
description: Maintains visual consistency across portfolio UI components. Use when creating or modifying components, styling pages, or ensuring design consistency. Includes coral colour tokens (OKLCH), typography scale, spacing rules, animations, and component patterns.
---

# Design Language System

Use this guide when creating or modifying UI components to ensure visual consistency across the portfolio.

---

## Colour Tokens

### Base Palette

| Token | OKLCH | Hex | Usage |
|-------|-------|-----|-------|
| `--background` | `oklch(0.985 0.005 90)` | `#FAF9F7` | Page background (warm paper white) |
| `--foreground` | `oklch(0.15 0.01 270)` | `#1F1F23` | Primary text (deep charcoal) |
| `--card` | `oklch(1 0 0)` | `#FFFFFF` | Card backgrounds |
| `--card-foreground` | `oklch(0.15 0.01 270)` | `#1F1F23` | Card text |
| `--muted` | `oklch(0.96 0.005 90)` | `#F3F2F0` | Muted backgrounds |
| `--muted-foreground` | `oklch(0.45 0.01 270)` | `#6B6B73` | Secondary text |
| `--border` | `oklch(0.90 0.005 90)` | `#E5E4E2` | Borders |

### Coral Accent (Primary)

| Token | OKLCH | Hex | Usage |
|-------|-------|-----|-------|
| `--primary` | `oklch(0.60 0.18 25)` | `#E07356` | Primary buttons, links, accents |
| `--primary-foreground` | `oklch(0.98 0.01 25)` | `#FDF8F7` | Text on primary |
| `--ring` | `oklch(0.70 0.15 25)` | `#EBA08A` | Focus rings, hover glows |

---

## Typography

### Fonts
- **Sans (Body)**: `Figtree` via `--font-sans`
- **Mono (Code)**: `Geist Mono` via `--font-mono`

### Scale

| Variant | Class | Usage |
|---------|-------|-------|
| `h1` | `text-5xl font-bold tracking-tight` | Page titles |
| `h2` | `text-3xl font-semibold tracking-tight` | Section headings |
| `h3` | `text-xl font-semibold` | Card titles |
| `body-lg` | `text-lg leading-relaxed` | Introductions, emphasis |
| `body` | `text-base` | Default body text |
| `body-sm` | `text-sm` | Secondary content |
| `caption` | `text-sm text-muted-foreground` | Metadata, dates |
| `label` | `text-xs font-medium uppercase tracking-wider` | Labels, categories |

### Heading Styles
- Letter-spacing: `-0.03em` on h1, h2
- Use `tracking-tight` class
- Colour: `text-foreground`

---

## Spacing

### Rules
- Use `gap-*` utilities for spacing between elements
- Avoid `margin-top`, prefer `margin-bottom` or `gap`
- Use even numbers only: `gap-2`, `gap-4`, `gap-6`, `gap-8`, `gap-12`
- Use `gap-*` instead of `gap-x-*`/`gap-y-*` (cleaner, same behaviour in flex containers)

### Spacing Scale (Even Numbers Only)

| Gap | Size | Purpose |
|-----|------|---------|
| `gap-2` | 8px | Micro: icons + text, badges, inline elements |
| `gap-4` | 16px | **Standard**: card content, grids, forms |
| `gap-6` | 24px | Section: between related components |
| `gap-8` | 32px | Macro: major page divisions, section separators |
| `gap-12` | 48px | Page: hero to content transitions |

### Guidelines
- **Default to gap-4** when unsure
- Icon + heading pairs: `gap-2`
- Card internal content: `gap-4`
- Section containers: `gap-6` or `gap-8`

---

## Background Effects (Moderate)

### Gradient Orbs
```css
.gradient-orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.15;
  pointer-events: none;
}
```
- Colour: `bg-rose-400`
- Primary orb: 600px, top-right
- Secondary orb: 500px, bottom-left (opacity * 0.7)

### Noise Texture
```css
.noise-overlay {
  opacity: 0.04;
  mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml,...");
}
```

---

## Animations

### Priority: CSS First
Use CSS for all simple animations. Only use `motion/react` for scroll-triggered or complex sequenced animations.

### CSS Specs

| Animation | Duration | Easing | Properties |
|-----------|----------|--------|------------|
| Hover states | 200ms | ease-out | All transitions |
| Page transitions | 250ms | cubic-bezier(0.4, 0, 0.2, 1) | Opacity, transform |
| Card hover | 200ms | ease-out | translateY(-2px), box-shadow |
| Button hover | 200ms | ease-out | scale(1.02), box-shadow |

### Hover Effects
- **Cards**: `hover:-translate-y-0.5` + coral glow shadow
- **Buttons**: `hover:scale-[1.02]` + shadow lift
- **Links**: Underline slides in from left via `::after`
- **Icons**: `hover:scale-110` or subtle rotation

### When to Use motion/react
- Scroll-triggered animations (fade-in on scroll)
- Complex multi-step sequences
- Gesture-based interactions

---

## Component Patterns

### Cards
```tsx
className="rounded-2xl border border-border bg-card p-6 shadow-sm
           transition-all duration-200 hover:-translate-y-0.5"
// Add coral glow on hover via inline style or CSS
```

### Buttons
```tsx
// Primary
className="rounded-full bg-primary text-primary-foreground px-6 py-3
           font-medium transition-all duration-200 hover:scale-[1.02] hover:shadow-lg"

// Outline
className="rounded-full border-2 border-primary text-primary px-6 py-3
           font-medium transition-all duration-200 hover:scale-[1.02]"
```

### Badges
```tsx
className="rounded-full bg-primary text-primary-foreground px-4 py-1.5
           font-medium text-sm transition-all duration-200 hover:-translate-y-0.5"
```

### Header
```tsx
className="fixed top-0 left-0 z-50 w-full border-b border-border
           bg-background/90 backdrop-blur-lg px-8 py-3"
```

---

## Component Rules

1. **NEVER modify** `components/ui/*` (shadcn/ui primitives)
2. Use composition via `components/shared/` wrappers
3. Styling changes go in CSS or wrapper components
4. Use `cn()` utility for conditional classes
5. Use CVA for component variants

---

## Quick Reference

### Coral Glow Shadow
```tsx
style={{ boxShadow: `0 8px 30px -10px oklch(0.60 0.18 25 / 0.4)` }}
// Or use: shadow-[0_8px_30px_-10px_theme(colors.primary/0.4)]
```

### Semantic Colours
- Primary text: `text-foreground`
- Secondary text: `text-muted-foreground`
- Accent: `text-primary`
- Backgrounds: `bg-background`, `bg-card`, `bg-muted`
- Borders: `border-border`
