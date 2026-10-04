---
name: vite-impl-library-mode
description: >
  Use when building a library, creating an npm package, configuring UMD/ESM/CJS output,
  or setting up package.json exports.
  Prevents bundling peer dependencies into the library or misconfiguring output formats.
  Covers build.lib configuration, external dependencies, output formats (es, cjs, umd, iife),
  CSS handling, multiple entry points, vite-plugin-dts, and package.json exports.
  Keywords: build.lib, library mode, npm package, external, UMD, ESM, CJS, vite-plugin-dts, exports.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-impl-library-mode

## Quick Reference

### build.lib Configuration Options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `entry` | `string \| string[] \| Record<string, string>` | YES | Entry point(s) for the library |
| `name` | `string` | UMD/IIFE only | Global variable name exposed on `window` |
| `fileName` | `string \| ((format, entryName) => string)` | NO | Output file name (auto-adds format extension) |
| `formats` | `('es' \| 'cjs' \| 'umd' \| 'iife')[]` | NO | Output formats (see defaults below) |
| `cssFileName` | `string` | NO | Custom CSS output filename |

### Default Output Formats

| Entry Type | Default Formats | Reason |
|-----------|-----------------|--------|
| Single entry | `['es', 'umd']` | UMD provides browser/Node compatibility |
| Multiple entries | `['es', 'cjs']` | CJS for Node, ES for bundlers |

### Critical Warnings

**ALWAYS** set `name` when using `umd` or `iife` formats -- this defines the global variable name (e.g., `window.MyLib`). Builds FAIL without it.

**ALWAYS** externalize peer dependencies (React, Vue, Angular, etc.) -- bundling them causes version conflicts and bloated packages.

**NEVER** rely on `build.assetsDir` in library mode -- it has NO effect. Assets are placed alongside output files.

**NEVER** import CSS at the library entry point and expect consumers to get it automatically -- CSS is extracted to a separate file that consumers MUST import explicitly.

**ALWAYS** use `rolldownOptions.external` in Vite 8.x and `rollupOptions.external` in Vite 6.x/7.x -- the option name changed with the bundler migration.

---

## Decision Tree: Library Mode Setup

```
Need to build an npm package with Vite?
├── YES → Set build.lib with entry point
│   ├── Single entry point?
│   │   ├── YES → entry: resolve(import.meta.dirname, 'lib/main.ts')
│   │   │   ├── Need browser global (UMD)? → Set name + formats: ['es', 'umd']
│   │   │   └── ESM only? → Set formats: ['es']
│   │   └── NO (multiple entries) → entry: { name: 'path', ... }
│   │       └── Default formats: ['es', 'cjs']
│   ├── Has peer dependencies (React, Vue, etc.)?
│   │   └── YES → Add to rolldownOptions.external + output.globals (UMD)
│   ├── Has CSS?
│   │   └── YES → Set cssFileName, add export to package.json
│   └── Need TypeScript declarations?
│       └── YES → Install vite-plugin-dts
└── NO → Use standard Vite app build
```

---

## Minimal Library Configuration

### TypeScript Library (ESM + UMD)

```typescript
// vite.config.ts
import { resolve } from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    lib: {
      entry: resolve(import.meta.dirname, 'lib/main.ts'),
      name: 'MyLib',
      fileName: 'my-lib',
    },
    rolldownOptions: {  // Vite 8.x — use rollupOptions for Vite 6.x/7.x
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
        },
      },
    },
  },
})
```

### JavaScript Library (ESM only)

```javascript
// vite.config.js
import { resolve } from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    lib: {
      entry: resolve(import.meta.dirname, 'lib/main.js'),
      formats: ['es'],
    },
    rolldownOptions: {
      external: ['vue'],
    },
  },
})
```

---

## External Dependencies

### Why Externalize

Peer dependencies (frameworks, large utilities) MUST be externalized to:
- Prevent version conflicts when consumer has their own copy
- Reduce bundle size
- Avoid duplicate framework instances (causes crashes in React, Vue)

### Pattern: Externalize All Dependencies

```typescript
// vite.config.ts — externalize everything in dependencies + peerDependencies
import pkg from './package.json' with { type: 'json' }

export default defineConfig({
  build: {
    rolldownOptions: {
      external: [
        ...Object.keys(pkg.dependencies ?? {}),
        ...Object.keys(pkg.peerDependencies ?? {}),
      ],
    },
  },
})
```

