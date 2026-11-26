---
name: tech-stack-typescript
description: TypeScript/JavaScript stack context — package manager build and test commands (Vitest, Jest), Prisma and Drizzle guidance, React, React Native/Expo, Next.js, Tauri and Node patterns.
license: MIT
compatibility:
  - claude-code
  - codex
type: tech-stack
user-invocable: false
---

# Tech Stack: TypeScript

## Overview

TypeScript/JavaScript context for the workflow skills and review agents: commands, detection markers, the data-layer and framework rules that bite (React, React Native/Expo, Next.js, Tauri, Node), settings and scan recipes. Generic framework practice is assumed, not restated. JavaScript-only projects use the same skill; the type rules become recommendations.

## When To Use

Loaded automatically when the active tech stack is `typescript`; never invoked directly.

## Build & Test Commands

`setup-bootstrap` writes the detected package manager to `.claude/tech-stack-pm`; `<pm>` below is that value. Detection, first match wins:

```bash
if [ -f bun.lock ] || [ -f bun.lockb ]; then echo bun
elif [ -f pnpm-lock.yaml ]; then echo pnpm
elif [ -f yarn.lock ]; then echo yarn
else echo npm   # package-lock.json, or package.json only
fi
```

- **Install:** `<pm> install`
- **Type check (compile-equivalent):** `<pm> run typecheck` if defined in `package.json`, else `npx tsc --noEmit --pretty false` (or `tsc -b` for project references)
- **Build:** `<pm> run build` (verifies full toolchain — bundler, type check, assets)
- **Test (batch):** `<pm> test <path/to/file>` or `<pm> run test -- <pattern>` (vitest/jest support filter flags; check `package.json` scripts)
- **Test (full):** `<pm> test` or `<pm> run test`
- **Bounded output is the default.** Pass `--reporter=dot` (vitest) or `--silent` (jest) where the runner supports it. Batch checkpoints run these through `bash scripts/mtk-verify-run.sh --label <batch-id>-<step> -- <cmd>` — the wrapper's bounded tail is the evidence, the log path is the receipt.
- **Format:** see `## Format Command`.
- **Lint:** `<pm> run lint` if defined, else `npx eslint <path>` or `npx biome check <path>` based on project config. Always ignore `node_modules` explicitly on the command line (`oxlint --ignore-pattern node_modules`) — oxlint reads it from `.gitignore` only inside a git repo, and its config `ignorePatterns` does not stop the walk. To tell new errors from pre-existing ones, lint the changed files and keep only errors on lines the diff touched (`git diff -U0`).

**Tauri (when `src-tauri/` exists):** from `src-tauri/`, `cargo check` (fast) or `cargo build`, `cargo test`, `cargo fmt`, `cargo clippy -- -D warnings`; full app `<pm> run tauri dev` / `<pm> run tauri build`.

## File Extensions & Markers

How `setup-bootstrap` detects this stack in a repository:

| Marker | Confidence |
|---|---|
| `package.json` | High |
| `tsconfig.json` | High (TypeScript-specific) |
| `bun.lock`, `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json` | Medium (package manager signal) |
| `src-tauri/Cargo.toml` | Tauri sidecar |
| `next.config.{js,ts,mjs}` | Next.js project |
| `vite.config.{js,ts}` | Vite-based (React, Vue, Svelte) |
| `react-native` / `expo` in `package.json` deps | React Native / Expo project |
| `app.json`, `app.config.{js,ts}` | Expo config |
| `metro.config.{js,ts}` | React Native (Metro bundler) |

Detection command:
```bash
find . -maxdepth 2 -name "package.json" -not -path "*/node_modules/*" 2>/dev/null | head -1
test -f tsconfig.json && echo "typescript"
test -f src-tauri/Cargo.toml && echo "has-tauri-sidecar"
grep -qE '"(react-native|expo)"' package.json 2>/dev/null && echo "has-react-native"
ls app.json app.config.js app.config.ts metro.config.js metro.config.ts 2>/dev/null
```

