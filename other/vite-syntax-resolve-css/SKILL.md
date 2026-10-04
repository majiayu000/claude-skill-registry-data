---
name: vite-syntax-resolve-css
description: >
  Use when configuring path aliases, CSS modules, CSS preprocessors, PostCSS,
  Lightning CSS, or module resolution behavior.
  Prevents resolve.alias misconfiguration breaking imports and CSS preprocessor
  options not matching the installed preprocessor version.
  Covers resolve.alias, resolve.dedupe, resolve.conditions, resolve.extensions,
  resolve.tsconfigPaths, css.modules, css.postcss, css.preprocessorOptions
  (Sass/Less/Stylus), css.transformer, css.lightningcss, css.devSourcemap,
  json.namedExports, json.stringify, and html.cspNonce.
  Keywords: vite, resolve, alias, CSS modules, PostCSS, Lightning CSS, Sass, preprocessor.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-syntax-resolve-css

## Quick Reference — resolve.* Options

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `resolve.alias` | `Record<string, string> \| Array<{ find, replacement }>` | — | Path aliases for imports |
| `resolve.dedupe` | `string[]` | — | Force single copy of listed deps |
| `resolve.conditions` | `string[]` | `['module', 'browser', 'development\|production']` | Conditional exports resolution |
| `resolve.mainFields` | `string[]` | `['browser', 'module', 'jsnext:main', 'jsnext']` | package.json entry fields |
| `resolve.extensions` | `string[]` | `['.mjs', '.js', '.mts', '.ts', '.jsx', '.tsx', '.json']` | Auto-resolved extensions |
| `resolve.preserveSymlinks` | `boolean` | `false` | Use original path for identity |
| `resolve.tsconfigPaths` | `boolean` | `false` | Enable tsconfig `paths` resolution |

### resolve.conditions — SSR vs Client

| Context | Default Conditions |
|---------|-------------------|
| Client | `['module', 'browser', 'development\|production']` |
| SSR | `['module', 'node', 'development\|production']` |

`'development|production'` is automatically replaced based on `NODE_ENV`.

## Quick Reference — css.* Options

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `css.modules` | `CSSModulesOptions` | — | CSS Modules behavior config |
| `css.postcss` | `string \| PostCSSConfig` | — | Inline PostCSS config or config path |
| `css.preprocessorOptions` | `Record<string, object>` | — | Sass/Less/Stylus options |
| `css.preprocessorMaxWorkers` | `number \| true` | `true` (CPUs - 1) | Max preprocessor threads |
| `css.devSourcemap` | `boolean` | `false` | Experimental: dev sourcemaps |
| `css.transformer` | `'postcss' \| 'lightningcss'` | `'postcss'` | CSS processing engine |
| `css.lightningcss` | `LightningCSSOptions` | — | Lightning CSS config (targets, drafts, etc.) |

## Quick Reference — json.* and html.* Options

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `json.namedExports` | `boolean` | `true` | Named imports from .json files |
| `json.stringify` | `boolean \| 'auto'` | `'auto'` | Convert to JSON.parse() (>10kB with 'auto') |
| `html.cspNonce` | `string` | — | Nonce placeholder for script/style tags |

---

## Critical Warnings

**NEVER** add `resolve.tsconfigPaths: true` without considering the performance cost. The TypeScript team discourages this feature due to its overhead. Prefer explicit `resolve.alias` entries instead.

**NEVER** omit extensions from `resolve.extensions` for custom types like `.vue`. ALWAYS import `.vue` files with the explicit extension.

**NEVER** install Vite plugins for CSS preprocessors. ALWAYS install only the preprocessor package itself (`sass-embedded`, `less`, or `stylus`). Vite handles integration automatically.

**NEVER** use `css.modules` options when `css.transformer` is set to `'lightningcss'`. ALWAYS use `css.lightningcss.cssModules` instead — the `css.modules` config has no effect with Lightning CSS.

**NEVER** set `html.cspNonce` to a static value in production. ALWAYS replace the nonce placeholder per-request on the server for actual security.

---

## Resolve Alias Patterns

### Object Format (Simple)

```typescript
import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  resolve: {
    alias: {
      '@': resolve(import.meta.dirname, 'src'),
      '@components': resolve(import.meta.dirname, 'src/components'),
      '@utils': resolve(import.meta.dirname, 'src/utils'),
    },
  },
})
```

### Array Format (Supports Regex)

```typescript
export default defineConfig({
  resolve: {
    alias: [
      { find: '@', replacement: resolve(import.meta.dirname, 'src') },
      { find: /^@lib\/(.*)/, replacement: resolve(import.meta.dirname, 'lib/$1') },
    ],
  },
})
```

ALWAYS use the array format when regex matching is needed. The object format does NOT support regex patterns.

---

## CSS Modules Pattern

### File Naming Convention

ALWAYS use the `.module.css` suffix for CSS Modules. This is the ONLY pattern Vite recognizes:

```
component.module.css      ← CSS Module
component.module.scss     ← CSS Module with Sass
component.css             ← Regular CSS (NOT a module)
```

### Usage

```typescript
import classes from './Button.module.css'

document.getElementById('btn').className = classes.primary
```

