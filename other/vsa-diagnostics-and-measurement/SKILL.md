---
name: vsa-diagnostics-and-measurement
description: Load when you need to MEASURE something on the VSA website instead of eyeballing it — verifying RLS security (scripts/verify-rls-security.mjs), auditing Supabase storage/egress (docs/supabase-usage-audit.sql), checking bundle size (npm run analyze), running Lighthouse/axe/web-vitals for performance and accessibility, inspecting Edge Function or Vercel logs, checking Graphify graph staleness, or answering "how big / how slow / how exposed is X?". Provides every diagnostic instrument in the repo with exact invocation, output interpretation, and what "good" looks like, plus two ready-made helpers (check-graph-freshness.sh, route-inventory.mjs).
---

# VSA Diagnostics and Measurement

This skill is the instrument panel for the VSA website. It tells you, for every measurable question about the codebase or the production system, which tool answers it, the exact command to run, how to read the output, and what a healthy result looks like. Use it whenever you are tempted to say "looks fine" — measure instead.

**When NOT to use this skill:**

| If you need… | Load instead |
|---|---|
| To fix something a measurement revealed is broken | `vsa-debugging-playbook` |
| The story behind the egress crisis or RLS recursion outage | `vsa-failure-archaeology` |
| RLS/migration authoring theory (SECURITY DEFINER, view grants) | `vsa-supabase-security-reference` |
| The evidence bar for calling a change "done" (lint/build/test) | `vsa-validation-and-qa` |
| To actually deploy, run migrations, or operate the image pipeline | `vsa-run-and-operate` |
| Permission to change what you measured (protected domains) | `vsa-change-control` |
| The mobile/UI improvement campaign that consumes these numbers | `vsa-ui-excellence-campaign` (if present) |

Jargon used below, defined once: **RLS** = Row Level Security, Postgres per-row access policies — the only thing standing between the anon key (which ships in the JS bundle) and member data. **Egress** = bytes served out of Supabase (Storage downloads + DB responses); it is the billable resource that caused this project's costliest incident. **anon key** = the public Supabase API key; everything it can do, any visitor can do. **CRA** = Create React App, this project's build tooling.

---

## 1. Which instrument for which question

| Question | Instrument | Command | Section |
|---|---|---|---|
| "How does subsystem X work / what touches file Y?" | Graphify | `./scripts/graphify-run query "..."` | §2 |
| "Is the code graph up to date?" | freshness helper | `bash .claude/skills/vsa-diagnostics-and-measurement/scripts/check-graph-freshness.sh` | §2, §9 |
| "Can anon/users read or write what they shouldn't?" | RLS verifier | `node scripts/verify-rls-security.mjs` | §3 |
| "What is eating Supabase storage / egress / DB size?" | usage audit SQL | run sections of `docs/supabase-usage-audit.sql` in the SQL editor | §4 |
| "Did my change bloat the JS bundle or break lazy loading?" | source-map-explorer | `npm run analyze` (or `:css`, `:all`) | §5 |
| "Is the site fast on a phone?" | Lighthouse | `npx lighthouse http://localhost:3000 ...` against a prod build | §6 |
| "Is the page accessible?" | axe | `npx @axe-core/cli http://localhost:3000` | §6 |
| "What are real users' Core Web Vitals?" | web-vitals | wired in `src/reportWebVitals.ts` (currently a no-op — see §6) | §6 |
| "Why is a query refetching / cache stale?" | react-query devtools | not installed by default — see §7 | §7 |
| "What did the Edge Function do at runtime?" | Supabase logs | `supabase functions logs <name>` or Dashboard → Edge Functions → Logs | §7 |
| "What happened on the deployed site?" | Vercel logs | `npx vercel logs <deployment-url>` | §7 |
| "What routes exist right now?" | route inventory helper | `node .claude/skills/vsa-diagnostics-and-measurement/scripts/route-inventory.mjs` | §9 |

---

## 2. Graphify — measure the codebase before reading it

