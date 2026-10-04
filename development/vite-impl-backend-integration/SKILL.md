---
name: vite-impl-backend-integration
description: >
  Use when integrating Vite with a backend framework, rendering Vite assets from server-side
  templates, or setting up dev/production HTML serving.
  Prevents incorrect manifest.json traversal and missing CSS chunk resolution in production.
  Covers build.manifest configuration, .vite/manifest.json structure, ManifestChunk properties,
  dev mode HTML setup, production rendering, CSS/JS chunk resolution, and modulepreload polyfill.
  Keywords: backend integration, manifest.json, ManifestChunk, Django, Laravel, Rails, modulepreload.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-impl-backend-integration

## Quick Reference

### When This Skill Applies

Use this skill when:
- Integrating Vite with a backend framework (Django, Laravel, Rails, Express, ASP.NET, etc.)
- Rendering Vite-built assets from server-side templates
- Setting up dev/production HTML serving for a non-SPA architecture
- Reading `.vite/manifest.json` to resolve hashed asset paths

### Architecture Overview

| Concern | Development | Production |
|---------|------------|------------|
| Asset serving | Vite dev server (localhost:5173) | Static files from `dist/` |
| HTML generation | Backend injects Vite client + entry scripts | Backend reads manifest.json, renders tags |
| HMR | Automatic via `@vite/client` | N/A |
| CSS | Injected by Vite dev server | Extracted as separate files |
| Entry resolution | Direct source path | Hashed filename from manifest |

### Critical Warnings

**NEVER** omit `import 'vite/modulepreload-polyfill'` from your entry point -- without it, `<link rel="modulepreload">` tags will not work in browsers that lack native support.

**NEVER** hardcode hashed filenames in production templates -- ALWAYS read `.vite/manifest.json` at runtime or build time. Hashed names change on every build.

**NEVER** serve the Vite dev server scripts in production -- ALWAYS use environment detection to switch between dev mode HTML and production manifest rendering.

**NEVER** omit the React preamble when using `@vitejs/plugin-react` with a backend -- HMR will silently fail without it.

**ALWAYS** set `build.manifest: true` in `vite.config.ts` when integrating with a backend framework.

**ALWAYS** set `server.cors` to allow your backend origin during development.

**ALWAYS** specify `build.rollupOptions.input` (Vite 6/7) or `build.rolldownOptions.input` (Vite 8+) to define your entry point explicitly.

---

## Configuration

### vite.config.ts (Backend Integration)

```typescript
import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    cors: {
      origin: 'http://my-backend.example.com',
    },
  },
  build: {
    manifest: true,
    // Vite 6/7:
    rollupOptions: {
      input: '/path/to/main.js',
    },
    // Vite 8+:
    // rolldownOptions: {
    //   input: '/path/to/main.js',
    // },
  },
})
```

### Entry Point Setup

ALWAYS add the modulepreload polyfill as the first import in your entry file:

```javascript
// main.js
import 'vite/modulepreload-polyfill'

// Rest of your application code
import './styles/app.css'
import { createApp } from './app'

createApp()
```

---

## Development Mode

### HTML Template (Dev)

In development, your backend template MUST include two scripts pointing to the Vite dev server:

```html
<!-- Backend template: development mode -->
<html>
  <head>
    <!-- No CSS links needed -- Vite injects CSS via JS in dev -->
  </head>
  <body>
    <div id="app"></div>

    <!-- 1. Vite client for HMR -->
    <script type="module" src="http://localhost:5173/@vite/client"></script>

    <!-- 2. Your entry point -->
    <script type="module" src="http://localhost:5173/main.js"></script>
  </body>
</html>
```

### React Preamble (Dev Only)

When using `@vitejs/plugin-react`, ALWAYS inject the React Refresh preamble BEFORE the Vite client script:

```html
<!-- React preamble: MUST come before @vite/client -->
<script type="module">
  import RefreshRuntime from 'http://localhost:5173/@react-refresh'
  RefreshRuntime.injectIntoGlobalHook(window)
  window.$RefreshReg$ = () => {}
  window.$RefreshSig$ = () => (type) => type
  window.__vite_plugin_react_preamble_installed__ = true
</script>

<!-- Then Vite client -->
<script type="module" src="http://localhost:5173/@vite/client"></script>

<!-- Then entry -->
<script type="module" src="http://localhost:5173/main.js"></script>
```

---

## Production Mode

### Manifest Location

After running `vite build`, the manifest file is located at:

```
dist/.vite/manifest.json
```

### ManifestChunk Properties