### Named Imports with localsConvention

```typescript
// vite.config.ts
export default defineConfig({
  css: {
    modules: {
      localsConvention: 'camelCaseOnly',
    },
  },
})
```

```typescript
// With camelCaseOnly, kebab-case class names become camelCase
import { applyColor } from './example.module.css'
```

---

## CSS Preprocessor Setup

### Installation (No Plugins Needed)

```bash
# Sass (recommended: sass-embedded for performance)
npm add -D sass-embedded
# OR: npm add -D sass

# Less
npm add -D less

# Stylus
npm add -D stylus
```

### Preprocessor Options

```typescript
export default defineConfig({
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@/styles/variables" as *;`,
      },
      less: {
        math: 'parens-division',
      },
      stylus: {
        define: { isProd: process.env.NODE_ENV === 'production' },
      },
    },
  },
})
```

### Key Behaviors

- `@import` in preprocessors respects `resolve.alias` paths
- URL references in imported files are automatically rebased to correct paths
- Combine preprocessors with CSS Modules: `style.module.scss`

---

## Lightning CSS Setup

```bash
npm add -D lightningcss
```

```typescript
import { browserslistToTargets } from 'lightningcss'

export default defineConfig({
  css: {
    transformer: 'lightningcss',
    lightningcss: {
      targets: browserslistToTargets(browserslist('>= 0.25%')),
      drafts: { customMedia: true },
      cssModules: {
        pattern: '[name]_[local]_[hash]',
      },
    },
  },
  build: {
    cssMinify: 'lightningcss',
  },
})
```

ALWAYS set `build.cssMinify: 'lightningcss'` when using `css.transformer: 'lightningcss'` to ensure consistent processing in both dev and build.

---

## PostCSS Configuration

### Auto-Detection (Recommended)

Vite auto-detects PostCSS config from standard config files (`postcss.config.js`, `.postcssrc.json`, etc.). No Vite config needed.

### Inline Config

```typescript
export default defineConfig({
  css: {
    postcss: {
      plugins: [
        autoprefixer(),
        tailwindcss(),
      ],
    },
  },
})
```

### Path to Config Directory

```typescript
export default defineConfig({
  css: {
    postcss: './config',  // looks for postcss.config.js in ./config/
  },
})
```

---

## CSS Import Control

### ?inline Query — Prevent Injection

```typescript
import styles from './tooltip.css?inline'
// styles is a string, NOT injected into the page
// Use for shadow DOM or manual insertion
```

### @import Inlining

Vite pre-configures `postcss-import` for CSS `@import` inlining. All `url()` references in imported files are automatically rebased to maintain correct paths.

---

## JSON Import Patterns

```typescript
// Full import
import pkg from './package.json'
console.log(pkg.version)

// Named import (tree-shakeable when json.namedExports: true)
import { version, name } from './package.json'
```

With `json.stringify: 'auto'` (default), JSON files larger than 10kB are converted to `JSON.parse("...")` for faster parsing at runtime.

---

## CSP Nonce Configuration

```typescript
export default defineConfig({
  html: {
    cspNonce: 'NONCE_PLACEHOLDER',
  },
})
```

Vite adds `nonce="NONCE_PLACEHOLDER"` to all generated `<script>` and `<style>` tags, and injects a `<meta property="csp-nonce" nonce="NONCE_PLACEHOLDER" />` tag. ALWAYS replace the placeholder with a unique value per request on the server.

---

## Decision Trees

### Which Alias Format?

```
Need regex matching?
├── YES → Use array format with { find: /regex/, replacement: '...' }
└── NO → Use object format { '@': '/src' } (simpler)
```

### Which CSS Transformer?

```
Need modern CSS features (nesting, custom media, color functions)?
├── YES → css.transformer: 'lightningcss' + build.cssMinify: 'lightningcss'
└── NO
    Need PostCSS plugins (Tailwind, Autoprefixer)?
    ├── YES → css.transformer: 'postcss' (default)
    └── NO → Default postcss is fine
```

### CSS Modules Config Location?

```
Using Lightning CSS?
├── YES → Configure in css.lightningcss.cssModules
└── NO → Configure in css.modules
```

### Preprocessor Installation?

```
Which preprocessor?
├── Sass → npm add -D sass-embedded (or sass)
├── Less → npm add -D less
└── Stylus → npm add -D stylus
Then: NO plugin installation needed. Vite detects automatically.
```

---

## Reference Links

- [references/config-options.md](references/config-options.md) — All resolve.*, css.*, json.*, html.* options with types and defaults
- [references/examples.md](references/examples.md) — Aliases, CSS Modules, preprocessors, Lightning CSS, PostCSS examples
- [references/anti-patterns.md](references/anti-patterns.md) — Common resolve and CSS configuration mistakes

### Official Sources

- https://vite.dev/config/shared-options.html#resolve-alias
- https://vite.dev/config/shared-options.html#css-modules
- https://vite.dev/config/shared-options.html#css-preprocessoroptions
- https://vite.dev/guide/features.html#css
- https://vite.dev/config/shared-options.html#json-namedexports
- https://vite.dev/config/shared-options.html#html-cspnonce
