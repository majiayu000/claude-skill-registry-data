---
name: shadcn-customization
description: Use when building React UIs with shadcn/ui that need cohesive, distinctive styling beyond defaults - provides systematic approach to theme tokens, component variants, related component groups, animations, and design system coherence. Transforms uniform shadcn into memorable branded experiences.
---

# shadcn/ui Customization System

## Overview

This skill transforms shadcn/ui from a uniform component library into a cohesive, distinctive design system. The key insight: shadcn components share visual DNA through CSS variables, Tailwind classes, and structural patterns. When you customize one aspect (like border radius), you must propagate that change to all related components to maintain coherence.

**Core principle:** Every customization creates ripples. A design system is a network of interconnected decisions, not isolated component tweaks.

## When to Use

**Use this skill when:**

- Building production React apps with shadcn/ui that need brand identity
- Default shadcn feels "too uniform" or "generic"
- You need consistent customizations across component families
- Creating a custom theme or design system on top of shadcn
- Wanting to add distinctive animations or interactions

**Don't use when:**

- Quick prototypes where defaults are acceptable
- Using shadcn as-is without customization needs

## The Customization Cascade

```
Theme Tokens (globals.css)
    ↓
Component Families (related components)
    ↓
Individual Variants (cva patterns)
    ↓
Instance Overrides (className props)
```

Always work top-down. Token changes cascade automatically; component changes require manual propagation to siblings.

---

## Part 1: Theme Token System

### CSS Variable Architecture (Tailwind v4)

shadcn/ui uses a layered CSS variable system. Understanding this prevents broken themes:

```css
/* Layer 1: Raw values in :root */
:root {
  --radius: 0.625rem;
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
}

/* Layer 2: Theme mapping via @theme inline */
@theme inline {
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
}

/* Layer 3: Components consume mapped values */
/* Button uses: rounded-lg (--radius-lg), bg-primary, text-primary-foreground */
```

### Complete Token Reference

| Token Category           | Variables                                        | Used By                       |
| ------------------------ | ------------------------------------------------ | ----------------------------- |
| **Radius**               | `--radius`, `--radius-sm/md/lg/xl`               | All interactive elements      |
| **Colors - Core**        | `--background`, `--foreground`                   | Body, text                    |
| **Colors - Surfaces**    | `--card`, `--popover`, `--muted`                 | Cards, dialogs, sheets, menus |
| **Colors - Interactive** | `--primary`, `--secondary`, `--accent`           | Buttons, links, selections    |
| **Colors - States**      | `--destructive`, `--ring`, `--border`, `--input` | Errors, focus, borders        |
| **Colors - Charts**      | `--chart-1` through `--chart-5`                  | Charts, data viz              |
| **Colors - Sidebar**     | `--sidebar-*` variants                           | Sidebar component family      |

### Creating a Custom Theme

**Step 1: Define your palette in OKLCH** (better perceptual uniformity than HSL):

```css
:root {
  /* Brand colors */
  --primary: oklch(0.65 0.25 250); /* Vibrant blue */
  --primary-foreground: oklch(0.98 0.01 250);

  /* Semantic adjustments */
  --destructive: oklch(0.55 0.22 25); /* Rich red */
  --accent: oklch(0.75 0.15 180); /* Teal accent */

  /* Surface hierarchy (maintain contrast) */
  --background: oklch(0.99 0.005 250);
  --card: oklch(1 0 0);
  --muted: oklch(0.96 0.01 250);
  --popover: oklch(1 0 0);
}

.dark {
  --primary: oklch(0.75 0.2 250); /* Lighter for dark mode */
  --primary-foreground: oklch(0.15 0.02 250);

  --background: oklch(0.13 0.02 250);
  --card: oklch(0.18 0.02 250);
  --muted: oklch(0.22 0.02 250);
  --popover: oklch(0.2 0.02 250);
}
```

**Step 2: Adjust radius for personality:**

