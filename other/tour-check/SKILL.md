---
name: tour-check
description: Verify the guided spotlight tours end-to-end by walking every tour step in a real browser (frontend/scripts/walk-tours.mjs) against a seeded demo account, and assert each step spotlights a visible element. Use after ANY change to tour steps or the UI they target — SPOTLIGHT_TOURS in src/core/spotlightStore.ts, Spotlight.tsx, data-tour anchors, the sidebar, or a page's layout — and before releases (e.g. "/tour-check", "verify the tours", "are the tours still working?"). Also use when a tour walk reports failures that smell like the API died under it.
---

# /tour-check — walk every guided tour and verify the spotlights

Onboarding is a set of per-page spotlight tours. Their anchors rot silently when the UI is
refactored, so the only trustworthy check is walking every step in a real browser.
`frontend/scripts/walk-tours.mjs` does that and exits non-zero if any step's spotlight misses.

## Two layers, and why you need both

1. **Static guardrails** — `src/core/__tests__/spotlightStore.test.ts` (runs in `pnpm test`).
   Proves every step targets a `[data-tour="..."]` anchor, that the anchor key exists in some
   component's source, that every `requiredPage` is a real route, and that **every route is
   reachable from the sidebar**. Cheap, runs in CI, catches renames and orphaned pages.
2. **The browser walk** — this skill. Proves each anchor is actually _rendered and visible_
   when the tour reaches it. A static check cannot know that an anchor sits behind a tab, in a
   collapsed section, or on a page that renders an empty state with no data.

**CI runs neither the walk nor anything else that would catch a rotted anchor at runtime.** No
workflow invokes `pnpm run test:tours`; the walk is a local gate, run by hand before a release.
The E2E workflow is a different suite that happens to share the same `wrangler dev` — which is why
a wrangler problem shows up in both at once and looks like two unrelated bugs.

## Steps

1. **Boot the app and seed the account.** The tours point at real rows; walking an empty database
   produces empty states and false MISSes.

   **Do not start `wrangler dev` yourself — the walk starts and restarts it** (see below). You
   need two things running: the dev server, and a seeded database with a saved session.

   ```sh
   # terminal 1 — the app. API_PROXY_TARGET pins /api at the Worker the walk will run.
   cd frontend && API_PROXY_TARGET=http://127.0.0.1:8787 npm run dev -- --port 3800 --strictPort
   # terminal 2 — applies migrations, seeds the fixture profile, writes tests/.auth/state.json.
   # It starts its own wrangler for the seeding and stops it again on the way out.
   cd frontend && pnpm exec playwright test --project=setup
   ```

   `global.setup.ts` does not sign in per-spec: the login route is rate-limited, and one shared
   session is the whole point of it. The walk loads that saved session rather than logging in.

   A fresh worktree also needs `worker/.dev.vars` (gitignored) or the setup fails with
   `login failed: 500 {"error":"Auth not configured"}`.

2. **Walk.** Same terminal 2, once the setup has finished.

   ```sh
   cd frontend
   pnpm run test:tours              # desktop 1280x800
   MOBILE=1 pnpm run test:tours     # iPhone 390x844 (touch)
   TOUR=categories pnpm run test:tours   # just one tour
   ```

   Env: `BASE_URL` (default `http://127.0.0.1:3800`), `E2E_API_PORT` (default 8787 — must match
   what the dev server proxies at), `CHROMIUM` (sandboxes usually need
   `CHROMIUM=/opt/pw-browsers/chromium`), `WORKER_MAX_UPTIME_MS` (see below).

   The mobile walk is several minutes slower than desktop — each tour reopens the sidebar
   drawer. It is not stuck.

3. **Read the output.** Every step prints `ok` or `MISS` with its title and the spotlight's
   pixel size, and the run ends with one of three verdicts:

   | Verdict          | Exit | Means                                                          |
   | ---------------- | ---- | -------------------------------------------------------------- |
   | `GATE: PASSED`   | 0    | every step of every tour spotlighted a visible element         |
   | `GATE: FAILED`   | 1    | a real tour regression; the MISSes are listed under "Failures" |
   | `GATE: UNPROVEN` | 2    | the Worker would not stay up — NOT a pass, NOT a tour failure  |

   A `MISS` means either the app raised its own "target missing" banner, or the highlight rect
   never reached a sane size. Fix by checking, in order: does the `data-tour` key still exist in
   the component? is the anchor rendered in the page's _empty_ state too (the targeting contract
   requires it)? is it behind a tab or collapse that the tour never opens? did the page fail to
   load its lazy chunk?