Graphify indexes the repo into a knowledge graph (`graphify-out/graph.json`). This repo enforces query-first exploration: run a graph query before opening source files.

```bash
./scripts/graphify-run query "how does check-in points flow work?"   # scoped subgraph answer
./scripts/graphify-run explain "EventsRepository"                    # one node + neighbors, plain language
./scripts/graphify-run path "src/routes/index.tsx" "supabase.ts"     # shortest connection between two things
./scripts/graphify-run hook status                                   # is the auto-update git hook active?
```

Use the `./scripts/graphify-run` wrapper, not bare `graphify` — subagent PATH usually lacks `~/.local/bin`.

**Reading the output:** `query` prints NODE lines (name, source file, line) and EDGE lines (relationships). The `src=` / `loc=` fields are the payload — they tell you exactly which file and line to read next. `explain` gives prose. If the answer looks thin or names files that no longer exist, check staleness.

**Staleness check** — `graphify-out/GRAPH_REPORT.md` records `Built from commit:` near the top. Compare with `git rev-parse --short HEAD`:

```bash
bash .claude/skills/vsa-diagnostics-and-measurement/scripts/check-graph-freshness.sh
```

Exit 0 = fresh; exit 1 = stale (or report missing). A stale graph is not useless — architecture answers usually survive a few commits — but do not trust it for anything touched by recent commits (`git log --oneline <graph-commit>..HEAD` shows exactly what it is blind to). Refresh with `graphify . --update` (interactive sessions only; commit the graph output separately per `vsa-docs-and-writing`).

**When to fall back to grep:** Graphify not installed (wrapper prints an install error), the graph is stale over the area you are investigating, or you need exact strings/line numbers (grep is the right tool for "find every `supabase.from('members')`"). Fall back to *targeted* `grep -rn` / `ls`, never to reading whole directories.

---

## 3. RLS verification — `scripts/verify-rls-security.mjs`

**What it measures:** whether the database's RLS policies actually enforce the project's security model, by connecting with the same anon key the public site uses and attempting reads/writes that must fail (and admin operations that must succeed). This is the instrument that would have caught both of the project's costliest incidents earlier; run it after ANY migration touching policies, grants, views, or the points/attendance tables. Companion runbook: `docs/rls-verification-checklist.md`.

### Invocation

```bash
node scripts/verify-rls-security.mjs
```

No npm script wraps it (as of 2026-07-06); plain `node` works, it needs only `@supabase/supabase-js` which is already a dependency. The script loads `.env.local` then `.env` from the cwd, without overriding variables already in your shell.

### Environment variables (read at lines 31–32 and 62–100, 342–366 of the script)

| Variable | Purpose | Required? |
|---|---|---|
| `VITE_SUPABASE_URL` **or** `REACT_APP_SUPABASE_URL` | target database (VITE_ checked first, falls back to REACT_APP_ — so your normal `.env.local` just works) | yes |
| `VITE_SUPABASE_ANON_KEY` **or** `REACT_APP_SUPABASE_ANON_KEY` | anon key | yes |
| `RLS_TEST_USER_EMAIL` / `RLS_TEST_USER_PASSWORD` | ordinary (non-admin) test account | no — section 2 SKIPs without it |
| `RLS_TEST_ADMIN_EMAIL` / `RLS_TEST_ADMIN_PASSWORD` | admin test account | no — section 3 SKIPs without it |
| `RLS_TEST_EVENT_ID`, `RLS_TEST_MEMBER_ID`, `RLS_TEST_DATA_RIGHTS_REQUEST_ID` | real UUIDs for targeted checks (default: the zero UUID) | no |
| `RLS_ALLOW_MUTATION_TESTS` | `true` enables admin INSERT/DELETE tests on `event_attendance` / `user_points` | no — default off |

**Never** put a `service_role` key in this tool's environment — it bypasses RLS and makes every check meaningless (checklist §9). Use dedicated test accounts, not live member accounts.

### Check categories and what each proves