```css
:root {
  /* Sharp/Technical: */
  --radius: 0.25rem;
  /* Balanced: */
  --radius: 0.5rem;
  /* Soft/Friendly: */
  --radius: 0.75rem;
  /* Pill-like: */
  --radius: 1rem;
  /* Fully rounded: */
  --radius: 9999px;
}
```

**Step 3: Extend with custom tokens:**

```css
:root {
  /* Custom semantic colors */
  --success: oklch(0.65 0.2 145);
  --success-foreground: oklch(0.98 0.02 145);
  --warning: oklch(0.8 0.18 85);
  --warning-foreground: oklch(0.25 0.05 85);
  --info: oklch(0.7 0.15 230);
  --info-foreground: oklch(0.98 0.01 230);
}

@theme inline {
  --color-success: var(--success);
  --color-success-foreground: var(--success-foreground);
  --color-warning: var(--warning);
  --color-warning-foreground: var(--warning-foreground);
  --color-info: var(--info);
  --color-info-foreground: var(--info-foreground);
}
```

---

## Part 2: Component Family Groups

### Critical Insight: Components Travel in Packs

When you modify one component's visual properties, related components become inconsistent. Here are the families you must update together:

### Family 1: Overlays & Floating Surfaces

| Component    | Shared Properties                                          |
| ------------ | ---------------------------------------------------------- |
| Dialog       | `rounded-lg`, `border`, `bg-background`, shadow, animation |
| Sheet        | Same surface treatment, different positioning              |
| Popover      | Same but smaller, arrow optional                           |
| DropdownMenu | Same surface, specific item patterns                       |
| ContextMenu  | Identical to DropdownMenu                                  |
| Tooltip      | Simplified surface, different timing                       |
| HoverCard    | Between Tooltip and Popover                                |
| AlertDialog  | Dialog variant with action emphasis                        |
| Command      | Dialog variant with search pattern                         |

**When customizing overlays, update ALL of these:**

```tsx
// Example: Adding consistent glass morphism to all overlays
// In each component file, update the content wrapper:

// dialog.tsx
const DialogContent = React.forwardRef<...>(({ className, ...props }, ref) => (
  <DialogPrimitive.Content
    className={cn(
      "bg-background/80 backdrop-blur-xl border-white/20",
      "shadow-2xl shadow-black/10",
      // ... rest of classes
      className
    )}
    {...props}
  />
))

// Apply same pattern to: SheetContent, PopoverContent,
// DropdownMenuContent, TooltipContent, HoverCardContent
```

### Family 2: Form Controls

| Component  | Shared Properties                   |
| ---------- | ----------------------------------- |
| Input      | Height, padding, border, focus ring |
| Textarea   | Same but multi-line                 |
| Select     | Input-like trigger, overlay content |
| Combobox   | Input + dropdown hybrid             |
| DatePicker | Input trigger + calendar overlay    |
| InputOTP   | Multiple small inputs               |

**Unified form control styling:**

```tsx
// Create shared input styles
const inputBaseStyles = cn(
  'h-11 px-4', // Consistent sizing
  'rounded-lg', // Match radius
  'border-2 border-input', // Visible borders
  'bg-transparent', // Or bg-muted/50
  'transition-all duration-200', // Smooth states
  'focus-visible:ring-2 focus-visible:ring-ring/50',
  'focus-visible:border-primary',
  'placeholder:text-muted-foreground/60'
);

// Apply to Input, Textarea, Select trigger, etc.
```

### Family 3: Buttons & Actions

| Component       | Shared Properties         |
| --------------- | ------------------------- |
| Button          | Core interactive element  |
| Toggle          | Button variant for on/off |
| ToggleGroup     | Multiple toggles          |
| ButtonGroup     | Multiple buttons          |
| Tabs (triggers) | Button-like triggers      |
| Pagination      | Button-based navigation   |

**Unified button treatment:**

