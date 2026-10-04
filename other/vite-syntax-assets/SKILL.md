---
name: vite-syntax-assets
description: >
  Use when importing static assets, using glob imports, configuring the public directory,
  loading Web Workers, or handling WebAssembly modules.
  Prevents incorrect query suffix usage, broken new URL() patterns, and misconfigured public directory paths.
  Covers asset imports, query suffixes (?url, ?raw, ?inline, ?worker), import.meta.glob,
  public directory, JSON imports, WebAssembly ?init, and Web Worker patterns.
  Keywords: asset import, query suffix, ?raw, ?url, ?worker, import.meta.glob, public directory, WebAssembly, Web Worker.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-syntax-assets

## Quick Reference

### Asset Import Behavior

| Environment | Import Result | Example |
|-------------|--------------|---------|
| Development | Unbundled path from root | `/src/img.png` |
| Production | Hashed path in assets dir | `/assets/img.2d8efhg.png` |

```js
import imgUrl from './img.png'
document.getElementById('hero-img').src = imgUrl
```

Assets smaller than `assetsInlineLimit` (default: 4096 bytes / 4 KiB) are inlined as base64 data URLs. Git LFS placeholders are ALWAYS excluded from inlining.

### Query Suffixes Table

| Suffix | Result | Use Case |
|--------|--------|----------|
| `?url` | Resolved URL string | Assets not auto-detected as static |
| `?raw` | File content as string | Shaders, text files, SVGs as markup |
| `?inline` | Force base64 inlining | Small assets you ALWAYS want inlined |
| `?no-inline` | Force separate file | SVGs or small assets you NEVER want inlined |
| `?worker` | Web Worker constructor | Import JS as dedicated worker |
| `?sharedworker` | SharedWorker constructor | Import JS as shared worker |
| `?worker&inline` | Inlined worker (base64) | Workers without separate file |
| `?worker&url` | Worker URL only | When you need the URL, not the constructor |
| `?init` | WASM init function | WebAssembly module import |

### Critical Warnings

**NEVER** use variables or expressions in `import.meta.glob` arguments -- ALWAYS use string literals. Vite performs static analysis at build time and cannot evaluate runtime values.

**NEVER** rely on `new URL(path, import.meta.url)` in SSR code -- `import.meta.url` has different semantics in browsers vs Node.js. This pattern is client-only.

**NEVER** import public directory assets with `import` statements -- reference them as absolute URL paths (`/icon.png`). Public assets are copied as-is without processing.

**ALWAYS** use static strings in `new URL()` patterns -- dynamic expressions prevent Vite from analyzing and transforming the import at build time.

---

## Asset Import Patterns

### Standard Import (Auto-detected Types)

Common image, media, and font types are automatically detected:

```js
import logo from './logo.svg'
import video from './intro.mp4'
import font from './custom.woff2'
```

CSS `url()` references are handled automatically with the same resolution logic.

### Explicit URL Import (`?url`)

For file types NOT in the auto-detected list:

```js
import workletURL from 'extra-scalloped-border/worklet.js?url'
CSS.paintWorklet.addModule(workletURL)
```

### Raw String Import (`?raw`)

```js
import shaderString from './shader.glsl?raw'
```

### `new URL()` Pattern

Uses native ESM for asset resolution:

```js
const imgUrl = new URL('./img.png', import.meta.url).href
```

Supports template literals for dynamic paths (static analysis still applies):

```js
function getImageUrl(name) {
  return new URL(`./dir/${name}.png`, import.meta.url).href
}
```

**Constraints**: The URL string MUST be static or a template literal with a static prefix. Does NOT work with SSR.

### Additional Asset Types (`assetsInclude`)

Register custom file types as assets:

```js
// vite.config.js
export default defineConfig({
  assetsInclude: ['**/*.gltf', '**/*.hdr'],
})
```

---

## Public Directory

| Config | Default | Description |
|--------|---------|-------------|
| `publicDir` | `'public'` | Directory for unprocessed static assets |
| `build.copyPublicDir` | `true` | Copy public dir to outDir on build |

**Behavior**:
- Files served at root `/` during development
- Copied to `dist/` root during build (no hashing, no transforms)
- Reference as absolute paths: `public/icon.png` becomes `/icon.png` in code

**When to use public directory**:
- Files never referenced in source code (e.g., `robots.txt`, `favicon.ico`)
- Files that MUST retain exact filenames (no content hashing)
- Files that need no processing

ALWAYS prefer `import` for assets that ARE referenced in source code -- this enables hashing, tree-shaking, and `assetsInlineLimit` optimization.

---

## JSON Imports

```js
// Full object import
import json from './example.json'

// Named export (tree-shakeable)
import { field } from './example.json'
```

| Config | Default | Description |
|--------|---------|-------------|
| `json.namedExports` | `true` | Enable named imports from JSON |
| `json.stringify` | `'auto'` | Use `JSON.parse()` for performance (auto: >10 KiB) |

---

## Glob Import (`import.meta.glob`)

