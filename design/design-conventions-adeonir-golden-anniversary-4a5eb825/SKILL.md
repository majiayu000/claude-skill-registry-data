---
name: design-conventions
description: Golden Anniversary design system with OKLCH color palette, typography (Inter, Playfair Display, Dancing Script), component states, Framer Motion patterns, and accessibility requirements. Use when working on styling, UI components, or visual changes.
---

# Design Conventions

## Golden Colors (OKLCH)

```css
:root {
  --gold-50: oklch(98% 0.02 85);
  --gold-100: oklch(95% 0.04 85);
  --gold-200: oklch(88% 0.08 85);
  --gold-300: oklch(82% 0.12 85);
  --gold-400: oklch(75% 0.15 85);
  --gold-500: oklch(68% 0.18 85);
  --gold-600: oklch(60% 0.15 85);
  --gold-700: oklch(52% 0.12 85);
  --gold-800: oklch(44% 0.09 85);
  --gold-900: oklch(36% 0.06 85);
  --gold-950: oklch(28% 0.04 85);
}
```

**Validated contrast combinations** (>= 4.5:1):
- gold-600 + white (4.8:1)
- gold-700 + white (6.2:1)
- gold-800 + gold-50 (4.6:1)
- Avoid: gold-400 + white (3.8:1)

## Typography

```tsx
// Inter - Body text, UI elements
const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

// Playfair Display - Section titles
const playfair = Playfair_Display({ subsets: ["latin"], variable: "--font-serif" });

// Dancing Script - Couple names, special text
const dancingScript = Dancing_Script({ subsets: ["latin"], variable: "--font-script" });
```

**Usage:**
```tsx
<h1 className="font-script text-gold-500">Iria e Ari</h1>
<h2 className="font-heading text-gold-700">Golden Anniversary</h2>
<p className="font-body text-muted-foreground">Body text</p>
```

## Breakpoints (mobile-first)

- Mobile: 375px+ (base)
- Tablet: 768px+ (md:)
- Desktop: 1024px+ (lg:)

## Component States

**Buttons:**
```tsx
bg-primary → bg-primary/90 + scale-105 → bg-primary/80 → bg-muted
// Default → Hover → Active → Disabled
```

**Cards:**
```tsx
border-border → border-gold-200 + shadow-lg → ring-2 ring-ring
// Default → Hover → Focus
```

**Images:**
```tsx
skeleton gold-100 → normal → scale-105 + brightness-110 → bg-muted + icon
// Loading → Default → Hover → Error
```

## Framer Motion Patterns

- **Scroll animations**: `useInView` for gradual appearance
- **Hover effects**: `whileHover={{ y: -4, scale: 1.02 }}`
- **Loading states**: Pulse animation on skeletons
- **Success feedback**: Checkmark animation

## Accessibility Requirements

- Touch targets: min 44px (`min-h-11`)
- Focus visible: `ring-2 ring-ring`
- Contrast: >= 4.5:1
- Keyboard navigation: logical tab order
- Text scaling: functional up to 200% zoom

## Shadcn/ui Components Used

**Base:** Button, Card, Input, Textarea, Badge, Dialog, Tabs, Tooltip, Select, Checkbox, Avatar

**Custom:** TimeCard, PhotoCarousel, MessageCard, TimelineItem
