---
name: configuring-tailwind-v4
description: Configure Tailwind CSS v4 using Vite plugin, PostCSS, or CLI with CSS-first configuration via @import and @theme directives. Use when setting up new projects or migrating build tools.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Configuring Tailwind v4

## Purpose

Configure Tailwind CSS v4 using modern CSS-first configuration. Tailwind v4 eliminates JavaScript configuration files in favor of CSS-based setup using `@import` and `@theme` directives.

## Installation Methods

### Vite Projects (Recommended)

**Step 1: Install Dependencies**

```bash
npm install tailwindcss @tailwindcss/vite
```

**Step 2: Configure Vite Plugin**

Add the Tailwind plugin to `vite.config.js`:

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```

**Step 3: Import Tailwind in CSS**

Create or update your main CSS file (e.g., `src/index.css`):

```css
@import 'tailwindcss';
```

### PostCSS Projects

**Step 1: Install Dependencies**

```bash
npm install tailwindcss @tailwindcss/postcss
```

**Step 2: Configure PostCSS**

Create `postcss.config.js`:

```javascript
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
};
```

**Step 3: Import Tailwind in CSS**

```css
@import 'tailwindcss';
```

### CLI Usage

**Step 1: Install CLI**

```bash
npm install tailwindcss @tailwindcss/cli
```

**Step 2: Create Input CSS**

```css
@import 'tailwindcss';
```

**Step 3: Run Build Command**

```bash
npx @tailwindcss/cli -i input.css -o output.css --watch
```

## CSS-First Configuration

Tailwind v4 uses the `@theme` directive for all customization:

```css
@import 'tailwindcss';

@theme {
  --font-display: 'Satoshi', 'sans-serif';
  --font-body: 'Inter', 'sans-serif';

  --color-brand-primary: oklch(0.65 0.25 270);
  --color-brand-accent: oklch(0.75 0.22 320);

  --breakpoint-3xl: 120rem;
  --breakpoint-4xl: 160rem;

  --spacing-18: 4.5rem;
  --spacing-72: 18rem;

  --radius-4xl: 2rem;

  --shadow-brutal: 8px 8px 0 0 rgb(0 0 0);
}
```

## Automatic Content Detection

Template files are discovered automatically using built-in heuristics. No content array configuration required. Files in `.gitignore` are automatically excluded.

**Manual Source Control (when needed):**

```css
@import 'tailwindcss';

@source "../node_modules/@my-company/ui-lib";
@source "./legacy-components";
```

**Exclude paths:**

```css
@source not "./legacy";
@source not "./docs";
```

**Disable automatic detection:**

```css
@import 'tailwindcss' source(none);
@source "./src";
```

## Key Differences from v3

| v3 | v4 |
|---|---|
| `tailwind.config.js` | CSS `@theme` directive |
| `@tailwind base;` | `@import 'tailwindcss';` |
| `content: []` array | Automatic detection |
| `postcss-tailwindcss` | `@tailwindcss/postcss` |

## Performance

- Full builds: **3.78x faster** than v3
- Incremental rebuilds with new CSS: **8.8x faster**
- Incremental rebuilds without new CSS: **182x faster**

## Browser Requirements

Tailwind v4 requires:
- Safari 16.4+
- Chrome 111+
- Firefox 128+

Projects requiring older browser support must stay on v3.4.

## See Also

- references/vite-setup.md - Complete Vite configuration examples
- references/postcss-setup.md - PostCSS configuration patterns
- references/nextjs-setup.md - Next.js specific setup
