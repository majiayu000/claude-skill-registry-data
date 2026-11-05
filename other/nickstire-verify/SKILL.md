---
name: nickstire-verify
description: Use before committing or pushing changes to the nickstire app (apps/nickstire/) — the real local verification sequence, the brand-voice linter false-positive trap, and the prerender regen rule.
triggers: nickstire commit, nickstire push, verification sequence, brand-voice linter, false positive, prerender regen, verify gate, lint, typecheck, ai_force_ollama, railway watch-paths
---

# nickstire-verify

Verify a nickstire change is safe to commit/push. The master gate is
`pnpm run verify`, but it has a few non-obvious traps that have burned
multiple sessions.

## Run, in order (from `apps/nickstire/`)

0. `bash scripts/preflight.sh` (`BASE=<GitHub main sha>` from a hook-free clone): the CI gates that
   turned PRs red, about 4 minutes. Every push bills a full CI run (2026-10-10: 14 PRs, 29 pushes).
   Run it as `node scripts/agent-os/heavy.mjs run -- bash apps/nickstire/scripts/preflight.sh` FROM GIT BASH, so `bash` resolves
   and the heavy lease is kept (from PowerShell `bash` is not on PATH and the run fails with "'bash' is not recognized"); expect
   it to wait while another session holds the heavy lease or the chrome slot. It catches the proc-census, knip orphan-gate and
   fail-open-slice reds that a lane's own test files miss (witnessed 2026-10-18: 3 real reds).
   A test that reads a DATA file at runtime (`readFileSync`) is selected only by the text scan, never by `vitest related`
   (witnessed #3152: preflight green, CI red on `completionAuthority.test.ts`): after any `docs/operations/*.json` edit run
   `node scripts/preflight-text-scan.mjs <file>` and the tests it names.
1. `pnpm run check` — `tsc --noEmit`. Must be 0 errors.
2. `pnpm test` — vitest. Must end `Test Files N passed (N)`, exit 0.
3. `pnpm run build` — `vite build` + esbuild server + maybe-prerender.
4. (full gate) `pnpm run verify` — env + check + lint + source-lint +
   hooks-lint + route-validate + tests + build.

## Before pushing a diff that touches `client/` — the DoD compiler

The completion-authority steps of the agent-policy job derive their requirements **per-diff**. Touching any
`client/` file (an edit, a rename, even a DELETION) derives an
`operator-walkthrough` requirement, and any evidence already on `main` was
written for a PREVIOUS diff — so it is **stale by definition** and fails the
gate.

Write the evidence for THIS diff in a NEW per-PR fragment,
`.completion/evidence.d/<branch-slug>.json` (format in that directory's
README): `{ "evidence": { "operator-walkthrough": { "ref": "..." } } }`, or
`{ "deferred": "<reason>" }`. Say what the operator sees, and if the answer is
"nothing", prove it (zero importers, identical render) rather than asserting
it. A new file per PR never conflicts with a sibling PR. Freshness is by
content: an entry whose exact text is already on the merge-base (any fragment,
any legacy key) reads STALE, so copying old evidence does not pass. Rewriting
the legacy `.completion/evidence.json` entry still counts, but conflicts with
every concurrent PR — don't.

Witnessed on #1428: red in 22s on a stale entry, green in 31s once rewritten.

**One check name, FOUR different sub-gates — a red is not "the same gate
again."** Witnessed on #1830: the completion-authority steps of the agent-policy job went red four times
on one PR, each a different sub-gate, ~50 minutes of fix-push-poll cycles
because only sub-gate 1 was documented:
1. Stale or missing per-diff completion evidence (above) — fix: add a
   fragment in `.completion/evidence.d/` written for THIS diff.
2. Unresolved P1 review threads from the Codex review bot — fix: reply,
   then resolve via GraphQL `resolveReviewThread`.
3. A capability-ledger cross-axis rule (`operator_only` requires >=
   `integration_verified`) — fix: obey the ledger ladder; fix the
   LABEL, never inflate the state to satisfy the rule.
4. An un-rendered `REALITY-LEDGER.md` diff — fix: always run
   `scripts/render-reality-ledger.mjs` and commit the `.md` beside the
   `.json`.

## Traps

- **A new tRPC read that calls `invokeLLM` must be listed in `client/src/lib/unbatchedProcedures.ts` and pass a bounded
  `slotWaitMs`.** Otherwise one slow call freezes every batched sibling panel on the page (witnessed PR 3137, `lot.officeDigest`).
- **Never text-match a database error.** drizzle-orm 0.45 wraps every driver
  error; the wrapper's message is the SQL and its params, and the code/errno
  live on `.cause`. A regex on `err.message` misses the real 1054/1062/1146
  and matches any query whose params contain those digits or whose SQL names
  the table. Twenty sites did this until #2574/#2589. Use
  `server/lib/dbErrors.ts`; test with drizzle's own `DrizzleQueryError`, not a
  look-alike, plus a wrapped timeout whose params hold the code as the control.
- **A test within ~2x of its timeout is a shuffled-order failure waiting to
  happen.** `tableWriterCoverage` passed at 13s in default order and timed out
  at 34-36s under `--sequence.shuffle.files --sequence.seed=29`, reproducibly
  (2026-09-23; fixed by reading each file once, 0.14s). Sweep a few seeds before
  shipping test changes, and compare runs only on the SAME file set: a branch
  with a different test-file count shuffles into a different order, so "main
  passes seed 29" proved nothing until the same tree ran without the change.
- **`.completion/evidence.json` conflicted on nearly every base merge**
  (witnessed 3x on 2026-09-23) because sibling sessions rewrote the same
  per-diff keys. Fixed by per-PR fragments (above) — write a fragment, not the
  manifest. If an OLDER branch still carries a manifest edit and conflicts:
  resolve three-way, per key, against the merge-base — take the side that
  changed; if both changed, OURS stays current and THEIRS is kept as
  `<key>-superseded-<date>-sibling-main`; write with
  `json.dumps(d, indent=2, ensure_ascii=False) + "\n"` (round-trips byte-exact);
  then re-run `node scripts/dod-compiler.mjs --base origin/main --enforce`.
  A merged PR's conflict also stops `pull_request` CI from running at all:
  "no checks" on a pushed head means check `mergeable_state` first.
- **Wait on a background suite by its SUMMARY line, never `pgrep -f`.** A loop
  like `until ! pgrep -f "vitest run"` matches its own command line (which
  contains the pattern) and never exits; two such waiters sat out a 600s
  timeout on 2026-09-23. Poll the log for `^\s+Tests ` instead, or capture `$!`.
- **A derived scan set must include the WIRING file it derives from.**
  `server/__tests__/cronNoSwallowedFailure.test.ts` scanned every module
  `scheduler.ts` imports and never `scheduler.ts` itself — which held 13
  inline `catch { return { details: "X failed" } }` wrappers, one of them
  re-swallowing a rethrow the same wave had added one frame below. The
  "every cron fails loudly" claim was false for 13 jobs while its canary was
  green (2026-09-02, found by an independent reviewer). When a gate scans
  "every module X imports", scan X too, with its own positive control: the
  inline handler inside the registry is the shape a module scan cannot see.
- **The SMS `uncertain` outcome means do-not-retry, not not-delivered.**
  `sendSms` returns `success:true, uncertain:true` on a shop-gateway timeout
  and `server/sms.ts` documents it as "the relay may well have delivered".
  Any change to how a send result is interpreted must be checked against
  the FOUR outcomes in `server/lib/smsOutcome.ts`: a claim is consumed for
  every outcome except a definite failure (`smsClaimConsumed`); only the
  COUNTERS keep uncertain apart from sent; never collapse uncertain to
  `failed` on a receipt a human reads — it invites a re-send. The 2026-09-01
  wave's first rule ("consume only on sent|queued") re-texted customers every
  tick at five sites until the second review caught it.
- **A multi-commit wave is not done after the author's own pass.** Over a
  10-commit wave the author's hostile re-read found 5 defects; three
  parallel independent reviewers (silent-failure hunter on `server/`,
  contract reviewer on schema + cross-app, client/docs reviewer) over the
  full diff found 24 more, including two P0 regressions the wave itself
  introduced and three corrections to its audit claims. Before calling a
  wave done, run a hostile per-subsystem pass over the full diff, in-session
  unless the operator asked for agents (he rejected two unrequested Explore
  spawns on 2026-10-08), with a file:line checklist and a "verified OK / not
  checked" answer shape, then verify the top findings yourself. A single author pass over more than ~20 files has not once been
  sufficient (2026-08-12 onward).
- **A numeric test fixture is a claim about the PRODUCER's scale or
  domain.** Before inventing a value (0.05 vs 5.0, cents vs dollars,
  x10000 vs percent), grep the function that produces it in production
  and one existing consumer that renders it — a self-consistent
  wrong-scale fixture keeps every test green around a real x100 bug.
  Witnessed 2026-08-13: the real producer (`getTopPosts()`,
  `server/pipelines/instagram-data.ts:576`) returns `engagementRate` on
  a PERCENTAGE scale (5.23 for 5.23%), but two test fixtures invented a
  0-1 fraction production never produces — every test stayed green
  while a real reel would have rendered "523.00%" (#1558, caught only
  by a post-merge audit, fixed in #1561).
- **`as never` / `as unknown as X` on a JSON.parse'd field silences
  the exact compiler check that would catch a nonexistent field or a
  wrong-domain value.** Validate through a normalizer that degrades
  unknowns honestly, and read `reel_jobs.payload` through
  `shared/reelJobPayload.ts`'s `parseReelJobPayload()` — never a fresh
  ad-hoc inline type. Witnessed 2026-08-13, two instances in one diff:
  `attentionMicrostructureStore.ts` cast `brief.ctaType as never` for a
  field no real payload has (making `hasCta` structurally always
  false), and `dailyReelPost.ts:493` force-cast raw JSON into
  `EntailmentVerdict` the same way — both merged in #1558 behind a
  green suite.
- **An e2e "proof" test that hand-builds the input a real IO function
  normally derives can bypass the exact gate it claims to prove.** If
  the derivation is inline in the IO layer, extract it into a pure
  shared function and call THAT from both the IO layer and the test.
  Witnessed 2026-08-13: `scanfinishRun2EndToEnd.test.ts` hand-fed all
  14 Local Discovery topics unfiltered, silently skipping the
  e_check -> government_feed evidence-gate split that
  `gatherTopicSignals()` performs inline — the docstring claimed "the
  REAL functions" while bypassing the one load-bearing derivation
  (#1558); fixed in #1561 by extracting `splitLocalDiscoveryTopics()`
  so the IO layer and the test share one implementation.
- **Brand-voice linter on CSS class names.** The pre-commit
  `brand-voice` linter regex-matches banned words (`premium`, `tier`,
  etc.) in the staged diff — including CSS class names. The
  project-wide Tailwind utility `btn-premium` appears in 5+ existing
  files but triggers the lint when added in a new diff. The lint
  message itself suggests `git commit --no-verify` — DO NOT. The
  correct fix is to edit the **newly-added** content: rephrase
  comments and remove `btn-premium` (or any flagged utility) from
  newly-added classNames. Pre-existing usages stay untouched (the
  linter only checks the staged diff).
- **The exit code lies in two different ways — read the SUMMARY LINE.**
  `pnpm test | tail` reports `tail`'s status (0), not vitest's. And
  `pnpm test; echo "EXIT=$?"` — which this skill used to recommend — is
  no better under `run_in_background`: a compound command reports the
  LAST command's status, so the completion notification said
  **"exit code 0" while 24 files and 234 tests had failed** (2026-08-08).
  Run the command ALONE and read `Test Files … passed/failed`. If no
  summary line was printed at all, the run did not finish — see the
  teardown-crash trap below.
  The same holds for EVERY gate, not only vitest: never pipe a gate's output.
  `node merge-gate.mjs ... | tail -4; echo EXIT=$?` printed `tail`'s exit, and
  `pnpm run check | tail -3` read as "tsc exit=0" while tsc had failed
  (2026-10-18, twice in one session). Redirect to a file, then read the file
  and the exit code separately (`cmd > log 2>&1; echo $?`). `merge-gate.mjs`
  needs the FULL 40-character sha: a short sha prints usage and exits 64.
- **`pnpm run verify` can hit a pnpm-bootstrap glitch.** If `verify`
  fails before any of the inner gates run (no actionable output),
  fall back to running each gate individually (check / test / build).
- **The full suite can CRASH AT TEARDOWN and print no summary.** On
  Windows the default pool has ended with `ELIFECYCLE Test failed` after
  every test passed — observed 2026-08-08 with **528 pass markers, 0 fail
  markers, 0 "Failed Tests" banners, and no summary line** (a libuv
  `UV_HANDLE_CLOSING` assertion appeared from a separate script the same
  session). Do not read that as a regression, and do not read it as
  green. Triage by counting markers —
  `grep -cE '^ *(×|❯) '` returning 0 means nothing failed — then re-run
  under `--pool=forks --poolOptions.forks.singleFork=true` for an actual
  summary. **Marker counting is triage; the summary line is the receipt.**
- **Never mutate the working tree while a suite is running.** A
  background suite reads the tree continuously, so a `git checkout`,
  `git stash`, or edit mid-run rewrites files under it and produces
  phantom failures. The tell is that failures cluster in ONE vitest
  project — 2026-08-08: **24 failed files, every one `client/**`, zero
  `server/**`**, and a clean re-run passed 425/425. Wait for the run, or
  branch before starting it.
- **When a fail-open is safe only because another middleware runs
  first, that ORDER is the security control — pin it with a test.**
  `adminProcedure` chains `requireAdminIdentity` (throws FORBIDDEN for
  non-admins) before `requireFreshMfaAndPermission` (which contains a
  deliberate, documented fail-open to pre-RBAC owner when the role row
  is unreadable). The fail-open is correct — choosing `viewer` would let
  a DB hiccup lock the owner out mid-shift, the exact lockout reversed on
  2026-07-16 — but it is safe ONLY because authentication already ran.
  As of 2026-08-08 no test covers that ordering, so a refactor
  reordering `.use()` calls would silently turn an authorization
  fail-open into an authentication one. Assert that the EARLIER gate
  rejects, not just that the later one behaves.
- **Migrations are hand-applied SQL.** After editing
  `drizzle/schema.ts`, generate / hand-write the `drizzle/NNNN_*.sql`
  migration and apply it to the DB before re-running `pnpm run check`.
  There is no auto-migrate. The check fails until the migration is
  applied.
- **Prerender is generated, not hand-edited.** Changes to nav, SEO,
  NAP, or page copy that should appear in `prerendered/*.html` need
  `pnpm run prerender` (or `PRERENDER_ON_BUILD=1 pnpm run build`).
  CI audits this. The SPA hydrates on top of prerendered HTML — so a
  nav change reaches users via the JS bundle immediately, but the
  prerendered HTML (what crawlers see) stays stale until regen.
- **A check that a page EXISTS is not a check that it CARRIES its
  content.** Prod serves two documents for nickstire routes: crawlers
  get ~150KB of committed prerendered HTML, browsers get the ~14KB SPA
  shell. Assert the payload (row counts, card counts, absence of a
  not-found branch), not just the metadata. Witnessed 2026-08-15:
  `prerender:semantic-check` validated title/description/canonical/H1/
  NAP/JSON-LD across 9 routes and passed all of: a 1-star review under
  the homepage's "five-star reviews" headline, a price-comparison route
  with ZERO per-size floor rows while the live endpoint served 9, and
  10 blog articles serving HTTP 200 with "ARTICLE NOT FOUND" while
  `content.articleBySlug` had full content for every one — ten
  acquisition pages invisible to search for four days, all green
  (#1588).
- **Never run `pnpm run regen` locally to refresh the committed
  prerendered tree.** `regen` (`scripts/regen-prerender.mjs`) rewrites
  the tracked tree — a different script from `prerender` above, which
  only writes `dist/`. A LOCAL regen loses DB-backed payloads; a CI
  regen loses Places-API-backed payloads unless `GOOGLE_MAPS_API_KEY`
  is set in that workflow. Check what the environment can actually
  reach BEFORE regenerating, and diff the payload afterwards.
  Witnessed 2026-08-15: a local regen (`6d99b9e3c`) broke all 10 blog
  articles plus the price floors; the CI refresh that then "fixed" it
  regressed `/reviews` (132,918 bytes / 5 cards -> 107,213 bytes / 0
  cards) because that workflow has no `GOOGLE_MAPS_API_KEY` — the tree
  has oscillated between environments for weeks (#1588).
- **After every regen, verify the swap didn't silently drop routes.**
  `pnpm run regen` can exit 0 and report "Broken: 0" while tolerating
  up to 10% failed routes — and the swap DELETES those routes' previous
  files. (1) grep the regen log for `✗` and for `skipped`. (2) Run
  `node scripts/check-prerender.mjs` and git-restore any missing route
  dirs (`git checkout -- prerendered/<route>`) before committing.
  Witnessed 2026-08-19: exit 0 / "Broken: 0" while 10 blog routes
  failed on a latent scoping bug and the swap dropped their files (340
  -> 327); two more routes timed out on the 50s budget the second run
  and also needed git-restore (#1709).
- **`lint:source` matches `confirm (` / `prompt (` even inside a
  single-line JSX comment.** Its comment-skip heuristic tests for a line
  starting with `//`, `*` or `/*`, and a `{/* … */}` line starts with `{`
  — so the words "confirm (two-tap)" inside a JSX comment failed a commit
  (2026-08-12, `ApprovalsSection.tsx`). Reword the comment; do not fight
  the regex and never `--no-verify`.
- **`lint:pii` false-positives have a sanctioned line waiver.** A regex
  CONSTANT like `/email/i` reads to the linter as PII in a URL path
  (2026-08-12, `services/activityLedger.ts` — the matcher that MASKS
  emails). The mechanism is `// pii-allow: <reason>` on the line, and the
  reason is required. Read `scripts/lint-pii.mjs` before assuming a hit
  is real; it also allowlists the shop's own public numbers.
- **Do not fake timers around a sub-2 s REAL sleep that sits behind
  `await import()`.** `advanceTimersByTimeAsync` can run before the dynamic
  imports reach the `setTimeout`, so the sleep never fires; local speed hides it.
  `server/postInvoiceFollowUp.test.ts` passed locally and timed out at 30 s in
  CI (2026-10-02, fixed in `faa36e64`). Use real timers with an explicit
  per-test timeout, or inject the sleep.
- **Run the fail-open-slice gate when a diff adds a test that slices source
  text:** `pnpm exec vitest run server/failOpenSliceGate.test.ts` (3 ms), and use
  `sliceBlock()` from `server/testUtils/sourceBlock.ts`, never raw
  `slice(indexOf(...))`. Red in CI on 2026-10-01 (#2865), 2026-10-02 and again
  2026-10-08 (`tierCadence.test.ts`, `declaredSourceAtGeneration.test.ts`); the
  full suite is the only other place it shows.
- **Do not `export` a value only so a test can read it.** knip's orphan gate
  does not count a test as a consumer (`ASS_CAPTION_MARGIN_V`,
  `DUE_CHECK_SLACK_MS`, 2026-10-08: found after a 474 s suite, twice). Derive
  the value in the test from the function's behaviour or its output. When the
  diff adds an `export`, run `pnpm run lint:orphans` in the targeted loop.
- **Before changing a call site, find the source-shape pins on it:**
  `grep -rn '<fnName>(' --include='*.test.ts*'`. A test that asserts source
  text goes red only at full-suite time
  (`contentExperimentArmKey.test.ts`, 2026-10-08).
- **A render or pixel test uses the PRODUCTION asset** (font, overlay, LUT). OS
  faces are fallbacks only: `captionSafeZone.test.ts` rendered with DejaVu Sans
  Bold as "wider, so conservative" and measured 936 px against an 894 px
  budget on every Linux box, while production's Anton measures 600 px.
- **A script that rewrites a committed data file aborts on a failed round-trip
  check, it does not print.** A Python edit of `angle-bank.json` printed
  `round-trip identical: False`, wrote anyway, and turned a 7-line change into
  a 1,515-line diff. `sys.exit` on mismatch; a file with its own layout gets a
  line edit.
- **A refusal on a path a scheduler calls must throw what the caller's catch
  types.** `dailyReelPost` advances the rotation only on
  `ReelPreflightBlockedError`; four bare `Error` throws in `enqueueReelJob`
  would have cost every following day's Reel (2026-10-08, one was a new gate
  whose test pinned the bare throw). `reelEnqueueRefusalAdvance.test.ts` now
  fails on any new one; a test that pins the throw's text pins the bug.
- **`pnpm run lint:hooks` audits hook-after-early-return.** A hook
  called after an `if (...) return null` silently breaks React. The
  lint catches it; don't bypass.
- **`pnpm run validate:routes` confirms registered routes match
  handler files.** Run after adding / removing routes.

## Instrument runs (cage match / ghost replay / any measurement script)

Three instrument-integrity failures in one arc (2026-08-06/07) share a
shape: the measurement lied while every gate stayed green.

- **A liveness probe must exercise the EXACT model/lane/config the
  measured work uses.** The 2026-08-07 cage gauntlet probed the ambient
  default lane (gpt-4o, key present), then burned all 8 seeds against the
  pinned adversary lane (Ollama, key absent). A probe of a different lane
  is a false-green generator. Fixed structurally in #1416
  (`probeBothLanes()`); hold new instruments to the same bar.
- **A run that completed ZERO units of work must exit non-zero.** The
  same gauntlet printed `0 losses` with exit 0 after 0 matches ran.
  Zero-measured must never render as zero-findings.
- **Model lanes must be pinned in the instrument, never ambient.**
  Without `AI_FORCE_OLLAMA` a bare `invokeLLM` resolves to
  `LLM_MODEL || gpt-4o` on OpenAI; with it, EVERY request — explicit
  pins included — flattens onto one model, silently defeating duel
  role-diversity. Pin by Ollama-native substring name (routes with no
  flag); see `AGENT_MODEL` in `scripts/cage-match.ts` and
  `GHOST_AGENT_MODEL` in `server/services/ghostReplay.ts`.

## Running a script that needs real credentials

- **nickstire's `.env` does NOT carry the Ollama key.** `OLLAMA_API_KEY`
  lives in `apps/statenour/.env` locally and on Railway in prod — grep
  proof 2026-08-07: absent from both the primary and worktree nickstire
  `.env`. Inject it per-shell for local instrument runs.
- **Background / `run_in_background` shells inherit NO inline env.**
  Earlier runs worked only because the interactive shell happened to
  carry the key; the fresh background shell had nothing. Set the env in
  the SAME command that runs the script.
- Scripts that need a foreign-app key must fail fast naming its home
  (pattern: `scripts/cage-match.ts` after #1416).

## Multi-session push protocol

`main` is shared between concurrent Claude sessions (e.g., nickstire
+ statenour). On a push:

1. `git fetch origin` first.
2. Read `git log origin/main..HEAD --oneline` to see all unpushed
   commits — including the **other** session's. Whoever pushes carries
   everyone's committed work.
3. The pre-push hook runs `turbo run build --filter=...[$UPSTREAM]`
   for **both apps**. If the other session has a broken build in its
   working tree, your push is also blocked. Do NOT `--no-verify`
   (that's the gate stopping a broken deploy).
4. Don't rewrite shared history (disrupts the other session).
5. If blocked by the other app, surface to the operator with a
   self-contained prompt for that session to fix and push.

## Deploy verification

After a successful push:
1. `curl -s https://nickstire.org/api/health` returns `uptime` in
   seconds since the container started. A successful redeploy resets
   it. Poll uptime; when it drops to a low value, the new container
   is serving.
2. Browser caches OLD JS bundles aggressively. Verify a deploy by
   either (a) `curl` for the actual bundle and grep for new strings,
   or (b) hard-reload with `?cb=fresh` query param to force a clean
   load.
3. Railway watch-paths are per-app: `apps/nickstire/**` triggers a
   nickstire redeploy only; `apps/statenour/**` triggers statenour.
   A test-only file under `apps/nickstire/` still triggers a redeploy
   (bundle is identical, but container restarts).

## Verifying a user-facing copy change

Source-grep is necessary and not sufficient. Both halves failed once on
2026-09-03 (fixed in #2099):

1. **Sweep case-insensitively.** A grep for `"new ownership"` missed the
   capitalized `"New ownership"` in a hero intro and it shipped. Use
   `grep -ri`, always.
2. **Confirm the rendered page in REAL Chrome, not the in-app browser.**
   The in-app browser blocks the site's fonts, so it is not a fair visual
   check — the miss above was only caught by loading the live page in
   real Chrome.
3. **Source and served HTML can disagree.** #2094's indexing was silently
   defeated because 10 of 12 routes served STALE prerender snapshots with
   the old `noindex`. The drift-catcher
   `client/src/__tests__/prerender-indexability-consistency.test.ts`
   (#2098) now proves the `indexed` flag, `routes.ts`, `SITEMAP_ROUTES`
   and the prerender snapshot robots all agree — run it after any
   indexability or copy change that a crawler reads.

**Business-truth claims are operator-owned facts.** `shared/business.ts`
is canonical and `client/src/__tests__/canonical-business-truth.test.ts`
enforces agreement with it. Never assert tenure, ownership, review count
or rating from code inference — Nick's is the SAME owner who renamed
Moe's Tire & Auto (owner-confirmed 2026-09-03), so "new ownership" and
"run by Moe" are both false.
