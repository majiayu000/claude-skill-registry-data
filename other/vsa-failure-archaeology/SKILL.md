---
name: vsa-failure-archaeology
description: Load this before re-investigating anything that feels "already fought" on the VSA website — Supabase egress/bandwidth spikes, RLS "infinite recursion" errors, check-in code exposure, auth redesigns, House-year data confusion, dual points systems, Ask VSA answer quality, image migration behavior — or when you find a dead branch, a revert, or an odd migration and wonder why it exists. Provides the full chronicle of every major incident, dead end, rejected fix, and revert with commit/PR/migration evidence, plus a "settled battles — do not reopen" table.
---

# VSA Failure Archaeology

**What this skill is for.** This is the incident history of the VSA website: every major investigation, outage, dead end, and revert, recorded as *Symptom → Root cause → Evidence → Status* so no future session re-fights a settled battle or re-proposes a rejected fix. When you see a strange migration, a revert commit, or a branch that never merged, look here first — the answer is usually a battle someone already fought.

**When NOT to use this skill:**

| You need... | Load instead |
|---|---|
| Whether a change is allowed / the never-do list | `vsa-change-control` |
| Live triage of a broken thing (symptom → first command) | `vsa-debugging-playbook` |
| RLS mechanics, SECURITY DEFINER theory, migration authoring | `vsa-supabase-security-reference` |
| System design, invariants, provider hierarchy | `vsa-architecture-contract` |
| How to run the image-migration pipeline today | `vsa-run-and-operate` |

**Jargon used below** — *RLS*: Row Level Security, Postgres per-row access policies. *Egress*: outbound bandwidth billed by Supabase. *SECURITY DEFINER*: a Postgres function that runs with its owner's privileges, bypassing the caller's RLS. *Edge Function*: Deno function hosted by Supabase.

