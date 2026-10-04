---
name: setup-tsup
description: Set up tsup (esbuild-based bundler) for a TypeScript package. Use when you need single-file bundled output, faster builds, and better startup time for Node.js CLIs or libraries. Covers tsup config, bin entry point, package.json scripts, and keeping tsc for type-checking only.
---

# Set Up tsup Build

## Goal

Replace or add `tsup` as the build tool for a TypeScript package. Keep `tsc --noEmit` for type-checking only.

## Why

- Single-file bundled output = 2-5x faster startup (fewer fs reads during module resolution)
- Tree-shakes unused code from dependencies
- esbuild-based = sub-second builds vs multi-second tsc

## Steps

### 1. Install tsup

```bash
pnpm add -D tsup
```

### 2. Create tsup.config.ts

```ts
import { defineConfig } from 'tsup'

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['esm'],
  target: 'node22',
  clean: true,
  splitting: false,
  sourcemap: true,
  dts: false,
  // For CLIs: add shebang
  banner: {
    js: '#!/usr/bin/env node',
  },
  // Native/dynamic deps that shouldn't be bundled
  external: [],
})
```

For libraries (not CLIs), remove the `banner` and consider `dts: true` for declaration files.

### 3. Update package.json scripts

```json
{
  "scripts": {
    "build": "tsup",
    "dev": "tsup --watch",
    "ts:check": "tsc --noEmit"
  }
}
```

### 4. Update bin entry point (CLIs only)

The bin file should point to the tsup output. tsup outputs to `dist/` by default:

- Verify the `bin` field references `dist/index.js` (or `dist/index.mjs`)
- Since tsup adds the shebang via `banner`, the bin file can point directly to the bundled output

### 5. Verify

```bash
pnpm build           # Should produce dist/index.js (single file)
pnpm ts:check        # Type checking still works
node dist/index.js --help  # CLI works (if applicable)
```

### 6. Update .gitignore

Ensure `dist/` is in `.gitignore`.

## Gotchas

- If any dependency uses `__dirname` or `require.resolve`, tsup may need those deps in `external`
- Dynamic `import()` calls are preserved by esbuild — this is fine
- Keep `prepare` or `prepublishOnly` script as `pnpm build` for npm publish workflow
- For ESM packages, ensure `"type": "module"` in package.json
