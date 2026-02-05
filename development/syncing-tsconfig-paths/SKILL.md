---
name: syncing-tsconfig-paths
description: Synchronizes tsconfig.json paths from package.json imports field. Ensures TypeScript resolves subpath imports (#imports) correctly during development.
---

# Syncing TSConfig Paths

Keep tsconfig paths in sync with package.json subpath imports.

## Steps

### Syncing

```bash
pnpm exec tsx .claude/skills/syncing-tsconfig-paths/scripts/sync-tsconfig-paths.ts
```

### Auditing

Run with `--check` flag to verify without modifying:
```bash
pnpm exec tsx .claude/skills/syncing-tsconfig-paths/scripts/sync-tsconfig-paths.ts --check
```

## Reference

The script transforms package.json imports to tsconfig paths:

```json
// package.json
{
  "imports": {
    "#pkg": "./build/_.js",
    "#foo": "./build/foo.js"
  }
}
```

Becomes:

```json
// tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "#pkg": ["./src/_.ts"],
      "#foo": ["./src/foo.ts"]
    }
  }
}
```

Key transformation: `./build/` → `./src/` (extension stays `.js` - TypeScript with nodenext resolves to `.ts`)

## Notes

- Run after modifying any package's `imports` field
- Conditional imports (objects with browser/default) are skipped with a warning
- This enables TypeScript to resolve `#` imports during development before build