**How to read entries.** Each entry: Symptom → Root cause → Evidence (commit SHA / PR # / migration file — all verifiable with `git show <sha>` or `cat supabase/migrations/<file>`) → Status (**settled** / **partially settled** / **open**) → Lesson → Do-not-retry notes where applicable.

---

## 1. The Supabase egress crisis (May–June 2026) — the project's costliest battle

**Symptom.** Supabase egress (outbound bandwidth) blew past free-tier limits. Two independent drivers: (a) the app re-fetched heavy queries constantly, and (b) every public page load streamed full-resolution images out of Supabase Storage.

**Root causes (three separate ones, found in phases):**
1. **API egress**: react-query's default `refetchOnWindowFocus: true` caused continuous re-fetches, and `eventsRepository.getEvents` had an N+1 that pulled thousands of unused `event_attendance` rows on every public events-page load.
2. **Storage egress**: admin uploads went to Supabase Storage at full resolution and were served from there to every visitor.
3. **Unpaginated lists**: gallery and past-events pages fetched everything at once.

**The fix arc (chronological — each phase, with evidence):**

| Phase | What was done | Evidence |
|---|---|---|
| 0 | First image-egress reduction (upload handling) | `84367b0c`, `b41e4200` (PR #42, branch `fix/supabase-egress-uploads`, 2026-05-15) |
| 1 | QueryClient defaults: `staleTime` 5m, `refetchOnWindowFocus: false`; removed N+1 attendance query from public events list | `6427cd16` (#67, 2026-05-25) |
| 2 | Compress admin image uploads client-side before Storage write | `7ce2a02b` (#69) |
| 3 | Paginate gallery and past events | `bb8e51df` (#70), branch `codex/gallery-events-pagination-egress-phase-3` |
| 4 | Serve public storage images as thumbnails | `3bf631a1` (#72), branch `codex/storage-thumbnail-egress-fix`, migration `20260526000000_add_storage_thumbnail_urls.sql` |
| 5 | **The structural fix**: migrate images out of Supabase entirely to repo-hosted `/public/images/**` served by Vercel | script `scripts/migrate-supabase-images-to-public.ts` (#75, `49d00b42`), path helper fix #76 (`51fae761`), nightly workflow `7cd0c241` |
| 6 | Manual workflow + Edge Function trigger so migration runs on Supabase image updates | `.github/workflows/migrate-images.yml`, `.github/workflows/migrate-event-images.yml` (#88 `7f7dd506`, **#89 `6f22ce86`**), Edge Function `supabase/functions/trigger-event-image-migration/` |
| 7 | Extend pipeline to House events | **#96 `d2944165`**, Edge Function `supabase/functions/trigger-house-event-image-migration/` |

**How the pipeline works now** (full runbook in `vsa-run-and-operate`; doc of record `docs/event-image-migration.md`): admin uploads still go to Supabase Storage first (browser can't write to the repo), then the migration workflow downloads, optimizes, commits to `public/images/**`, pushes to `main` (`chore: migrate ... images to static assets [skip ci]` bot commits — dozens of these in `git log` are *normal*, not noise), and rewrites the DB row to the local path. Supabase Storage is a **staging buffer**, not the serving tier.

**Status: settled** (architecture); operating cost is ongoing (the bot commits keep landing on `main`).

**Lesson.** Egress problems on this stack are almost never one bug — audit all three: query refetch behavior, image serving path, and pagination. The permanent answer for public images is "serve from Vercel static, stage in Supabase."

**Do not retry:**
- Do NOT "clean up" Supabase Storage by deleting originals after migration. `docs/event-image-migration.md` § "Why old Supabase files are not deleted" (line ~115): originals are intentionally kept because CDN/browser caches may still point at the old URLs; manual cleanup only after all DB rows are confirmed updated and caches expired. `AGENTS.md` § "Things to never do": "Don't delete database rows or Supabase Storage files."
- Do NOT serve new public image features directly from Supabase Storage URLs — that re-opens the crisis. Extend the migration pipeline instead (see #96 as the template for adding a category).
- Do NOT remove the `[skip ci]` bot commits or squash them away; they are the pipeline's write path to `main`.

---

## 2. user_profiles RLS recursion outage (June 2026) — the self-inflicted wound

**Symptom.** After the June 2026 emergency security hardening shipped, queries touching `user_profiles` failed with Postgres error `infinite recursion detected in policy for relation "user_profiles"` — admin checks (`useAdmin()`) and profile reads broke.

**Root cause.** The hardened admin SELECT policy on `user_profiles` checked admin status by querying `user_profiles` itself. Evaluating the policy required evaluating the policy: infinite recursion. Sharpest part: the emergency migration's own comment asserted this was safe — `supabase/migrations/20260619000000_emergency_security_hardening.sql` line 74 says "…so no recursive RLS loop occurs." **The comment was wrong.** The recursion shipped in the emergency fix itself (`8183caba`, #145).

**The fix** (`9e0c102e`, #160; migration `20260620020000_fix_user_profiles_rls_recursion.sql`; branch `codex/fix-user-profiles-rls-recursion`):
- New function `public.is_admin_user(p_user_id uuid DEFAULT auth.uid())` — `SECURITY DEFINER`, `STABLE`, `SET search_path = ''`. SECURITY DEFINER means policy evaluation reads `user_profiles` with the function owner's privileges, **bypassing table RLS**, which breaks the loop.
- Caller-bound: the function requires `p_user_id = auth.uid()`, so it cannot be used to enumerate other users' admin status.
- `REVOKE ALL ... FROM PUBLIC, anon; GRANT EXECUTE ... TO authenticated`.
- Rewrote the admin SELECT policy to `USING (public.is_admin_user(auth.uid()))`.
- Bonus hardening in the same migration: the self-INSERT policy now has `WITH CHECK (auth.uid() = id AND is_admin = false)` — a new account cannot insert itself as admin.

**Status: settled.**

**Lesson.** Any RLS policy on table T that queries T recurses. The project-standard escape hatch is a caller-bound SECURITY DEFINER helper — reuse `is_admin_user()`, don't invent a second one. And never trust a migration comment claiming "no recursion risk"; the comment that said so is the one that recursed.

**Do not retry:** do not "simplify" `is_admin_user()` back into an inline `EXISTS (SELECT ... FROM user_profiles ...)` subquery inside a `user_profiles` policy — that is the exact outage. Do not drop the `p_user_id = auth.uid()` guard (it prevents admin-status enumeration). RLS theory home: `vsa-supabase-security-reference`.

---

## 3. June 2026 security emergency (the week of 2026-06-19)

**Symptom.** A security review found publicly readable data that should never have been public: event check-in codes (anyone could self-award points), auth UUIDs exposed in public member views/leaderboard, weak attendance-insert policies, and a user_profiles surface that let clients touch `is_admin`.

**Root cause.** Early schema (2024-era migrations) was built permissive-first: policies granted broad SELECT to `anon`, check-in codes lived as a column on `events`, and views exposed base-table columns wholesale.

**The fix arc (all within ~10 days):**

| Step | Change | Evidence |
|---|---|---|
| Emergency hardening: RLS, admin protection, check-in, `user_points` | `8183caba` (#145), migration `20260619000000_emergency_security_hardening.sql`, branch `claude/emergency-rls-checkin-points-hardening` |
| Minimize public member exposure; strip auth UUIDs from public views + leaderboard | `09edbf80` (#153), migration `20260619040000_minimize_public_member_exposure.sql` |
| Move `check_in_code` off `events` into admin-only `event_check_in_secrets` | `c453eb5a` (#154), migrations `20260619050000_check_in_code_secrets.sql` + `20260620000000_move_check_in_code_to_secrets_table.sql`, branch `claude/check-in-code-secrets` |
| Harden attendance INSERT policies | `e1bf169c` (#157), migration `20260620010000_harden_attendance_rls.sql` |
| RLS verification tooling (`scripts/verify-rls-security.mjs`) | `af2461be` (#158), branch `antigravity/rls-verification-tooling` |
| Browser security headers | `2f3a89a1` (#162) |
| Final compliance re-audit documented | `7157c3cf` (#156), `docs/final-compliance-reaudit.md`; wording softened `e3bd80ef` (#171) |

**Status: settled** — but it directly caused Entry 2 (the recursion outage was introduced by `8183caba` and fixed 5 PRs later). Emergency fixes under time pressure ship their own bugs.

**Lesson.** Check-in codes are secrets, never event columns; public views must be column-allowlisted, never `SELECT *`. After any RLS change, run `node scripts/verify-rls-security.mjs` (interpretation guide: `vsa-diagnostics-and-measurement`).

**Do not retry:** do not move `check_in_code` back onto `events` "for simpler joins," and do not add auth UUIDs to any public view — both were deliberate removals with PR trails (#154, #153).

---

## 4. Auth redesign revert (October 2025) — a parked feature, not a bug

**Symptom.** `git log` shows `a4b2fca9` (2025-10-06) `Revert "Redesign authentication: admin-only sign-in, public browsing for general members"`, reverting `46678975` (2025-10-05) — shipped and reverted within ~22 hours. Yet a later commit `63d37d1a` ("Make sign-in admin-only", PR #28) landed the admin-only direction anyway.

**What happened.** The first redesign attempt (touching `AdminRoute.tsx`, `UserMenu.tsx`, `routes.tsx`) was rolled back the next day; the admin-only sign-in model was reintroduced deliberately seven months later via #28 (`63d37d1a`, 2026-05-12). Net state today: sign-in is effectively admin-oriented; general members browse publicly and use "Find My Points" instead of accounts. Member self-service (`/profile` for regular members) is **intentionally parked**, not missing. The reason the specific 2025-10-05 attempt was reverted is not recorded in the commit body — UNVERIFIED beyond the revert itself.

**Status: settled** (current model deliberate); member self-service = **open/parked**.

**Lesson.** Before "fixing" the auth flow to give members accounts, know that this exact redesign was tried, reverted, and then landed in a narrower form. Any re-attempt is a gated change — route through `vsa-change-control`.

---

## 5. House-year content mix-ups (May–June 2026)

**Symptom.** Seeding legacy House archive data clobbered or displaced *current-year* (2025–2026 Mario Houses) rows; House pages showed wrong or missing Houses for the current year. Separately, admin House tabs drifted out of sync on academic year.

**Root cause.** `house_page_assets` keys rows by `(academic_year_start, house)` / `(academic_year_start, house_key)`; the legacy seeding migration (`20260531000000_seed_legacy_house_assets.sql`) interacted badly with existing current-year rows, requiring a restore.

**Evidence.** Restore migration `20260601010000_restore_mario_house_assets.sql` (header: "restores 2025-2026 Mario House assets after legacy seeding removed current-year rows", preserves existing media URLs on conflict); fix arc `076e4dc7` (#109) "restore 2025 house profiles", `27acffc8` (#113) admin year sync, `3305c263` (#114) admin House year selection, `b712b89d` (#116) official standings fallback. `AGENTS.md` carries hard House-year facts (2025–2026 = Bowser/Donkey Kong/Boo/Toad; 2026–2027 = placeholders, never invent) precisely because of this confusion.

**Status: settled** (data restored; AGENTS.md facts are the guardrail).

**Lesson.** House data is year-keyed; any seed/backfill must be idempotent (`on conflict ... do nothing/update` preserving existing media) and must never touch the current year's rows. The year↔theme mapping lives in `AGENTS.md` — treat it as canon, home for the facts is `vsa-change-control`/`vsa-seasonal-operations`.

**Do not retry:** never re-run or imitate a legacy seed that upserts into current-year rows without the conflict-preservation pattern from `20260601010000_restore_mario_house_assets.sql`.

---

## 6. Dual points systems — OPEN, do not "discover" it again

**Symptom.** Two parallel attendance/points systems exist and every few sessions someone rediscovers this as "a bug."

**Reality (by design, temporarily).** Public leaderboard truth = `member_event_attendance` + `events` + `academic_terms` (surfaced via `member_yearly_points` view, migration `20260512000003_create_member_yearly_points_view.sql`). A second system (`event_attendance` + `user_points`, 2024-era migrations) serves authenticated check-ins. `docs/leaderboard-system.md` § Future Considerations states consolidation is future work, gated on verifying `user_id` coverage for all members.

**Status: OPEN.** Consolidation has NOT happened. Do not present it as done; do not half-consolidate in a side PR. This is a protected domain — see `vsa-change-control`. Architecture detail home: `vsa-architecture-contract`.

---

## 7. Data-rights arc and the anonymization safety gaps (June 2026)

**Symptom (final incident).** Multi-agent review of the new anonymization feature found it could be applied twice to the same request, could pass its own correctness gate via planner caching, and could silently report success for auth users with no profile row.

**Root causes** (fixed in `171067ef`, #167):
- `preview_data_rights_anonymization` was declared `STABLE` but reads `auth.uid()` + live table state and gates a VOLATILE caller after row locks — `STABLE` allowed planner caching to bypass the gate. Fixed: `VOLATILE`.
- Requests were left at `approved_for_future_action` after a successful run → double-application possible. Fixed: auto-set `status = 'completed'` before the audit INSERT.
- Auth user with no `user_profiles` row returned `profiles=0` + `ready_for_anonymization=true` silently. Fixed: explicit deferred-action warning.

**The wider arc:** privacy notice #147 (`79c1b2aa`) → architecture doc #148 → deletion guard #149 (`73972a6b`) → request tracker #150 → dependency preview #151 → admin export #152 (`99fc92fc`) → anonymization workflow #164 (`2d9cf704`, migration `20260620020000_add_data_rights_anonymization.sql`) → safety gaps #167. Runbook of record: `docs/data-rights-anonymization-runbook.md`.

**Status: settled.**

**Lesson.** Postgres function volatility is a correctness property, not an optimization hint — a `STABLE` function used as a safety gate inside a VOLATILE transaction can be cached past the gate. Also note the migration-timestamp collision: two different migrations share prefix `20260620020000` (anonymization + RLS recursion fix) — filename timestamps are not unique here; ordering questions go to `vsa-run-and-operate`.

---

## 8. Repo cleanup #172 (July 2026) — the fictional infrastructure purge

**Symptom.** The repo carried Kubernetes manifests, Terraform, Prometheus config, an Express backend stub, `schema.sql`, and a `docs/cloud-architecture.md` describing an architecture that **did not exist**. Sessions (human and AI) kept orienting on this fiction.

**Fix.** `6c15a458` (#172, 2026-07-02): deleted `k8s/`, `infrastructure/terraform/`, `monitoring/`, `backend/`, `schema.sql`, `env.example`, `setup-chat.js`, stray output files, and the fictional cloud-architecture doc; kept Dockerfile/docker-compose (simplified to one frontend service); moved `DESIGN.md`, `DEPLOYMENT_GUIDE.md`, `stitch-prompts.md` into `docs/`; fixed stale `AGENTS.md` references.

**Status: settled.**

**Lesson / do not retry:** the real architecture is CRA SPA → Supabase → Vercel, nothing else. Do not restore or re-scaffold k8s/Terraform/Express "for production readiness" — that scaffolding was deliberately judged fictional and removed with rationale in the commit body. If a doc contradicts the deploy reality, the doc is the suspect (authority order: `vsa-docs-and-writing`).

---

## 9. Ask VSA quality arc — three overhauls before the v2 settlement

**Symptom.** The AI assistant ("Ask VSA", Edge Function `supabase/functions/vsa-ai-assistant/`, Gemini-backed) repeatedly gave stale, duplicated, or wrong answers about volatile facts (House signups, application windows, dates). Quality fixes kept being re-attempted because knowledge lived in overlapping seeded rows and prompt text with no freshness model.

**The arc:** MVP #79 (`6f6b79d4`) → knowledge improvements `20260530000000_improve_ai_knowledge.sql`, #115 (`2ec4e273`), #143 (`63c21240`), seed `20260618000000_seed_ai_knowledge.sql`, house-signup patch `20260702000000_improve_ai_knowledge_house_signup.sql` → chat-UX overhauls #173 (`6702d529`), #174 (`7c0b6005`), #175 (`4feabee1`) → feedback loop #168 (`a3597b2b`) → **knowledge v2** #181 (`9bbbb975`, branch `feat/ask-vsa-knowledge-v2`), migrations `20260704000000_ai_knowledge_v2_schema.sql`, `20260704000001_ai_knowledge_v2_dedupe.sql`, `20260704000002_ai_knowledge_v2_expansion.sql`.

**What v2 settled** (verified in `supabase/functions/vsa-ai-assistant/index.ts` line 34 `SYSTEM_PROMPT` and the v2 schema migration): a hard split — *behavior rules* live in the Edge Function's `SYSTEM_PROMPT`; *volatile facts* live in `ai_knowledge_base` rows with `aliases text[]`, `confidence` (high/medium/low), `freshness` (stable/yearly/quarterly/event_live), `academic_year`, `valid_until`; retrieval skips expired entries. Duplicates are deactivated (`is_active = false` throughout the dedupe migration), never deleted. #181 is merged to `origin/main` (verified `git merge-base --is-ancestor`, 2026-07-06).

**Status: partially settled** — the v2 architecture is the settlement (do not re-litigate prompt-vs-DB placement); answer *content* quality remains an ongoing tuning loop via the #168 feedback tables.

**Do not retry:** don't stuff volatile facts (dates, links, current Houses) back into the SYSTEM_PROMPT, and don't hard-delete knowledge rows — deactivation preserves dedupe history.

---

## Graveyard: instructive dead branches (`git branch -a --no-merged main`, as of 2026-07-06)

Dead ≠ worthless: most were superseded by a merged squash/rework. Check before reviving anything.

| Branch | Attempted | Apparent status |
|---|---|---|
| `codex/reduce-supabase-egress` | Egress phase 1 | Superseded by #67 (`6427cd16`) squash-merge |
| `codex/gallery-events-pagination-egress-phase-3` | Egress phase 3 pagination | Merged via #70/#71; branch stale |
| `codex/storage-thumbnail-egress-fix` | Thumbnail serving | Merged via #72; branch stale |
| `codex/event-image-egress-layout-fix`, `codex/event-image-upload-compression-layout` | Image layout + compression variants | Superseded by #86/#87 |
| `claude/emergency-rls-checkin-points-hardening` | June security emergency | Landed as #145; branch stale |
| `codex/fix-user-profiles-rls-recursion` | Recursion fix | Landed as #160; branch stale |
| `claude/check-in-code-secrets` | Check-in secrets table | Landed as #154; branch stale |
| `antigravity/rls-verification-tooling` | RLS test script | Landed as #158; branch stale |
| `gemini/house-event-image-migration` | House-event image pipeline | Landed as #96 (`d2944165`) |
| `feat/ask-vsa-knowledge-v2` | Ask VSA knowledge v2 | Landed as #181 (`9bbbb975`), in `origin/main`; branch stale |
| `codex/reactbits-ui` (current) | ReactBits-flavored UI experiments | Active UI-campaign work, not dead |

Pattern: multi-agent branches (`claude/`, `codex/`, `gemini/`, `antigravity/`) are usually squash-merged via PR, leaving the branch "unmerged" forever. `git log --all --grep="#<PR>"` before declaring work missing. Branch lifecycle etiquette: `vsa-research-methodology`.

---

## Settled battles — do not reopen

| Battle | Settlement | Reopening requires |
|---|---|---|
| Public images served from Supabase Storage | Serve from `/public/images/**` via migration pipeline (#75–#96) | Owner sign-off; would re-create egress crisis |
| Deleting Storage originals post-migration | Never — Storage is the staging buffer | Explicit owner request (destructive-op rule, AGENTS.md) |
| Inline admin-check subquery in `user_profiles` policies | `is_admin_user()` SECURITY DEFINER helper (#160) | Nothing — this is closed; inline = outage |
| `check_in_code` as a column on `events` | Admin-only `event_check_in_secrets` (#154) | Nothing — closed |
| Auth UUIDs in public views / leaderboard | Removed (#153) | Nothing — closed |
| Member self-service accounts / auth redesign | Admin-only sign-in (revert `a4b2fca9` → #28); member self-service parked | Gated change via `vsa-change-control` |
| Legacy House seeds touching current-year rows | Conflict-preserving idempotent upserts only (`20260601010000_...`) | Nothing — closed |
| k8s / Terraform / Express backend scaffolding | Removed as fictional (#172) | Real architecture change, owner-driven |
| Ask VSA facts in the system prompt | Prompt = behavior, DB = facts (v2, #181) | Nothing — closed design decision |
| Dual points systems | NOT settled — OPEN; consolidation is future work | Protected domain; full acceptance criteria + owner approval |

---

## Provenance and maintenance

Compiled 2026-07-06 from repo evidence on branch `codex/reactbits-ui` (main head `fc51c96c`). Owner interview 2026-07-05 weighted entries 1–2 heaviest.

**Sources:** `git log --oneline main`; `git branch -a --no-merged main`; commits `6427cd16`, `7ce2a02b`, `bb8e51df`, `3bf631a1`, `49d00b42`, `7cd0c241`, `7f7dd506`, `6f22ce86`, `d2944165`, `8183caba`, `09edbf80`, `c453eb5a`, `e1bf169c`, `af2461be`, `9e0c102e`, `a4b2fca9`, `46678975`, `63d37d1a`, `076e4dc7`, `2d9cf704`, `171067ef`, `6c15a458`, `6702d529`, `7c0b6005`, `4feabee1`, `a3597b2b`, `9bbbb975`; migrations named inline; `docs/event-image-migration.md`, `docs/leaderboard-system.md`, `docs/data-rights-anonymization-runbook.md`, `docs/final-compliance-reaudit.md`; `AGENTS.md`.

**Re-verification one-liners:**

```bash
git show --stat <sha>                                   # any commit cited above
git log --all --oneline --grep="#160"                   # find a PR by number
ls supabase/migrations/ | grep 20260620                 # confirm migration filenames (incl. duplicate timestamp)
grep -n "recursive" supabase/migrations/20260619000000_emergency_security_hardening.sql
grep -n "is_admin_user" supabase/migrations/20260620020000_fix_user_profiles_rls_recursion.sql
grep -n -A4 "Future Considerations" docs/leaderboard-system.md   # dual points still open?
git branch --contains 9bbbb975                          # is Ask VSA v2 (#181) merged yet?
git branch -a --no-merged main                          # refresh the graveyard table
```

Maintenance rule: when a new incident closes, add an entry here (symptom → root cause → evidence → status + lesson) in the same commit era as the fix; when an OPEN item (dual points, member self-service) closes, flip its status here and in the settled-battles table.