```tsx
// button.tsx - Define comprehensive variants
const buttonVariants = cva(
  cn(
    'inline-flex items-center justify-center gap-2',
    'font-medium transition-all duration-200',
    'focus-visible:outline-none focus-visible:ring-2',
    'focus-visible:ring-ring focus-visible:ring-offset-2',
    'disabled:pointer-events-none disabled:opacity-50',
    // Add micro-interaction
    'active:scale-[0.98]'
  ),
  {
    variants: {
      variant: {
        default: cn(
          'bg-primary text-primary-foreground',
          'hover:bg-primary/90',
          'shadow-md shadow-primary/25',
          'hover:shadow-lg hover:shadow-primary/30'
        ),
        secondary: cn(
          'bg-secondary text-secondary-foreground',
          'hover:bg-secondary/80',
          'border border-border'
        ),
        outline: cn(
          'border-2 border-input bg-transparent',
          'hover:bg-accent hover:text-accent-foreground',
          'hover:border-accent'
        ),
        ghost: cn('hover:bg-accent/50 hover:text-accent-foreground'),
        destructive: cn(
          'bg-destructive text-destructive-foreground',
          'hover:bg-destructive/90',
          'shadow-md shadow-destructive/25'
        ),
        // Custom variants
        success: cn(
          'bg-success text-success-foreground',
          'hover:bg-success/90'
        ),
        link: cn('text-primary underline-offset-4', 'hover:underline'),
      },
      size: {
        default: 'h-10 px-5 py-2',
        sm: 'h-8 px-3 text-sm',
        lg: 'h-12 px-8 text-lg',
        xl: 'h-14 px-10 text-xl',
        icon: 'h-10 w-10',
        'icon-sm': 'h-8 w-8',
        'icon-lg': 'h-12 w-12',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);
```

### Family 4: Data Display

| Component   | Shared Properties                         |
| ----------- | ----------------------------------------- |
| Card        | Container with consistent padding, border |
| Table       | Row styling, cell padding                 |
| DataTable   | Table + interactions                      |
| Accordion   | Expandable sections                       |
| Collapsible | Simple expand/collapse                    |

### Family 5: Navigation

| Component      | Shared Properties |
| -------------- | ----------------- |
| NavigationMenu | Top-level nav     |
| Sidebar        | Side navigation   |
| Breadcrumb     | Location trail    |
| Tabs           | Section switching |
| Menubar        | Application menu  |

---

## Part 3: Animation & Motion System

### Default shadcn Animations (tw-animate-css)

shadcn uses `tw-animate-css` for enter/exit animations. Customize timing and easing globally:

```css
/* In globals.css, after imports */
:root {
  /* Animation timing */
  --animation-duration: 200ms;
  --animation-duration-slow: 400ms;
  --animation-duration-fast: 150ms;

  /* Easing curves */
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out-expo: cubic-bezier(0.87, 0, 0.13, 1);
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@theme inline {
  --animate-duration: var(--animation-duration);
}
```

### Adding Custom Animations

**Approach 1: CSS Keyframes (simpler)**

```css
@keyframes slide-up-fade {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

/* Apply to components */
.animate-slide-up-fade {
  animation: slide-up-fade var(--animation-duration) var(--ease-out-expo);
}
```

**Approach 2: Motion library (React, more control)**

```tsx
import { motion, AnimatePresence } from "framer-motion"

// Wrap Dialog content
const DialogContent = React.forwardRef<...>(({ className, children, ...props }, ref) => (
  <DialogPrimitive.Portal>
    <DialogPrimitive.Overlay asChild>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 bg-black/80"
      />
    </DialogPrimitive.Overlay>
    <DialogPrimitive.Content asChild ref={ref} {...props}>
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 10 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 10 }}
        transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
        className={cn("fixed left-1/2 top-1/2 ...", className)}
      >
        {children}
      </motion.div>
    </DialogPrimitive.Content>
  </DialogPrimitive.Portal>
))
```

### Micro-Interaction Patterns

```tsx
// Button press effect
'active:scale-[0.98] transition-transform duration-100';

// Hover lift
'hover:-translate-y-0.5 hover:shadow-lg transition-all duration-200';

// Focus glow
'focus-visible:ring-4 focus-visible:ring-primary/20 transition-shadow duration-200';

// Skeleton loading
'animate-pulse bg-muted';
// Or shimmer:
'bg-gradient-to-r from-muted via-muted/50 to-muted bg-[length:200%_100%] animate-shimmer';
```