| Property | Type | Description |
|----------|------|-------------|
| `src` | `string` | Original source file path |
| `file` | `string` | Hashed output file path |
| `css` | `string[]` | CSS files associated with this chunk |
| `assets` | `string[]` | Non-JS/CSS assets imported by this chunk |
| `isEntry` | `boolean` | Whether this is an entry point |
| `name` | `string` | Short name of the chunk |
| `isDynamicEntry` | `boolean` | Whether this is a dynamic import entry |
| `imports` | `string[]` | Keys of statically imported chunks |
| `dynamicImports` | `string[]` | Keys of dynamically imported chunks |

### Rendering Order (CRITICAL)

For each entry point, ALWAYS render tags in this exact order:

1. `<link rel="stylesheet">` for the entry chunk's own CSS files
2. `<link rel="stylesheet">` for all recursively imported chunks' CSS files
3. `<script type="module">` for the entry chunk's JS file
4. `<link rel="modulepreload">` for all recursively imported JS chunks

```html
<!-- 1. Entry CSS -->
<link rel="stylesheet" href="/dist/assets/main-5UjPuW-k.css" />
<!-- 2. Imported chunks' CSS (recursive) -->
<link rel="stylesheet" href="/dist/assets/shared-ChJ_j-JJ.css" />
<!-- 3. Entry JS -->
<script type="module" src="/dist/assets/main-BRBmoGS9.js"></script>
<!-- 4. Modulepreload for imported JS -->
<link rel="modulepreload" href="/dist/assets/shared-B7PI925R.js" />
```

### Manifest Traversal Algorithm

Use this recursive algorithm to collect all imported chunks (prevents duplicates via `seen` Set):

```typescript
import type { Manifest, ManifestChunk } from 'vite'

export default function importedChunks(
  manifest: Manifest,
  name: string,
): ManifestChunk[] {
  const seen = new Set<string>()

  function getImportedChunks(chunk: ManifestChunk): ManifestChunk[] {
    const chunks: ManifestChunk[] = []
    for (const file of chunk.imports ?? []) {
      const importee = manifest[file]
      if (seen.has(file)) continue
      seen.add(file)
      chunks.push(...getImportedChunks(importee))
      chunks.push(importee)
    }
    return chunks
  }

  return getImportedChunks(manifest[name])
}
```

---

## Dev vs Production Switching

### Decision Tree

```
Is this a development environment?
├─ YES → Inject Vite dev server scripts into HTML
│        ├─ Using React? → Add React preamble FIRST
│        ├─ Add @vite/client script
│        └─ Add entry point script
└─ NO  → Read .vite/manifest.json
         ├─ Look up entry chunk by source path
         ├─ Collect CSS from entry + recursive imports
         ├─ Render <link rel="stylesheet"> tags
         ├─ Render <script type="module"> for entry
         └─ Render <link rel="modulepreload"> for imports
```

### Server-Side Switching Pattern

```python
# Example: Python/Django-style pseudocode
def vite_tags(entry: str) -> str:
    if settings.DEBUG:
        return dev_tags(entry)
    else:
        return production_tags(entry)

def dev_tags(entry: str) -> str:
    return f'''
        <script type="module" src="http://localhost:5173/@vite/client"></script>
        <script type="module" src="http://localhost:5173/{entry}"></script>
    '''

def production_tags(entry: str) -> str:
    manifest = load_manifest('dist/.vite/manifest.json')
    chunk = manifest[entry]
    imported = get_imported_chunks(manifest, entry)
    tags = []
    # 1. Entry CSS
    for css in chunk.get('css', []):
        tags.append(f'<link rel="stylesheet" href="/dist/{css}" />')
    # 2. Imported CSS
    for imp in imported:
        for css in imp.get('css', []):
            tags.append(f'<link rel="stylesheet" href="/dist/{css}" />')
    # 3. Entry JS
    tags.append(f'<script type="module" src="/dist/{chunk["file"]}"></script>')
    # 4. Modulepreload
    for imp in imported:
        tags.append(f'<link rel="modulepreload" href="/dist/{imp["file"]}" />')
    return '\n'.join(tags)
```

---

## Reference Links

- [references/manifest-reference.md](references/manifest-reference.md) -- ManifestChunk interface, manifest.json structure, traversal algorithm details
- [references/examples.md](references/examples.md) -- Complete dev HTML, production rendering, React preamble examples
- [references/anti-patterns.md](references/anti-patterns.md) -- Common backend integration mistakes and how to avoid them

### Official Sources

- https://vite.dev/guide/backend-integration.html
- https://vite.dev/config/build-options.html#build-manifest
- https://vite.dev/config/server-options.html#server-cors
