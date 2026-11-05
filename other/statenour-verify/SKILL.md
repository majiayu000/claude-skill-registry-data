---
name: statenour-verify
description: Use before committing or pushing changes to the statenour app (apps/statenour/) — the real local verification sequence and the two gates that silently pass when run naively.
triggers: statenour commit, statenour push, verification sequence, gates that silently pass, tsc noemit, cross-env, windows paths in .env, verify gate, prunetools phrasings
---

# statenour-verify

Verify a statenour change is safe to commit/push. The gate names are
non-obvious and two of them silently lie if run carelessly.

## Run, in order (from `apps/statenour/`)

1. `pnpm typecheck` — `tsc --noEmit`. Must be 0 errors.
2. `pnpm lint` — `eslint .` (2026-07 consolidation; the old
   `lint:source` script no longer exists — if you see it referenced,
   that doc is stale).
3. `pnpm test` — vitest. Must end `Test Files N passed (N)`, exit 0.
4. (full gate) `pnpm verify:hard` — typecheck:raw + lint + test +
   check:raw-sql + check:crons + check:stale-docs (strict) +
   prompt:size-check + prisma validate.

## Traps

- **`vitest.setup.ts` is not wired, so no test runs in a fixed timezone.**
  `apps/statenour/vitest.setup.ts:1` sets `TZ` to America/New_York, but
  `vitest.config.ts:27` lists only `tests/setup/auth-guard-mock.ts` in
  `setupFiles`, so that file never loads. Never assume a timezone in a test:
  run any date test once with `TZ=UTC` from Git Bash before trusting a local
  green (this laptop runs Eastern, CI runs UTC). Witnessed 2026-10-22: a
  due-date test passed locally and failed in CI on PR 3239.
- **A script that loads env in its body must not statically import
  `lib/prisma` (directly or transitively).** ES imports are hoisted above a
  `process.loadEnvFile(...)` call, and `lib/prisma` reads only
  `apps/statenour/.env*`, so the client is built with no `DATABASE_URL`
  ("No database host"). Import Prisma inside the function that needs it and
  pin it with a test that the module loads without loading Prisma
  (`tests/lib/obsidian-engine-status-lazy-prisma.test.ts`). Witnessed
  2026-10-02: the Obsidian engine never wrote a status row to prod.
- **Windows paths in `.env` use forward slashes.** Inside double quotes
  Node's `loadEnvFile` expands `\n`, so `"C:\Users\nourd\..."` loads as
  `C:\Users` plus a newline (witnessed 2026-10-02 on `OBSIDIAN_VAULT_PATH`).
- **A typecheck error inside `.next/types/**` is a STALE LOCAL ARTIFACT,
  not your diff.** Symptom: `tsc --noEmit` fails on
  `.next/types/validator.ts` — `Cannot find module '../../app/api/<x>/
  route.js'` — for a route that does not exist. Cause: `main` deleted the
  route after your worktree's last `next build`; the generated validator
  still enumerates it. Fix: **overwrite** the offending generated file
  (e.g. write a one-line comment into it); the next build regenerates it.
  Do NOT recursively delete `.next/types` — `Remove-Item -Recurse` on a
  worktree path is policy-blocked (the junctions walk into the primary
  checkout). Witnessed 2026-08-07 on `app/api/system/prompt-compare`.
- **`pnpm test | tail` masks the exit code.** A piped command's exit
  status is `tail`'s (0), not vitest's. Read the actual
  `Test Files … failed` summary line, or run `pnpm test; echo "EXIT=$?"`
  with no pipe.
- **PowerShell `Select-String` is case-insensitive by default.** A vitest
  summary capture with a bare `'Tests'` pattern also matches `tests 14ms`
  inside the Duration line — witnessed 2026-08-04: four mutation probes
  printed Duration lines as their "results" and verified nothing. Use
  `-CaseSensitive` with an anchored pattern (`'^\s*Tests\s+\d'`), and read
  one captured line before trusting a batch of them.
