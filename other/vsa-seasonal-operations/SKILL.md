---
name: vsa-seasonal-operations
description: Load when a VSA-website task touches anything calendar-driven — summer-break empty states or seasonalState.ts, House signups/House Reveal content, application windows (ace_application, house_fall/winter/spring, intern, cabinet, VCN interest forms, wnc_team_form), VCN or WNC pages, VSA Wrapped, new-academic-year launch content, academic_terms rows, or yearly turnover ("new school year" setup). Also load BEFORE changing House data/reveal content, application links/gating, or VCN surfaces at any time of year, to check the FREEZE WINDOWS policy (owner-confirmed rule, 2026-07-05; House UI exempted 2026-09-27). Provides the seasonal state machine, the academic-year content cycle, the freeze-window policy and pre-change check, and the yearly turnover runbook.
---

# VSA Seasonal Operations — the academic-year clock

This site serves a student org that lives on the UCSD academic calendar (Fall/Winter/Spring quarters + summer break). Content, application windows, House data, and several UI surfaces change state with the calendar. This skill documents (a) the seasonal state machine in code, (b) the yearly content cycle, (c) the **freeze windows policy** — an owner-confirmed rule written down here for the first time, and (d) the yearly turnover runbook.

**When NOT to use this skill:**

| If your task is… | Load instead |
|---|---|
| General change gating, protected domains, PR conventions | `vsa-change-control` |
| Env vars, application_links as a *config axis*, site settings | `vsa-config-and-flags` |
| Leaderboard/points mechanics or dual points systems | `vsa-architecture-contract` (invariants) / `vsa-debugging-playbook` (broken) |
| RLS on application_links or new views | `vsa-supabase-security-reference` |
| Past incidents behind these rules | `vsa-failure-archaeology` |
| Domain-scoped edits (House pages, cabinet, applications UI) | `.claude/agents/vsa-house-system.md`, `vsa-cabinet-leadership.md`, `vsa-applications-forms.md` playbooks |

---

## 1. The seasonal state machine: `src/utils/seasonalState.ts`

The only *computed* seasonal state in the codebase (109 lines; test: `src/utils/seasonalState.test.ts`). Everything else seasonal (application windows, current VCN, active academic term) is *configured* in Supabase by admins.

**States** (`VsaSeason` union): `active_year` | `summer_break`.

- `isSummerBreak(date?)` — true from **June 15 (inclusive) to September 15 (exclusive)**, computed in the `America/Los_Angeles` timezone (`VSA_TIME_ZONE` const) via `Intl.DateTimeFormat`. Sept 15 itself is already `active_year`. Boundaries are hardcoded constants `SUMMER_BREAK_START`/`SUMMER_BREAK_END` — a code comment says they "can be updated when the next academic year calendar is finalized."
- `getCurrentVsaSeason(date?)` — maps the boolean to the union.
- `shouldUseSummerEmptyState(hasActiveItems, date?)` — summer empty states only render when there is **no live content** (`!hasActiveItems && isSummerBreak(date)`). Real content always wins over the seasonal message.
- `getSummerBreakMessage(context)` — returns `{badge, title, body}` copy per surface context: `homepage`, `events`, `house`, `houseStandings`, `externals`, `gallery`, `points`, `default`.

**State/consumer table** (verified 2026-07-06):

| State | Date window (LA time) | Surfaces affected | Source of truth |
|---|---|---|---|
| `summer_break` | Jun 15 – Sep 14 inclusive | Homepage "This Week in VSA" (`src/components/features/home/ThisWeekInVSA.tsx` — next-event card ~L90, House standings ~L254, latest-memory card ~L397); Events page (`src/pages/Events.tsx` ~L432); Calendar (`src/pages/Calendar.tsx` ~L204); Gallery (`src/pages/Gallery.tsx` ~L79); House page (`src/pages/House.tsx` ~L635); Leaderboard points note (`src/pages/Leaderboard.tsx` ~L593); UVSA externals (`src/pages/UVSANetwork.tsx` ~L119) | Computed from system clock, hardcoded month/day constants in `seasonalState.ts` |
| `active_year` | Sep 15 – Jun 14 | Normal rendering everywhere | Same |
| Application window open/closed | Per-row `open_at`/`due_at` | `ApplicationCTA` buttons on program pages | **Configured**: `application_links` table via `public_application_links` view (§2) |
| Current academic term | Admin-set | Leaderboard year filters, event term assignment | **Configured**: `academic_terms` rows (one `is_active`) |

