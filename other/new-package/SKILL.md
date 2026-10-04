---
name: new-package
description: >-
    Scaffold a new @plainworks/* package the canonical way — drive the turbo gen golden generator
    (never hand-roll files), pick the one-plain-word concern name, place it in the layer map, and
    wire it into the boundaries layer map (layers.json) so it is enforced from birth. Use when adding a new
    capability or package to plainworks, or when unsure where a package belongs.
---

# Adding a package to plainworks

plainworks packages are **born from a golden generator**, never hand-written. The template creates the human-owned files, then `plainworks-shape sync` derives `package.json` exports, files, side effects, scripts, and preset dev dependencies from the typed `tsdown.config.ts` build description. Do not create package files by hand; drive the generator, then place the package in the layer map.

## Step 1 — Name it: one concern, one plain word

- The package name is its **single concern, one plain word, the same word everywhere** — `std`, `state`, `channel`, `connect`, `query`, `auth`, `app`, `testkit`, `mocks`, `ui`. Kebab-case is allowed for a genuinely two-word concern, but avoid it if one word fits.
- **Banned names:** `core`, `engine`, `foundation`, and junk-drawer `utils`. If you reach for one of those, the concern isn't named yet — find the real word.
- Before committing to a name, sanity-check the npm scope isn't already taken by something unrelated: `npm view @plainworks/<name> 2>/dev/null`.

## Step 2 — Decide the layer

Place the package in the [layer map](../../../docs/architecture.md#layer-map). Its single source is [`internal/boundaries/layers.json`](../../../internal/boundaries/layers.json); the boundary gate and every doc copy are generated from it.

A package in `Ln` may import `@plainworks` packages only in a strictly lower layer. If the new package needs something from a higher layer, you have the direction wrong — **define the seam in the lower package and implement it higher** (`std` owns shared contracts/event shapes). Dev/test-only tooling that is never published goes under `internal/` (like `@plainworks/boundaries`, `@plainworks/tsdown-config`), not `packages/`. Test machinery that consumers use ships in `testkit` or `mocks`, never next to the runtime code it fakes.

The reasoning lives in the ADRs: [0006](../../../docs/adr/0006-seams-go-down.md) (shared seams go down), [0008](../../../docs/adr/0008-placement-and-dependencies.md) (placement and one owner per concern), and [0010](../../../docs/adr/0010-test-versus-runtime-ownership.md) (test versus runtime ownership).

## Step 3 — Generate it

```bash
bun run gen package
# name:        <one-plain-word>
# description: <one line>
# hasClient:   true only if the package ships interactive React (a "use client" ./client entry)
```

Or non-interactively (as CI does): `bun run gen package --args <name> "<description>" <true|false>`.

Answer `hasClient: true` only when the package ships React bindings. The generated `./client` is DOM-free, so it also runs on React Native; put browser behavior on an adapter subpath (see [`new-backend`](../new-backend/SKILL.md)), or declare `dom: true` in `tsdown.config.ts` when the package's product is browser UI. A pure server-safe capability (such as `std`) is `false` — it ships only neutral entries. `hasClient: true` adds the `./client` export, a `"use client"` module, jsdom test env, and `react`/`react-dom` `catalog:` peers.

Then install so the workspace picks it up:

```bash
bun install
```

Every subpath uses the one entry vocabulary ([ADR 0007](../../../docs/adr/0007-entry-vocabulary.md)): neutral `.` and concern subpaths, `./client`, `./server`, adapter subpaths named after what they do, and `./testing`. If you add or rename a public subpath, edit `build.entry` in `tsdown.config.ts` and run `bun run sync-shape` ([ADR 0009](../../../docs/adr/0009-generated-workspace-shape.md)). Never hand-edit `exports`, `files`, `sideEffects`, or the standard `build` / `typecheck` / `test` / `check-packaging` scripts.

## Step 4 — Wire it into the layer map

The generated package is **not yet in the layer map**, so the boundary gate (correctly) forbids it from importing any other `@plainworks` package — it fails **closed**, never vacuously green. Add it to `internal/boundaries/layers.json` at its chosen layer, then run `bun run sync-layer-map` to regenerate the README, `docs/architecture.md`, and instructions copies. A freshly generated package imports nothing internal, so it stays gate-passing until you add real cross-package imports.

Update the boundaries fixture test if the new layer relationship needs coverage (`turbo run test --filter=@plainworks/boundaries`).

## Step 5 — Build the capability test-first

Follow the [`apply-step`](../apply-step/SKILL.md) discipline: failing vitest test → minimal code → refactor while green. **Organize by concern from the start** — `src/index.ts` re-exports only; put logic in concern-named modules, and group a concern that spans more than one module into a **folder with its own re-export-only `index.ts` barrel** plus concern-named files inside (as `rskit` groups `retry/{backoff,policy}.rs` under a barrel-only `mod.rs`, and as `packages/mocks` does with `data/`/`filter/`/`handlers/`). Names must be self-documenting by path — no junk-drawer `utils`/`helpers`/`core`, no bare verb modules/exports (`compose`, `classify`); qualify them (`pipeline/interceptor.ts` → `composeInterceptors`). Reuse `@plainworks/std` (errors, result, guards, contracts, resilience) rather than re-owning a concern. Security-load-bearing packages (`auth`) raise their `vitest.config.ts` coverage threshold to ≥ 85%.

For a `hasClient` package, the server `.` graph holds the pure logic/types; the `"use client"` leaf holds only DOM/hook-bound code and never imports server-only auth. Interactive components are **accessible and responsive by default** — semantic roles, keyboard/focus, WCAG 2.2 AA, mobile-first/fluid layout with container-query adaptivity, `prefers-reduced-motion`/`-color-scheme` — and each component test queries by role (`@testing-library/user-event`, not `fireEvent`), mocks the network with MSW, and carries an axe assertion. See [`../../instructions/components.instructions.md`](../../instructions/components.instructions.md) and review pass [`08`](../review/references/08-ui-accessibility.md).

A UI package composes atoms from `@plainworks/elements/<name>` — never copy one in or edit it. **Vendored atoms** (`src/shadcn/`) are **locked**; a needed deviation follows the **deviation ladder** (theme → call site → `ui` wrapper), and a new primitive we write goes in `elements/src/atoms/`. See the [Vendored atoms](../../copilot-instructions.md#vendored-atoms) baseline.

## Step 6 — Validate

```bash
bun install
bun run check-shape
bun run verify --filter=@plainworks/<name>
bun run changeset          # add the release note
```

## Checklist

- [ ] Name is one plain concern-word; not `core`/`engine`/`foundation`/`utils`
- [ ] Created via `bun run gen package` (no hand-rolled package files)
- [ ] `bun run check-shape` is green; generated manifest fields were not hand-edited
- [ ] `hasClient` chosen correctly; server `.` entry stays React/DOM-free
- [ ] For a client package: components are accessible (WCAG 2.2 AA) and responsive; tests query by role, mock with MSW, and assert axe cleanliness
- [ ] For a UI package: atoms consumed from `@plainworks/elements`, never copied or edited
- [ ] Added to `internal/boundaries/layers.json` and `bun run sync-layer-map` run
- [ ] Imports only strictly-lower layers; a cross-layer need is a seam defined lower
- [ ] `src/index.ts` re-exports only; logic in concern-named modules; multi-module concerns grouped into folders with barrel-only `index.ts`; names self-documenting by path (no `utils`/bare verbs); no `any` in the public surface
- [ ] `bun run verify --filter=@plainworks/<name>` green; Changeset added

Per repo workflow, **create the branch and make edits only** — the maintainer commits and pushes.
