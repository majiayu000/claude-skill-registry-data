---
name: vsa-debugging-playbook
description: Load this when something on the VSA website is broken and the cause is unknown — pages showing fallback/ContentUnavailableState, Supabase queries returning empty rows or "permission denied", points/attendance changes not appearing, stale UI after a mutation, jest/CRA build or test failures, deno check errors on Edge Functions, wrong colors or broken dark mode, admin access not recognized, broken or slow images, or stale Graphify answers. Provides a symptom→triage table with exact first-check commands, discriminating experiments that separate look-alike causes, and the known time-costing traps.
---

# VSA Debugging Playbook

**What this skill is for.** You have a symptom, not a diagnosis. This playbook maps each of this project's real failure modes to a first check (exact command), ranked likely causes, a discriminating experiment, and where to go for the fix. It exists because several of this project's failure modes look identical on the surface (empty rows vs. denied rows; degraded mode vs. bad query; the two parallel points systems) and picking the wrong branch has historically cost hours.

**When NOT to use this skill:**

| If you need… | Go to |
|---|---|
| Full incident narratives (root cause, evidence, commits) | `vsa-failure-archaeology` |
| Whether a change is even allowed / how to get it approved | `vsa-change-control` |
| RLS theory, SECURITY DEFINER, migration-authoring checklist | `vsa-supabase-security-reference` |
| Design tokens, dark mode conventions, component layering depth | `vsa-design-system-reference` |
| Setting up a dev environment from scratch | `vsa-build-and-env` |
| Deploying, applying migrations, running the image pipeline | `vsa-run-and-operate` |
| Diagnostic tooling deep-dives (verify-rls-security.mjs, audits, Lighthouse) | `vsa-diagnostics-and-measurement` |
| What counts as verification evidence before you ship | `vsa-validation-and-qa` |

**Jargon, defined once:**

- **RLS** — Row Level Security: Postgres policies that filter which rows a role can see/write. A query blocked by RLS returns *empty rows*, not an error.
- **Grant** — SQL-level permission (`GRANT SELECT ON …`) that a role needs before RLS is even evaluated. A missing grant returns `permission denied` (code `42501`).
- **Degraded mode** — the app's designed behavior when Supabase is unreachable or over quota: public pages render static fallback content instead of crashing (see `AGENTS.md` "Degraded mode").
- **Egress** — bandwidth billed when data (mostly images) is served *out* of Supabase Storage. This project had a real egress crisis; see traps below.
- **SECURITY DEFINER** — a Postgres function that runs with its owner's privileges, bypassing the caller's RLS. Used deliberately in `is_admin_user()`; dangerous when accidental (views).
- **CRA** — Create React App (react-scripts 5). This project is CRA, not Vite/Next; jest and build behavior follow CRA rules.

---

## Symptom → triage table

Commands run from the repo root. Commands marked **[live creds]** need `.env.local` populated or Supabase dashboard access — everything else is repo-local and safe.

