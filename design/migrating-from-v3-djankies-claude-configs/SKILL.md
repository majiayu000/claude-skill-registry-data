---
name: migrating-from-v3
description: Migrate from Tailwind CSS v3 to v4 including configuration migration (JS to CSS), utility renames, opacity changes, and color system updates. Use when upgrading existing projects to v4.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Migrating from v3 to v4

## Purpose

Migrate existing Tailwind CSS v3 projects to v4's CSS-first configuration, updated utilities, and modern color system.

## Automated Migration Tool

Tailwind provides an automated upgrade tool:

```bash
npx @tailwindcss/upgrade@next
```

**Requirements:**
- Node.js 20 or higher
- Run in a new git branch
- Review all changes manually
- Test thoroughly

**What it handles:**
- Updates dependencies
- Migrates configuration to CSS
- Updates template files
- Converts utility class names

**What it doesn't handle:**
- Custom plugins (manual migration needed)
- Complex configuration logic
- Dynamic class generation

## Configuration Migration

### JavaScript Config → CSS Theme

**v3 (tailwind.config.js):**

```javascript
module.exports = {
  content: ['./src/**/*.{html,js}'],
  theme: {
    extend: {
      colors: {
        brand: '#3b82f6',
        accent: '#a855f7',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Satoshi', 'sans-serif'],
      },
      spacing: {
        18: '4.5rem',
        72: '18rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
    },
  },
  plugins: [],
};
```

**v4 (CSS @theme):**

```css
@import 'tailwindcss';

@theme {
  --font-sans: 'Inter', sans-serif;
  --font-display: 'Satoshi', sans-serif;

  --color-brand: oklch(0.65 0.25 270);
  --color-accent: oklch(0.65 0.25 320);

  --spacing-18: 4.5rem;
  --spacing-72: 18rem;

  --radius-4xl: 2rem;
}
```

### Content Detection

**v3:**

```javascript
content: ['./src/**/*.{html,js,jsx,ts,tsx}']
```

**v4:**

Automatic detection. No configuration needed.

**Manual control (if needed):**

```css
@import 'tailwindcss';
@source "../packages/ui";
@source not "./legacy";
```

### Import Syntax Changes

**v3:**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**v4:**

```css
@import 'tailwindcss';
```

## Utility Class Renames

### Opacity Modifiers

**v3:**

```html
<div class="bg-black bg-opacity-50"></div>
<div class="text-gray-900 text-opacity-75"></div>
<div class="border-blue-500 border-opacity-60"></div>
```

**v4:**

```html
<div class="bg-black/50"></div>
<div class="text-gray-900/75"></div>
<div class="border-blue-500/60"></div>
```

**Migration pattern:**

- `bg-opacity-{value}` → `bg-{color}/{value}`
- `text-opacity-{value}` → `text-{color}/{value}`
- `border-opacity-{value}` → `border-{color}/{value}`

### Flex Utilities

**v3:**

```html
<div class="flex-shrink-0"></div>
<div class="flex-shrink"></div>
<div class="flex-grow-0"></div>
<div class="flex-grow"></div>
```

**v4:**

```html
<div class="shrink-0"></div>
<div class="shrink"></div>
<div class="grow-0"></div>
<div class="grow"></div>
```

**Migration pattern:**

- `flex-shrink-*` → `shrink-*`
- `flex-grow-*` → `grow-*`

### Shadow Utilities

**v3:**

```html
<div class="shadow-sm"></div>
```

**v4:**

```html
<div class="shadow-xs"></div>
```

**Migration:**

- `shadow-sm` → `shadow-xs`
- All other shadow utilities remain the same

### Ring Width

**v3 default:**

```html
<input class="ring" />
```

Ring width: 3px

**v4 default:**

```html
<input class="ring" />
```

Ring width: 1px

**To keep v3 behavior:**

```html
<input class="ring-3" />
```

## Color System Changes

### Default Border and Ring Colors

**v3:**

```html
<div class="border"></div>
```

Border color: gray-200

**v4:**

```html
<div class="border"></div>
```

Border color: currentColor

**To keep v3 behavior:**

```html
<div class="border border-gray-200"></div>
```

### OkLCh Color Space

**v3 (RGB):**

```javascript
colors: {
  brand: '#3b82f6',
}
```