- **`typecheck` does NOT cover `tests/`.** A green `tsc --noEmit` says
  nothing about test-fixture correctness — only a test run does. Proven
  2026-07-30 (#1238): a test fixture omitted a newly-required field on
  an interface, typecheck exited 0, and vitest was the only thing that
  caught it. Never report "verified" off typecheck alone.
- **`pnpm typecheck` never compiles `scripts/` either** — both `scripts/`
  and `tests/` are tsconfig-excluded. Verify a new or changed script with
  a scoped tsconfig extending the app's, with the script under `files`:
  `{"extends":"./tsconfig.json","files":["scripts/<file>","next-env.d.ts"],
  "include":[]}`, then `tsc --noEmit -p` that file. Check
  `tsc --listFilesOnly -p <config>` names the script before trusting its
  exit 0: a child `include` does not undo the base `exclude`, so the old
  `include` form compiled nothing and exited 0 (measured 2026-11-05, a
  planted type error went unseen). Tests have no such workaround —
  they're verified by execution only, never by typecheck.
- **A green `tsc` can still ship a broken `next build` — a different
  failure mode from the `tests/`/`scripts/` exclusion above, same "green
  tsc lied" shape.** Before importing between `lib/observability/*` (or
  anything reachable from `*.client.config.ts` / `instrumentation-client.ts`),
  ask which bundle the IMPORTER lands in — a Node-only dependency reachable
  from the browser graph fails `next build`, never `tsc --noEmit`. Run the
  real build when you change an import edge, not just typecheck.
- **A comment asserting "covered by `<other file>`" is a coverage CLAIM,
  not a fact** — grep the named file for the symbol/category before
  writing it, exactly like any other receipt. If the coverage doesn't
  exist yet, write the test first, or write "NOT yet covered" instead.
