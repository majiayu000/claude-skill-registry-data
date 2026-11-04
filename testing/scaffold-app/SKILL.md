---
name: scaffold-app
description: >-
  Create the PWA and shared packages from scratch: apps/pwa with Vite + React + TS, vite-plugin-pwa, router,
  Vitest, Playwright + axe, and packages core/content/brand/ui wired into pnpm + Turborepo. Use for "scaffold
  the app", "set up the project", "create a package", or when apps/pwa is missing.
---

# Scaffold the app

The repo root (pnpm workspace, `turbo.json`, Prettier, husky, commitlint, harness) already exists. This skill
adds the workspaces. Owner: the `pwa-engineer` agent (packages: their owners in the `add-feature` skill's map,
but the first scaffold is one PR).

## 0. Check versions first, never from memory

```bash
node -v && pnpm -v                         # Node 22.x, pnpm 10.x (packageManager pins it)
pnpm view vite version
pnpm view vite-plugin-pwa version peerDependencies
pnpm view @vitejs/plugin-react version peerDependencies
pnpm view react-router version
pnpm view vitest version peerDependencies
pnpm view @playwright/test version
pnpm view typescript dist-tags
```

Read the release notes or docs for each major version you get (vite.dev, vite-pwa-org.netlify.app,
reactrouter.com, vitest.dev, playwright.dev). Cite what you checked in the PR.

### TypeScript version check (settled: 6.0.x, see the stack decision record)

The root has `typescript@7` (the Go port). Before relying on it in a workspace:

- Does `vite-plugin-pwa`, `typescript-eslint`, `vitest` typecheck or `vue-tsc`-style tooling call the
  TypeScript JS API? If any peer range excludes 7, pin `typescript` 5.x/6.x **in that workspace**
  (`pnpm add -D typescript@<ver> --filter <ws>`) and note it in `docs/decisions/stack-2026-10-24.md`.
- `pnpm exec tsc --version` inside the workspace must show the version you intend.

## 1. The app

```bash
cd apps && pnpm create vite pwa --template react-ts && cd ..
```

Then in `apps/pwa/package.json`: `"name": "@mobywatel/pwa"`, `"private": true`, `"type": "module"`.

```bash
pnpm add react-router --filter @mobywatel/pwa
pnpm add -D vite-plugin-pwa vitest @testing-library/react @testing-library/jest-dom jsdom --filter @mobywatel/pwa
pnpm add -D @playwright/test @axe-core/playwright --filter @mobywatel/pwa
pnpm --filter @mobywatel/pwa exec playwright install chromium webkit
```

Scripts the root expects (exact names; `turbo.json` runs them):

| Script      | Command                                    |
| ----------- | ------------------------------------------ |
| `dev`       | `vite`                                     |
| `build`     | `tsc -b && vite build`                     |
| `preview`   | `vite preview`                             |
| `typecheck` | `tsc -b --noEmit` (or `tsc --noEmit -p .`) |
| `lint`      | ESLint (flat config) once added            |
| `test:unit` | `vitest run`                               |
| `test:e2e`  | `playwright test`                          |

Create the planned folders (CLAUDE.md layout): `src/app/`, `src/pwa/`, `src/platform/`,
`src/features/{home,documents,matters,assistant,reminders,privacy,settings}/`, `messages/pl/`, `e2e/`. Delete
the Vite demo (counter, logos, `App.css` literals). Note that Vite's template CSS has hex colours, and the
post-edit hook blocks new ones: take them from tokens.

PWA config details (manifest, strategy, update prompt): the `pwa-platform` skill.

Playwright config: projects for `iPhone 13` (webkit) and `Pixel 7` (chromium), `webServer` running
`pnpm run build && pnpm run preview --port 4173`, `baseURL` `http://localhost:4173`.

## 2. Shared packages

For each of `core`, `content`, `brand`, `ui` under `packages/<name>/`:

```json
{
  "name": "@mobywatel/<name>",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "exports": { ".": "./src/index.ts" },
  "scripts": { "typecheck": "tsc --noEmit", "test:unit": "vitest run" }
}
```

- Source-only TS packages (no build step); Vite in the app compiles them. `tsconfig.json` with `strict`,
  `moduleResolution: "bundler"`, `noEmit`, `isolatedModules`, `verbatimModuleSyntax`.
- Put one shared base in `packages/config/tsconfig.base.json` if three or more copies would repeat (owner: the
  `harness-engineer` agent).
- Dependencies point inward: `ui → brand`; `content → core`; app → all. `core` imports nothing from React or
  the browser. `brand` is plain TS (tokens, copy).
- Add each to the app: `pnpm add @mobywatel/core@workspace:* --filter @mobywatel/pwa` (same for the others).

### Minimum content at scaffold time

- `packages/brand/src/copy.ts` exports `UNOFFICIAL_DISCLAIMER` (text: the `prototype-guardrails` skill) and
  the working name; `tokens.ts` with a first palette and type scale (the `design-system` skill); `css.ts`
  exporting `cssVariables(theme)`.
- The app's start screen renders the disclaimer in an element with `data-disclaimer`. Without it,
  `pnpm run audit:guardrails` fails.

## 3. Verify the scaffold

```bash
pnpm install
pnpm run typecheck
pnpm test
pnpm run build && pnpm preview          # open on a phone viewport, check the manifest in DevTools
pnpm run test:e2e                       # one smoke flow: start screen + disclaimer + axe
pnpm run audit:guardrails && pnpm run audit:harness
pnpm run ci:quality
```

Then follow the `verify-change` skill's report format and the `ship-branch` skill (one PR,
`chore(pwa): scaffold app and packages`).
