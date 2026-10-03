---
name: dependency-sweep
layer: method
description: Run the "get dependencies current" flow for this monorepo — sweep for available updates, triage into safe / deliberate / wait buckets, bump the pnpm catalog, and prove it with the typecheck + e2e gate. Use when asked to "update dependencies", "are we on the latest", "do the quarterly sweep", "bump deps", or when the recurring sweep ticket comes due. We run NO update bot on purpose (#141) — this skill IS the update process.
allowed-tools: Bash, Read, Edit, Grep, Glob, AskUserQuestion, mcp__github__issue_write, mcp__github__sub_issue_write, mcp__github__issue_read, mcp__github__search_issues
---

# Dependency Sweep

The deliberate, no-bot way to stay current. Shared versions live **once** in the
`catalog:` block of `pnpm-workspace.yaml` (#142); this skill sweeps for updates,
ships the safe ones through a gate, and tracks the rest. It does **not** chase
latest blindly — for this codebase even some minor/patch framework bumps need a
small package-side type fix first (precedent: nuxt 4.4 → #241, vue 3.5.38 → #242).

> Why no Renovate/Dependabot: decided in #141/#143 — PR firehose, not help, for a
> solo dev. On-demand `taze` + this skill replaces it.

## Step 1 — Sweep: what's available?

Get the gap between the catalog floors and latest. `taze` is catalog-aware but can
be slow/blocked on a restricted network — fall back to `npm view` per dep.

```bash
npx taze minor -r            # review patch/minor across the workspace (no -w yet)
npx taze major -r            # majors, review only
# Fallback if taze hangs (network): direct check of the cataloged set
for p in nuxt vue vue-router typescript wrangler @libsql/client drizzle-orm drizzle-kit @nuxt/ui; do
  printf "%-16s " "$p"; npm view "$p" version
done
```

Read the current floors from `pnpm-workspace.yaml` (`catalog:`) and build a
**gap table**: `package | catalog floor | latest | gap (patch/minor/major)`.

## Step 2 — Triage into buckets

| Bucket | What | Action |
|--------|------|--------|
| **Safe** | patch/minor on **leaf** deps (DB, tooling — drizzle, libsql, etc.) | bump now, this PR |
| **Deliberate (in-major)** | big in-major jumps that touch every surface (`@nuxt/ui`, `wrangler`) | own gated bump / own issue |
| **Wait** | real majors that must follow Nuxt's supported range (`vue-router`, `typescript`) | hold; record why, re-check next sweep |

**Framework minors (`nuxt`, `vue`) are "safe-looking" but not auto-safe here** —
run them through the gate (Step 4); if red, demote to its own `type:fix pkg:*`
issue and hold the floor. Don't force a red bump into the safe PR.

## Step 3 — Bump the single dial

- Edit **only** the `catalog:` block in `pnpm-workspace.yaml`. Never per-package.
- Transitive singletons that no package declares directly (`vue`, `zod`,
  `@tiptap/*`) live in root `package.json` → `pnpm.overrides`, not the catalog
  (#140). If you bump `vue`/`nuxt`, bump their `pnpm.overrides` floor to match so
  the lockfile actually moves.
- Keep package **peer** ranges wide (`^3 || ^4`) — untouched.
- **`@playwright/test` is special — sync the E2E container tag.** If you bump it,
  also bump the CI image tag in `.github/workflows/e2e.yml`
  (`container: mcr.microsoft.com/playwright:v<x.y.z>-jammy`) to the **same**
  version. The image ships the matching Chromium + system libs, so a drift makes
  Playwright warn about a browser/library version mismatch — and the whole point
  of that container is to be version-matched (#392/#395).

```bash
pnpm install            # regenerates the lockfile
```

⚠️ **Caret ranges don't downgrade.** `^4.3.1` already satisfies an installed
4.4.8, so lowering the caret will NOT revert it. To back out a bump, reset the
files **and** the lockfile, then reinstall:
```bash
git checkout pnpm-workspace.yaml package.json pnpm-lock.yaml && pnpm install
```

## Step 4 — The gate (MANDATORY before commit)

```bash
pnpm -r --filter './apps/*' typecheck      # all apps must be green
```
Then the runtime check — invoke the **`e2e-smoke`** skill (pick the fixture that
exercises the change; `minimal` covers core/auth/CRUD/DB).

⚠️ **Stale-install gotcha:** a `Cannot find module '@vue/compiler-sfc'` from
`nuxt typecheck` is NOT a real error — it's an unhoisted node_modules after
repeated checkout/installs. Fix: `rm -rf node_modules && pnpm install`, then
re-run. Establish a clean **baseline** typecheck before blaming a bump.

- **Green** → ship.
- **Red** → identify the offending dep, hold its floor, open a `type:fix pkg:*`
  issue describing the failure (see #241/#242 for the format), and ship the rest.

## Step 5 — Track + commit

- Follow **ISSUE-FIRST**: the dependency epic is **#233**; open/`update` the
  relevant sub-issue (safe-bump issue, or a new `type:fix pkg:*` for a red dep).
- Commit with **`/commit`** — `chore(root): …`, reference `(#NN)`. The deliverable
  is `pnpm-workspace.yaml` + `pnpm-lock.yaml` (+ any `pnpm.overrides`).
- Open a PR (don't push to `main`); the e2e smoke runs in CI as the real gate
  (the local container can't download the Playwright chromium binary).

## Step 6 — If this was the recurring sweep

Re-arm the cadence: open next quarter's **"Quarterly dependency sweep — due
<+3 months>"** ticket (link #233), then close the current one. Re-check the
standing deliberate/wait items (#235 @nuxt/ui, #236 wrangler, #237 TS6/vue-router5)
each sweep.

## Known catalog gaps (carry forward)

- Several packages pin **drizzle** directly instead of via `catalog:`, so old
  copies linger after a bump. Catalog-ising those is a separate cleanup.
- `vitest` / `@vitest/coverage-v8` / `happy-dom` / `@nuxt/kit|schema` are
  deliberately **not** cataloged yet (version spreads need a real migration — #141).
