---
name: crouton-validation-reality
layer: stack
description: How to actually run every kind of test in nuxt-crouton (unit/e2e/typecheck/lint, verified commands) plus the HONEST coverage picture — which packages have real tests vs zero, the dormant skipped/todo cases behind three mocking walls, and what CI truly gates vs what CLAUDE.md claims. Use when asked "how do I run the tests", "is X covered by tests", "what does CI actually check", "why is this suite skipped", "where do I add a test", or before trusting a green build as evidence that something works.
---

# Validation Reality — what counts as evidence in nuxt-crouton

One-line purpose: the verified test-running commands, the honest coverage map, and the gap between claimed and actual gating — so you know what a green check does and does not prove.

## When to use / when NOT to use

| You want | Go to |
|---|---|
| Run/interpret the **fixture smoke** end-to-end, pick a fixture, triage its failures | **e2e-smoke** skill (but see the staleness note in §2 — several of its facts have drifted) |
| The **test-first sign-off gate** — proposing a failing test for human approval before writing `packages/*` logic | **test-review** skill |
| Fixture manifest schema, auth-helper internals, adding a fixture | `e2e/CLAUDE.md` + `fixtures/CLAUDE.md` (canonical) |
| Which CI **workflow** a failing check belongs to, deploy pipeline | **crouton-ci-and-deploy-map** skill |
| A test fails with an unfamiliar **error string** | **crouton-diagnostics-index** skill |
| Fresh clone won't build/boot before tests can run | **crouton-build-and-env** skill |
| This skill | Run any test kind; know what coverage actually exists; know what CI enforces |

## 1. What counts as evidence here

