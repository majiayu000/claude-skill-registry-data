---
name: validate
description: >-
    Build, typecheck, lint, boundary-check, version-check, and test plainworks changes through bun
    run and turbo — scoped to the packages that actually changed. Use whenever you need to validate a
    plainworks change, run the DoD gates, reproduce CI locally, or check the affected area of an edit
    before handing it off.
---

# Validating plainworks changes with bun run / turbo

plainworks is a bun-workspace monorepo (`packages/*`, `apps/*`, `internal/*`) driven by **Turborepo**. **`bun run verify` is the Definition of Done**: it runs every gate in order and stops at the first failure. The gate list lives only there (`internal/verify`); CI and the release workflow call the same command, so a local green means the same thing as a CI green.

## Run the gates

```bash
bun run verify --list                          # the gates, in order, and what each enforces
bun run verify --filter=@plainworks/<name>     # one package (+ what it needs)
bun run verify --filter='...[origin/main]'     # only packages affected by the diff
bun run verify                                 # everything — CI sign-off, audits, releases
```

`--filter` takes any turbo filter and is repeatable. It scopes the package gates (typecheck, build, test, packaging, production); the repo-wide gates (versions, lint, comments, layer map, atom lock, workspace shape, boundaries) are cheap and always run over the whole graph.

Plus a **Changeset** (`bun run changeset`) and the architecture invariants (no import-time side effects, no module-level singletons, header-only auth, typed errors, no `any` in public APIs).

## Iterate on one gate

While you work, run a single gate directly. Every gate is a root script or a turbo task:

```bash
turbo run test --filter=@plainworks/<name>    # one task for one package
bun run lint                                   # one repo-wide gate (`bun run format` fixes)
bun run check-shape                            # generated workspace manifests
cd packages/<name> && bun run test             # a package's own script
```

Finish with `verify` before you hand work off.

## Boundary and layer-map changes

`check-boundaries` has a fixture-backed test proving the gate rejects an upward import. If you touch `internal/boundaries/layers.json` or `.dependency-cruiser.cjs`, run `turbo run test --filter=@plainworks/boundaries` too, and `bun run sync-layer-map` to regenerate the layer-map docs (`verify` fails until you do).

## Atom and theme changes

If you touched `packages/elements` or `packages/theme`, also check the vendored atoms and the theme contract they read:

```bash
bun run check-registry                       # atoms match shadcn.lock.json (part of verify)
turbo run test --filter=@plainworks/elements # lock test + theme-variables contract
```

A lock failure means a file under `src/shadcn/` changed outside the pipeline. Don't relock by hand: restore the file, or rerun `registry:update <atom>` and move your change down the deviation ladder (see the [Vendored atoms](../../copilot-instructions.md#vendored-atoms) baseline and the [`update-atoms`](../update-atoms/SKILL.md) skill).

## Generator changes

If you touched `turbo/generators/**`, prove the golden template still yields a gate-passing package (both variants), then remove the throwaway:

```bash
bun run gen package --args scratch "scratch" false && bun install
bun run check-shape
turbo run typecheck build test check-packaging --filter=@plainworks/scratch
rm -rf packages/scratch && bun install
```

## Starter changes

`apps/next-host` is the source of the `create-plainworks` starter. If you touched it, the eject, or a package the starter depends on, prove a fresh starter still works outside the monorepo:

```bash
cd packages/create-plainworks && bun run smoke
```

The smoke packs the kit, scaffolds a starter, installs it, and runs the starter's own gates: typecheck, build, boot, and e2e. CI runs the same script in the `create-smoke` job.

## Production exclusion

`check-production` builds each host with source maps and fails when a forbidden source (the development inspector) reaches the production bundle, or when the scan can't see the app's expected sources. Each app declares its rule in `devtools-exclusion.json`. Paths starting with `./` are app paths, other entries are package paths resolved like imports, and `allowUnmapped` lists output files without a source map, as globs or `manifest.json#field`.

## Before you hand work off

The minimum passing standard for a self-contained change is `bun run verify` green over the affected set (`--filter='...[origin/main]'`), Vitest race/shuffle safe, the `elements` tests green when `theme` changed, and a Changeset. Run the unscoped `bun run verify` for an audit or release.

Treat a green run as **necessary but not sufficient**: it does not catch unbounded streams/buffers, missing timeouts/cancellation, module-level singletons, import-time side effects, or a token leaking into a URL. Those are on the reviewer.

For a client/UI package, accessibility and responsiveness are part of the acceptance bar (review pass [`08`](../review/references/08-ui-accessibility.md)): each component test runs `expectNoAxeViolations` in-band with the scoped `turbo run test`. `bun run check-axe-coverage` is the repo-wide gate that fails any render test file that never awaits that assertion or importing `axe-core` directly.

For a change an app user can see, `verify` is not enough: also meet the [UI Definition of Done](../../copilot-instructions.md#build-test-and-lint) in the app. Run the touched flows in the app's e2e suite (`bun run e2e -- e2e/flows.spec.ts --grep "<flow>"`); a failed check leaves its evidence in `.ui-artifacts/latest/report.md`. Then `bun run ui:capture --flow <flow>` and look at the frames. Exit code 1 means a flow broke; exit code 2 means the harness could not run: fix the setup, don't retry blindly. Start `bun run ui:host` once to keep captures fast.

Per repo workflow, **make edits only** — the maintainer commits and pushes.
