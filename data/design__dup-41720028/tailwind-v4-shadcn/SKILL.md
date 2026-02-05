---
name: tailwind-v4-shadcn
description: |
  Set up Tailwind v4 with shadcn/ui using @theme inline pattern and CSS variable architecture. Four-step mandatory pattern: define CSS variables at root, map to Tailwind utilities, apply base styles, get automatic dark mode.

  Use when: initializing React projects with Tailwind v4, setting up shadcn/ui dark mode, or fixing colors not working, theme not applying, CSS variables broken, tw-animate-css errors, or migrating from v3.
---

# Tailwind v4 + shadcn/ui Production Stack

**Production-tested**: WordPress Auditor (https://wordpress-auditor.webfonts.workers.dev)
**Last Updated**: 2026-01-03
**Versions**: tailwindcss@4.1.18, @tailwindcss/vite@4.1.18
**Status**: Production Ready ✅

---

## Quick Start (Follow This Exact Order)

```bash
# 1. Install dependencies
pnpm add tailwindcss @tailwindcss/vite
pnpm add -D @types/node tw-animate-css
pnpm dlx shadcn@latest init

# 2. Delete v3 config if exists
rm tailwind.config.ts  # v4 doesn't use this file
```

**vite.config.ts**:
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: { alias: { '@': path.resolve(__dirname, './src') } }
})
```

**components.json** (CRITICAL):
```json
{
  "tailwind": {
    "config": "",              // ← Empty for v4
    "css": "src/index.css",
    "baseColor": "slate",
    "cssVariables": true
  }
}
```

---

## The Four-Step Architecture (MANDATORY)

Skipping steps will break your theme. Follow exactly:

### Step 1: Define CSS Variables at Root

```css
/* src/index.css */
@import "tailwindcss";
@import "tw-animate-css";  /* Required for shadcn/ui animations */

:root {
  --background: hsl(0 0% 100%);      /* ← hsl() wrapper required */
  --foreground: hsl(222.2 84% 4.9%);
  --primary: hsl(221.2 83.2% 53.3%);
  /* ... all light mode colors */
}

.dark {
  --background: hsl(222.2 84% 4.9%);
  --foreground: hsl(210 40% 98%);
  --primary: hsl(217.2 91.2% 59.8%);
  /* ... all dark mode colors */
}
```

**Critical**: Define at root level (NOT inside `@layer base`). Use `hsl()` wrapper.

### Step 2: Map Variables to Tailwind Utilities

```css
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  /* ... map ALL CSS variables */
}
```

**Why**: Generates utility classes (`bg-background`, `text-primary`). Without this, utilities won't exist.

### Step 3: Apply Base Styles

```css
@layer base {
  body {
    background-color: var(--background);  /* NO hsl() wrapper here */
    color: var(--foreground);
  }
}
```

**Critical**: Reference variables directly. Never double-wrap: `hsl(var(--background))`.

### Step 4: Result - Automatic Dark Mode

```tsx
<div className="bg-background text-foreground">
  {/* No dark: variants needed - theme switches automatically */}
</div>
```

---

## Dark Mode Setup

**1. Create ThemeProvider** (see `templates/theme-provider.tsx`)

**2. Wrap App**:
```typescript
// src/main.tsx
import { ThemeProvider } from '@/components/theme-provider'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
    <App />
  </ThemeProvider>
)
```

**3. Add Theme Toggle**:
```bash
pnpm dlx shadcn@latest add dropdown-menu
```

See `reference/dark-mode.md` for ModeToggle component.

---

## Critical Rules

### ✅ Always Do:

1. Wrap colors with `hsl()` in `:root`/`.dark`: `--bg: hsl(0 0% 100%);`
2. Use `@theme inline` to map all CSS variables
3. Set `"tailwind.config": ""` in components.json
4. Delete `tailwind.config.ts` if exists
5. Use `@tailwindcss/vite` plugin (NOT PostCSS)

### ❌ Never Do:

1. Put `:root`/`.dark` inside `@layer base`
2. Use `.dark { @theme { } }` pattern (v4 doesn't support nested @theme)
3. Double-wrap colors: `hsl(var(--background))`
4. Use `tailwind.config.ts` for theme (v4 ignores it)
5. Use `@apply` directive (deprecated in v4)
6. Use `dark:` variants for semantic colors (auto-handled)

---

## Common Errors & Solutions

This skill prevents **5 common errors**.

### 1. ❌ tw-animate-css Import Error

**Error**: "Cannot find module 'tailwindcss-animate'"

**Cause**: shadcn/ui deprecated `tailwindcss-animate` for v4.

**Solution**:
```bash
# ✅ DO
pnpm add -D tw-animate-css

# Add to src/index.css:
@import "tailwindcss";
@import "tw-animate-css";