---

## Part 4: Typography Integration

### Adding Custom Fonts

**Step 1: Import fonts** (using next/font, Google Fonts, or local)

```tsx
// app/layout.tsx (Next.js example)
import { Instrument_Serif, DM_Sans } from 'next/font/google';

const displayFont = Instrument_Serif({
  subsets: ['latin'],
  weight: '400',
  variable: '--font-display',
});

const bodyFont = DM_Sans({
  subsets: ['latin'],
  variable: '--font-body',
});

export default function RootLayout({ children }) {
  return (
    <html className={`${displayFont.variable} ${bodyFont.variable}`}>
      {children}
    </html>
  );
}
```

**Step 2: Configure in CSS**

```css
@theme inline {
  --font-sans: var(--font-body), system-ui, sans-serif;
  --font-display: var(--font-display), Georgia, serif;
}

@layer base {
  body {
    font-family: var(--font-sans);
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    font-family: var(--font-display);
  }
}
```

**Step 3: Apply to components**

```tsx
// card.tsx - Use display font for titles
const CardTitle = React.forwardRef<...>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "font-display text-2xl font-semibold tracking-tight",
      className
    )}
    {...props}
  />
))
```

---

## Part 5: Coherence Checklist

When making ANY customization, check these for consistency:

### Radius Changes

- [ ] Button
- [ ] Input, Textarea, Select
- [ ] Card
- [ ] Dialog, Sheet, Popover
- [ ] DropdownMenu, ContextMenu
- [ ] Tooltip
- [ ] Badge, Alert
- [ ] Avatar
- [ ] Tabs (triggers)
- [ ] Toggle, Switch

### Shadow Changes

- [ ] Button (especially primary)
- [ ] Card
- [ ] Dialog, Sheet
- [ ] Popover, Dropdown
- [ ] Hover states on interactive cards

### Border Changes

- [ ] Input, Textarea, Select
- [ ] Card
- [ ] Table
- [ ] Separator
- [ ] All overlay components

### Color Changes

When changing primary:

- [ ] Button (default variant)
- [ ] Links
- [ ] Focus rings
- [ ] Switch (checked)
- [ ] Slider (track fill)
- [ ] Progress (indicator)
- [ ] Checkbox, Radio (checked)
- [ ] Tabs (active indicator)

### Animation Timing Changes

- [ ] Dialog enter/exit
- [ ] Sheet slide
- [ ] Dropdown appear
- [ ] Tooltip delay and fade
- [ ] Accordion expand/collapse
- [ ] Collapsible toggle
- [ ] Toast enter/exit

---

## Part 6: Advanced Patterns

### Pattern 1: Semantic Variants via Data Attributes

```tsx
// Instead of multiple component variants, use data attributes
<Card data-variant="elevated">
<Card data-variant="outlined">
<Card data-variant="filled">

// Style with attribute selectors
const Card = React.forwardRef<...>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-lg",
      // Base styles
      "data-[variant=elevated]:bg-card data-[variant=elevated]:shadow-lg",
      "data-[variant=outlined]:border-2 data-[variant=outlined]:border-border",
      "data-[variant=filled]:bg-muted",
      className
    )}
    {...props}
  />
))
```

### Pattern 2: Compound Components with Consistent Spacing

```tsx
// Use CSS custom properties for internal spacing
const Card = React.forwardRef<...>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    style={{ '--card-padding': '1.5rem' } as React.CSSProperties}
    className={cn("rounded-lg border bg-card", className)}
    {...props}
  />
))

const CardHeader = ({ className, ...props }) => (
  <div
    className={cn(
      "px-[var(--card-padding)] pt-[var(--card-padding)]",
      className
    )}
    {...props}
  />
)

const CardContent = ({ className, ...props }) => (
  <div
    className={cn("px-[var(--card-padding)]", className)}
    {...props}
  />
)

const CardFooter = ({ className, ...props }) => (
  <div
    className={cn(
      "px-[var(--card-padding)] pb-[var(--card-padding)]",
      className
    )}
    {...props}
  />
)
```

