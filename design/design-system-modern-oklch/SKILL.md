---
name: design-system-modern-oklch
description: Use when setting up modern UI design systems with OKLCH colors, Shadcn components, and Tailwind v4 - provides production-ready design tokens, component patterns, and complete setup for cutting-edge color science
---

# Modern OKLCH Design System

## Overview

Complete production-ready design system featuring OKLCH color space (perceptually uniform, superior to HSL/RGB), Shadcn UI components, CVA variants, custom shadows, and modern design patterns.

**Core principle:** Use OKLCH for color accuracy, CVA for type-safe variants, data-slots for semantic components, and soft shadows for elevated design.

## When to Use

Use this skill when users want to:
- Set up a **modern design system** with **OKLCH colors**
- Replicate **TLDW-style aesthetics** (soft, rounded, elevated)
- Upgrade from **HSL/RGB to OKLCH** colors
- Create **Shadcn components** with advanced design tokens
- Implement **dark mode** with perceptually uniform colors
- Build **Next.js/React projects** with production-ready UI

## When NOT to Use

**NEVER use this skill for:**
- Basic Tailwind setup without specific design system needs
- Educational questions about OKLCH ("What is OKLCH?")
- Generic styling questions ("How do I center a div?")
- Non-React frameworks (Vue, Angular, Svelte)
- Projects not using Tailwind CSS

## Quick Reference

| Task | Command/Pattern |
|------|----------------|
| Install dependencies | `npm install @radix-ui/react-slot class-variance-authority clsx tailwind-merge lucide-react` |
| Install Tailwind v4 | `npm install -D tailwindcss@4 @tailwindcss/postcss@4 tw-animate-css` |
| Check word count | `wc -w app/globals.css` |
| Verify OKLCH support | Check browser supports OKLCH (Chrome 111+, Safari 15.4+) |

## Essential Patterns

### 1. Complete globals.css Setup

**Create or update `app/globals.css`:**

```css
@import "tailwindcss";
@import "tw-animate-css";

@custom-variant dark (&:is(.dark *));

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  /* ... all color tokens ... */
  --radius-sm: calc(var(--radius) - 4px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
}

:root {
  --radius: 1.25rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  /* ... complete light mode colors ... */
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --primary: oklch(0.922 0 0);
  /* ... complete dark mode colors ... */
}

@layer base {
  html { font-size: 14.4px; /* 10% compact */ }
  body { @apply bg-background text-foreground; }
}
```

**See [reference.md](reference.md) for complete globals.css template.**

### 2. Utility Functions

**Create `lib/utils.ts`:**

```typescript
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### 3. Button Component with CVA

**Create `components/ui/button.tsx`:**

```typescript
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-2xl text-sm font-medium transition-all disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow-[0px_0px_12px_0px_rgba(0,0,0,0.1)] hover:bg-primary/90",
        outline: "border bg-background hover:bg-accent"
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 px-3",
        lg: "h-10 px-6"
      }
    },
    defaultVariants: { variant: "default", size: "default" }
  }
)

export function Button({ className, variant, size, ...props }) {
  return <button className={cn(buttonVariants({ variant, size }), className)} {...props} />
}
```

**See [examples.md](examples.md) for Card, Input, and more components.**

### 4. Font Configuration (Geist)

**Update `app/layout.tsx`:**

```typescript
import { Geist, Geist_Mono } from "next/font/google";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        {children}
      </body>
    </html>
  );
}
```

## Core Design Tokens

### OKLCH Color System

**Format:** `oklch(Lightness Chroma Hue)`
- Lightness: 0-1 (0 = black, 1 = white)
- Chroma: 0-0.4 (saturation)
- Hue: 0-360 (color angle)

**Benefits:**
- Perceptual uniformity (colors appear consistent)
- Better gradients and interpolation
- Wider color gamut
- Predictable lightness

### Shadow System

```typescript
// Card shadow (soft, elevated)
"shadow-[0px_18px_59.6px_0px_rgba(0,0,0,0.06)]"

// Button shadow
"shadow-[0px_0px_12px_0px_rgba(0,0,0,0.1)]"

// Input shadow
"shadow-[0px_1px_3px_0px_rgba(0,0,0,0.06)]"
```

### Radius System

- Base: `--radius: 1.25rem` (20px)
- Small: `calc(var(--radius) - 4px)` (16px)
- Large: `var(--radius)` (20px)
- XL: `calc(var(--radius) + 4px)` (24px)

Buttons use `rounded-2xl`, Cards use `rounded-3xl`.

### Typography

- Base font size: **14.4px** (10% reduction for compact UI)
- Fonts: **Geist Sans** (body), **Geist Mono** (code)
- Line heights: Tight (`leading-none`) for headings

## Common Mistakes

**1. Using HSL/RGB instead of OKLCH** - Loses perceptual uniformity. Always use `oklch()` format for colors.

**2. Missing Tailwind v4 syntax** - Using old `@config` instead of `@theme inline`. Ensure Tailwind v4 installed.

**3. Forgetting dark mode colors** - Only defining :root colors. Must define `.dark` class with inverted OKLCH values.

**4. Arbitrary shadow values without rgba** - Using HSL in shadows. Shadows use `rgba(0,0,0,0.06)` format.

**5. No data-slot attributes** - Missing semantic component identification. Add `data-slot="button"` to components.

**6. CVA without VariantProps** - Not exporting TypeScript types. Export `buttonVariants` and use `VariantProps<typeof buttonVariants>`.

## Verification Checklist

After applying the design system:

- [ ] All dependencies installed (`class-variance-authority`, `clsx`, `tailwind-merge`, Tailwind v4)
- [ ] `globals.css` updated with complete OKLCH colors (light + dark)
- [ ] `lib/utils.ts` created with `cn()` utility
- [ ] Fonts configured (Geist or alternative)
- [ ] At least one component created with CVA variants
- [ ] Dark mode working (test by toggling `.dark` class on `<html>`)
- [ ] Custom shadows visible on components
- [ ] Focus states working (tab through buttons, see ring)

## Additional Resources

**Detailed documentation in supporting files:**
- **[reference.md](reference.md)** - Complete globals.css template, all color tokens, full schemas
- **[examples.md](examples.md)** - Card, Input, Dialog, Badge components with CVA patterns
- **[troubleshooting.md](troubleshooting.md)** - OKLCH browser support, CVA errors, dark mode issues

**Official resources:**
- **Tailwind CSS v4:** https://tailwindcss.com/docs
- **Shadcn UI:** https://ui.shadcn.com
- **CVA:** https://cva.style
- **OKLCH Explained:** https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl

## Best Practices

- **Use OKLCH for all colors:** Consistent perceptual brightness
- **Add data-slot attributes:** Enables powerful CSS selectors without className pollution
- **Export CVA variants:** Type-safe component APIs with `VariantProps`
- **Consistent spacing:** `gap-6` for cards, `gap-2` for compact layouts
- **Round corners generously:** 2xl for buttons, 3xl for cards
- **Test dark mode thoroughly:** Verify all components in both themes

---

**Word Count:** 823 words (target: <1000)
**Tested:** Yes (pressure tests available)
**Source:** Extracted from TLDW production application