## The walk owns the Worker

A `wrangler dev` that dies mid-walk is indistinguishable, from the browser's side, from the app
breaking: pages render empty states, spotlights find nothing, and every remaining tour MISSes.
Five consecutive "tour regressions" turned out to be exactly that and nothing else.

So `walk-tours.mjs` supervises the API rather than assuming it
(`frontend/scripts/lib/worker-supervisor.mjs`):

- **Starts it.** Nothing on the port means it spawns `wrangler dev` in its own process group and
  waits for `/api/health`. A wrangler already listening is **adopted, not killed** — someone
  else's terminal is not the walk's to close — and replaced with a managed one the first time it
  dies.
- **Watches it two ways.** The child's `exit` event catches a crash; a 3s health poll (two
  consecutive misses) catches a worker that wedges without exiting. Neither alone is enough.
- **Restarts and re-walks.** A death mid-tour rolls that attempt back wholesale — its steps, its
  MISSes and its failure lines all disappear — and the tour is walked again from step 1 against a
  fresh Worker, up to three times. Only a walk that ran end to end on a live API is allowed to
  say anything about a tour.
- **Never blames the app for it.** Before recording any MISS the walk probes `/api/health` twice;
  if the API is gone, that is a `[worker]` line and a re-walk, never a failure line.
- **Recycles it early.** `WORKER_MAX_UPTIME_MS` (default 60000) restarts a Worker older than that
  _between_ tours, because a restart costs seconds while a mid-tour death costs the restart plus
  a re-walk. Set `WORKER_MAX_UPTIME_MS=0` to keep only crash recovery.

Everything the Worker does prints on `[worker]` lines and is counted separately in the summary:
`Worker: 1 adopted, 1 start, 1 crash recovered, 1 tour re-walk. None of that is a tour failure.`

### The crash this was built for

```
[ERROR] Error in ProxyController: Error inside ProxyWorker
  cause: { message: 'Network connection lost.' }
  at castErrorCause -> emitErrorEvent -> onProxyWorkerMessage
```

The ProxyWorker websocket to workerd drops, ProxyController treats it as fatal, and wrangler
exits — measured at `durationMs: 104348`, roughly 100s after startup, though not deterministic. A
15-tour walk always outlives that, so it could never finish in one wrangler lifetime.

**There is no version to pin your way out of this.** It reproduces identically on wrangler 4.116.0
with stable miniflare 4.20260730.0 (death at 154s) and on 4.126.0 with the miniflare 5 alpha
(death at ~104s) — same stack, same cause. It is an upstream `wrangler dev` bug. Surviving it is
the only fix available, and that is what the supervision above is.

**Do not try to grep a CI log for this signature.** It never reaches stdout. All wrangler prints
there is an empty `[ERROR]` marker; the ProxyController stack and the `Network connection lost`
cause go only to the debug log under `~/.config/.wrangler/logs/`, which
`.github/workflows/e2e.yml` uploads as an artifact for exactly this reason. A grep of job stdout
for "ProxyController" comes back empty on runs that _did_ crash — which has already sent one
investigation to a wrong root cause. Count the empty `[ERROR]` lines, or read the uploaded log.

## Architecture (where things live)

- **Tours & steps**: `src/core/spotlightStore.ts` — `SPOTLIGHT_TOURS`, built through the
  `step(key, page, title, description, placement)` helper, which produces the
  `[data-tour="<key>"]` selector and sets `requiredPage`.
- **Engine**: `src/components/Spotlight.tsx` — resolves the target with a MutationObserver
  (~6s budget, so a lazy page chunk has time to mount), draws an SVG backdrop with a cutout
  plus a glow rect, and renders a `targetMissing` banner when the selector never resolves.
- **Navigation**: `App.tsx` watches the active step and navigates to `step.requiredPage`
  (`setActivePage` + `window.location.hash`). This is why a tour can strand a user on a page
  that has no sidebar entry — the static guardrail above now blocks that.
- **Entry point**: the sidebar "What's New" button (`[data-test-id="whats-new-btn"]`) opens
  `TourSelectionModal.tsx`, which lists every tour and calls `startTour(id)`.
- **The walk**: `frontend/scripts/walk-tours.mjs`, with the Worker lifecycle in
  `frontend/scripts/lib/worker-supervisor.mjs`.

## Targeting contract

Anchor every step on a dedicated `data-tour="<key>"` attribute — never a CSS-module class
(they are hashed), a tag, a placeholder, or a `data-test-id`. The anchor must be **always
rendered** on its page, including the empty state, so a fresh account sees the same tour as a
populated one.