The test (`src/utils/seasonalState.test.ts`, 34 lines) pins the boundary dates (Jun 14 active / Jun 15 summer / Sep 14 summer / Sep 15 active) and the has-content override. If you ever change the boundary constants, update the test in the same PR.

---

## 2. The academic-year content cycle

Jargon: **VCN** = Vietnamese Culture Night (annual stage production). **WNC** = Wild 'N Culture. **ACE** = Anh Chị Em mentor-family program ("ACE lines"). **House Reveal** = the event where each year's new Houses and assignments are announced.

### Application windows (configured, never hardcoded)

Schema: `supabase/migrations/20260604000000_create_application_links.sql`. Each row has `application_key`, `open_at`, `due_at` (timestamptz, `due_at > open_at` enforced), `is_enabled`, `before_open_message`, `after_close_message`, and a `target_url` that the public **only ever sees while the window is open**. Public access is exclusively through the `public_application_links` view, which masks `target_url` unless `is_enabled AND now() BETWEEN open_at AND due_at`, and computes `status` ∈ `disabled | not_open | closed | open`. The base table has admin-only RLS policies; seeded rows are disabled placeholders pointing at `https://example.com/placeholder` — **no real URL lives in the repo, ever** (AGENTS.md: "Closed or future application URLs must not be exposed publicly").

The 9 keys (CHECK-constrained in the migration; mirrored in AGENTS.md "Domain-critical facts" and `ApplicationKey` in `src/types/database.ts`):

| Key | Cycle (quarter-level) | Notes |
|---|---|---|
| `house_fall` | Fall quarter | House signups run once per quarter |
| `house_winter` | Winter quarter | |
| `house_spring` | Spring quarter | |
| `ace_application` | Fall (UNVERIFIED-ask-leadership for exact dates) | Followed by **ACE Reveal** — the term appears in commit `1ec81d83` ("Fix ACE Reveal copy…", changed "ACE fams" → "ACE lines" in the Wrapped recap card) |
| `intern_application` | Placeholder copy says "Check back next year" → annual (quarter UNVERIFIED-ask-leadership) | |
| `cabinet_application` | Annual, typically late spring for next year's cabinet (UNVERIFIED-ask-leadership) | |
| `vcn_stage_ninja_interest` | "closer to VCN" (per seeded copy) | VCN quarter itself: UNVERIFIED-ask-leadership (historically winter/spring) |
| `vcn_props_team_interest` | Same | |
| `wnc_team_form` | "closer to Wild 'N Culture" (per seeded copy); quarter UNVERIFIED-ask-leadership | |

Frontend path: `src/data/repos/applicationLinks.ts` (repo) → `src/lib/applicationLinks.ts` (helpers) → `src/components/common/ApplicationCTA.tsx` (the gate/button rendered on program pages). Admin management: `src/pages/Admin/Applications.tsx`.

### The rest of the year's clock (git + code evidence)