### UMD Globals Mapping

When using UMD format, ALWAYS provide `output.globals` for every external dependency:

```typescript
rolldownOptions: {
  external: ['react', 'react-dom', 'lodash'],
  output: {
    globals: {
      react: 'React',
      'react-dom': 'ReactDOM',
      lodash: '_',
    },
  },
}
```

---

## Multiple Entry Points

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    lib: {
      entry: {
        'my-lib': resolve(import.meta.dirname, 'lib/main.ts'),
        utils: resolve(import.meta.dirname, 'lib/utils.ts'),
        components: resolve(import.meta.dirname, 'lib/components.ts'),
      },
    },
    rolldownOptions: {
      external: ['react', 'react-dom'],
    },
  },
})
```

Matching package.json exports:

```json
{
  "exports": {
    ".": {
      "import": "./dist/my-lib.js",
      "require": "./dist/my-lib.cjs"
    },
    "./utils": {
      "import": "./dist/utils.js",
      "require": "./dist/utils.cjs"
    },
    "./components": {
      "import": "./dist/components.js",
      "require": "./dist/components.cjs"
    }
  }
}
```

---

## CSS in Library Mode

CSS imported in library source is extracted to a separate file. It is NOT injected automatically.

```typescript
// vite.config.ts
build: {
  lib: {
    entry: resolve(import.meta.dirname, 'lib/main.ts'),
    name: 'MyLib',
    fileName: 'my-lib',
    cssFileName: 'my-lib',  // outputs dist/my-lib.css
  },
}
```

Consumers MUST import CSS explicitly:
```typescript
import 'my-lib/style.css'
```

---

## DTS Generation

Vite does NOT generate `.d.ts` files. ALWAYS use `vite-plugin-dts` for TypeScript libraries:

```bash
npm add -D vite-plugin-dts
```

```typescript
// vite.config.ts
import dts from 'vite-plugin-dts'

export default defineConfig({
  plugins: [dts()],
  build: {
    lib: {
      entry: resolve(import.meta.dirname, 'lib/main.ts'),
      formats: ['es'],
    },
  },
})
```

---

## Recommended package.json

### Single Entry (ESM + UMD)

```json
{
  "name": "my-lib",
  "version": "1.0.0",
  "type": "module",
  "files": ["dist"],
  "main": "./dist/my-lib.umd.cjs",
  "module": "./dist/my-lib.js",
  "types": "./dist/main.d.ts",
  "exports": {
    ".": {
      "types": "./dist/main.d.ts",
      "import": "./dist/my-lib.js",
      "require": "./dist/my-lib.umd.cjs"
    },
    "./style.css": "./dist/my-lib.css"
  },
  "peerDependencies": {
    "react": "^18.0.0 || ^19.0.0",
    "react-dom": "^18.0.0 || ^19.0.0"
  }
}
```

### ESM-Only Library

```json
{
  "name": "my-lib",
  "version": "1.0.0",
  "type": "module",
  "files": ["dist"],
  "module": "./dist/my-lib.js",
  "types": "./dist/main.d.ts",
  "exports": {
    ".": {
      "types": "./dist/main.d.ts",
      "import": "./dist/my-lib.js"
    }
  }
}
```

---

## Version Differences

| Feature | Vite 6.x / 7.x | Vite 8.x |
|---------|----------------|----------|
| External deps config | `rollupOptions.external` | `rolldownOptions.external` |
| UMD globals | `rollupOptions.output.globals` | `rolldownOptions.output.globals` |
| Build engine | Rollup | Rolldown |
| Behavior | Identical | Identical |

ALWAYS check which Vite version the project uses and apply the correct option name.

---

## Reference Links

- [references/config-options.md](references/config-options.md) -- Complete build.lib options and package.json exports patterns
- [references/examples.md](references/examples.md) -- Working examples: single entry, multiple entries, CSS handling, DTS
- [references/anti-patterns.md](references/anti-patterns.md) -- Common library mode mistakes and how to avoid them

### Official Sources

- https://vite.dev/guide/build.html#library-mode
- https://vite.dev/config/build-options.html#build-lib
- https://www.npmjs.com/package/vite-plugin-dts
