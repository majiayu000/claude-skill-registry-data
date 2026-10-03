---
name: e2e-smoke
layer: stack
description: Run the Playwright fixture smoke harness to prove a real generated crouton app still boots, authenticates, and does CRUD after a dependency bump or package change. Use when asked to "smoke test", "run e2e", "verify against a fixture", or to check that a packages/ change doesn't break consuming apps.
allowed-tools: Bash, Read, Grep, Glob, AskUserQuestion
---

# E2E Smoke — fixture harness runner

Boots a **real generated crouton app** (`fixtures/<name>`) and runs the
Playwright smoke (login/register → create team → per-collection CRUD → optional
package surfaces). This is the "did a packages/ change or dep bump break a
consuming app" check.

> **Reference, not this file:** the harness internals (manifest format, auth
> realities, adding a fixture, gotchas) live in **`e2e/CLAUDE.md`**. This skill
> is only about *running* it and reading the result. Read `e2e/CLAUDE.md` before
> editing the harness or a manifest.

## When to use
- After changing anything in `packages/` (especially `crouton-core`, `crouton-cli`, `crouton-pages`, `crouton-bookings`, `crouton-auth`).
- After a dependency bump / `pnpm.overrides` change (this is exactly what it's for — e.g. the tiptap 3.20 bump).
- When the user says "smoke test", "run the e2e", "check the fixtures", "verify nothing broke".

## Step 1 — Pick the fixture that exercises the change

One fixture per run (they all use port 3000). Match the change to the fixture
whose packages actually mount the affected code — booting `minimal` won't touch
pages/editor code.

| Fixture | Exercises | Use when you changed… |
|---------|-----------|------------------------|
| `minimal` | core + auth + i18n, one `items` collection | crouton-core, crouton-auth, crouton-i18n, generator core, generic CRUD |
| `with-pages` | + `@fyit/crouton-pages` → transitively `@fyit/crouton-editor`; surface = pages workspace (mounts `CroutonEditorBlocks` → the real tiptap editor) | crouton-pages, **crouton-editor**, tiptap deps |
| `with-bookings` | + `@fyit/crouton-bookings` (locations/settings/slots); surface = bookings admin | crouton-bookings, heavy domain-package scaffolding |
| `with-assets` | + `@fyit/crouton-assets`; surface = the optional `CroutonAssetsPicker` mounts (not the core stub) | crouton-assets, the stub/`hasApp` system |
| `with-collab` | + `@fyit/crouton-collab`; surface = realtime collab UI mounts single-client (spike) | crouton-collab |
| `with-maps` | + `@fyit/crouton-maps`; a `venues` collection with address+coordinate fields — MapLibre map mounts in the generated form, `/api/maps/geocode` proxies live Nominatim | crouton-maps |
| `with-sales` | + `@fyit/crouton-sales` + `@fyit/crouton-printing`; two-tier POS smoke — order placed, print job pending→done against an in-test fake `:9100` ESC/POS printer | crouton-sales, crouton-printing |
| `with-devtools` | + `@fyit/crouton-devtools` + `@fyit/crouton-feedback`; surface = the feedback "glasses" launcher mounts via devtools `installModule` | crouton-devtools, crouton-feedback |

If unsure which fixture covers the change, grep the fixtures for the affected
component/package (`grep -rl '<Component>' fixtures/`) before guessing. If none
cover it, say so — the honest answer may be "no fixture exercises this; add one
(see `e2e/CLAUDE.md` → Adding a new fixture) or smoke a real app instead."

Use `AskUserQuestion` to confirm the fixture only if the change spans several or
the mapping is ambiguous; otherwise pick the obvious one and state it.

## Step 2 — Build the fixture's workspace deps (fresh checkout/worktree only)

The dev server loads the dist-consumed `@fyit/*` packages; on a clean tree they
aren't built yet. Build the fixture's transitive deps first (the `^...` excludes
the fixture app itself):

```bash
pnpm --filter "e2e-fixture-<name>^..." build
```

Skip this if you've been building/typechecking these packages this session and
they're already current. If the dev server errors with `Could not load '@fyit/crouton'`, this build is the fix.

## Step 2.5 — Browser binary in a sandbox (remote/CI env without the matching Chromium)

In a remote/sandboxed env the run can fail at the `setup` project with
`browserType.launch: Executable doesn't exist at /opt/pw-browsers/chromium…` and
`pnpm exec playwright install` then **fails too** —
`403 … Host not in allowlist: playwright.download.prss.microsoft.com` (the egress
policy blocks the download). The cause is a version skew: the installed
`@playwright/test` pins a browser build (e.g. 1200) that isn't on disk, while the
sandbox ships a slightly older one (e.g. 1194). You can't download the exact build.

**Fix — launch the build that *is* installed, via `PW_EXECUTABLE_PATH`** (the
config honours it → `launchOptions.executablePath`):

```bash
ls /opt/pw-browsers                       # find the installed build, e.g. chromium-1194
# full binary: /opt/pw-browsers/chromium-<build>/chrome-linux/chrome
E2E_FIXTURE=<name> BETTER_AUTH_SECRET=dev BETTER_AUTH_URL=http://localhost:3000 \
  PW_EXECUTABLE_PATH=/opt/pw-browsers/chromium-<build>/chrome-linux/chrome \
  pnpm test:e2e
```

A one-build skew (1194 vs 1200) launches fine for a smoke. `PW_EXECUTABLE_PATH`
is a committed escape hatch in `playwright.config.ts` — no source edit per run.
Watch out: a piped `… | tail` masks the real failure (tail exits 0), so check the
tail content for `Executable doesn't exist`, not just the exit code.

## Step 3 — Run

**`BETTER_AUTH_SECRET` and `BETTER_AUTH_URL` are required** — without the secret,
crouton-auth refuses to mint sessions and `auth.setup.ts` fails with "Could not
authenticate test user." Any value works locally.

```bash
E2E_FIXTURE=<name> \
BETTER_AUTH_SECRET=dev \
BETTER_AUTH_URL=http://localhost:3000 \
pnpm test:e2e
```

- The config's `webServer` boots `pnpm --filter e2e-fixture-<name> dev` on `:3000`, or **reuses a server already running there** (so if a dev server is up on 3000, kill it or expect it to be reused).
- First run is slow: cold `nuxt dev` compiles routes/auth-modal on demand (timeouts are deliberately high — 240s per test / 30s per expect / 180s webServer boot; `e2e/playwright.config.ts`). Don't lower them; give the run several minutes before suspecting a hang.
- Run in the background if it's long, and report when it returns.

## Faster runs (the cold-compile tax)

A run is slow (~5+ min for `with-pages`) almost entirely because it boots
`nuxt dev`, which **compiles each route on first hit** — and a fresh
checkout/remote container pays that cold every time. Levers, by payoff:

- **Reuse a warm server (biggest win when iterating).** `webServer.reuseExistingServer`
  is on, so start the fixture's dev server **once** and leave it up; every
  subsequent `pnpm test:e2e` reuses it and the routes stay compiled (runs 2..N
  are seconds, not minutes):
  ```bash
  # leave this running in the background:
  pnpm --filter e2e-fixture-<name> dev
  # then re-run the smoke as many times as you like — it attaches to :3000
  ```
- **Run only the specs the change touches.** A render/CRUD change doesn't need
  the auth-smoke trio (logout/re-login/team-switch). `setup` must always run:
  ```bash
  pnpm test:e2e e2e/collection.smoke.spec.ts e2e/surface.smoke.spec.ts   # + setup runs automatically
  ```
- **Don't chase the font errors.** The `Could not initialize provider bunny/google`
  lines are an instant egress 403 (fail-fast), not a timeout — log noise, not a
  time sink. Disabling remote fonts cleans logs but won't speed the smoke.
- **The structural fix (tens of seconds, not minutes): #246** — boot a *prebuilt*
  app (`nuxt preview`) instead of `nuxt dev` so routes compile once. Blocked by a
  prod-SSR auth-cookie 500; tracked there.

## Step 4 — Read the result

- **Pass:** all `setup` + `*.smoke.spec.ts` projects green. Report which fixture, which collections/surfaces ran.
- **Fail:** Playwright writes a report to `playwright-report/` and traces/screenshots to `test-results/` (both gitignored). Open the report or read the failing spec's error. Distinguish:
  - *Auth/setup failure* → usually missing `BETTER_AUTH_SECRET`, or a stale `e2e/.auth/` (delete it and rerun).
  - *List/CRUD failure* → the generated collection or a package surface regressed — that's a real signal, investigate the app, not the harness.
  - *Boot failure* (`Could not load '@fyit/...'`) → Step 2 build was skipped/stale.
- If you captured any screenshot manually, it goes in `screenshots/` (repo root), never the app or root dir.

## Scope notes (set expectations honestly)
- The smoke proves **boot + auth + CRUD + surface render**. It does **not** deeply
  drive package UIs — e.g. `with-pages` confirms the editor *workspace mounts*
  under the current tiptap, but doesn't type into the editor. Say what a pass does
  and doesn't prove.
- A **type-only** fix (e.g. `ref`→`shallowRef`) is validated by `pnpm typecheck`,
  not by this smoke — don't claim the smoke covers it. The smoke's value for that
  PR is catching **runtime** fallout from the accompanying dep bump.
- To drive a surface deeper (type a block, assert content), extend the fixture's
  `e2e.manifest.json` `surfaces` or add a fixture — see `e2e/CLAUDE.md`. Editing
  the manifest/fixture is fine (they're in `fixtures/`, not `packages/`); editing
  the harness specs in `e2e/` is also outside the packages gate.