| Milestone | Timing | Repo evidence |
|---|---|---|
| Launch content for new year | Late summer / fall launch | Branch `codex/launch-content-2026-2027-audit` (commit `cc1c5e3d`); admin launch checklist page `src/pages/Admin/LaunchChecklist.tsx` at `/admin/launch-checklist`; presidents fallback `src/data/presidentsContent.ts` (April Pham & Havyn Nguyen for 2026–2027) |
| House Reveal | Start of fall (summer copy in `seasonalState.ts`: "House apps, House Reveal, and new standings will come back with the school year"); exact date UNVERIFIED-ask-leadership | Pre-reveal placeholder UI in `src/pages/House.tsx` ~L673: "Houses have not been announced yet. Check back after House Reveal"; points to @vsaatucsd Instagram for official announcements |
| VCN production + archives | UNVERIFIED-ask-leadership (interest forms open "closer to VCN") | `supabase/migrations/20260512000006_create_vcn_archives.sql`; current-VCN content `20260513010000_add_program_content_and_current_vcn.sql`; admin page `src/pages/Admin/VcnArchives.tsx`; public reads via the `published_vcn_archives` view |
| WNC | UNVERIFIED-ask-leadership | Page `src/pages/WildNCulture.tsx`; `wnc_team_form` key |
| VSA Wrapped (year in review) | End of academic year (merged 2026-07-03) | Merge `fc51c96c` of `feat/vsa-wrapped-year-in-review` (PR #178, `a3d7ea60`); recap card lives on the home page: `src/components/features/home/WrappedRecapCard.tsx`; public-safe aggregates in `src/utils/wrapped.ts` (community-level numbers only, never individual member stats) |
| Summer break | Jun 15 – Sep 14 | §1 |

---

## 3. FREEZE WINDOWS policy (the rule, stated as policy)

> **Source: owner interview, 2026-07-05.** This calendar-driven discipline rule existed only in the owner's head until this skill was written. It is now policy. It complements — never overrides — AGENTS.md and `vsa-change-control`.
>
> **Amended by the owner, 2026-09-27: House UI is not frozen.** Presentational changes to House pages — layout, styling, heroes, shared components, responsive and dark-mode polish — are routine at any time of year, including while a House Reveal is pending, as long as they do not change House data, reveal gating, or *what* the page shows. The House Reveal freeze covers House **data and reveal content** only.

**The rule:** around **House Reveals**, **application-window opens**, and **VCN**, the affected surfaces are frozen. Do not change them without explicit owner approval — *even for "safe" refactors, copy tweaks, styling passes, or dependency-driven churn* (House is the exception: only its data and reveal content freeze, not its UI — see the 2026-09-27 amendment above). A broken button or wrong placeholder during a reveal or an application open is a public, time-critical failure for 600+ members that cannot wait for a next deploy cycle.

Frozen surfaces per event:

| Calendar event | Frozen surfaces |
|---|---|
| House Reveal | House **data and reveal content**: House assets/profiles (rows and images), `src/constants/houses.ts`, reveal placeholder copy and the announced-vs-not-announced gating logic in `src/pages/House.tsx` / `HouseDetail.tsx`, House standings data. **Not frozen:** House page UI — layout, styling, heroes, shared components (routine; owner amendment 2026-09-27) |
| Application window opening (any of the 9 keys) | `application_links` rows and the `public_application_links` view, `ApplicationCTA.tsx`, `src/lib/applicationLinks.ts`, `src/data/repos/applicationLinks.ts`, the program page hosting that CTA (e.g. `src/pages/Ace.tsx`, `Internship.tsx`, `WildNCulture.tsx`) |
| VCN season | VCN program page/content, VCN archives admin + `published_vcn_archives`, `vcn_*_interest` application rows |

**Pre-change check — run before touching any of the surfaces above, at any time of year:**

1. **Are any application windows open or opening soon?** Check the admin UI (`/admin/applications`) or query the public view (safe, anon-readable):
   ```sql
   select application_key, status, open_at, due_at
   from public_application_links
   order by sort_order;
   ```
   `status = 'open'`, or `not_open` with `open_at` within ~2 weeks → the corresponding surfaces are frozen.
2. **Is a House reveal pending?** If the current year's Houses are still placeholders (as of 2026-07-06, 2026–2027 Houses are placeholders — AGENTS.md), a reveal is by definition pending. Never invent House names, themes, or assignments; never "pre-fill" reveal content. The placeholder state in `src/pages/House.tsx` *is* the correct production state until leadership announces. A pending reveal freezes House data and reveal content — it does **not** freeze House page UI work, provided the UI change leaves the placeholder state and its copy intact.
3. **Is VCN season active?** Check whether `vcn_stage_ninja_interest` / `vcn_props_team_interest` are open (query above) and whether current-VCN content is live (admin `/admin/vcn`). If yes → VCN surfaces frozen.
4. If any check fires and your change touches a frozen surface: **stop and get explicit owner approval** (see `vsa-change-control` for the approval flow). Record the approval in the PR body.

What is *not* frozen: unrelated surfaces during a freeze (e.g. gallery work during an application open), and the frozen surfaces themselves outside their windows — normal `vsa-change-control` rules apply then.

---

## 4. Yearly turnover runbook

> **Tooling:** most of this runbook now has an admin workflow, so a President does not need SQL. **New Year Setup** (`/admin/year-setup`) previews and creates the year's terms, inactive Cabinet year, ACE cycle, Intern cohort, and (once profiles exist) an empty House batch, plus a separate application reset; **Cabinet Rollover** (`/admin/cabinet/rollover`) copies last year's positions (never people) and publishes the new roster without activating it. Houses stay unrevealed and application URLs are never invented. See `docs/yearly-operations.md`. The numbered steps below remain the policy; the wizard is how to carry them out.

Reconstructed from git/migration evidence of the 2025→2026 turnover. Run at end of spring / over summer, before fall launch. Every step below still goes through normal branch-and-PR flow (`vsa-change-control`); migrations are applied manually per `vsa-run-and-operate`.

1. **Archive last year's cabinet.** The cabinet archive machinery exists: seed migration `supabase/migrations/20260512000004_seed_historical_cabinet_archive.sql`, archive import commit `cd2c8775` (PR #29), archive URL state PR #122 (`13c99b78`), admin year/term management `2ce699b1` → `src/pages/Admin/YearsTerms.tsx` and `src/pages/Admin/Cabinet.tsx`. Never mix current cabinet with archive members (AGENTS.md).
2. **Archive last year's Houses.** Legacy-House machinery: `src/data/legacyHouseArchive.ts` (+ its test — one of the repo's domain-fact-protecting tests; see `vsa-validation-and-qa` §2), seed migrations `20260531000000_seed_legacy_house_assets.sql` and `20260601010000_restore_mario_house_assets.sql`, membership history `20260525000000_add_house_membership_history.sql`.
3. **Add new `academic_terms` rows** for the new year's quarters (`supabase/migrations/20260512000000_add_academic_terms_and_cabinet_years.sql`: `academic_year_end = academic_year_start + 1` CHECK; a unique partial index enforces **exactly one `is_active` term**). Events must be assigned to terms (`events.academic_term_id`) for the yearly leaderboard — `docs/leaderboard-system.md`: leaderboard truth is `member_event_attendance` joined through `events` to `academic_terms`. Admin UI: `/admin/years` (`src/pages/Admin/YearsTerms.tsx`).
4. **Update president/launch fallbacks**: `src/data/presidentsContent.ts` (2026–2027: "April Pham & Havyn Nguyen"), plus degraded-mode copy in `src/config/publicFallbackContent.ts`. Cross-check the launch audit pattern: branch `codex/launch-content-2026-2027-audit` and the admin launch checklist (`/admin/launch-checklist`).
5. **Reset/verify application windows**: for each of the 9 `application_links` rows, set new `open_at`/`due_at`, refresh `before_open_message`/`after_close_message`, and keep rows `is_enabled = false` with placeholder URLs until leadership provides real links. Freeze-window rules (§3) apply the moment a window opens.
6. **Seed new House placeholders only when officially announced.** Until House Reveal, the House page's built-in "not announced yet" state is correct. Never invent Houses (AGENTS.md; §5).
7. **Update AGENTS.md "Domain-critical facts"** (new presidents, new Houses once revealed, year rollover) — and then update every skill that quotes those facts, including this one and the domain playbooks in `.claude/agents/`. AGENTS.md is the canonical home; skills must not drift from it.
8. **Review `seasonalState.ts` boundaries** against the new year's actual calendar (the code invites this: "can be updated when the next academic year calendar is finalized"). If changed, update `seasonalState.test.ts` in the same PR.

