---
name: tailwind-v4-shadcn
description: Tailwind CSS v4 + shadcn/ui theming in monorepos. Use when working with @theme, @theme inline, @source, debugging missing utility classes, or setting up a shared design-system package consumed by apps. Triggers on @theme, @theme inline, @source, bg-primary missing, utility class not generated, Tailwind v4 monorepo, shadcn theme.
---

# Tailwind v4 + shadcn/ui Theming

## Critical Rules

### 1. Single `@import 'tailwindcss'` — EVER

Only the **consuming app's CSS** imports Tailwind. Shared theme files (design-system packages) must **never** include `@import 'tailwindcss'`, `@import 'tw-animate-css'`, or `@import 'shadcn/tailwind.css'`.

Duplicate imports create conflicting Tailwind instances that silently break `@theme` resolution.

```css
/* ❌ BAD — theme.css in a shared package */
@import 'tailwindcss';
@theme inline { --color-primary: var(--primary); }

/* ✅ GOOD — theme.css in a shared package */
/* No framework imports — just tokens */
@theme inline { --color-primary: var(--primary); }
```

### 2. `@source` for Monorepo Workspace Packages

Tailwind v4's Vite plugin (`@tailwindcss/vite`) only scans the **app's own source**. Classes used in workspace packages won't generate utilities unless you add `@source` directives.

```css
/* apps/studio/src/styles.css */
@import 'tailwindcss';
@import 'tw-animate-css';
@import '../../../packages/design-system/src/theme.css';

@source "../../../packages/design-system/src";
@source "../../../packages/visual-editor/src";
```

**Symptom without `@source`:** `.bg-primary`, `.text-primary-foreground`, etc. exist in source code but are absent from compiled CSS. File size is suspiciously small.

### 3. `@theme inline` for `var()` References

Tailwind v4 has two theme block types:

| Block | Use for | Generates utilities? |
|-------|---------|---------------------|
| `@theme { }` | Static values (`#3b82f6`, `0.5rem`) | Yes — Tailwind resolves at build time |
| `@theme inline { }` | `var()` references (`var(--primary)`) | Yes — deferred to runtime |

Putting `var()` references in a plain `@theme` block can corrupt Tailwind's theme resolution and silently prevent utility generation.

```css
/* ❌ BAD */
@theme {
  --color-node-bg: var(--card);       /* var() in regular @theme */
  --color-data: #3b82f6;              /* static — fine here */
}

/* ✅ GOOD */
@theme inline {
  --color-node-bg: var(--card);       /* var() refs go here */
}
@theme {
  --color-data: #3b82f6;              /* static values go here */
}
```

## shadcn Semantic Bridge Pattern

shadcn/ui defines CSS custom properties like `--primary`, `--background`, etc. Tailwind v4 maps utilities via `--color-*` namespace. The bridge connects them:

```css
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  /* ...chart, sidebar tokens follow same pattern */
}
```

Then `:root` / `.dark` define the actual oklch values:

```css
:root {
  --primary: oklch(0.488 0.243 264.376);
  --primary-foreground: oklch(0.984 0.003 247.858);
  /* ... */
}
.dark {
  --primary: oklch(0.746 0.16 232.661);
  /* ... */
}
```

## Correct File Architecture

```
packages/design-system/src/
  theme.css        ← tokens only, NO @import 'tailwindcss'
    ├── @custom-variant dark
    ├── @theme inline { }   ← shadcn bridge + any var() refs
    ├── @theme { }           ← domain static tokens
    ├── :root { }            ← light palette
    ├── .dark { }            ← dark palette
    └── @layer base { }      ← defaults (border-border, bg-background)

apps/studio/src/
  styles.css       ← single Tailwind entry point
    ├── @import 'tailwindcss'
    ├── @import 'tw-animate-css'
    ├── @import '…/theme.css'
    ├── @source "…/design-system/src"
    ├── @source "…/visual-editor/src"
    └── app-specific styles
```

## Debugging Checklist

When utilities like `bg-primary` aren't working:

1. **Check if the class exists in compiled CSS** — View page source or `grep` the built CSS for `.bg-primary`. If absent, it's a generation issue.
2. **Check CSS file size** — Suspiciously small output means `@source` is missing for workspace packages.
3. **Check computed `--color-primary`** — In DevTools, inspect the element. If `--color-primary` is empty but `--primary` has a value, the `@theme inline` bridge is broken (likely duplicate `@import 'tailwindcss'`).
4. **Count `@import 'tailwindcss'`** — Search all CSS files in the import chain. Must be exactly one.
5. **Check `@theme` vs `@theme inline`** — Any `var()` in a plain `@theme` block? Move it to `@theme inline`.
6. **Verify dark mode** — `@custom-variant dark (&:is(.dark *))` must be present. The `<html>` element needs class `dark`.