| Symptom | First check (exact command) | Likely causes, ranked | Discriminating experiment | Fix route |
|---|---|---|---|---|
| Page renders fallback content, `ContentUnavailableState`, or `DegradedModeBanner` | `grep -c "REACT_APP_SUPABASE_URL\|REACT_APP_SUPABASE_ANON_KEY" .env.local` (expect 2) | 1. Missing/wrong env vars (client never connects) 2. Supabase outage or quota exhaustion 3. A caught error that `isSupabaseUnavailable()` classifies as an outage | Read `src/utils/isSupabaseUnavailable.ts` (L9): it returns true for HTTP 429/402/503/504, any `TypeError` (network/CORS), and message fragments like `quota`, `egress`, `bandwidth`, `fetch failed`. Check the browser console for the raw error, then check https://status.supabase.com. If env vars are present and Supabase is up, the error is being *misclassified* — inspect the actual thrown error's status/message. | Env setup → `vsa-build-and-env`. Real outage/quota → `vsa-run-and-operate`. Fallback content itself lives in `src/config/publicFallbackContent.ts` (playbook agent: `vsa-public-content`). |
| Query returns **empty rows, no error** | Confirm it's not degraded mode first (row above), then run Experiment A below | 1. RLS policy filters out the rows for this role 2. The data genuinely isn't there (wrong filter, wrong table — see dual points row) 3. Querying a view whose underlying join drops rows | Experiment A (RLS vs. grant vs. no-data), below the table | RLS policy details → `vsa-supabase-security-reference`; schema truth is `supabase/migrations/` |
| Query errors with **"permission denied"** (`42501`) | Same Experiment A | 1. Missing `GRANT` for `anon`/`authenticated` on a new table/view/function 2. Grants revoked but re-grant forgotten (revoke-then-grant pattern half-applied) | Experiment A: `permission denied` = grants problem; `[]` = RLS problem. These are different fixes — don't "fix" RLS when the grant is missing | `vsa-supabase-security-reference` (owns the grant/revoke patterns and migration checklist) |
| Points or attendance change **not visible in UI** | `grep -rn "member_event_attendance\|member_yearly_points\|event_attendance\|user_points" src/data/repos/*.ts` | 1. You wrote to one points system, the UI reads the other (see Experiment B) 2. Event missing `academic_term_id` → excluded from yearly totals 3. Stale react-query cache (next row) | Experiment B (dual points systems), below the table | Protected domain — do NOT modify points/leaderboard logic without explicit request (`AGENTS.md` "Things to never do"). Audit via playbook agent `vsa-points-attendance-guardian`. Architecture rationale → `vsa-architecture-contract` |
| Event's points appear in All-Time but **missing from a yearly leaderboard** | **[live creds]** SQL editor: `select id, title, academic_term_id from events where academic_term_id is null;` | 1. Event has no `academic_term_id` (documented hard requirement — `docs/leaderboard-system.md`: "Events MUST have an academic_term_id assigned to be counted in yearly totals") | Assign the term in Admin → Events, re-check the `member_yearly_points` view | Playbook agent `vsa-points-attendance-guardian` for anything beyond assigning the term |
| **Stale data after a mutation** (create/edit succeeds, list doesn't update) | `grep -rn "invalidateQueries" src/hooks/useEvents.ts src/hooks/usePoints.ts` | 1. Mutation's `onSuccess` doesn't invalidate the query key the list reads 2. Query key mismatch (`['events']` vs `'event-stats'` — both styles exist) 3. You bypassed the repo/hook layer | Working examples: `src/hooks/useEvents.ts` L86–133 — e.g. check-in invalidates `['event', id]`, `['events']`, `['user-points']`, `['leaderboard']` in one `onSuccess`. Compare your mutation against these. This is react-query **v3** (`react-query@3.39.3` in package.json), not @tanstack v4/v5 — v5 idioms from training data may not apply | Pattern home → `vsa-architecture-contract` |
| Test fails: `Cannot use import statement outside a module` / SyntaxError inside `node_modules/zod` or `@hookform/resolvers` | `grep -n "transformIgnorePatterns" package.json` | 1. A new ESM-only dependency isn't in the jest `transformIgnorePatterns` allowlist (currently `node_modules/(?!(zod\|@hookform/resolvers)/)`) | Add the failing package name inside the `(?!(…))` group in `package.json` → `jest` and re-run. See trap 4 below | `vsa-build-and-env` (owns setup traps); tests → playbook agent `vsa-testing-qa` |
| `npm test` hangs / CI never finishes | Use `CI=true npm test -- --watchAll=false` | 1. CRA jest defaults to watch mode; without `CI=true … --watchAll=false` it waits for input forever | n/a | `vsa-validation-and-qa` (owns the verification command set) |
| Console warnings during tests (jsdom, ThemeProvider, Framer Motion) | Check the exit code, not the noise: `CI=true npm test -- --watchAll=false; echo "exit=$?"` | 1. Known-acceptable warnings — `AGENTS.md` (Testing): "Existing jsdom, ThemeProvider, and Framer Motion console warnings are acceptable when the test command exits successfully" | If exit code is 0, ship. If non-zero, read the first *failure*, not the first warning | `vsa-validation-and-qa` |
| Build fails on TypeScript syntax that "should work" | `grep '"typescript"' package.json` | 1. This repo is TypeScript **4.9.5** — `satisfies` works (4.9+) but `const` type parameters, 5.x decorator syntax, etc. do not 2. Strict mode violation (`any` is banned; use `unknown` + narrowing per AGENTS.md) | Check the TS version before assuming the code is wrong | `vsa-build-and-env` |
| `deno check` on an Edge Function shows ~a dozen type errors | `deno check supabase/functions/vsa-ai-assistant/index.ts` | 1. **Pre-existing esm.sh type-resolution noise, not your regression** — verified 2026-07-06: exactly `Found 12 errors.` on an untouched checkout | Run `deno check` on the *unmodified* function first (e.g. `git stash` your edits mentally — read the file from HEAD via `git show HEAD:supabase/functions/vsa-ai-assistant/index.ts`) and diff the error *count and locations* against your edited version. New errors at your lines = yours; the baseline 12 = noise. See trap 5 | Edge Function deploy/ops → `vsa-run-and-operate`; Ask VSA behavior → playbook agent `vsa-ai-knowledge` |
| Edge Function returns 500 in production | **[live creds]** Supabase Dashboard → Edge Functions → *function* → Logs (functions in repo: `analytics-proxy`, `trigger-event-image-migration`, `trigger-house-event-image-migration`, `vsa-ai-assistant` — verify with `ls supabase/functions/`) | 1. Missing function secret 2. Runtime error visible only in logs 3. Schema drift between function SQL and applied migrations 4. Historical functions may still be deployed even after repo source deletion; `secure-ai` is one such issue #353 cleanup case | Reproduce with a curl against the function URL and compare the logged error to local `deno check` output | Secrets catalog → `vsa-config-and-flags`; deploy order → `vsa-run-and-operate` |
| Wrong colors / dark mode broken on one component | `grep -rn "text-gray-\|bg-white\|bg-gray-900" src/path/to/component` | 1. Hardcoded palette classes instead of semantic tokens — `tailwind.config.js` defines `surface`, `surface2`, `text-primary` as CSS-variable-driven tokens; hardcoded grays don't flip with theme 2. Class strings concatenated raw instead of via `cn()` (`src/lib/utils.ts`) 3. Missing `dark:` variant where tokens are insufficient | Toggle theme: dark mode is class-based (`darkMode: 'class'` in tailwind.config.js; `ThemeContext` sets the class on `<html>`). If the element doesn't change on toggle, it's hardcoded | `vsa-design-system-reference` for token depth; `AGENTS.md` bans hardcoded color classes |
| Logged-in user not recognized as **admin** | `cat src/hooks/useAdmin.ts` — it selects `is_admin` from `user_profiles` where `id = user.id` | 1. `user_profiles.is_admin` is false/missing for that user **[live creds]** 2. The query errors and `useAdmin` **fails closed** — its catch sets `isAdmin=false` and only `console.error`s, so an RLS/grant problem *looks like* "not an admin" 3. RLS recursion regression on `user_profiles` (see trap 1) | Open the browser console: `Error checking admin status:` present = cause 2/3 (data-access problem), absent = cause 1 (data problem). For cause 3, the fix shape is the `is_admin_user()` SECURITY DEFINER helper in `supabase/migrations/20260620020000_fix_user_profiles_rls_recursion.sql` | `vsa-supabase-security-reference`; full incident → `vsa-failure-archaeology` (#160) |
| A **new view** returns data to `anon` unexpectedly, or is writable | `grep -n "revoke all" supabase/migrations/<your_migration>.sql` (expect a revoke before any grant) | 1. Default-privileges gotcha: this project's `ALTER DEFAULT PRIVILEGES` grants ALL on new relations *including views* to anon/authenticated, and definer-owned simple views are auto-updatable — writes pass through, bypassing base-table RLS | Model migration: `supabase/migrations/20260701000000_add_member_photo_requests.sql` L235–260 — comment reads "Revoke everything, then grant SELECT only." Every new view needs `revoke all … from anon, authenticated;` then an explicit `grant select` | `vsa-supabase-security-reference` (owns the full pattern) |
| Images broken or page **slow with heavy image traffic** | Inspect the failing URL in devtools Network tab: does the host contain `supabase.co/storage`? | 1. Image still served from Supabase Storage instead of `/public` (egress trap — see trap 2) 2. Migrated path wrong/missing in `/public` 3. Storage object actually deleted (should never happen — deletion is banned in AGENTS.md) | `npm run migrate:images:dry` reports what the image-migration pipeline (`scripts/migrate-supabase-images-to-public.ts`) would move — dry-run only, safe. Compare its report to the broken URL | Pipeline operation → `vsa-run-and-operate`; audits → playbook agent `vsa-storage-egress` |
| Graphify gives answers that don't match the code | `grep -n "Built from commit" graphify-out/GRAPH_REPORT.md && git rev-parse --short HEAD` | 1. Stale graph — the two hashes differ (e.g. report says `a3d7ea60` while HEAD is newer) 2. Git hooks not installed | `./scripts/graphify-run hook status` — expect `post-commit: installed` and `post-checkout: installed`. Refresh with `graphify . --update` (interactive sessions only; never inside a feature PR) | Graphify workflow → `docs/graphify-workflow.md` and the `graphify` skill |

---

## Discriminating experiments

### Experiment A — empty rows vs. permission denied vs. no data

These three look similar from the UI (something doesn't show up) but have disjoint fixes. RLS filtering silently returns `[]`; a missing grant raises `permission denied`; absent data is neither's fault.

1. **[live creds]** In the Supabase SQL editor (runs as a privileged role, bypasses RLS):

   ```sql
   select count(*) from <table_or_view>;  -- ground truth: does the data exist at all?
   ```

   Count is 0 → **no data**: the write never landed (check Experiment B if points-related) or your filter is wrong. Stop here.

2. **[live creds]** Same query as the `anon` role via REST, from your shell (reads keys from `.env.local`):

   ```bash
   set -a; source .env.local; set +a
   curl -s "$REACT_APP_SUPABASE_URL/rest/v1/<table_or_view>?select=*&limit=3" \
     -H "apikey: $REACT_APP_SUPABASE_ANON_KEY" \
     -H "Authorization: Bearer $REACT_APP_SUPABASE_ANON_KEY"
   ```

   - `[]` (empty array, HTTP 200) → **RLS is filtering**. The role has permission to query but no policy admits these rows. Fix the policy (via `vsa-supabase-security-reference` patterns), never by weakening RLS broadly (banned in `AGENTS.md`).
   - `{"code":"42501", …"permission denied"…}` → **missing grant**. RLS was never reached. Add/restore the `GRANT`.
   - Rows returned → the backend is fine for `anon`; if the app still shows nothing, the bug is client-side: wrong repo method, wrong query key, or an `authenticated`-role policy difference (repeat with a logged-in user's JWT as the Bearer token).

3. To test the `authenticated` role specifically, replace the Bearer token with a real session JWT (copy from devtools → Application → Local Storage → the `sb-*-auth-token` entry, `access_token` field). Policies frequently differ between `anon` and `authenticated`.

### Experiment B — which points system did your write land in?

There are **two parallel points systems** (documented in `docs/leaderboard-system.md`; consolidation is FUTURE work, not done):

| System | Tables | Feeds which UI | Repo/consumers (verified 2026-07-06) |
|---|---|---|---|
| Member/leaderboard system (**source of truth for public + admin leaderboards**) | `member_event_attendance` + `events` + `academic_terms`, aggregated by the `member_yearly_points` view (and `house_member_yearly_points` for Houses) | Public Leaderboard, admin Members/Points/Import, MyVSACard | `src/data/repos/leaderboard.ts` (reads `member_yearly_points`, `house_member_yearly_points`); `src/pages/Admin/{Members,Points,Import}.tsx`; `src/components/features/points/MyVSACard.tsx` |
| Authenticated check-in system | `event_attendance` + `user_points` | Logged-in member dashboard, live check-in flows | `src/data/repos/points.ts` (reads `user_points`, `event_attendance`); `src/data/repos/events.ts`; `src/hooks/useEventAttendance.ts`; `src/components/features/dashboard/MemberDashboard.tsx` |

The experiment: **[live creds]** after the write, check both sides in the SQL editor:

```sql
select count(*) from member_event_attendance where member_id = '<id>';
select count(*) from event_attendance      where user_id   = '<id>';
```

If the row is in `event_attendance` but the *leaderboard* doesn't move — that's by design; the leaderboard doesn't read that table. If it's in `member_event_attendance` but yearly totals don't move — check the event's `academic_term_id` (yearly-totals row in the triage table). Do not "fix" this by writing to both tables or altering calculation logic: points/leaderboard are protected domains (`AGENTS.md` "Things to never do"); route changes through the `vsa-change-control` skill and audit via the `vsa-points-attendance-guardian` playbook agent.

---

## Traps that cost real time

One-paragraph versions. Full chronicles with evidence live in `vsa-failure-archaeology` — read that before touching any of these areas.

1. **`user_profiles` RLS recursion (incident #160, commit `9e0c102e`).** An RLS policy on `user_profiles` checked admin status by querying `user_profiles` — policy evaluation triggered the policy again, recursively, taking down profile reads (and with them, admin detection) in production. The fix (`supabase/migrations/20260620020000_fix_user_profiles_rls_recursion.sql`) extracts the check into `is_admin_user()`, a caller-bound `SECURITY DEFINER` SQL function with `SET search_path = ''` so policy evaluation bypasses the table's own RLS without letting callers enumerate other users' admin status. The trap for you: any policy on table T that selects from T is a recursion; the symptom is errors or hangs on reads of T, which surface in this app as "nobody is admin" because `useAdmin` fails closed. → `vsa-failure-archaeology` for the timeline; `vsa-supabase-security-reference` for the pattern.

2. **The Supabase egress crisis.** Serving event/gallery/House images straight from Supabase Storage burned through the bandwidth quota; when the quota exhausted, Supabase started failing requests and the whole site degraded — which is exactly why `isSupabaseUnavailable()` explicitly matches `quota`, `egress`, and `bandwidth` message fragments, and why the app has a designed degraded mode at all. The response was a whole pipeline (`scripts/migrate-supabase-images-to-public.ts`, `npm run migrate:images:{dry,apply}`, commits `5fa96185`, PRs #71/#72/#80, `docs/event-image-migration.md`) migrating image URLs to `/public` assets served by Vercel. The trap: any new feature that renders Supabase Storage URLs on a public page reopens the wound. Never delete the Storage originals. → operation details in `vsa-run-and-operate`; full story in `vsa-failure-archaeology`.

3. **New views are born world-writable.** This project's `ALTER DEFAULT PRIVILEGES` configuration grants ALL on newly created relations — *including views* — to `anon` and `authenticated`, and Postgres makes simple definer-owned views auto-updatable, so a "read-only" view silently accepts INSERT/UPDATE/DELETE that bypass the base table's RLS. This was caught during the member-photo-requests work; the canonical fix is in `supabase/migrations/20260701000000_add_member_photo_requests.sql` (L235–260): `revoke all on <view> from anon, authenticated;` then grant exactly `select` to exactly the roles that need it, for **every** new view, every time. → mechanics and checklist in `vsa-supabase-security-reference`.

4. **Jest chokes on ESM dependencies.** CRA's jest doesn't transform `node_modules` by default, so ESM-only packages blow up with `Cannot use import statement outside a module` — hours have been lost reading that as a broken test rather than a config gap. The repo already allowlists the two known offenders in `package.json` → `jest`: `"transformIgnorePatterns": ["node_modules/(?!(zod|@hookform/resolvers)/)"]`. When you add a dependency and tests suddenly fail *inside* `node_modules/<pkg>`, append `<pkg>` inside that negative-lookahead group — don't rewrite the test. → `vsa-build-and-env` owns the full setup-traps list.

5. **`deno check` noise on `vsa-ai-assistant` is not your regression.** Type-checking the Ask VSA Edge Function on a clean checkout reports exactly `Found 12 errors.` (verified 2026-07-06, Deno from Homebrew) — all esm.sh remote-type resolution artifacts (`Type '"public"' is not assignable to type 'never'` and friends), none of them shipping-blocking since the function runs fine deployed. The trap runs both ways: don't burn an afternoon "fixing" the baseline 12, and don't let a *13th* error hide among them — always diff your error count and line numbers against the untouched baseline (`git show HEAD:supabase/functions/vsa-ai-assistant/index.ts > /tmp/base.ts && deno check /tmp/base.ts`). → `vsa-failure-archaeology`.

---

## Provenance and maintenance

Written 2026-07-06 against commit `368fbf63` (branch `codex/reactbits-ui`). Sources: `AGENTS.md`; `docs/leaderboard-system.md`; `package.json`; `src/utils/isSupabaseUnavailable.ts`; `src/hooks/useAdmin.ts`; `src/hooks/useEvents.ts`; `src/hooks/usePoints.ts`; `src/data/repos/{leaderboard,points}.ts`; `src/lib/supabase.ts`; `tailwind.config.js`; `src/context/ThemeContext.tsx`; `supabase/migrations/20260620020000_fix_user_profiles_rls_recursion.sql`; `supabase/migrations/20260701000000_add_member_photo_requests.sql`; live `deno check` run; `git log` (commits `9e0c102e`, `5fa96185`).

Re-verify before trusting, if this file is old:

```bash
grep -n "transformIgnorePatterns" package.json                  # jest ESM allowlist still zod + @hookform/resolvers?
grep -n '"typescript"\|"react-query"' package.json               # still TS 4.9.x / react-query v3?
grep -n "429\|quota" src/utils/isSupabaseUnavailable.ts          # degraded-mode signals unchanged?
grep -n "member_yearly_points" src/data/repos/leaderboard.ts     # leaderboard still reads the view?
grep -rn "from('user_points')" src/data/repos/points.ts | head -1  # second system still live? (consolidation was FUTURE work as of 2026-07-06)
deno check supabase/functions/vsa-ai-assistant/index.ts 2>&1 | tail -2  # baseline error count still 12?
ls supabase/functions/                                           # Edge Function inventory
grep -n "Built from commit" graphify-out/GRAPH_REPORT.md         # graph freshness
```

If `docs/leaderboard-system.md` gains a "consolidation complete" note, Experiment B's table split is obsolete — rewrite that section before anything else.
