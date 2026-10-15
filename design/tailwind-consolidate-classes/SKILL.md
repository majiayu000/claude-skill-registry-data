---
name: tailwind-consolidate-classes
description: Enforces consolidation of static Tailwind CSS classes into a single template literal when using cn(), clsx(), or classnames(). Use when writing or reviewing Tailwind CSS class merging utilities, or when the user mentions cn(), clsx(), or className consolidation.
---

# Tailwind CSS: Consolidate Static Classes

When using `cn()`, `clsx()`, or `classnames()`, consolidate all static class names into a single template literal string to enable automatic sorting and deduplication by `eslint-plugin-better-tailwindcss`.

## Preferred

```tsx
className={cn(
  `
    relative overflow-hidden rounded-xl
    bg-white text-gray-900
    dark:bg-gray-800 dark:text-white
  `,
  className,
)}
```

## Avoid

```tsx
className={cn(
  'relative overflow-hidden rounded-xl',
  `
    bg-white text-gray-900
    dark:bg-gray-800 dark:text-white
  `,
  className,
)}
```

## Exception

Separate strings are acceptable only when conditional logic requires it:

```tsx
className={cn(
  `
    relative overflow-hidden rounded-xl
    bg-white text-gray-900
    dark:bg-gray-800 dark:text-white
  `,
  isActive && 'ring-2 ring-primary',
  className,
)}
```