1. **Anonymous client** — anon must NOT read `members.user_id`/`members.email`, `event_check_in_secrets`, or `data_rights_requests`, and must NOT call the data-rights RPCs (`get_data_rights_dependency_preview`, `generate_data_rights_export`). Anon MUST still read safe member columns (`first_name`, `house`, `points`, …) — the public leaderboard depends on it, so this section catches over-tightening too.
2. **Ordinary authenticated user** — must NOT insert/update `event_attendance` or `user_points` directly (points are server-authoritative via the `check_in_to_event` RPC), must NOT read check-in secrets or data-rights rows/RPCs.
3. **Admin** — MUST read `event_check_in_secrets` and `data_rights_requests` and reach both data-rights RPCs. With `RLS_ALLOW_MUTATION_TESTS=true` only: verifies admin can directly insert then delete `event_attendance` (manual check-in support) and `user_points` rows.

### Reading the output

Each line is `PASS` (green), `FAIL` (red), or `SKIP` (yellow). Nuances:

- "returned empty list due to RLS" **PASS** — Supabase often returns 0 rows instead of an error when RLS filters everything; the script treats empty-as-denied for reads. For UPDATEs, "0 rows updated" is likewise a pass.
- The one asymmetric case: anon selecting sensitive member columns that returns *empty without error* is reported **FAIL** ("unconfirmed privilege state") — an empty table can't prove the columns are protected.
- Exit code 0 + `VERIFICATION PASSED` = all executed checks passed. Exit code 1 + `VERIFICATION FAILED` = at least one FAIL.
- SKIPs are not passes. A run with both credential pairs unset only proves the anon surface. For a release-grade claim, provide both test accounts so all three sections execute.

**Any FAIL means stop and audit migrations** — most likely a new table/view got default grants without RLS, or a policy was weakened. Interpretation theory (auto-updatable views, revoke-then-grant) lives in `vsa-supabase-security-reference`.

### Staging-before-production discipline (docs/rls-verification-checklist.md §3–4)

1. Run against staging first with full credentials; get all PASS.
2. Then run against production **read-only** (`RLS_ALLOW_MUTATION_TESTS` unset or `false`).
3. Mutation tests on production require an explicitly approved maintenance window and confirmed backups — they really write and delete rows in `event_attendance`/`user_points`, even though they clean up after themselves.
4. Manual dashboard checks the script cannot do: Storage bucket policies (anon = SELECT only; writes admin-only) and a codebase sweep that no client file mutates `event_attendance`/`user_points` outside the RPC path (checklist §8).

---

## 4. Supabase usage and egress — `docs/supabase-usage-audit.sql`

**What it measures:** where storage bytes, database bytes, and egress-driving content actually live. Run sections in the Supabase Dashboard SQL editor (SQL editor runs as postgres, so it can see `storage.objects`). Sections 1–7 are read-only; the file's own header says do not run the commented cleanup templates until you have reviewed exact candidate rows.

| § | Query | What it reveals | How to act |
|---|---|---|---|
| 1 | Storage usage by bucket | total GB and object counts per bucket, which buckets are public | The biggest bucket is your egress suspect #1. Public buckets serve bytes to anyone. |
| 2 | 200 largest objects in the image buckets | individual multi-MB images | Candidates for compression or migration to `public/images/` (the egress fix — `vsa-run-and-operate` owns the pipeline). |
| 3 | Storage by bucket + MIME/extension | e.g. uncompressed PNGs vs WebP | Fat PNG/HEIC populations = compression opportunity. |
| 4 | Duplicate files by ETag | identical content uploaded multiple times | `possible_savings` column quantifies the win; dedupe via Storage UI after manual review. |
| 5 | Referenced storage objects from app tables | which DB columns point at which storage objects | The reference map you need before deleting or migrating anything. |
| 6 | Orphaned storage candidates | objects no current app row references | Deletion candidates ONLY — export and review first; delete via Storage UI/API, never raw SQL on `storage.objects` (§12 note). |
| 7 | Largest Postgres tables and indexes | DB bloat, dead rows, unused indexes (`idx_scan` = 0) | Big tables with high dead-row counts → vacuum/cleanup conversation. |
| 8 | Largest rows in text-heavy tables | oversized `gallery_events` / `homepage_content` / `program_content` rows | Huge rows inflate every SELECT (= DB egress). |
| 9 | Attendance duplicate checks | duplicate `member_event_attendance` / `event_attendance` rows, import bursts | Points integrity, not egress. Findings route through `vsa-change-control` — attendance is a protected domain; the cleanup template in §12 is commented for a reason. |
| 10–11 | Test/demo rows; duplicate members | junk data, merge candidates | Review-only; member merges use `smart_merge_members` RPC only after the 11b/11c previews. |
| 12 | Cleanup templates | intentionally commented | Never run without a reviewed preview and (for protected tables) owner approval. |

