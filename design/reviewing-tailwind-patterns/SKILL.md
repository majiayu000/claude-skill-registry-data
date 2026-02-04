---
name: reviewing-tailwind-patterns
description: Review Tailwind CSS v4 patterns for configuration, theming, and utility usage. Use when reviewing CSS files, Vite configs, or components using Tailwind.
review: true
allowed-tools: Read, Grep, Glob
---

# Reviewing Tailwind v4 Patterns

## Purpose

Review Tailwind CSS v4 implementations for correct configuration, modern patterns, and best practices.

## Review Checklist

### Configuration Review

**Check build tool configuration:**

- [ ] Using `@tailwindcss/vite` for Vite projects (preferred over PostCSS)
- [ ] Using `@tailwindcss/postcss` for other build tools
- [ ] No `tailwind.config.js` file (v4 uses CSS configuration)
- [ ] PostCSS config uses correct plugin name (`@tailwindcss/postcss`)
- [ ] Not using deprecated plugins (autoprefixer, postcss-import)

**Vite config pattern:**

```javascript
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```

**PostCSS config pattern:**

```javascript
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
};
```

### CSS File Review

**Check import syntax:**

- [ ] Using `@import 'tailwindcss';` (not @tailwind directives)
- [ ] @theme directive present for customization
- [ ] Theme variables use correct namespaces
- [ ] Colors use oklch() format (not hex or rgb)
- [ ] @keyframes defined within @theme (not outside)

**Correct pattern:**

```css
@import 'tailwindcss';

@theme {
  --font-sans: 'Inter', sans-serif;
  --color-primary: oklch(0.65 0.25 270);
  --spacing-18: 4.5rem;

  @keyframes fade-in {
    0% { opacity: 0; }
    100% { opacity: 1; }
  }
}
```

**Anti-patterns:**

```css
@tailwind base;

@theme {
  --color-primary: #3b82f6;
}

@keyframes fade-in {
  0% { opacity: 0; }
  100% { opacity: 1; }
}
```

### Theme Variables Review

**Check namespace usage:**

- [ ] Color variables use `--color-*` prefix
- [ ] Font families use `--font-*` prefix
- [ ] Spacing uses `--spacing-*` prefix
- [ ] Border radius uses `--radius-*` prefix
- [ ] Animations use `--animate-*` prefix
- [ ] Semantic naming over generic scales

**Good pattern:**

```css
@theme {
  --color-primary: oklch(0.65 0.25 270);
  --color-secondary: oklch(0.75 0.22 320);
  --color-success: oklch(0.72 0.15 142);
  --color-error: oklch(0.65 0.22 25);
}
```

**Anti-pattern:**

```css
@theme {
  --primary: oklch(0.65 0.25 270);
  --blue: oklch(0.75 0.22 320);
  --my-color: oklch(0.72 0.15 142);
}
```

### Color Format Review

**Check color definitions:**

- [ ] Using oklch() format (not hex, rgb, or hsl)
- [ ] Lightness between 0-1
- [ ] Chroma between 0-0.4
- [ ] Hue between 0-360

**Correct:**

```css
--color-brand: oklch(0.65 0.25 270);
```

**Incorrect:**

```css
--color-brand: #3b82f6;
--color-accent: rgb(168, 85, 247);
--color-success: hsl(142, 76%, 36%);
```

### Utility Usage Review

**Check for v3 patterns:**

- [ ] No `bg-opacity-*` utilities (use `bg-{color}/{opacity}`)
- [ ] No `flex-shrink-*` (use `shrink-*`)
- [ ] No `flex-grow-*` (use `grow-*`)
- [ ] No `shadow-sm` (use `shadow-xs`)
- [ ] Explicit border colors (not bare `border`)
- [ ] Explicit ring widths if expecting 3px (use `ring-3`)

**v4 patterns:**

```html
<div class="bg-black/50"></div>
<div class="shrink-0 grow"></div>
<div class="shadow-xs"></div>
<div class="border border-gray-200"></div>
<input class="ring-3 ring-blue-500" />
```

**v3 anti-patterns:**

```html
<div class="bg-black bg-opacity-50"></div>
<div class="flex-shrink-0 flex-grow"></div>
<div class="shadow-sm"></div>
<div class="border"></div>
<input class="ring" />
```

### Container Query Review

**Check container query usage:**

- [ ] Parent has `@container` or `@container/{name}`
- [ ] Container breakpoints use `@` prefix
- [ ] Named containers use consistent naming
- [ ] Mixing container and viewport queries correctly