### Options Table

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `eager` | `boolean` | `false` | Static import instead of lazy `() => import()` |
| `import` | `string` | — | Named export to extract (`'default'`, `'setup'`, etc.) |
| `query` | `string \| object` | — | Custom query suffix (`'?raw'`, `'?url'`, `{ foo: 'bar' }`) |
| `base` | `string` | — | Resolve globs relative to this directory |

### Lazy Loading (Default)

```js
const modules = import.meta.glob('./dir/*.js')
// Result: { './dir/foo.js': () => import('./dir/foo.js'), ... }

for (const path in modules) {
  modules[path]().then((mod) => {
    console.log(path, mod)
  })
}
```

### Eager Loading

```js
const modules = import.meta.glob('./dir/*.js', { eager: true })
// Result: { './dir/foo.js': Module, ... }
```

### Multiple and Negative Patterns

```js
const modules = import.meta.glob(['./dir/*.js', './another/*.js'])
const filtered = import.meta.glob(['./dir/*.js', '!**/bar.js'])
```

### Named Imports (Tree-Shakeable)

```ts
const setups = import.meta.glob('./dir/*.js', { import: 'setup', eager: true })
// Transforms to: import { setup as ... } from './dir/foo.js'
```

Use `import: 'default'` for default exports.

### Custom Queries

```ts
const rawSvgs = import.meta.glob('./dir/*.svg', { query: '?raw', import: 'default' })
const svgUrls = import.meta.glob('./dir/*.svg', { query: '?url', import: 'default' })
const custom = import.meta.glob('./dir/*.js', { query: { foo: 'bar', bar: true } })
```

### Base Path Option

```ts
const modules = import.meta.glob('./**/*.js', { base: './base' })
// Keys: './dir/foo.js' -> resolves to './base/dir/foo.js'
```

Base MUST be a relative directory path or absolute against project root. Aliases and virtual modules are NOT supported as base.

### Glob Caveats

- **Vite-only feature** -- NOT a web or ES standard
- **String literals ONLY** -- NEVER use variables, expressions, or template literals as arguments
- Patterns MUST be relative (`./`), absolute (`/`), or alias paths
- Matching uses `tinyglobby` internally

---

## WebAssembly

### `?init` Import

```js
import init from './example.wasm?init'

init().then((instance) => {
  instance.exports.test()
})
```

### With Import Object

```js
import init from './example.wasm?init'

init({
  imports: {
    someFunc: () => { /* ... */ },
  },
}).then(() => { /* ... */ })
```

### Multiple Instances (URL Import)

```js
import wasmUrl from './example.wasm?url'

const response = await fetch(wasmUrl)
const { module, instance } = await WebAssembly.instantiateStreaming(response)
```

Production: `.wasm` files smaller than `assetsInlineLimit` are inlined as base64.

---

## Web Workers

### Constructor Pattern (Recommended)

```ts
const worker = new Worker(new URL('./worker.js', import.meta.url))

// Module worker
const moduleWorker = new Worker(new URL('./worker.js', import.meta.url), {
  type: 'module',
})
```

**Constraint**: `new URL()` MUST appear directly inside `new Worker()`. All options MUST be static values.

### Query Suffix Pattern

```js
import MyWorker from './worker?worker'
const worker = new MyWorker()

// Inline (base64)
import InlineWorker from './worker?worker&inline'

// URL only
import workerUrl from './worker?worker&url'
```

Worker scripts can use ESM `import` statements (native in dev, compiled for production).

---

## Asset Configuration Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `assetsInlineLimit` | `number \| function` | `4096` | Base64 inline threshold in bytes |
| `assetsInclude` | `string \| RegExp \| array` | — | Additional file types treated as assets |
| `publicDir` | `string \| false` | `'public'` | Static asset directory served at root |
| `base` | `string` | `'/'` | Public base path for all assets |
| `build.assetsDir` | `string` | `'assets'` | Output subdirectory for generated assets |
| `build.copyPublicDir` | `boolean` | `true` | Copy public dir contents to outDir |

### HTML Asset Elements

Vite processes asset references in these HTML elements: `<script src>`, `<link href>`, `<img src>`, `<img srcset>`, `<video src>`, `<video poster>`, `<audio src>`, `<source src>`, `<embed src>`, `<object data>`, `<track src>`, `<input src>`, `<meta content>`.

Add the `vite-ignore` attribute to any HTML element to skip asset processing for that element.

---

## Reference Links

- [references/import-patterns.md](references/import-patterns.md) -- Complete import suffix reference, glob options, worker patterns
- [references/examples.md](references/examples.md) -- Working code examples for assets, glob, JSON, WebAssembly, workers
- [references/anti-patterns.md](references/anti-patterns.md) -- Common asset handling mistakes and how to avoid them

### Official Sources

- https://vite.dev/guide/assets
- https://vite.dev/guide/features#glob-import
- https://vite.dev/guide/features#json
- https://vite.dev/guide/features#web-workers
- https://vite.dev/guide/features#webassembly
- https://vite.dev/config/shared-options#publicdir
- https://vite.dev/config/build-options#build-assetsinlinelimit