## ORM & Data Layer Guidance

Match the ORM the project already uses. The rules that cause real defects:

- **Prisma:** run `prisma generate` after every schema change (stale types otherwise); `PrismaClient` is server-only (Next.js: server actions, route handlers, server components) and a module-level singleton in serverless; `select` over `include` on read-heavy queries; `prisma migrate deploy` in CI/prod, `migrate dev` locally.
- **Drizzle:** review `drizzle-kit` generated SQL before applying; it can read a rename as drop + add.
- **Schema changes** ship expand-then-contract (`.claude/references/schema-migrations.md`): no drop, rename, type narrowing or `NOT NULL` on existing rows in the same deploy as code that still uses the old shape. Run every down path before merging; where the tool generates none, write the rollback SQL.
- **TanStack Query:** `queryKey` arrays must be stable (`['resource', id, filters]`; a fresh object literal per render is a refetch loop); set `staleTime` explicitly; never mirror server state into `useState`.
- **Test provider:** SQLite does not validate Postgres behavior (JSONB, arrays, `ILIKE`, partial indexes, advisory locks). Use `testcontainers` or an ephemeral Postgres when semantics matter.

## Framework Patterns

- **React — never set state after an `await` in a mutation callback.** The `await` yields; anything set afterwards races what the user did meanwhile. Commit the selection first, then refetch:
  ```ts
  onSuccess: (saved) => {
    setSelectedId(saved.id)
    void queryClient.invalidateQueries({ queryKey: ['templates'] })
  }
  ```
  With the order reversed, a user who pressed "New" during the await gets a blank form whose next save **renames the record they left**. It needs two operations in one session, so e2e tests find it and unit tests do not.
- **React:** browser APIs (`window`, `localStorage`) only inside `useEffect` or behind `typeof window !== 'undefined'`, or SSR breaks.
- **React Native / Expo:** no DOM or web APIs; tokens and secrets in `expo-secure-store`, never AsyncStorage (unencrypted); long lists in `FlatList`/`SectionList` with a stable `keyExtractor`, never `.map()` in a `ScrollView`; know whether the app is managed or a dev build before adding native modules (`expo prebuild` / EAS, not Expo Go).
- **Next.js:** Server Actions are public HTTP endpoints; validate input and identity in every one. Push `'use client'` down to the leaf that needs it.
- **Tauri:** each `#[tauri::command]` is the trust boundary; validate inputs Rust-side. Grant v2 capabilities (`src-tauri/capabilities/*.json`) narrowly, never `$HOME/**` or `"windows": ["*"]`; a `tauri.conf.json` `allowlist` means the app is still on v1. Sign updater releases.
- **Node backends:** validate request shape at the boundary (Zod, Valibot, TypeBox); every external call carries an explicit timeout; never return raw exception text to clients.

## Test Level Guidance

Match existing conventions (runner, file placement). Component tests query by role and accessible name; integration tests mock the network with MSW, not internal modules; E2E uses Playwright. React Native uses `@testing-library/react-native` with `jest-expo`, and Detox or Maestro on device, never browser E2E. Details and the MSW cookie trap: `.claude/references/typescript/testing-supplement.md`.

## Coding Style Reference

Path: `.claude/references/typescript/coding-guidelines.md` — a placeholder (`status: placeholder`, not shipped by bootstrap) until the team writes real guidelines. Until then: strict `tsconfig.json` (`strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`), `unknown` over `any` at boundaries, `import type` for type-only imports, ESM only, named exports.

## Analyzer Configuration

`.claude/references/typescript/analyzer-config.md` carries the strict tsconfig and Biome rules. Type check with analyzer capture:
```bash
npx tsc --noEmit 2>&1 | bash "${CLAUDE_PLUGIN_ROOT}/hooks/parse-build-diagnostics.sh" --format tsc > .mtk/analyzer-output.json
```

## Recommended Tooling

`docs/recommended-tooling/typescript.md` (with `docs/recommended-tooling/shared.md`): `context7`, `playwright` MCP, TypeScript and Biome language servers. `setup-bootstrap` prints both; install is manual.