- **TS2307 "cannot find module" in a file OUTSIDE your diff = stale-junction
  phantom, not your regression.** Worktree node_modules are junctions to the
  PRIMARY checkout; if the primary sits behind main, packages added since
  (witnessed 2026-08-27: `edge-tts-universal` from #1930) do not resolve.
  Confirm with `git show HEAD:apps/statenour/package.json | grep <pkg>` vs
  what is installed - the fix is refreshing the PRIMARY checkout, never
  patching the app.
- **lefthook's parallel pre-commit jobs can flake red under memory
  pressure** and pass unchanged on retry (witnessed twice 2026-08-27:
  statenour-typecheck 149s red -> green, agent-os-verify red while the
  same command passed standalone). Rerun ONCE before diagnosing; twice
  red at identical duration = real.
- **A green CI job is not a green sweep; read the TASK count.**
  `paths-filter` (`.github/workflows/test.yml`) decides whether the `node` JOB
  runs; `turbo run --affected` decides which PACKAGES run inside it. A
  workflow-only diff satisfies the first and is empty to the second, so the job
  goes green having compiled nothing (witnessed 2026-09-16: #2362 was cited as
  the heaviest case and it passed; it ran zero turbo tasks). Before citing a CI
  run as proof a build-level change worked, open the sweep step's log:
  `Tasks: 0 successful, 0 total` and a full sweep are the same colour.
- **Any build-resource number must be taken COLD.** CI always is (fresh
  checkout, remote caching disabled); a local repeat is not. `Compiled
  successfully in <10s` is the tell: that run skipped the compile and
  type-check phases that hold the peak. Delete `.next` between arms, and never
  write a locally measured MB figure into a workflow comment without naming
  the cache state (witnessed 2026-09-16: warm 4962 MB vs cold 6778 MB; #2368
  existed only to retract the figures).
- **The full suite runs from a shell with `bash` on PATH.**
  `tests/repo/anti-slop-gate.test.ts` and
  `tests/redteam/repo-canary-gates.redteam.test.ts` spawn `bash`; from the
  PowerShell tool they fail (39 tests, exit 1, empty output on 2026-10-15) and
  pass from Git Bash (195 tests). Before diagnosing either with exit 1 and no
  output, check `Get-Command bash` / `which bash` in the shell that ran the
  suite; both helpers fold every spawn error into exit 1, so that signature
  alone does not prove a missing bash. If those two files are the only reds in
  PowerShell, rerun them from Git Bash before calling them real.
- **A partial directory list is not a sweep.** Before RETURN on any copy or
  class sweep, run the whole statenour vitest suite once, from Git Bash, alone.
  Witnessed 2026-10-16: a lane ran six directories and reported green; CI then
  failed on `tests/home/waiting-line.test.tsx:59`, a casing pin outside that
  list (about 45 runner-minutes).
- ~405 eslint `any` warnings are pre-existing and non-blocking — only
  `error`-severity problems fail the gate.
- Vitest can abort with a native `failed to delete napi ref` crash on
  Windows (exit 0xC0000409) right after other heavy node processes —
  that's infra flake, not a test failure. Re-run standalone.
- Pushing `main` deploys statenour to Railway; the repo-level pre-push
  hook runs `turbo build`, NOT the test suite — confirming a green
  `pnpm test` locally is on you.
- **`git push` itself runs `build:affected` inside pre-push** — give it a
  600s timeout and run it in the background (the default 120s times out
  as exit 143 with nothing pushed). The local SHA is not the receipt that
  the push landed; prove it with `git ls-remote origin refs/heads/<branch>`.
- **Never invoke `cross-env` bare in PowerShell, and never trust a
  `FINAL_EXIT=$LASTEXITCODE` sentinel after a `&&` chain.** Witnessed:
  chaining gates through `... && cross-env STALE_DOCS_STRICT=1 pnpm
  check:stale-docs && ...` broke at bare `cross-env` — CommandNotFound is
  a resolution error, not an exit code, so the trailing sentinel printed
  **0** while three gates had silently never run. Use
  `$env:VAR='1'; pnpm <script>` instead, and **count the gate outputs
  rather than reading the sentinel** — a green sentinel after a broken
  chain reports the last RESOLVED command.
- **`check:lint-baseline` reporting NEW FILE on a file outside your diff
  is dep-bump archaeology, not your regression.** Confirm with
  `git diff origin/main -- <file>` (empty = not yours), then compare the
  baseline snapshot's last commit against the last eslint bump — a bump
  mints new warning classes in files nobody touched. Witnessed 2026-08-06:
  `app/(mastery)/system/fleet/page.tsx` was byte-identical to `main`
  while #1357's eslint dev-minor bump minted a fresh react-hooks class.
  Root `AGENTS.md` classifies this check non-blocking-red: **disclose it,
  chip the fix, do not absorb it into your PR.**
- **A prompt section joins the budget/trim economy ONLY with a `## `
  title.** `trimPromptToBudget` splits on `\n## ` and nothing else, so
  `###` sub-blocks FUSE into the preceding `## ` section and the trimmer
  can then only keep or drop the fused blob wholesale. Root cause of
  #1450: the Master Content Engine's ~30 `###` sub-blocks fused into one
  atomic ~80k section, so the 65k runtime slice dropped the ENTIRE engine
  on the primary lane — every non-anthropic content turn served with no
  content engine, behind a `prompt:size-check` that had been red since
  #687 and that everyone had learned to ignore.
- **A fire-and-forget write sharing a mocked model with the code under test
  spills calls ACROSS tests.** `vi.clearAllMocks` cannot fence an unawaited
  promise — the Phase-1 memory gateway's shadow receipts ride the SAME mocked
  `brainMemory.create` the tests spy on, and receipts from earlier tests land
  in later tests' spy windows (5 visible in one window; red on main for a day,
  #1532). Assert with a discriminator filter (e.g.
  `category !== "memory_gateway_shadow"`), never raw call counts, and treat
  `calls[0]` reads as the same hazard.
- **N concurrent FIRST-TIME dynamic imports of a mocked module can race the
  mock registry** — some callers get the real module instead of the mock.
  Import the mocked module once before the fan-out and pass the binding
  down; don't let each concurrent caller `import()` it cold. A "mocked"
  test emitting the real module's log lines, or taking seconds instead of
  milliseconds, is this bug.
- **State shared between `instrumentation.ts` and app code must live on
  `globalThis`** (or another process-global), never module scope — the two
  load as separate bundles, so a module-scoped variable set in one is
  invisible in the other. Canary shape: `vi.resetModules()` plus a fresh
  import must still read the settled state; reading the pre-reset default
  instead means the state was module-scoped.
- **Before deleting a file, `grep -rn '<basename>' tests/`** — not just its
  import. A source-reading guard (`readSource`/`readFileSync`) references a
  file by string and survives an import-based dead-code sweep untouched,
  then breaks when the file it names is gone. When the guard's subject is
  legitimately retired, retarget the contract at the replacement surface —
  don't delete the canary.