The house rule: **done is signed off, not asserted** (AGENTS.md) — green proxies each lied during a real graduation (#988; full story: sibling `crouton-failure-archaeology`).

Concrete local example: a staging preview deployed green but with an empty database, so a loading-skeleton change "showed no difference" — the deploy proved nothing until the advertised path was walked with real data ([#695](https://github.com/FriendlyInternet/nuxt-crouton/issues/695)). So the evidence ladder, weakest → strongest:

1. `pnpm typecheck` green — proves types compile, nothing about behaviour.
2. `pnpm test` green — proves the *existing* assertions pass (totals: the run summary); see §4 for what has zero assertions.
3. E2E fixture smoke green — proves a generated app boots → authenticates → does CRUD → mounts package surfaces; it does **not** deeply drive package UIs (e.g. `with-pages` mounts the editor workspace but never types into it).
4. Walking the advertised path yourself (the `verify` skill's job) and a human sign-off — the only "done".

## 2. Run every test kind (commands verified — see Provenance)

| Kind | Command | Notes |
|---|---|---|
| Unit, all | `pnpm test` | Vitest. Root `vitest.config.ts` is a **projects** config: `projects: ['packages/*/vitest.config.ts']` — only packages shipping their own `vitest.config.ts` participate (count them: `ls packages/*/vitest.config.ts`). Suite totals (passed/skipped/todo) come from the run summary — re-verify block. |
| Unit, one package | `pnpm --filter @fyit/crouton-i18n test` | Each participating package has `"test": "vitest run"`. |
| Unit, watch / coverage / UI | `pnpm test:watch` · `pnpm test:coverage` · `pnpm test:ui` | Coverage is v8, per package config. |
| E2E fixture smoke | `E2E_FIXTURE=<name> pnpm test:e2e` | = `playwright test --config e2e/playwright.config.ts`; default fixture `minimal`; one fixture per run (all bind :3000). Full workflow → **e2e-smoke** skill. |
| E2E, subset of specs | `pnpm test:e2e e2e/collection.smoke.spec.ts e2e/surface.smoke.spec.ts` | The `setup` project (login) always runs first via project dependency. |
| Typecheck (the gate) | `pnpm typecheck` | = `pnpm -r --filter './apps/*' typecheck` — **apps only**. NEVER `npx nuxt typecheck` from root (no app context → thousands of false positives; root CLAUDE.md; mechanics in `crouton-build-and-env` §4). |
| Typecheck fixtures | `pnpm typecheck:fixtures` | The #197 generator-regression gate surface. |
| Typecheck MCP | `pnpm typecheck:mcp` | = `pnpm --filter @fyit/crouton-mcp typecheck` (was a silent no-op with a stale filter name until fixed under [#1098](https://github.com/FriendlyInternet/nuxt-crouton/issues/1098)). Stale-name inventory: `crouton-config-registry` § "Silent no-ops". |
| MCP server tests | `pnpm --filter @fyit/crouton-mcp build && pnpm --filter @fyit/crouton-mcp test` | Build first — CI does (`ci.yml` mcp-server-tests job). |
| Lint | `pnpm lint` / `pnpm lint:fix` | `eslint .` from root, `eslint.config.mjs`. **No CI workflow runs repo-wide `pnpm lint`** (the misnamed "Lint & Type Check" job was renamed `typecheck-mcp` under [#1097](https://github.com/FriendlyInternet/nuxt-crouton/issues/1097); CI still runs no eslint). |
| Publish validation | `pnpm check:publint` · `pnpm check:attw` | Both target `./packages/crouton` only. |

E2E environment realities (verified in `e2e/playwright.config.ts`):

- **Auth env is self-provided**: `webServer.env` defaults `BETTER_AUTH_SECRET=dev`, `BETTER_AUTH_URL=http://localhost:3000`; fixtures also commit a dummy `.env`. Exported vars override (how CI injects its own). Exporting them is harmless.
- **The REAL timeouts are deliberately huge** — per-test/navigation/webServer-boot in the minutes, `expect`/action in the tens of seconds (read current values with the re-verify grep). The smoke runs against `nuxt dev`, and cold route compiles on CI take minutes; tightening them is what made the smoke flake (comment in the config itself).
- Sandboxes with blocked browser downloads: `PW_EXECUTABLE_PATH=/opt/pw-browsers/chromium-<build>/chrome-linux/chrome` is a committed escape hatch in the config.
- Fresh worktree prerequisite: `pnpm --filter "e2e-fixture-<name>^..." build` (dist-consumed `@fyit/*` deps must exist).
- Shell trap (reproduced): `pnpm test \| tail` masks the real exit code — check output content, not `$?`.

### Staleness in the e2e-smoke skill

Its *workflow* is correct, but several of its facts have drifted — stale timeout claim, fixture table missing the newer fixtures, over-strict "env vars are required" claim — **tracked as [#1103](https://github.com/FriendlyInternet/nuxt-crouton/issues/1103) (row 7)**. `e2e/CLAUDE.md` carries the current story; trust it over the skill's numbers.

## 3. The fixture harness — what exists and what each proves

Vocabulary: a **fixture** is a real generated crouton app under `fixtures/<name>/` (throwaway, never deployed) that the Playwright harness in `e2e/` boots and smokes. What each fixture smokes is declared in its `fixtures/<name>/e2e.manifest.json`; the specs are generic and manifest-driven — you almost never write per-fixture test code. Full manifest schema + auth internals: `e2e/CLAUDE.md` (canonical). Delta this skill carries:

Fixtures on disk vs in CI's `ALL` list — count both fresh (`ls fixtures/`; `grep 'ALL=' .github/workflows/e2e.yml`). **Snapshot 2026-07-02 — regenerate before relying on it:**

| Fixture | Adds | In CI `ALL`? |
|---|---|---|
| `minimal` | core + auth + i18n, one `mainItems` collection | ✅ |
| `with-pages` | crouton-pages → transitively crouton-editor | ✅ |
| `with-bookings` | crouton-bookings | ✅ |
| `with-assets` | crouton-assets | ✅ |
| `with-maps` | crouton-maps | ✅ |
| `with-devtools` | crouton-devtools + crouton-feedback | ✅ |
| `with-collab` | crouton-collab | ❌ **deliberately excluded** — pre-existing type errors fail the #197 typecheck gate; #210 keeps it a local-only spike (comment in `e2e.yml`) |

Manifest keys (typed as `FixtureManifest` in `e2e/helpers.ts`): `packages` (drives smart CI fixture selection, #622), `collections[]` (`key`, `heading`, `create`, optional `update`/`requiredField`/`a11y`), optional `surfaces[]`, `i18n`, `maps`, root `a11y`. Real example — `fixtures/minimal/e2e.manifest.json` declares one collection (`mainItems`, `requiredField: "name"`) plus an i18n flip (`"Your teams"` → `"Jouw teams"`).

**Auth realities in specs** (the non-obvious ones; verified in `e2e/helpers.ts` / `e2e/auth.setup.ts`):

| Reality | Consequence |
|---|---|
| Login/register is a **RouteModal overlay**, not a form page | Helpers fill inputs inside the modal; `/auth/login` redirects to `/` and opens it |
| Signup creates **no team** | `ensureTeam()` POSTs better-auth org endpoints, which need an `Origin` header (CSRF) |
| Better-auth 415s bodyless POSTs | Always send `Content-Type: application/json` (`signOut()` passes `data: {}`) |
| `get-session` is cookie-cached (5-min TTL) | Force `?disableCookieCache=true` for true state; setup **strips** the `session_data` cookie from saved storageState so slow runs don't SSR logged-out |
| Sign-out kills the shared session | Auth specs mint their **own** browser contexts; content specs call `ensureAuthed()` (self-healing re-login) |
| Test identity | `e2e-user@example.com` / `TestPassword123!`, team `e2e-team` (constants in `e2e/helpers.ts`) |

**A11y in the smoke** (verified in `e2e/helpers.ts`): axe runs on every collection list + surface; only `critical`/`serious` block; `color-contrast` excluded (theme-owned); baseline of known upstream shell violations = `['aria-allowed-attr']` (#735) — `button-name` was driven to zero and removed, so regressions there now fail.

**CI e2e** (`.github/workflows/e2e.yml`): smart per-PR fixture selection by changed paths (#622); packages in `UNIVERSAL` (`crouton crouton-core crouton-i18n crouton-cli crouton-auth`) → full matrix; push to `main` + nightly cron → always full matrix. Runs in the `mcr.microsoft.com/playwright` container whose tag must track the repo's `@playwright/test` version (read both in `e2e.yml` + the lockfile). Each job **regenerates the fixture from committed schemas** (`crouton-generate.js config --force`) and **typechecks the regenerated output** (the #197 generator-regression gate) before testing — so after changing a generator template, regenerate fixtures and commit, or CI diverges from your tree.

## 4. The honest coverage table

Test files per package — `*.test.ts`/`*.spec.ts` excluding node_modules/dist/.nuxt/.output. **Snapshot 2026-07-02 — regenerate with the re-verify block before relying on numbers.** At the snapshot, fewer than half the packages had any tests (14 of 31; 17 at zero):

| Package | Test files | | Package | Test files |
|---|---|---|---|---|
| crouton-core | 29 | | crouton-sales | 2 |
| crouton-layout | 17 | | crouton-mcp | 2 |
| crouton-cli | 15 | | crouton-analytics | 2 |
| crouton-auth | 14 | | crouton-assets | 1 |
| crouton-flow | 8 | | crouton-feedback | 8 |
| crouton-collab | 6 | | crouton-printing | 5 |
| crouton-i18n | 4 | | crouton-triage | 3 |

**Zero unit tests at the snapshot:** `crouton` (meta), `crouton-admin`, `crouton-ai`, `crouton-atelier`, `crouton-audio`, `crouton-bookings`, `crouton-charts`, `crouton-designer`, `crouton-devtools`, `crouton-editor`, `crouton-email`, `crouton-events`, `crouton-maps`, `crouton-mcp-toolkit`, `crouton-pages`, `crouton-themes`, `crouton-three`.

Mitigations and their limits:

- `pages`/`bookings`/`assets`/`maps`/`devtools` get e2e fixture smoke coverage (§3); `editor` only transitively (`with-pages` mounts the workspace). `collab` has unit tests but **no CI e2e** (excluded fixture) — and its one component test file is `describe.skip`'d with a note that it "tests an inline mock component, not the actual CollabEditingBadge.vue" (`packages/crouton-collab/tests/components/CollabEditingBadge.test.ts`).
- **`apps/*` and `pocs/*` have 0 test files** (verified by find). Consistent with the stage model (`node scripts/harness-stages.mjs apps/velo` → test-first `opt-in`; `pocs/*` → off) — but it means launched apps (fanfare/velo/triage) have no automated behaviour tests beyond typecheck and fanfare's dual-preset CI build.
- The tests that exist are real, not placeholders (spot-checked: `crouton-core/tests/api/*.test.ts`, `crouton-layout/app/utils/__tests__/layout-viability.test.ts`).

Gotcha (reproduced at the snapshot): `packages/crouton-charts` ships a `vitest.config.ts` but zero test files — standalone `npx vitest run` there prints "No test files found, exiting with code 1", while the root projects run tolerates the empty project (root `pnpm test` is green). Anyone adding `--project` filtering will hit this.

## 5. The skipped-suite inventory — three mocking walls

The run summary reports a large skipped + todo tail (exact totals: `pnpm test 2>&1 | tail -4`; marker counts: the greps in the re-verify block). The dormant cases cluster behind **three mocking walls** — fixing these mocks is the single highest-leverage test-debt target (on the order of 170 dormant cases at the snapshot, many asserting security-relevant behaviour like team limits):

| Wall | What's dormant | Files (verified `describe.skip` / todo locations) |
|---|---|---|
| **Better Auth nanostore** (+ `window.location`, WebAuthn) | crouton-auth's **entire integration suite** (login + registration flows) whole-file skipped; a stack of `it.todo`s in useTeam/useAuth | `packages/crouton-auth/tests/integration/auth-registration.test.ts`, `auth-login.test.ts`, `tests/unit/composables/useTeam.test.ts`, `useAuth.test.ts` |
| **Nuxt `#imports` / `useRuntimeConfig`** | team-utils cases incl. team-limit / allowCreate / single-tenant enforcement; `useScopedAccess` (`import.meta.client` unmockable post-import) | `packages/crouton-auth/tests/unit/server/team-utils.test.ts`, `tests/unit/composables/useScopedAccess.test.ts` |
| **Yjs / WebSocket** | crouton-flow's **entire realtime-sync feature** — unit + integration whole-file skipped, e2e suite skipped, dagre-mock `describe.todo`s → the sync feature has zero passing coverage of any kind | `packages/crouton-flow/test/composables/useFlowSync.test.ts`, `test/integration/flow-sync.test.ts`, `test/e2e/multiplayer-flow.spec.ts`, `test/composables/useFlowLayout.test.ts` |

Smaller items: `crouton-core` useCollectionQuery/useCollectionMutation logging todos/skips; `crouton-i18n/app/composables/__tests__/zod-sanity.test.ts` encodes a do-not-use Zod v4 pattern (`z.record(valueSchema)` breaks — use the two-arg form) as a skipped sanity test.

## 6. What CI actually gates vs what CLAUDE.md claims

`ci.yml` jobs:

| Job | What it actually does | Gap vs the claim |
|---|---|---|
| `typecheck-mcp` + `typecheck-apps` | MCP-server typecheck, and the full app sweep (`pnpm typecheck`) | Fixed under [#1097](https://github.com/FriendlyInternet/nuxt-crouton/issues/1097): `typecheck-apps` builds the apps' workspace deps, `nuxt prepare`s each app, and runs the exact local sweep — root CLAUDE.md's "EVERY change requires `pnpm typecheck`" is now a CI gate too (was: `lint-and-typecheck`, MCP-only, no eslint — renamed since it overclaimed). e2e.yml's regenerated-fixture typecheck (#197) still covers fixtures; the `typecheck:mcp` script's stale filter was fixed under [#1098](https://github.com/FriendlyInternet/nuxt-crouton/issues/1098). |
| `build-fanfare` | Builds fanfare for `cloudflare-pages` + `node-server` presets | Fanfare **typecheck intentionally NOT gated** ("known pre-existing baseline of type errors" — comment in the job); the build is the smoke. |
| `test` | `pnpm install --ignore-scripts` → builds `crouton-auth`/`crouton-core`/`crouton` → `npx nuxt prepare` in each `apps/*` → **`pnpm test`** | This is the real unit-test gate. Other suited packages (layout, cli…) run from source; the three builds are for dist-consumers. |
| `mcp-server-tests` | Build then test `@fyit/crouton-mcp` | — |
| `changeset-check` | Detects `packages/` change without a changeset | Emits only `::warning` — **never fails a PR**. |
| `docs-check` / `sync-validation` / `package-check` | Docs audit script / field-types sync / publint | — |

Also: repo-wide `pnpm lint` runs in **no** workflow (part of the [#1097](https://github.com/FriendlyInternet/nuxt-crouton/issues/1097) picture). E2E gating lives in `e2e.yml` (§3), not `ci.yml`. For the full workflow map, defer to **crouton-ci-and-deploy-map**.

**Trust order when these conflict:** see `crouton-docs-trust-map` §1. CLAUDE.md's typecheck-everything rule stands as the required *working practice*; just don't claim CI enforces it.

## 7. Adding a test the house way

1. **Check the gate first**: `node scripts/harness-stages.mjs <path>` → `packages/*` = test-first **required**; `apps/*` opt-in; `pocs/*` off. For new `packages/*` logic, the order is owned by the **test-review** skill: enumerate edge cases in plain language → write the *failing* test → hold for a `lgtm`/`approve` **comment** (not a reaction/label, #572) → implement to green.
2. **Placement**: match the neighbours — `*.test.ts` beside the source or in `__tests__/`; `packages/crouton-core` is the reference layout (this is what test-review itself points at).
3. **If the package has no `vitest.config.ts`**, add one (copy a sibling, e.g. `crouton-i18n`) — the root projects glob `packages/*/vitest.config.ts` picks it up automatically; nothing to register at root.
4. **Run**: `pnpm --filter @fyit/<pkg> test`, then root `pnpm test`, then `pnpm typecheck`.
5. **E2E coverage for a package surface**: extend the relevant fixture's `e2e.manifest.json` (generic specs pick it up) rather than writing a new spec; new fixture → `e2e/CLAUDE.md` "Adding a fixture" — and remember CI never runs it until its name is appended to `ALL` in `e2e.yml`.

## Provenance and maintenance

verified: 2026-07-02

```bash
pnpm test 2>&1 | tail -4                                   # suite totals / skipped / todo
ls packages/*/vitest.config.ts | wc -l                     # participating packages
grep -n 'ALL=' .github/workflows/e2e.yml                   # CI fixture list (has with-collab returned?)
grep -nE 'timeout|Timeout' e2e/playwright.config.ts        # real e2e timeouts
for p in packages/*/; do echo "$(find $p -path '*node_modules*' -prune -o -type f \( -name '*.test.ts' -o -name '*.spec.ts' \) -print | wc -l) $p"; done | sort -rn | head -20   # coverage table
grep -rn 'describe\.skip' packages/*/test*/ packages/*/tests/ 2>/dev/null | grep -v node_modules      # mocking-wall status
grep -rnE '\b(it|describe|test)\.(todo|skip)\(' packages/*/test*/ packages/*/tests/ 2>/dev/null | grep -v node_modules | wc -l  # dormant-marker count
pnpm typecheck:mcp                                         # should run tsc in crouton-mcp (fixed #1098); "No projects matched" = regressed
```