## Reference Files

Loaded by commands and review agents when the active stack is `typescript`:

- `.claude/references/typescript/coding-guidelines.md` — TypeScript style guide (placeholder until written)
- `.claude/references/typescript/testing-supplement.md` — Vitest / Jest / Testing Library / Playwright / MSW
- `.claude/references/typescript/analyzer-config.md` — strict tsconfig and Biome rules
- `docs/recommended-tooling/typescript.md` — recommended MCPs, plugins and editor integrations

The data-layer and framework rules live in this skill (`## ORM & Data Layer Guidance`, `## Framework Patterns`).

## Settings Additions

`setup-bootstrap` merges these, after `.claude/references/settings-baseline.md`, into the project's `permissions.allow` / `permissions.deny` (never an `allowedTools` key).

### allow (merge: union)
- `Bash(bun:*)`
- `Bash(pnpm:*)`
- `Bash(yarn:*)`
- `Bash(npm:*)`
- `Bash(npx:*)`
- `Bash(node:*)`
- `Bash(tsc:*)`
- `Bash(cargo:*)` — only if `src-tauri/` exists

### deny (merge: union)
- `Read(**/.env.production)`
- `Read(**/.env.local)`
- `Bash(*publish*)` — npm publish requires explicit approval

### hooks (do NOT add)

`format-on-edit.sh` is wired by the plugin's own `hooks/hooks.json`. Bootstrap never copies an MTK hook into the target's `settings.json`; `setup-bootstrap` Settings Merge says why.

## Format Command

```bash
npx biome format --write <file>   # or
npx prettier --write <file>
```

At flush the hook picks biome, else prettier, by what is installed, once per edited `.ts/.tsx/.js/.jsx/.mjs/.cjs` file (deduped; files deleted during the turn dropped). Failures log to stderr and never block.

## Pre-Commit Review Items

Tool-keyed items for the generated `pre-commit-review-list.md`; `setup-bootstrap` keeps those whose tool the scan detected.

- [React] Rules of Hooks, SSR-safe browser access, stable list keys
- [React Native / Expo] no DOM/web APIs, secrets in `expo-secure-store` not AsyncStorage, `FlatList` over `.map()` in `ScrollView`
- [Next.js] `'use client'` at the boundary, server actions validated, `next/image` / `next/font` over raw tags
- [Tauri] minimal v2 capability files (no broad scopes, no `"windows": ["*"]`), every `#[tauri::command]` validates input
- [Prisma / Drizzle] `select` projection over `include`, indexes on foreign keys, paginated list queries
- [TanStack Query] explicit `staleTime`, stable `queryKey`, no server-state duplication in `useState`

## Scan Recipes

Used by `setup-audit` when auditing a TypeScript repository.

### Dependency Registry Verification

Before planning the install of any npm package not already in `package.json`, verify it exists and is the real one (criterion 0 of `.claude/references/dependency-intake-checklist.md`). Not found, or a typosquat-like name, is an immediate block; an unverified AI-recommended package is tagged `[ASSUMED]` with a `checkpoint:human-verify` step before any install.

```bash
npm view <pkg> name version time.modified
```

### Project Structure
```bash
find . -maxdepth 2 \( -name "package.json" -o -name "tsconfig*.json" \) -not -path "*/node_modules/*" 2>/dev/null | head -10
ls bun.lock bun.lockb pnpm-lock.yaml yarn.lock package-lock.json 2>/dev/null; test -f src-tauri/Cargo.toml && echo "Tauri sidecar"
find . -maxdepth 2 \( -name "pnpm-workspace.yaml" -o -name "turbo.json" -o -name "nx.json" -o -name "lerna.json" \) 2>/dev/null
find . -type d -maxdepth 3 -not -path "*/node_modules/*" -not -path "*/.next/*" -not -path "*/dist/*" -not -path "*/build/*" -not -path "*/.git/*" | sort
```