**Where egress shows in the Supabase Dashboard:** the usage page for your organization/project (navigation label changes between dashboard versions — as of 2026-07-06 look under the organization's **Usage** page, "Egress" chart, with a per-service breakdown; UNVERIFIED exact menu path). Storage egress dominating the chart while §1 shows large public image buckets is the classic signature.

**The lesson already paid for:** this project once served all images from Supabase Storage and blew through the egress quota; the fix was migrating images to `public/images/` served by Vercel (`scripts/migrate-supabase-images-to-public.ts`, `docs/event-image-migration.md`). Full incident narrative: `vsa-failure-archaeology`. The standing rule this audit enforces: **new large media must not be hot-served from Supabase Storage** — run §1/§2 after any feature that uploads images, and never delete Storage originals (`vsa-run-and-operate`).

---

## 5. Bundle analysis — `npm run analyze`

**What it measures:** what is inside the production JS/CSS bundles, via `source-map-explorer` (a devDependency). Defined in `package.json`:

```bash
npm run analyze       # build, then explore build/static/js/*.js
npm run analyze:css   # build, then explore build/static/css/*.css
npm run analyze:all   # build, then explore both
```

Each runs a full `npm run build` first (~minutes), then opens an HTML treemap in your browser showing every source file's share of each output chunk.

**How to read it:**

- **Chunk count is the lazy-loading signal.** Routes in `src/routes/index.tsx` are `React.lazy`-loaded, so `build/static/js/` should contain one `main.*.js` plus many small numbered chunks (one-ish per lazy page). If a page's code shows up inside `main.*.js` instead of its own chunk, someone added a static import of a page module — a lazy-loading regression. Grep the importing file for a non-`lazy` import of that page.
- **Heavy imports:** in the treemap, `node_modules` blocks dwarf app code. Watch for a library appearing in `main` when only one page uses it (should be in that page's chunk), or duplicated across many chunks (hoist or restructure).
- Also compare raw gzip sizes: the tail of `npm run build` output prints per-chunk gzipped sizes with deltas vs the previous build — the cheapest regression check of all.

**Baseline:** capture on first run — record `main.*.js` gzip size and chunk count from the build output before and after your change; a change that grows `main` by more than a few KB needs a named justification. (No committed baseline exists as of 2026-07-06.) Do NOT run `analyze` speculatively in agent sessions — it triggers a full build; run it when a bundle question is actually on the table.

---

## 6. Web performance and accessibility (the UI campaign's instruments)

### web-vitals (field data)

`web-vitals@^2.1.4` is a dependency, wired in `src/reportWebVitals.ts` and called from `src/index.tsx` — but called **without a handler** (`reportWebVitals()`), so as of 2026-07-06 it measures nothing in production; it only collects CLS/FID/FCP/LCP/TTFB if you pass a callback (e.g. `reportWebVitals(console.log)` locally, or a function that posts to analytics). Note v2 reports FID, not the newer INP metric. Wiring it to real analytics is an open candidate improvement, not an implemented fact.

### Lighthouse (lab data) — the standard procedure

Measure a **production build**, never the dev server (dev is unminified and unrepresentative):

```bash
npm run build
npx serve -s build -l 3000        # static server with SPA fallback (-s)
# in another terminal:
npx lighthouse http://localhost:3000 \
  --form-factor=mobile \
  --screenEmulation.mobile \
  --throttling-method=simulate \
  --output=html --output-path=./lighthouse-mobile.html \
  --chrome-flags="--headless=new" \
  --quiet
```

Mobile emulation is Lighthouse's default, but the flags above make it explicit — mobile is this project's hardest live problem, so mobile numbers are the numbers. For a desktop comparison run add `--preset=desktop` (and drop the two mobile flags). Neither `serve` nor `lighthouse` is a repo dependency; `npx` fetches them — no new deps added to the repo. Repeat runs vary a few points; run 2–3 times and take the median before claiming a regression or a win.

**Which scores matter, in order:**

1. **Performance** — driven by LCP (target < 2.5 s), CLS (< 0.1), TBT. Route-level code splitting (§5) and image weight are the usual levers here.
2. **Accessibility** — Lighthouse's a11y audit is shallow; treat it as a floor and use axe (below) for the real check.
3. Best Practices / SEO — keep green; rarely the bottleneck.

Score baselines: capture on first run against `main` before comparing a branch. (No committed Lighthouse baseline exists as of 2026-07-06.)

### axe (accessibility, per page)

```bash
npx @axe-core/cli http://localhost:3000            # against the serve'd build
npx @axe-core/cli http://localhost:3000/events     # repeat per route (see route-inventory helper, §9)
```

Output lists violations with impact (critical/serious/moderate/minor), the WCAG rule, and CSS selectors of offending nodes. "Good" = zero critical and serious violations on every public route. axe only sees the initially rendered state — open modals/bottom sheets manually (or test those states separately) for full coverage. `@axe-core/cli` is fetched by npx; not a repo dependency, and requires a Chrome/driver locally (UNVERIFIED on this machine — if it fails to launch, fall back to the axe DevTools browser extension).

---

## 7. Runtime diagnostics

### react-query devtools

`react-query` v3 ships devtools inside the main package (`react-query/devtools`) — no new dependency needed — but they are **not wired in this app** (no `ReactQueryDevtools` anywhere in `src/`, verified 2026-07-06). To inspect cache/refetch behavior during local debugging, temporarily add inside the `QueryClientProvider` in `src/App.tsx`:

```tsx
import { ReactQueryDevtools } from 'react-query/devtools';
// inside the provider tree:
<ReactQueryDevtools initialIsOpen={false} />
```

The component self-excludes from production builds (`process.env.NODE_ENV === 'development'` guard is built in). Remove before committing anyway — this repo has not adopted it.

### Supabase Edge Function logs

Four Edge Functions exist under `supabase/functions/` (analytics-proxy, trigger-event-image-migration, trigger-house-event-image-migration, vsa-ai-assistant). Read their runtime logs either in the Dashboard (**Edge Functions → select function → Logs**) or via CLI:

```bash
supabase functions logs vsa-ai-assistant --project-ref <PROJECT_REF>
```

(CLI subcommand availability depends on your installed Supabase CLI version — UNVERIFIED on this machine; the Dashboard path always works.) Look for: non-200 status lines, cold-start latency, and `console.error` output the function itself writes. This is the only visibility into `vsa-ai-assistant` answer failures.

### Vercel logs (production runtime/deploy)

```bash
npx vercel logs <deployment-url-or-id>   # runtime logs for a deployment
npx vercel inspect <deployment-url> --logs   # build logs
npx vercel ls                            # find recent deployment URLs
```

Requires `vercel login` and the project to be linked (`vercel link`) — CLI auth state on any given machine is UNVERIFIED; the Vercel Dashboard's Deployments → Logs view is the fallback. This is a static CRA site, so runtime logs are mostly edge/request-level; build logs are where deploy failures show.

---

## 8. Measurement discipline

- **State the number before you change anything.** Every optimization claim needs a before/after pair from the same instrument, same flags, same machine.
- **One instrument per claim.** "Feels faster" is not a Lighthouse score; "the query looks safe" is not a `verify-rls-security.mjs` PASS.
- Findings about protected domains (points, attendance, leaderboard, RLS) are *inputs* to `vsa-change-control`, never license to fix in place.

---

## 9. Shipped helpers (`.claude/skills/vsa-diagnostics-and-measurement/scripts/`)

### check-graph-freshness.sh

Compares `Built from commit:` in `graphify-out/GRAPH_REPORT.md` against `git rev-parse HEAD`. No dependencies beyond git + bash.

```bash
bash .claude/skills/vsa-diagnostics-and-measurement/scripts/check-graph-freshness.sh
```

- Exit 0: `FRESH` — graph matches HEAD.
- Exit 1: `STALE` — prints both commits and how many commits behind the graph is (plus a hint to run `graphify . --update`), or reports the report/graph file missing.

Run it at the start of any session that will rely on Graphify answers.

### route-inventory.mjs

Extracts every `path="..."` route from `src/routes/index.tsx` with a pure-regex parse (node only, zero dependencies) and classifies each as `public`, `protected`, or `admin` by its position relative to the `ProtectedRoute`/`AdminRoute` wrapper elements in the file.

```bash
node .claude/skills/vsa-diagnostics-and-measurement/scripts/route-inventory.mjs        # human-readable table + counts
node .claude/skills/vsa-diagnostics-and-measurement/scripts/route-inventory.mjs --json # machine-readable
```

Uses: generating the per-route loop for axe/Lighthouse sweeps (§6), spotting an unregistered page, verifying a new route landed in the right tier. The tier classification is heuristic (text-position based) — if `src/routes/index.tsx` is restructured away from wrapper elements, re-verify the script against a manual read of the file.

Note (as of 2026-07-07): the `protected` tier currently yields **zero** routes — `src/routes/index.tsx` uses no `ProtectedRoute` wrapper because member self-service is parked (see `vsa-architecture-contract` route-tier table). Expect only `public` and `admin` in the output today; `protected` is retained as a classification for when member accounts return.

---

## Provenance and maintenance

Sources (all read in full, repo state as of 2026-07-06, branch `codex/reactbits-ui`, HEAD `368fbf63`):

- `scripts/verify-rls-security.mjs` (441 lines — env fallback at L31–32, mutation gate at L361)
- `docs/rls-verification-checklist.md`, `docs/supabase-usage-audit.sql` (424 lines, 12 sections)
- `package.json` (scripts block; `web-vitals@^2.1.4`, `source-map-explorer` devDependency, `react-query@^3.39.3`)
- `src/reportWebVitals.ts`, `src/index.tsx` (web-vitals wiring), `src/routes/index.tsx` (route shapes)
- `graphify-out/GRAPH_REPORT.md` ("Built from commit" header), `CLAUDE.md` (graphify-run subcommands)

Re-verification one-liners (run when this skill might have drifted):

```bash
grep -n '"analyze' package.json                                  # bundle-analysis scripts still exist
grep -n 'VITE_SUPABASE_URL\|RLS_ALLOW_MUTATION' scripts/verify-rls-security.mjs   # env contract unchanged
grep -c '^-- [0-9]' docs/supabase-usage-audit.sql                # audit sections still numbered
grep -rn 'reportWebVitals(' src/index.tsx                        # still called without a handler?
grep -rn 'ReactQueryDevtools' src/ || echo "still not wired"     # devtools adoption status
grep -n 'Built from commit' graphify-out/GRAPH_REPORT.md         # freshness header format for the helper
ls supabase/functions                                            # Edge Function names
node .claude/skills/vsa-diagnostics-and-measurement/scripts/route-inventory.mjs --json | head -5   # route parser still matches
```

UNVERIFIED items are labeled inline (Supabase dashboard egress menu path, `supabase functions logs` subcommand on this CLI version, local Chrome availability for axe, Vercel CLI auth state).