---

## 5. Domain-facts table

Canonical home: **AGENTS.md → "Domain-critical facts"** (repo root, ~L229–236). Quoted as of 2026-07-06 — re-verify against AGENTS.md before relying on these, they roll over yearly:

| Fact | Value (AGENTS.md quote) |
|---|---|
| 2026–2027 presidents (fallback/copy) | "use April Pham and Havyn Nguyen" |
| 2026–2027 Houses | "placeholders only; do not invent Houses" |
| 2025–2026 Houses | "Bowser, Donkey Kong, Boo, and Toad" |
| 2023–2024 Houses | "drinks/treats, not designer Houses" |
| Designer Houses | "belong to 2019–2020"; "Mario Houses belong only to 2025–2026" |
| Application URLs | "Closed or future application URLs must not be exposed publicly" |
| Application keys | `ace_application`, `house_fall`, `house_winter`, `house_spring`, `intern_application`, `cabinet_application`, `vcn_stage_ninja_interest`, `vcn_props_team_interest`, `wnc_team_form` |
| Membership integrity | Never mix current with archive members; never create fake events, members, points, standings, application links, or House assignments |

---

## 6. Cross-references

- **Change gating and approval flow** for anything §3 freezes → `vsa-change-control`.
- **application_links as a configuration axis** (all config axes, add-a-config checklist) → `vsa-config-and-flags`.
- **RLS/view mechanics** behind `public_application_links` and `published_vcn_archives` (view-masking pattern, revoke-then-grant gotcha) → `vsa-supabase-security-reference`.
- **Domain playbooks** for hands-on edits: `.claude/agents/vsa-house-system.md`, `vsa-cabinet-leadership.md`, `vsa-applications-forms.md`, `vsa-public-content.md`.
- **Leaderboard/terms internals** → `docs/leaderboard-system.md` and `vsa-architecture-contract`.