### Patterns In Use
```bash
grep -oE '"(next|react|vite|react-native|expo|@tauri-apps/[a-z-]+|express|fastify|hono|@nestjs/core)"' package.json 2>/dev/null | sort -u
grep -rlE "from ['\"](zustand|jotai|valtio|mobx|redux|@tanstack/react-query|swr|@trpc|zod|valibot|yup|io-ts|@sinclair/typebox)" --include="*.ts" --include="*.tsx" 2>/dev/null | head -10
```

### Data Layer
```bash
find . -name "schema.prisma" -not -path "*/node_modules/*" 2>/dev/null | head -5; find . -name "drizzle.config.*" -not -path "*/node_modules/*" 2>/dev/null
grep -rlE "from ['\"](drizzle-orm|@prisma/client|typeorm|mikro-orm|kysely)" --include="*.ts" 2>/dev/null | head -5
find . -path "*/migrations/*" -not -path "*/node_modules/*" \( -name "*.sql" -o -name "*.ts" \) 2>/dev/null | head -10
grep -rnE "DATABASE_URL|PGUSER|POSTGRES_|DB_HOST" --include="*.ts" --include="*.env*" 2>/dev/null | head -5
grep -rnE "\.findMany\(|\.findFirst\(|\binclude:|\bselect:" --include="*.ts" 2>/dev/null | head -10
```

### Infrastructure
```bash
grep -rlE "from ['\"](@aws-sdk/|firebase|@google-cloud/)" --include="*.ts" 2>/dev/null | head -10
find . -maxdepth 3 \( -name "Dockerfile" -o -name "docker-compose*" -o -name "serverless.*" -o -name "cdk.json" -o -name "vercel.json" -o -name "netlify.toml" -o -name "wrangler.toml" -o -name "tauri.conf.json" \) -not -path "*/node_modules/*" 2>/dev/null
```

### Naming Conventions
```bash
find . -type f \( -name "route.ts" -o -name "page.tsx" -o -name "layout.tsx" \) -not -path "*/node_modules/*" | head -10
find . -path "*/api/*" -name "*.ts" -not -path "*/node_modules/*" | head -10
find . -name "*.tsx" -not -path "*/node_modules/*" -not -path "*/.next/*" | sed 's|.*/||' | head -20
```

### Testing Patterns
```bash
grep -oE '"(vitest|jest|jest-expo|@playwright/test|cypress|detox|msw|@testing-library/[a-z-]+)"' package.json 2>/dev/null | sort -u
find . -maxdepth 2 \( -name "vitest.config.*" -o -name "jest.config.*" -o -name "playwright.config.*" \) 2>/dev/null
find . -type f \( -name "*.test.ts" -o -name "*.test.tsx" -o -name "*.spec.ts" -o -name "*.spec.tsx" \) -not -path "*/node_modules/*" | head -10
```

### Configuration
```bash
grep -h '"strict"\|"target"\|"module"' tsconfig*.json 2>/dev/null | head -10
find . -maxdepth 2 \( -name "biome.json" -o -name ".prettierrc*" -o -name ".eslintrc*" -o -name "eslint.config.*" -o -name "vite.config.*" -o -name "next.config.*" -o -name "tsup.config.*" \) 2>/dev/null
find . -maxdepth 2 \( -name "app.json" -o -name "app.config.*" -o -name "metro.config.*" -o -name "eas.json" \) 2>/dev/null
find . -maxdepth 2 -name ".env*" -not -name ".env.example" 2>/dev/null | head -10
```

## Verification

- [ ] Tech stack skill is loaded when `.claude/tech-stack` contains `typescript`
- [ ] Package manager auto-detection populates `.claude/tech-stack-pm` correctly (bun / pnpm / yarn / npm)
- [ ] Build, type check, and test commands execute correctly for the target project
- [ ] Reference files exist at the paths listed in `## Reference Files`
- [ ] Scan recipes produce meaningful output for a TypeScript repository
- [ ] Tauri sidecar guidance is loaded when `src-tauri/Cargo.toml` is present
