---
name: typescript-library
# prettier-ignore
description: Use when developing TypeScript npm packages including tsconfig, package.json exports, dual CJS/ESM builds, and publishing
---

# TypeScript Library Development

## Quick Start

```json
// package.json
{
  "name": "my-library",
  "version": "1.0.0",
  "type": "module",
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": { "types": "./dist/index.d.ts", "default": "./dist/index.js" },
      "require": { "types": "./dist/index.d.cts", "default": "./dist/index.cjs" }
    }
  },
  "files": ["dist"]
}
```

## tsconfig.json Essentials

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "dist",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src"],
  "exclude": ["**/*.test.ts"]
}
```

## Key Practices

- **Exports field**: Required for proper ESM/CJS dual support
- **Types first**: In conditional exports, `types` must come before `default`
- **Files array**: Only publish what's needed (dist, README, LICENSE)
- **Declaration maps**: Enable go-to-definition in consuming projects
- **Peer dependencies**: For frameworks/libraries users must also install

## Publishing Checklist

1. Update version in package.json
2. Build: `npm run build`
3. Test the package: `npm pack` and inspect tarball
4. Publish: `npm publish` (or `npm publish --access public` for scoped)

## Common Tools

- **tsup**: Zero-config bundler for TypeScript libraries
- **unbuild**: Build system with automatic CJS/ESM
- **changesets**: Version management and changelogs

## Reference Files

- [references/tsconfig.md](references/tsconfig.md) - tsconfig options explained
- [references/exports.md](references/exports.md) - Package exports patterns
- [references/publishing.md](references/publishing.md) - npm publishing workflow
