---
name: tailwind
description: Tailwind CSS v4 best practices, CSS-first configuration and modern patterns. Use when writing styles, configuring themes or migrating from v3.
---

# Tailwind CSS v4 Best Practices

## When to Apply

Use this skill when:
- Writing or refactoring component styles
- Configuring themes and design tokens
- Migrating from Tailwind v3 to v4
- Working with dark mode, responsive design, or animations
- Deciding between utility classes and custom CSS

---

## Core Principles

### 1. CSS-First Configuration

Tailwind v4 eliminates `tailwind.config.js` in favor of native CSS.

**Do:**
- Use `@theme {}` for design tokens
- Define custom values directly in CSS
- Keep configuration co-located with styles

**Don't:**
- Create a `tailwind.config.js` (not needed in v4)
- Use JavaScript for simple theme customization

```css
/* index.css */
@import "tailwindcss";

@theme {
  --color-brand: #3b82f6;
  --color-brand-dark: #1d4ed8;
  --font-display: "Inter", sans-serif;
  --spacing-128: 32rem;
  --animate-slide-in: slide-in 0.3s ease-out;
}
```

### 2. Use `cn()` for Class Merging

Use the `cn` utility (clsx + tailwind-merge) for conditional classes and prop overrides.

**Do:**
- Use `cn()` when classes are conditional or come from props
- Let tailwind-merge resolve conflicts automatically

**Don't:**
- Use template literals for conditional classes
- Manually handle class conflicts

```tsx
import { cn } from "../utils/cn";

// Conditional classes
<div className={cn("p-4 rounded-lg", isActive && "bg-blue-500", className)}>

// Resolves conflicts: last value wins
cn("px-4 py-2", "p-6")  // → "p-6"
cn("text-red-500", "text-blue-500")  // → "text-blue-500"
```

---

## Setup & Configuration

### Basic Setup (Vite)

```css
/* index.css */
@import "tailwindcss";
```

```ts
// vite.config.ts
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss()],
});
```

### Theme Configuration

All design tokens use CSS custom properties with specific prefixes:

```css
@theme {
  /* Colors: --color-* */
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;

  /* Spacing: --spacing-* */
  --spacing-18: 4.5rem;

  /* Font families: --font-* */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: "Fira Code", monospace;

  /* Font sizes: --text-* */
  --text-tiny: 0.625rem;
  --text-tiny--line-height: 1rem;

  /* Border radius: --radius-* */
  --radius-pill: 9999px;

  /* Shadows: --shadow-* */
  --shadow-soft: 0 2px 8px rgb(0 0 0 / 0.1);

  /* Animations: --animate-* */
  --animate-fade: fade 0.2s ease-out;
}

@keyframes fade {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

---

## New v4 Features

### Native Cascade Layers

Tailwind v4 uses CSS `@layer` automatically:

```css
@layer base {
  /* Resets and base styles */
  html { @apply antialiased; }
}

@layer components {
  /* Reusable component classes */
  .btn { @apply px-4 py-2 rounded-lg font-medium; }
}

@layer utilities {
  /* Custom utilities */
  .text-balance { text-wrap: balance; }
}
```

### Container Queries

Built-in support for container queries:

```tsx
<div className="@container">
  <div className="@sm:flex @lg:grid @lg:grid-cols-2">
    {/* Responds to container size, not viewport */}
  </div>
</div>
```

### 3D Transforms

New 3D transform utilities:

```tsx
<div className="rotate-x-45 rotate-y-12 perspective-500">
  {/* 3D transformed element */}
</div>
```

### Wide Gamut Colors (P3)

Use P3 colors for vivid displays:

```css
@theme {
  --color-vivid-blue: oklch(0.6 0.25 250);
  --color-vivid-pink: oklch(0.7 0.3 350);
}
```

### Subgrid Support

```tsx
<div className="grid grid-cols-3">
  <div className="col-span-2 grid grid-cols-subgrid">
    {/* Inherits parent grid columns */}
  </div>