**v4 (OkLCh):**

```css
@theme {
  --color-brand: oklch(0.65 0.25 270);
}
```

Use conversion tool: https://oklch.com/

## PostCSS Configuration

### Plugin Changes

**v3:**

```javascript
module.exports = {
  plugins: {
    'tailwindcss': {},
    'autoprefixer': {},
  },
};
```

**v4:**

```javascript
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
};
```

No longer need `autoprefixer` or `postcss-import`.

### Vite Plugin

**v3:**

```javascript
import tailwindcss from 'tailwindcss';
import autoprefixer from 'autoprefixer';

export default defineConfig({
  css: {
    postcss: {
      plugins: [tailwindcss(), autoprefixer()],
    },
  },
});
```

**v4:**

```javascript
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [tailwindcss()],
});
```

## Preflight Changes

### Placeholder Colors

**v3:**

Placeholder text: gray-400

**v4:**

Placeholder text: currentColor at 50% opacity

**To keep v3 behavior:**

```css
@layer base {
  ::placeholder {
    color: theme('colors.gray.400');
  }
}
```

### Button Cursor

**v3:**

```css
button {
  cursor: pointer;
}
```

**v4:**

```css
button {
  cursor: default;
}
```

**To restore v3 behavior:**

```css
@layer base {
  button {
    cursor: pointer;
  }
}
```

## Feature Additions

### Built-in Container Queries

**v3 (plugin required):**

```javascript
plugins: [require('@tailwindcss/container-queries')]
```

**v4 (built-in):**

No plugin needed. Use `@container` and `@{breakpoint}:` syntax.

### 3D Transforms

**v3:**

Not available

**v4:**

```html
<div class="transform-3d rotate-x-45 rotate-y-30 translate-z-12"></div>
```

### Starting Variant for Animations

**v3:**

Not available

**v4:**

```html
<div class="opacity-100 starting:opacity-0 transition-opacity"></div>
```

## Breaking Changes Checklist

- [ ] Update dependencies to v4
- [ ] Migrate tailwind.config.js to @theme
- [ ] Replace @tailwind directives with @import
- [ ] Update PostCSS configuration
- [ ] Convert opacity utilities (bg-opacity → bg-{color}/{value})
- [ ] Rename flex utilities (flex-shrink → shrink)
- [ ] Update shadow-sm to shadow-xs
- [ ] Add explicit border colors if using bare `border`
- [ ] Update ring-3 if expecting 3px default
- [ ] Convert hex colors to oklch()
- [ ] Remove container-queries plugin (now built-in)
- [ ] Test placeholder colors
- [ ] Test button cursor behavior
- [ ] Update arbitrary value syntax (spaces → underscores)

## Migration Strategy

### Phase 1: Preparation

1. Create new git branch
2. Ensure all changes committed
3. Run automated migration tool
4. Review generated changes

### Phase 2: Configuration

1. Convert tailwind.config.js to CSS @theme
2. Update PostCSS/Vite configuration
3. Replace @tailwind directives
4. Add @source if needed

### Phase 3: Utilities

1. Search and replace opacity modifiers
2. Rename flex utilities
3. Update shadow utilities
4. Add explicit border colors
5. Convert hex colors to oklch()

### Phase 4: Testing

1. Test all pages/components
2. Verify responsive behavior
3. Check dark mode
4. Test interactive states
5. Validate production build

### Phase 5: Cleanup

1. Remove unused dependencies
2. Delete tailwind.config.js
3. Update documentation
4. Commit changes

## Common Issues

### Styles Not Applying

Check:
1. CSS import: `@import "tailwindcss";`
2. PostCSS plugin: `@tailwindcss/postcss`
3. Vite plugin: `@tailwindcss/vite`
4. Template files not in .gitignore

### Class Names Not Working

Ensure:
1. Class names are complete strings
2. Not using dynamic concatenation
3. Using underscores for spaces in arbitrary values

### Colors Look Different

OkLCh uses different color space. Convert hex to oklch using:
https://oklch.com/

### Build Errors

Check:
1. Node.js version (20+)
2. Dependencies updated
3. PostCSS config using correct plugin

## See Also

- references/breaking-changes.md - Complete breaking changes list
- references/migration-checklist.md - Step-by-step migration guide