- **Deleting the last file of a directory (a patch, a fixture, anything)
  can delete a directory a Dockerfile `COPY`s** — git does not track empty
  directories, so the next checkout simply lacks the dir the `COPY`
  expects. Run `tests/repo/dockerfile-copy-sources.test.ts` and read its
  message before pushing any change that deletes files under a `COPY`
  source; it exists in the suite specifically to catch this.

## Before declaring a prompt-injection / fencing fix done

One fixed renderer is not a fixed class. Witnessed: a fencing fix landed for
one of five assemblers that splice stored text into the chat system prompt
(contextual recall) while the cross-session thread, hybrid recall,
anticipatory recall, chat recall, and tool results (`searchColdMemory`,
`searchConversations`, customer-360 notes) all still reached the prompt bare
— found only by a hostile review, and again by a self-review after the "fix"
was declared closed.

Before declaring any such fix done, **enumerate every assembler** that
renders stored text into a prompt or a tool result — `brain-context.ts`
block producers, `system-prompt.ts` sections, `augment-final-prompt.ts`,
`context-hints.ts`, `lib/ai/tools/*` — and name each one as fenced,
allowlisted-with-reason, or not applicable. The durable gate shape is
`tests/ai/prompt-block-fencing-gate.test.ts`.

## Before shipping any report / diagnostic section

**Prove the source receives rows from the path it claims to observe.**
Run the query against prod — code inspection is not enough. A filter
whose discriminator value has no writer renders a fabricated all-clear,
and it is invisible to tests, typecheck, and lint.

This shape landed three times in one day (2026-07-30):

| Read | Reality |
|---|---|
| `apiRequestLog` where `path` starts `/api/ai/chat` | chat route never passes through the request logger — 0 rows ever |
| `ai_generations` where `status='failed'` | writers only ever emit `complete` / `error` |
| `error_logs` where `level='fatal'` | writers only ever emit `error` / `warn` |

Corollary: **a failed read must never render as good news.** Distinguish
"query failed" from "genuinely empty" — reference implementation is
`lib/observability/fleet-truth.ts`, where a thrown probe becomes
`unknown` and `unknown` never counts as healthy.

**When a finding rests on what a structure does NOT contain, read the
WHOLE structure by its delimiters — never a line-number window.**
`sed -n '/const typeMap/,/};/p'`, not `sed -n '140,165p'`. A truncated
read of a map is how orphaned-subject false positives are manufactured:
witnessed 2026-08-26, an audit reported nickstire's `typeMap` as having
"no mapping that yields booking" — delivered to the operator as a
finding — because the window cut off the map's head, whose first line is
`"nickstire:booking": "booking"`. Refuted only when fix work forced a
full read. Absence claims inherit the blast radius of "not in the repo
is a fact about your search": prove the search saw the whole subject.

**Before declaring a producer-side fix done on any rendered flag or
badge, grep the RENDER expression for every producer it ORs or aggregates
and check each one** — fixing one producer while a sibling still emits
the old value leaves the badge unchanged and the fix unproven. For chat
quality verdicts specifically, proof is reload + read the persisted
`tokenUsage.critic` / `tokenUsage.gate` blob via trpc `chat.conversation`
— a live-stream screenshot is a blind instrument for this surface; it
shows the stream, not what got persisted.

## Confirming a merge is DEPLOYED

"Merged" and "deployed" are different claims. Confirm via the
unauthenticated deploy surface, and compare by ANCESTRY, never equality:

```bash
DEPLOYED=$(curl -s https://bdnick.info/api/version | jq -r .data.build.commit)
git merge-base --is-ancestor <your-merge-sha> "$DEPLOYED" && echo LIVE
```

`jq` may be absent in git-bash — fall back to
`grep -o '"commit":"[a-f0-9]*"'` on the raw response body. Treat an EMPTY
`$DEPLOYED` as "the check is broken," never as "not deployed yet." Prefer
a per-turn one-shot check over a long-running background poll loop — a
turn boundary kills the loop silently and leaves you waiting on nothing.

Two waiter failure modes witnessed 2026-08-26, same session:
- **SHA equality breaks the moment a sibling merges** — the deployed SHA
  legitimately overtakes the one you await (watched prod run two
  later commits containing nothing of mine, then one containing
  everything; an equality waiter would call all three "not deployed").
