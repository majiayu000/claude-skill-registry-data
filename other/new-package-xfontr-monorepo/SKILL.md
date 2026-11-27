---
name: new-package
description: Scaffold a new project in this monorepo under packages/, apps/ or infrastructure/ — package.json with Nx tags and an exports map, the three wrapper configs, a README, and the boundary wiring. Use when adding a new workspace project, a new shared package, a new app, or a new infrastructure service.
---

# Scaffolding a workspace project

Six files have to agree, and two of them live outside the new directory. That is the whole reason
this skill exists — a scaffold that forgets step 5 lints clean until someone imports it.

## 1. Pick the root

| Root | For | Released? |
| --- | --- | --- |
| `packages/` | Shared product code an app imports | Versioned and tagged, never published — `nx.json` sets `release.projects: ["packages/*"]` and the release runs `--skip-publish`. Still `"private": true` |
| `apps/` | A user-facing product | No — `"private": true` |
| `infrastructure/` | A service apps reach **over the network** (`translations`), or repo-local dev tooling nothing imports (`scripts`) — either way, deployable/runnable on its own | No — `"private": true` |

The directory name is the package name: `packages/foo` → `@joinery/foo`. Infrastructure is not
separately namespaced (`infrastructure/translations` → `@joinery/translations`).

## 2. `package.json`

Copy the shape from the closest sibling rather than writing it fresh —
[`packages/observability/package.json`](../../../packages/observability/package.json) is the
plainest example, [`packages/content/package.json`](../../../packages/content/package.json) the one
with two entry points and optional peers. 2-space indent, because pnpm rewrites it that way.

```json
{
  "name": "@joinery/<dirname>",
  "version": "0.0.1",
  "description": "<three words, no marketing>",
  "private": true,
  "author": "Xifré Font",
  "license": "ISC",
  "type": "module",
  "exports": { ".": { "import": "./src/index.ts" } },
  "scripts": {
    "lint": "nx eslint:lint",
    "typecheck": "tsc --noEmit",
    "test": "vitest . --watch=false",
    "test:dev": "vitest .",
    "test:coverage": "vitest . --watch=false --coverage"
  },
  "nx": { "tags": ["type:<kind>", "scope:<area>"] },
  "devDependencies": {
    "@joinery/configs": "workspace:*",
    "@types/node": "catalog:",
    "@vitest/coverage-v8": "catalog:",
    "eslint": "catalog:",
    "typescript": "catalog:",
    "vitest": "catalog:"
  }
}
```

- **No build step**: the `exports` map points at source. No `main`, no `types`, no `dist`.
- **Script names are the stable ones** — `lint`, `typecheck`, `test`, `build` — delegating to the
  namespaced plugin target where there is one (`nx eslint:lint`). CI, the hooks and `pnpm check`
  call only those; [`conventions.md`](../../../docs/concepts/conventions.md) has why, and where
  files and types go inside the project.
- **Exactly two Nx tags**, `type:<kind>` and `scope:<area>`. They live here, not in a
  `project.json` — there are none in this workspace. Pick `<kind>` from the
  [root README's tag table](../../../README.md#architecture--boundaries): a vendor wrapper is
  `type:integration`, like `content` and `i18n`. Every project needs exactly one `scope:*` tag too,
  since the scope rules bind it the moment it is tagged: `scope:shared` for a package any app may
  use, otherwise the app or area it belongs to.
- If the package has internal layers, add Node subpath imports the way `content` and `i18n` do:
  `"imports": { "#core/*": "./src/core/*.ts" }`. Use them internally instead of `../../`.
- A second entry point (a framework integration) goes in the `exports` map with its framework deps
  as **optional peer dependencies**, so a consumer of the first entry point installs none of them.

## 3. The three wrapper configs

Never hand-roll these. Each is a one-liner over a `@joinery/configs` factory:

```ts
// eslint.config.ts
import { eslint } from "@joinery/configs";

export default eslint.createNodeConfig();   // or createVueConfig() / createNuxtConfig()
```

```ts
// vitest.config.ts
import { vitest } from "@joinery/configs";

export default vitest.createNodeConfig();   // or createVueConfig(viteConfig)
```

```json
// tsconfig.json
{
    "extends": "@joinery/configs/tsconfig/node.json",
    "include": ["src", "eslint.config.ts"]
}
```

`tsconfig/base.json` when the package needs no Node types, `tsconfig/node.json` when it does.

## 4. `README.md`

Follow the `house-docs` skill. A new package's README earns its keep by saying what the package is
*for* and what it deliberately does not do — not by listing its files.

## 5. The boundary wiring — the step that gets skipped

If the project introduces a **new** `type:` or `scope:` tag, three edits, all outside the new
directory:

1. Add its own `depConstraints` entry to
   [`boundaries.ts`](../../../packages/configs/src/eslint/lib/boundaries.ts). A leaf package gets
   `onlyDependOnLibsWithTags: ["type:config"]` — the rule of thumb is that apps compose and
   everything else stays a leaf.
2. Add the new tag to the `onlyDependOnLibsWithTags` of whatever is allowed to consume it — usually
   `type:app` alone. A new scope gets `["scope:<area>", "scope:shared"]` and joins no other list.
3. Run `pnpm docs:map`. It renders the tag and scope tables in the
   [root README](../../../README.md#architecture--boundaries) from `boundaries.ts` and every
   project's `nx.tags`; never edit them by hand.

## 6. The root README

Give `package.json` a `description` — one lower-case line, the same form as its neighbours'. The
workspace-layout block renders it as `@joinery/name — description` on the `pnpm docs:map` run
above.

## 7. Verify

```sh
pnpm install
pnpm exec nx show project @joinery/<name>    # targets inferred from the scripts and plugins?
pnpm exec nx run-many -t lint typecheck test --projects @joinery/<name>
```

If `lint` passes but the package is unreachable from its consumer, the tag wiring in step 5 is
what to check.