**Correct pattern:**

```html
<div class="@container/main">
  <div class="grid-cols-1 @md/main:grid-cols-2 @lg/main:grid-cols-3"></div>
</div>
```

**Anti-pattern:**

```html
<div>
  <div class="grid-cols-1 @md:grid-cols-2"></div>
</div>
```

### Custom Utility Review

**Check @utility usage:**

- [ ] Using `@utility` (not `@layer utilities`)
- [ ] Using `--value()` functions correctly
- [ ] Supporting arbitrary values when appropriate
- [ ] Providing variant support

**Correct pattern:**

```css
@utility tab-* {
  tab-size: --value(--tab-size- *);
  tab-size: --value(integer);
  tab-size: --value([integer]);
}
```

**Anti-pattern:**

```css
@layer utilities {
  .tab-4 {
    tab-size: 4;
  }
}
```

### Animation Review

**Check animation patterns:**

- [ ] @keyframes defined within @theme
- [ ] Animation variables use `--animate-*` prefix
- [ ] Animation shorthand includes timing
- [ ] Using `starting:` variant for entry animations

**Correct pattern:**

```css
@theme {
  --animate-fade-in: fade-in 0.3s ease-out;

  @keyframes fade-in {
    0% { opacity: 0; }
    100% { opacity: 1; }
  }
}
```

**Anti-pattern:**

```css
@keyframes fade-in {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

@theme {
  --animate-fade-in: fade-in;
}
```

### Component Pattern Review

**Check component reusability:**

- [ ] Components use container queries for portability
- [ ] Semantic color names (not numbered scales)
- [ ] Responsive utilities applied appropriately
- [ ] Dark mode variants when needed

**Good pattern:**

```html
<div class="@container">
  <article class="bg-white dark:bg-gray-900 rounded-lg p-4 @md:p-6">
    <h2 class="text-lg @md:text-xl font-bold text-primary">Title</h2>
    <p class="text-sm @md:text-base text-gray-600 dark:text-gray-300">Content</p>
  </article>
</div>
```

### Source Detection Review

**Check content detection:**

- [ ] No manual content array (automatic detection)
- [ ] Using `@source` only when needed
- [ ] Excluding unnecessary directories with `@source not`
- [ ] node_modules in .gitignore

**When to use @source:**

```css
@source "../packages/ui";
@source not "./legacy";
```

**Don't do this:**

```css
@import 'tailwindcss' source(none);
@source "./src/**/*.{html,js,jsx,ts,tsx}";
```

## Common Issues to Flag

### High Priority

1. **Using v3 syntax** - Opacity utilities, flex utilities
2. **Wrong import syntax** - `@tailwind` instead of `@import`
3. **Hex colors in theme** - Should use oklch()
4. **Wrong PostCSS plugin** - Should be `@tailwindcss/postcss`
5. **Missing @container** - Container queries without parent

### Medium Priority

1. **Non-semantic color names** - Using numbered scales
2. **Bare border/ring classes** - May render unexpectedly
3. **@keyframes outside @theme** - Won't generate utilities
4. **Wrong namespace prefixes** - Won't generate correct utilities
5. **Using @layer utilities** - Should use @utility

### Low Priority

1. **No dark mode variants** - May be intentional
2. **Mixing viewport and container queries** - May be correct
3. **Arbitrary values** - Sometimes necessary
4. **Not using Vite plugin** - PostCSS is valid alternative

## Review Process

1. **Check configuration** - Vite/PostCSS setup
2. **Review CSS file** - Import syntax, @theme, @utility
3. **Scan components** - Utility patterns, container queries
4. **Test build** - Verify compilation
5. **Visual check** - Confirm styles apply correctly

## Review Report Template

```markdown
## Tailwind v4 Review

### Configuration
- [ ] Build tool: [Vite/PostCSS/Other]
- [ ] Using correct plugin
- [ ] No v3 config file

### CSS
- [ ] Correct import syntax
- [ ] Theme variables properly namespaced
- [ ] Colors using oklch()
- [ ] Animations within @theme

### Components
- [ ] Container queries used correctly
- [ ] Semantic naming
- [ ] No v3 utility patterns

### Issues Found
1. [Priority] [Description]
2. [Priority] [Description]

### Recommendations
- [Specific recommendation]
- [Specific recommendation]
```

## See Also

- All other skills in tailwind-4 plugin for detailed patterns
- RESEARCH.md for comprehensive v4 documentation
