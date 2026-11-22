---
name: ts-pnpm-workflow
description: 'Adopt pnpm as the package manager or migrate from npm (install, lockfile, scripts). Use when starting a Node project or migrating an npm project to pnpm.'
disable-model-invocation: true
metadata:
  opencode/autoinvoke: 'false'
---

## Prerequisites

A `package.json` at the project root.

## Steps

1. **Install** — if `pnpm --version` fails: `corepack enable pnpm`, else `npm install -g pnpm`
2. **Clean npm artifacts** — delete `package-lock.json` and `node_modules/`
3. **Pin** — set `"packageManager": "pnpm@<version>"` in `package.json` (update if it already exists)
4. **`.npmrc`** — create it only if the project needs pnpm settings; do not add `shamefully-hoist` unless a dependency breaks without it
5. **Scripts** — replace `npm run <x>` with `pnpm <x>` in `package.json` scripts
6. **Install and verify** — `pnpm install` (generates `pnpm-lock.yaml`), then `pnpm build`

## Gotchas

- `preinstall`/`postinstall` lifecycle scripts can behave differently under pnpm — verify they run
- Commit `pnpm-lock.yaml`; make sure `package-lock.json` is removed from tracking
- Update CI to use pnpm

Report: summary, files changed, verify commands (`pnpm build`, `pnpm test`).