# ❌ DON'T
npm install tailwindcss-animate  # v3 only
```

---

### 2. ❌ Colors Not Working

**Error**: `bg-primary` doesn't apply styles

**Cause**: Missing `@theme inline` mapping

**Solution**:
```css
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  /* ... map ALL CSS variables */
}
```

---

### 3. ❌ Dark Mode Not Switching

**Error**: Theme stays light/dark

**Cause**: Missing ThemeProvider

**Solution**:
1. Create ThemeProvider (see `templates/theme-provider.tsx`)
2. Wrap app in `main.tsx`
3. Verify `.dark` class toggles on `<html>` element

---

### 4. ❌ Duplicate @layer base

**Error**: "Duplicate @layer base" in console

**Cause**: shadcn init adds `@layer base` - don't add another

**Solution**:
```css
/* ✅ Correct - single @layer base */
@import "tailwindcss";

:root { --background: hsl(0 0% 100%); }

@theme inline { --color-background: var(--background); }

@layer base { body { background-color: var(--background); } }
```

---

### 5. ❌ Build Fails with tailwind.config.ts

**Error**: "Unexpected config file"

**Cause**: v4 doesn't use `tailwind.config.ts` (v3 legacy)

**Solution**:
```bash
rm tailwind.config.ts
```

v4 configuration happens in `src/index.css` using `@theme` directive.

---

## Quick Reference

| Symptom | Cause | Fix |
|---------|-------|-----|
| `bg-primary` doesn't work | Missing `@theme inline` | Add `@theme inline` block |
| Colors all black/white | Double `hsl()` wrapping | Use `var(--color)` not `hsl(var(--color))` |
| Dark mode not switching | Missing ThemeProvider | Wrap app in `<ThemeProvider>` |
| Build fails | `tailwind.config.ts` exists | Delete file |
| Animation errors | Using `tailwindcss-animate` | Install `tw-animate-css` |

---

## Tailwind v4 Plugins

Use `@plugin` directive (NOT `require()` or `@import`):

**Typography** (for Markdown/CMS content):
```bash
pnpm add -D @tailwindcss/typography
```
```css
@import "tailwindcss";
@plugin "@tailwindcss/typography";
```
```html
<article class="prose dark:prose-invert">{{ content }}</article>
```

**Forms** (cross-browser form styling):
```bash
pnpm add -D @tailwindcss/forms
```
```css
@import "tailwindcss";
@plugin "@tailwindcss/forms";
```

**Container Queries** (built-in, no plugin needed):
```tsx
<div className="@container">
  <div className="@md:text-lg">Responds to container width</div>
</div>
```

**Common Plugin Errors**:
```css
/* ❌ WRONG - v3 syntax */
@import "@tailwindcss/typography";

/* ✅ CORRECT - v4 syntax */
@plugin "@tailwindcss/typography";
```

---

## Setup Checklist

- [ ] `@tailwindcss/vite` installed (NOT postcss)
- [ ] `vite.config.ts` uses `tailwindcss()` plugin
- [ ] `components.json` has `"config": ""`
- [ ] NO `tailwind.config.ts` exists
- [ ] `src/index.css` follows 4-step pattern:
  - [ ] `:root`/`.dark` at root level (not in @layer)
  - [ ] Colors wrapped with `hsl()`
  - [ ] `@theme inline` maps all variables
  - [ ] `@layer base` uses unwrapped variables
- [ ] ThemeProvider wraps app
- [ ] Theme toggle works

---

## File Templates

Available in `templates/` directory:

- **index.css** - Complete CSS with all color variables
- **components.json** - shadcn/ui v4 config
- **vite.config.ts** - Vite + Tailwind plugin
- **theme-provider.tsx** - Dark mode provider
- **utils.ts** - `cn()` utility

---

## Migration from v3

See `reference/migration-guide.md` for complete guide.

**Key Changes**:
- Delete `tailwind.config.ts`
- Move theme to CSS with `@theme inline`
- Replace `@tailwindcss/line-clamp` (now built-in: `line-clamp-*`)
- Replace `tailwindcss-animate` with `tw-animate-css`
- Update plugins: `require()` → `@plugin`

---

## Reference Documentation

- **architecture.md** - Deep dive into 4-step pattern
- **dark-mode.md** - Complete dark mode implementation
- **common-gotchas.md** - Troubleshooting guide
- **migration-guide.md** - v3 → v4 migration

---

## Official Documentation

- **shadcn/ui Vite Setup**: https://ui.shadcn.com/docs/installation/vite
- **shadcn/ui Tailwind v4**: https://ui.shadcn.com/docs/tailwind-v4
- **Tailwind v4 Docs**: https://tailwindcss.com/docs

---

**Last Updated**: 2026-01-03
**Skill Version**: 2.0.1
**Tailwind v4**: 4.1.18 (Latest)
**Production**: WordPress Auditor (https://wordpress-auditor.webfonts.workers.dev)