---

## Provenance and maintenance

Sources (verified 2026-07-06, branch `codex/reactbits-ui`):
- `src/utils/seasonalState.ts` (109 lines) and `src/utils/seasonalState.test.ts` (34 lines) — read in full.
- `AGENTS.md` — Domain-critical facts, Things to never do.
- `supabase/migrations/20260604000000_create_application_links.sql` (keys, window semantics, view masking); `20260512000000_add_academic_terms_and_cabinet_years.sql`; `20260512000004_seed_historical_cabinet_archive.sql`; `20260512000006_create_vcn_archives.sql`; `20260525000000_add_house_membership_history.sql`; `20260531000000_seed_legacy_house_assets.sql`; `20260601010000_restore_mario_house_assets.sql`.
- `docs/leaderboard-system.md` (terms→leaderboard dependency).
- Git: `1ec81d83` (ACE Reveal copy), `fc51c96c`/`a3d7ea60` (VSA Wrapped, PR #178), `cd2c8775`/#29 and `13c99b78`/#122 (cabinet archive), `2ce699b1` (years/terms admin), `cc1c5e3d` (`codex/launch-content-2026-2027-audit`).
- **Freeze-windows policy: owner interview, 2026-07-05** (previously unwritten; this file is its first written home). **Amended 2026-09-27 by the owner:** House UI changes are not frozen; the House Reveal freeze covers House data and reveal content only.

Re-verification one-liners:
```bash
sed -n '3,7p' src/utils/seasonalState.ts                      # summer boundary constants + season union
grep -rn "getSummerBreakMessage" src/pages src/components | cut -d: -f1 | sort -u   # current consumers
grep -n "application_key in" -A 12 supabase/migrations/20260604000000_create_application_links.sql  # the 9 keys
grep -n "Domain-critical facts" -A 10 AGENTS.md               # canonical domain facts (yearly rollover)
grep -n "April Pham" src/data/presidentsContent.ts            # presidents fallback
ls src/pages/Admin | grep -E "Applications|VcnArchives|YearsTerms|LaunchChecklist"  # admin surfaces still exist
```
Volatile: everything in §5 rolls over each academic year; §1 boundary dates may be edited when a new calendar is finalized; §2 quarter-level timings marked UNVERIFIED-ask-leadership need confirmation from VSA leadership, not the repo.