- **A prefix longer than `commitShort` never matches** — the endpoint's
  `commitShort` is `sha.slice(0, 7)`; a 9-char comparison printed
  "still not deployed" forever over a build that was already live.
  Compare full SHAs via ancestry, or exactly 7 chars, nothing between.

**Promote this to a hard step before any "shipped" wording, not an
optional spot-check.** Run BOTH `railway status` (read `Deploy failed`
per service) AND the ancestry check above; a merge with only one of the
two is MERGED, never SHIPPED. Trap: `railway logs --build` with no
deployment id shows the latest SUCCESSFUL build, not the current one —
list deployments first and pass the FAILED deployment id explicitly, or
you'll read a stale green build log and call a broken deploy healthy.

## When the operator DECLINES a gate finding

A gate that always fails is a gate everyone learns to ignore — the exact
rot this repo keeps removing. So when the operator waives a finding:

- Waive **by signature, not by filename.** Put a marker on the offending
  line with a dated reason. Excluding the whole file blinds the check to
  every future violation in it.
- **Red-green the waiver:** green with it in place, and a fresh violation
  in the same file must still fail. Verify both; don't assume.
- Precedent: `check:anti-slop` + the stats-page gradient (#1239).

## Extra checks worth running (not in `verify:hard`)

- `pnpm check:anti-slop` — UI slop signatures (Inter/Roboto/Arial fonts,
  purple SaaS gradients). Line-level `anti-slop-allow` waivers.
- `pnpm check:policy-coverage` — every active cron has an
  AutomationPolicy row. **Needs prod `DATABASE_URL`**, so it can never be
  a CI/pre-push gate; run it manually.
- **Skill-registry freshness** — if `data/skills-registry.json`
  `generatedAt` is stale or `scripts/audit-skill-embeddings.ts` reports
  missing embeddings, the recall layer is blind to recently-installed
  skills. Refresh with `build-skill-registry.ts --merge` (**never
  `--force`** — it drops entries belonging to your other machines), then
  embed. Target state is `verdict: IN SYNC ✓`.

## When no statenour toolchain exists on the box

Witnessed 2026-09-02 (#2068): the primary checkout's `apps/**` had been wiped,
every worktree's `apps/statenour/node_modules` junction dangled, and
`pnpm install` inside a worktree is policy-blocked — so `typecheck`, `lint`
and the full vitest could not run anywhere. What still verifies, in order:

1. **Pure helpers run under the SIBLING app's vitest.** Put an ad-hoc config
   INSIDE `apps/nickstire/` (a config in the scratchpad cannot resolve
   `vitest/config`): `root` = the statenour dir, `resolve.alias["@"]` = that
   dir, `test.include` = your test files; run
   `apps/nickstire/node_modules/.bin/vitest run --config <it>`; delete the
   config after. Proves the helper, not the app.
2. **Static `check:*` scripts run under nickstire's `tsx`.** These ran
   without statenour deps: `anti-slop`, `et-clock`, `stale-docs` (STRICT),
   `raw-sql`, `get-auth`, `mutations:strict`, `soft-delete`, `crons`,
   `runbooks`. These could NOT load: `prompt-injection` (needs `glob`),
   `policy-coverage` (needs `@prisma/client` and prod `DATABASE_URL`).
3. **Commit + push from a hookless sparse scratch clone**, because the
   lefthook pre-commit typecheck and pre-push build would fail on the missing
   toolchain: `git clone --no-checkout <url> <dir>` · `git sparse-checkout
   init --cone` · `git sparse-checkout set apps/statenour` · branch from
   `origin/main` · `git apply` the patch from your worktree · commit · push.
   No install, so no hooks. **Disclose it in the PR body** ("commit pushed from
   a hookless scratch clone; CI is the gate") and merge only on fully green.

**The same hookless-clone technique applies to a MULTI-APP wave sharing
one worktree, for a different reason:** `turbo build --affected` reads
the working tree, so another app's uncommitted edits make ITS build a
gate for your push too. Either use one worktree per app, or export
per-app patches (`git add -N` for new files, then `git diff HEAD --binary
--output=<file> -- <paths>`) and commit each from its own hookless
scratch clone. Run the per-app pre-commit gates by hand on the STAGED
files first — a brand-voice or lint scan reports 0 files scanned, not a
pass, unless you staged them.

## Before calling a wave done

The author's own hostile pass is necessary, not sufficient. On the 2026-09-01
nickstire wave it found 5 defects; three parallel independent reviewers over
the full diff (silent-failure, schema + cross-app contracts, client/docs) found
24 more, including two P0 regressions the wave introduced. Dispatch reviewers
per subsystem with a file:line brief and a "verified OK / not checked" answer
shape, verify their top findings yourself, then declare done.

## Running an operator script that needs real credentials

`.env.local` is **not** the full credential set — several keys live only
on Railway. A provider-failure cascade is not proof of a billing problem
until you check which lanes actually had keys.

**A key's PRESENCE — an env-check boolean, a `.env` line, a doc's claim —
is never evidence of VALIDITY.** When any provider lane misbehaves, the
only real check is one live, cheap call against the provider from the
runtime that actually holds the key. Reading the key's existence proves
nothing about whether it still authenticates.

> Prefer `railway run --service statenour-web <cmd>` over hand-exporting
> vars. It injects the real environment, so the preferred provider lane
> actually gets tried.

Proven 2026-07-30: `embed-skills.ts` failed every provider (HuggingFace
402 credits-depleted, OpenAI 429 quota) and looked billing-blocked. The
real cause was that **Cohere — first in the chain and the only lane pinned
to 1024 dimensions — has no key locally but does on Railway.** Under
`railway run` it embedded 8 skills in one second.

Dimension trap in the same chain: Cohere pins `output_dimension: 1024`
and rejects anything else, but the OpenAI fallback returns **1536** with
no length guard. "Succeeding" on that fallback would silently poison a
1024-dim corpus — check `embedding_dim` after any embedding backfill.

**When every scenario in a run errors with the provider's sentinel value
in seconds, check the provider breaker or cooldown FIRST** — a recent
stray call or a recent failed call can trip it, and the next real attempt
inherits the trip. Re-run the identical command once before touching any
code. Never grade or trust a run whose Nick calls came back as sentinels;
it measured the breaker, not your change.

## Credentials in fixtures and diffs

Fixtures use synthetic values with the same shape, never a real
credential — not even in a test that proves the value gets redacted.
Before committing anything touching credentials, grep the diff for
fragments of every value the operator has shown you this session,
screenshots included. A green gitleaks scan is shape-dependent, not
value-dependent: the same real key passes as an inline argument and
fails only as `const secret = "..."` — don't trust it as the sole check.

## Reading an ambiguous CI or hook result

Two of every three "failures" in the 2026-09-02 wave needed no code
change. Triage before fixing:

- **`##[error]The operation was canceled.` is INCONCLUSIVE, not a pass.**
  A cancel can be a sibling's merge superseding the run, a manual cancel,
  or a timeout — and in every case the checks did not finish, so an
  absence of `FAIL` lines proves nothing about whether they would have
  failed. Read the cancellation cause, then **rerun**; root `AGENTS.md`
  is explicit: "If CI is cancelled by a sibling's merge, rerun; don't
  debug." Never treat a cancelled run as green evidence.
- **The completion-authority steps of the agent-policy job evaluate review threads at run time.**
  Resolving threads afterwards leaves a STALE red. Re-run it; do not
  re-litigate the threads. It compiles four sub-gates — know the one-line
  fix for each: rewrite the per-diff evidence entry (never reuse a prior
  diff's); resolve review threads via GraphQL `resolveReviewThread` AFTER
  replying to each, not before; obey the ledger ladder — fix the LABEL,
  never inflate the state; always run `scripts/render-reality-ledger.mjs`
  and commit the regenerated `.md` beside the `.json`.
- **List review threads (`gh api graphql … reviewThreads`) and READ them
  before resolving, every time.** Reply with evidence, then resolve — but
  a thread is sometimes right about a real bug the tests missed. Never
  resolve a thread just to clear the gate; that converts a correct
  reviewer finding into a shipped defect.
- **Trace reachability before assuming authorship.** An e2e failure
  looked like the wave's until traced: `/api/intel` has no import path to
  the changed code, the error was a heartbeat timeout (`curl rc=28`),
  neighbouring runs were cancelled, and a re-run passed.
- ⚠ **A pre-commit eslint OOM (exit 134) aborts the commit while the
  subsequent push prints `Everything up-to-date`** — which reads exactly
  like success and leaves the work uncommitted. **Check `git log` after
  any commit whose hook output looks odd.**
- ⚠ **`echo $?` after `cmd | head` captures head's status, not the
  command's.** A subagent reported a false-green typecheck this way.
  **Do not pipe a gate you intend to read the exit code of** — run it
  unpiped and read the summary line. `${PIPESTATUS[0]}` recovers it in
  Bash only; this repo's primary shell is PowerShell, where that array
  does not exist and `$LASTEXITCODE` after a pipeline is likewise the LAST
  command's. Unpiped is the portable answer.
- **Check the CI database version, not just prod.** CI is
  `pgvector/pgvector:pg16`, prod is PG17 — `IS JSON OBJECT` needs PG16+.
  Both fine here, but the gap is real and untested by default.
- **A gate that reports a failure COUNT with no LOCATION needs the
  instrument fixed before the finding.** Witnessed: gitleaks printed
  `leaks found: 1` with no rule/file/line; guessing (a
  `google-site-verification` meta tag) shipped a wrong, mis-scoped
  allowlist while the red stayed red. `--report-format json
  --report-path` gave the real hit (`generic-api-key` on a minified
  analytics key). **Never scope an allowlist to a LINE on minified
  HTML** — one line can be the whole 15KB document, and a real secret
  sharing it would be exempted too. Scope to the matched text.
- **`gh pr checks` reporting zero rows is not "settled," and a pushed
  SHA with zero check-runs while Actions shows operational is a stalled
  event delivery, not a billing question.** Require a positive row
  count (`pass > 0`, not just `pending==0 && fail==0`) before trusting
  a settle loop. If check-runs never appear on a pushed SHA, push the
  next real commit — closing/reopening the PR does not re-fire them.

## After MODIFYING a verified query, re-run it

A receipt for the old version is not a receipt for the new one. Recorded
after a wave modified a SQL statement post-verification and shipped it
unre-run.

## A negative result from a third-party API is not evidence yet

Before recording "the record isn't there", clear two failure modes that both
return a clean, believable empty result:

1. **The vendor's naming convention.** Langfuse stores an observation as
   `<functionId>:<span>` — searching `observability-probe` finds nothing while
   `observability-probe:ai.generateText` is sitting right there.
2. **List endpoints are PROJECTIONS.** On `GET /api/public/v2/observations` a
   field comes back only if its group is requested with `fields=` (default
   `core,basic`), so an unrequested field reads as absent. The legacy
   `GET /api/public/traces[/<id>]` detail route is removed from Langfuse Cloud
   on 2026-11-16. Querying without the group returns "absent" for a field that
   is present.

Both fired in one run, and nearly recorded a WORKING pipeline as dead — in a
session whose whole subject was a health badge that lied. **Prove the reader
works by matching one record you know exists**, then trust its zeroes. Same
discipline as [empty-vs-error](../empty-vs-error/SKILL.md): absent and broken
are different answers, and a thin projection makes them look identical.

## Naming collisions in a spread-order barrel

`nourTools` spreads multiple domain files in order — the LAST one to declare a
given key wins, silently. Adding a tool whose name already exists elsewhere in
the barrel overwrites a working tool with no error, and the catalog's total
count stays flat (one key replaced the other), so a count-only sanity check
won't catch it. Witnessed: a new `scheduleFollowUp` silently shadowed an
existing customer-facing follow-up tool of the same name; caught only by
`catalog-integrity`'s stronger check.

Before adding a tool: `git grep -n '<name>: tool('` across `lib/ai/tools/`.
Register in BOTH `catalog.ts` and `tool-families.ts` — their category/cost
unions differ, and only the pre-commit typecheck catches a mismatch between
the two.

**Registration is not reachability for the chat pruner either.** A tool
correctly present in all three registries can still be invisible to
`pruneTools` for all but one of five realistic phrasings — the trigger
regex and the attach-pattern regex are different, and a tool can match one
without the other. After adding a chat tool, run `pruneTools` against 5
phrasings a real user would type and assert the tool actually surfaces; a
registered-but-unreachable tool measured this way on a real wave got
attached for only 1 of 5 tries.

## When NOT to use

Non-statenour work, or nickstire (it has its own `pnpm run verify`).
