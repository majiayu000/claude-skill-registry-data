---
name: styling-with-tailwind-cva
description: Use when creating design systems or styling components with Tailwind CSS v4 and Class Variance Authority (CVA) - provides type-safe component variants with CSS variables for design tokens
---

# Styling with Tailwind CSS + CVA

## Overview

Framework-agnostic design system pattern: **Tailwind CSS v4** (utility-first) + **CVA** (type-safe variants) + **CSS Variables** (design tokens).

## Tooling

```bash
pnpm add tailwindcss clsx class-variance-authority
pnpm add -D @tailwindcss/postcss
```

## CSS Variables for Design Tokens

**All design tokens as CSS variables for easy theming:**

```css
/* app/globals.css */
@import "tailwindcss";

:root {
  /* Colors */
  --color-background: #0A0A0A;
  --color-surface: rgba(255,255,255,0.03);
  --color-text-primary: #FFFFFF;
  --color-text-secondary: rgba(255,255,255,0.7);
  --color-accent: #00CED1;
  --color-border: rgba(255,255,255,0.1);

  /* Typography (1.25 ratio) */
  --font-size-sm: 1rem;
  --font-size-md: 1.25rem;
  --font-size-lg: 1.563rem;
  --font-size-xl: 1.953rem;
  --font-size-2xl: 2.441rem;

  /* Spacing (8px base) */
  --space-2: 1rem;      /* 16px */
  --space-3: 1.5rem;    /* 24px */
  --space-4: 2rem;      /* 32px */
  --space-6: 3rem;      /* 48px */

  /* Border Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;
}
```

## Tailwind Theme Integration

```css
@theme inline {
  --color-brand-bg: var(--color-background);
  --color-brand-surface: var(--color-surface);
  --color-brand-accent: var(--color-accent);
}
```

Usage: `bg-brand-surface`, `text-brand-accent`

## Component Variants with CVA

**Basic pattern:**

```typescript
import { cva, type VariantProps } from 'class-variance-authority'
import { ButtonHTMLAttributes, forwardRef } from 'react'

const buttonVariants = cva(
  // Base styles (always applied)
  'inline-flex items-center justify-center font-medium transition-all',
  {
    variants: {
      variant: {
        primary: 'bg-brand-accent text-black hover:shadow-lg',
        secondary: 'border border-brand-accent text-brand-accent',
        ghost: 'text-brand-accent hover:bg-brand-accent/10',
      },
      size: {
        sm: 'px-4 py-2 text-sm',
        md: 'px-6 py-3 text-base',
        lg: 'px-8 py-4 text-lg',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
)

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        className={buttonVariants({ variant, size, className })}
        ref={ref}
        {...props}
      />
    )
  }
)

export default Button
```

**Usage:**
```jsx
<Button variant="primary" size="lg">Click me</Button>
<Button variant="secondary">Default size</Button>
```

## Compound Variants

For complex interactions between variants:

```typescript
const cardVariants = cva('rounded-lg border transition-all', {
  variants: {
    variant: {
      default: 'bg-white border-gray-200',
      primary: 'bg-blue-50 border-blue-200',
    },
    interactive: {
      true: 'cursor-pointer hover:shadow-lg',
      false: '',
    },
  },
  compoundVariants: [
    {
      variant: 'primary',
      interactive: true,
      class: 'hover:bg-blue-100',
    },
  ],
})
```

## Conditional Classes with clsx

```typescript
import { clsx } from 'clsx'

function Component({ isActive, hasError, className }) {
  return (
    <div
      className={clsx(
        'base-class',
        isActive && 'active-class',
        hasError && 'error-class',
        className
      )}
    />
  )
}
```

## Responsive Design (Mobile-First)

```jsx
<div className="
  flex flex-col      // Mobile: column
  md:flex-row        // Tablet+: row
  gap-4              // All: 1rem gap
  md:gap-6           // Tablet+: 1.5rem
">
```

## Best Practices

1. **CSS variables for all tokens** - Easy theming
2. **Mobile-first responsive** - Start small, enhance larger
3. **Type-safe variants with CVA** - Catch errors at compile time
4. **Consistent spacing scale** - 8px base unit
5. **Semantic color naming** - `success`, `error` not `green`, `red`
6. **Accessible contrast** - 4.5:1 minimum for text

## Common Patterns

**Container component:**
```typescript
const containerVariants = cva('mx-auto px-4', {
  variants: {
    size: {
      default: 'max-w-7xl',
      content: 'max-w-4xl',
      narrow: 'max-w-2xl',
    },
  },
})
```

**Badge component:**
```typescript
const badgeVariants = cva('inline-flex items-center font-medium', {
  variants: {
    variant: {
      default: 'bg-gray-100 text-gray-800',
      success: 'bg-green-100 text-green-800',
      error: 'bg-red-100 text-red-800',
    },
    size: {
      sm: 'px-2 py-0.5 text-xs',
      md: 'px-3 py-1 text-sm',
    },
  },
})
```

## Quality Criteria

- All colors defined as CSS variables
- Typography follows consistent ratio
- Spacing uses 8px base unit
- Components have type-safe CVA variants
- Mobile-first responsive design
- Color contrast meets WCAG AA (4.5:1 minimum)
- Hover/focus states visible