### Pattern 3: Theme-Aware Shadows

```css
:root {
  --shadow-color: 220 3% 15%;
  --shadow-elevation-low:
    0.3px 0.5px 0.7px hsl(var(--shadow-color) / 0.1),
    0.4px 0.8px 1px -1.2px hsl(var(--shadow-color) / 0.1),
    1px 2px 2.5px -2.5px hsl(var(--shadow-color) / 0.1);
  --shadow-elevation-medium:
    0.3px 0.5px 0.7px hsl(var(--shadow-color) / 0.11),
    0.8px 1.6px 2px -0.8px hsl(var(--shadow-color) / 0.11),
    2.1px 4.1px 5.2px -1.7px hsl(var(--shadow-color) / 0.11),
    5px 10px 12.6px -2.5px hsl(var(--shadow-color) / 0.11);
}

.dark {
  --shadow-color: 220 40% 2%;
}

@theme inline {
  --shadow-sm: var(--shadow-elevation-low);
  --shadow-md: var(--shadow-elevation-medium);
}
```

---

## Quick Reference

### File Locations

| File                  | Purpose                             |
| --------------------- | ----------------------------------- |
| `globals.css`         | Theme tokens, base styles           |
| `components/ui/*.tsx` | Individual component customization  |
| `lib/utils.ts`        | `cn()` helper                       |
| `components.json`     | shadcn CLI config                   |
| `tailwind.config.ts`  | Extended theme (v3) / not used (v4) |

### Common Class Patterns

| Pattern           | Classes                                            |
| ----------------- | -------------------------------------------------- |
| Elevated surface  | `bg-card shadow-md`                                |
| Subtle surface    | `bg-muted/50`                                      |
| Interactive hover | `hover:bg-accent/50 transition-colors`             |
| Focus ring        | `focus-visible:ring-2 focus-visible:ring-ring`     |
| Disabled state    | `disabled:opacity-50 disabled:pointer-events-none` |
| Press feedback    | `active:scale-[0.98]`                              |

### OKLCH Color Manipulation

```css
/* Darken: reduce L (lightness) */
--primary: oklch(0.65 0.25 250);
--primary-hover: oklch(0.55 0.25 250);

/* Lighten: increase L */
--primary-light: oklch(0.75 0.25 250);

/* Desaturate: reduce C (chroma) */
--primary-muted: oklch(0.65 0.1 250);

/* Shift hue: change H */
--primary-complement: oklch(0.65 0.25 70); /* 250 + 180 = 430 → 70 */
```

---

## Common Mistakes

| Mistake                         | Fix                                            |
| ------------------------------- | ---------------------------------------------- |
| Changing radius only in Button  | Update all Family 1 & 2 components             |
| Hardcoding colors in components | Use CSS variables everywhere                   |
| Forgetting dark mode            | Always define `.dark` variants                 |
| Inconsistent animation timing   | Use global timing variables                    |
| Breaking focus states           | Keep focus ring for accessibility              |
| Mixing color formats            | Stick to OKLCH for consistency                 |
| Over-animating                  | Choose 2-3 high-impact moments, not everything |

---

## Integration with frontend-design Skill

This skill pairs with `frontend-design`. Use that skill's aesthetic direction guidance, then implement here:

1. **frontend-design** → Choose aesthetic direction (brutalist, refined, playful, etc.)
2. **shadcn-customization** → Implement that direction systematically across all components

Example flow:

- Direction: "Refined luxury" → Subtle shadows, generous spacing, serif display font, muted palette
- Direction: "Playful startup" → Rounded corners (--radius: 1rem), vibrant primary, bouncy animations
- Direction: "Technical/Developer" → Sharp corners (--radius: 0.25rem), monospace accents, minimal color
