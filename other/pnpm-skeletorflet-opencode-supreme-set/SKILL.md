---
name: pnpm
description: pnpm — fast, disk-efficient package manager with workspace monorepo and content-addressable store.
---

## pnpm

### Workspace Monorepo
- `pnpm-workspace.yaml`: `packages: - 'apps/*' - 'packages/*'` — define workspace members.
- Local dependencies: `"@repo/ui": "workspace:*"` — resolved from workspace.
- `pnpm add` respects workspace protocol; `pnpm publish` rewrites `workspace:` semver.

### Content-Addressable Store
- Single global store (`~/.pnpm-store`) — deduplicated by content hash.
- Hard links inside `node_modules` — saves disk space across projects.
- `pnpm store prune` — remove unreferenced packages; `pnpm store status` — check integrity.

### Dependency Resolution
- Strict hoisting: only direct deps in `node_modules/.pnpm` — prevents phantom dependencies.
- `pnpm.overrides` in `package.json` — force version resolution.
- `pnpm.peerDependencyRules.allowedVersions` — allow specific peer ranges.
- `.npmrc` — `shamefully-hoist=true` for legacy compat.

### Filter & Recursive
- `pnpm --filter <name> add dep` — scoped to workspace member.
- `pnpm -r build` — run across all packages; `pnpm -r --parallel` — concurrent.
- `pnpm --filter "{packages/*}..."` — glob filters with dependents graph.

### Publishing
- `pnpm publish --recursive` — publish changed packages.
- `pnpm pack` — create tarball; `pnpm publish --dry-run` — preview.
- Package patching: `pnpm patch <pkg>` / `pnpm patch-commit <dir>`.
