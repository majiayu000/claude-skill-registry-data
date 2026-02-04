---
name: typescript-default-lib
description: Install a default set of commonly used libraries when initializing a new TypeScript Node.js project (or retrofitting an existing one). Use when a user asks to "create a TypeScript project" and wants the standard dependencies installed (p-map, p-retry, luxon, lodash-es, winston, prisma + @prisma/client, ioredis, express, dotenv) plus common tooling (rimraf, tsc-alias) with optional @types packages and Prisma init.
---

# TypeScript Default Lib

Install (latest) versions of a standard dependency set for TypeScript + Node.js backends.

## Quick start

- Run the installer from your project root (must contain `package.json`):
  - `bash /home/harry/.codex/skills/typescript-default-lib/scripts/install_default_libs.sh`
  - Add Prisma scaffolding too: `bash /home/harry/.codex/skills/typescript-default-lib/scripts/install_default_libs.sh --init-prisma`

## What gets installed

**Dependencies**
- `p-map`
- `p-retry`
- `luxon`
- `lodash-es`
- `winston`
- `ioredis`
- `express`
- `dotenv`
- `@prisma/client`

**Dev dependencies**
- `prisma`
- `rimraf`
- `tsc-alias`
- `@types/express` (unless `--no-types`)
- `@types/lodash-es` (unless `--no-types`)

## Manual install commands (no script)

Use these if you don’t want to run the script:

- **npm**
  - `npm i p-map p-retry luxon lodash-es winston ioredis express dotenv @prisma/client`
  - `npm i -D prisma rimraf tsc-alias @types/express @types/lodash-es`
  - `npx prisma init` (optional)

- **pnpm**
  - `pnpm add p-map p-retry luxon lodash-es winston ioredis express dotenv @prisma/client`
  - `pnpm add -D prisma rimraf tsc-alias @types/express @types/lodash-es`
  - `pnpm prisma init` (optional)

- **yarn**
  - `yarn add p-map p-retry luxon lodash-es winston ioredis express dotenv @prisma/client`
  - `yarn add -D prisma rimraf tsc-alias @types/express @types/lodash-es`
  - `yarn prisma init` (optional)

## Notes / gotchas

- `p-map`, `p-retry`, and `lodash-es` are ESM-first; avoid compiling your app to CommonJS unless you plan to use dynamic `import()` or switch to TS `module` settings compatible with ESM (e.g. `NodeNext`/`Bundler`).
- Prisma best practice: keep `prisma` as a dev dependency; ship `@prisma/client` as a runtime dependency.
- `tsc-alias` is useful when you compile with `tsc` and rely on `paths` aliases; run it after `tsc` to rewrite emitted import paths.

### scripts/
Contains `scripts/install_default_libs.sh`.