</div>
```

---

## Dark Mode

### Automatic Dark Mode

Use the `dark:` variant:

```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  Content adapts to color scheme
</div>
```

### Custom Dark Mode Tokens

```css
@theme {
  --color-surface: #ffffff;
  --color-surface-dark: #1a1a1a;
}
```

```tsx
<div className="bg-[--color-surface] dark:bg-[--color-surface-dark]">
```

### Media Query Strategy (Default)

```css
/* Respects prefers-color-scheme automatically */
@import "tailwindcss";
```

### Class Strategy

```css
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));
```

---

## Responsive Design

### Breakpoint System

Default breakpoints (mobile-first):

| Prefix | Min-width | Common use |
|--------|-----------|------------|
| `sm:` | 640px | Large phones |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Laptops |
| `xl:` | 1280px | Desktops |
| `2xl:` | 1536px | Large screens |

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  {/* 1 col -> 2 cols -> 3 cols */}
</div>
```

### Custom Breakpoints

```css
@theme {
  --breakpoint-xs: 475px;
  --breakpoint-3xl: 1920px;
}
```

---

## Animations

### Define Custom Animations

```css
@theme {
  --animate-slide-up: slide-up 0.3s ease-out;
  --animate-bounce-in: bounce-in 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes bounce-in {
  0% { opacity: 0; transform: scale(0.3); }
  50% { transform: scale(1.05); }
  100% { opacity: 1; transform: scale(1); }
}
```

### Use Animations

```tsx
<div className="animate-slide-up">Slides up on mount</div>
<div className="animate-bounce-in">Bounces in</div>
```

---

## Arbitrary Values

### Inline Custom Values

```tsx
{/* One-off values */}
<div className="w-[50vw] h-[calc(100vh-4rem)]">
<div className="bg-[#1a1a2e] text-[--brand-color]">
<div className="grid-cols-[1fr_auto_2fr]">
```

### Arbitrary Variants

```tsx
{/* Custom selectors */}
<div className="[&>*:first-child]:mt-0">
<div className="[&_.title]:text-lg">
<div className="[@supports(backdrop-filter:blur())]:backdrop-blur">
```

---

## Best Practices

### 1. Composition Over Abstraction

Prefer composing utilities over creating component classes:

```tsx
// Good: Compose in JSX
<button className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">

// Only abstract if truly reused many times
```

### 2. Use Design Tokens for Brand Values

```css
@theme {
  --color-brand-primary: #3b82f6;
  --color-brand-secondary: #8b5cf6;
}
```

```tsx
<button className="bg-brand-primary hover:bg-brand-secondary">
```

### 3. Semantic Color Names

```css
@theme {
  /* Semantic names over raw colors */
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;
}
```

### 4. Group Related Styles

```tsx
{/* Group by concern for readability */}
<div className="
  flex items-center gap-4
  p-4 rounded-lg
  bg-white dark:bg-gray-800
  shadow-sm hover:shadow-md
  transition-shadow duration-200
">
```

### 5. Use @apply Sparingly

Only use `@apply` for highly reused patterns:

```css
@layer components {
  /* Good: frequently reused base button */
  .btn {
    @apply px-4 py-2 font-medium rounded-lg transition-colors;
  }
}
```

---

## Code Review Checklist

When reviewing Tailwind code:

- [ ] No `tailwind.config.js` (use CSS-first config)
- [ ] Custom values defined in `@theme {}`
- [ ] Using `cn()` for conditional/dynamic classes
- [ ] Using semantic color names
- [ ] Responsive styles are mobile-first
- [ ] Dark mode properly handled
- [ ] Animations defined with `--animate-*` tokens
- [ ] `@apply` used sparingly (prefer utilities)
- [ ] Related utilities grouped together
- [ ] No redundant utilities (e.g., `flex flex-row`)
