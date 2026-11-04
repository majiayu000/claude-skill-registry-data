---
name: jc-admin-refactor
description: Use when updating or refactoring existing JapaConnect Admin Panel code (apps/admin). Upgrades tables to the full DataTable spec, migrates charts to LayerChart, modernizes to Svelte 5 Runes and Bits UI.
---

# JapaConnect Admin Panel — Updating & Refactoring Skill

Conventions and gates: `jc-admin-develop`. Behavior-preserving modernization only; one-line comment per change.

## 0. Gates
Refactor needs a new endpoint (e.g. adding a missing Delete action)? Verify it exists first. Missing → ⚠️/⛔ alert, pause. **When refactoring an entity page, run Gate 2 (RBAC CRUD) on that entity** — refactoring is the moment to catch pages shipped without full CRUD.

## 1. Table → Full DataTable Spec Upgrade
Any table missing part of the mandatory spec gets upgraded to ALL of it:
- Add missing: sort (URL params) · search (`?q=` debounced) · filter panel (`<Accordion.Root>`) · pagination + page-size selector
- Add missing action-column items: View (modal) / Edit / Delete — plus state actions (Suspend/Unsuspend, Ban/Unban, Approve/Reject) conditional on row state
- Add bulk selection (`Set<string>`) + bulk bar
- Add Create button (non-readonly entities)
- Readonly entities: add Delete/Remove/Clear to the action column + "Clear all/older-than" bulk option
- Replace `window.confirm` → `<Dialog.Root>` confirmation · replace navigation-on-view → `<Dialog.Root>` preview

## 2. Chart Migration → LayerChart
Rewrite all Chart.js / canvas / raw-SVG / D3-DOM charts as LayerChart (pattern in `jc-main-refactor` §3). Dashboard stat cards get sparklines (`<Chart>` + `<Spline>`, no axes). Analytics pages get a date-range picker driving `?from=&to=`. Remove replaced chart libraries from package.json.

## 3. Data Fetching Modernization
`onMount` fetch → reactive `$effect` with loading/error/`finally`; params inside effect scope so sort/filter/page changes re-fetch.

## 4. Form Modernization
Single `$state` form object · `submitting` + `formError` states · CSRF header · dialog closes + table refreshes on success · unsaved-changes `beforeNavigate` guard on edit forms.

## 5. RBAC Hardening
Role-string checks → permission-node checks: `$derived(session?.permissions.includes('users.ban') ?? false)`. **Japa Academy**: each university action has its own node (`academy.instructor.approve`, `academy.course.approve`, `academy.payout.process`) — gate each individually, not by a blanket `university.*` role.

## 6. Standard Migrations
Svelte 4→5, Bits UI adoption, Tailwind v4, i18n sweep, a11y — apply `jc-main-refactor` §§1–2, 5. Consolidate duplicate fetches (user groups, spaces, content types) into `setContext`/`getContext` at admin root layout.

## 7. Japa Academy Admin Pages (ADR-063 + Section 39)
- **Add university entity pages** if missing: Universities (Section 39 space type) with full DataTable + CRUD + Verify state action + CSV bulk import. Instructor profiles with review dialog + both-direction state transitions. University course approval with Approve/Reject. Payout management with process/mark-failed state machine.
- **Mask payout_method:** any raw display of `academy_instructor_profiles.payout_method` → masked display (show last 4 digits or type only).
- **University logo:** if stored as a raw URL string → migrate to Section 34 media upload (SeaweedFS + imgproxy).
- **Run Gate 2 on every university entity** during refactor — refactoring is when missing CRUD/state routes get caught.

## 8. V2 (JEOS v1.23.1) Refactoring
Refactoring tasks for §§79–102 admin surfaces (Phases 24–27). ~819 routes total (~475 v1 + ~344 v2), 297 RBAC nodes, 18 Golden Rules. Apply these when modernizing existing v2 admin pages or bringing pre-v1.23.1 pages up to the new spec.

- **Add ADR-088 columns to admin content tables missing them:** Any admin content table for §§79–101 that can hold AI-generated content (stories, wiki revisions, scam alerts, digests, AMAs, services, arrival checklists, housing guides, attestations, tax guides) must have `ai_generated` (bool), `ai_model` (text), `hitl_reviewed_by` (text/uuid), `ai_generated_at` (timestamptz). If a table is missing any column, add a migration. Then update the admin form to surface a HITL review step — the publish/approve action must populate `hitl_reviewed_by` with the admin user's ID. If the existing form allows publishing AI-generated content without review, add the gate.
- **Convert admin lists from infinite scroll to filter+sort+paginate:** Any v2 admin list page using infinite scroll, "load more", or unbounded queries must be upgraded to the standard DataTable spec with `?page=&limit=&sort=&filter=` params and API `meta` pagination response. Add the page-size selector (25/50/100) and pagination navigation. This is the same upgrade as section 1 (Table → Full DataTable Spec) but specifically flag v2 admin lists that shipped with infinite scroll as a spec violation.
- **Apply geo-aware tool pattern to existing tool pages that hardcode nationalities:** Any §§90–97 or §§99–101 tool admin page that hardcodes a nationality (e.g. filtering by a specific country code in the query, or showing only "Nigeria" content) must be refactored to the geo-aware pattern: destination country is the primary data axis, `?dest=` filter on list endpoints, no hardcoded nationality. Add a destination country dropdown to the DataTable filter panel. Replace hardcoded country filters with the `?dest=` parameter.
- **Fix feature-flag middleware returning 403 instead of 404 (ADR-042):** If any v2 feature-flag middleware returns 403 (Forbidden) when a feature is disabled, refactor it to return 404 (Not Found). Update the admin frontend to handle 404 as "feature not available" rather than rendering a permission error UI.
- **Fix mentorship active_mentee_count computed at query time:** If the mentor list endpoint computes `active_mentee_count` via a `COUNT(*)` subquery or join, refactor to use a maintained column. Create/enable the `trg_mentee_count` PostgreSQL trigger that updates `active_mentee_count` on INSERT/UPDATE/DELETE of mentee connections. Remove the query-time computation from the endpoint. This is a performance + correctness refactor.

**V2 admin phases (20–27):** Persona Management + Content Studio (Phase 20) → Newsletter + Jobs (Phase 21) → Gamification/Analytics/Commerce (Phase 22) → QA (Phase 23) → Community Features Admin (Phase 24) → Tools Admin + HITL Queues (Phase 25) → QA Update (Phase 26) → Mentorship Admin (Phase 27). See `ROADMAP-ADMIN.md` for task breakdown.

**New admin surfaces in v2:** AI Persona management (`/admin/personas`), Content Studio (`/admin/studio`), Participation queue (tab in moderation queue), RAG index status widget, Remittance provider management, Newsletter composer, Gamification badge/challenge CRUD, Advanced analytics dashboard.

**V2 community features admin (Phase 24, §§79–89, §98):** Story verification (§79), wiki revision approval (§80), scam alert moderation (§81), planning group management (§82), visa timeline admin (§83), digest generation/publish (§84), mutual aid moderation (§85), calendar review (§86), japa stage profiles (§87), AMA moderation (§88), achievement management (§89), service directory verification/claim review (§98). All admin-managed content tables must carry ADR-088 AI generation columns (ai_generated, ai_model, hitl_reviewed_by, ai_generated_at) with mandatory HITL review before publish. Admin list endpoints must filter + sort + paginate (no infinite scroll).

**V2 functional tools admin (Phase 25, §§90–97, §§99–101):** Visa route management (§90), embassy polling configuration (§91), arrival checklist approval (§92), processing time tracker (§93), credential checker management (§94), CV formatter standards (§95), housing guide management (§96), attestation approval (§97), language test requirements (§99), tax guide/treaty management (§100), community locator review (§101). All tools follow the geo-aware tool pattern — destination country is the primary data axis, no hardcoded nationality, ?dest= filter on list endpoints.

**V2 mentorship admin (Phase 27, §102, ADR-110):** Mentorship connection management, mentor profile review. Verify active_mentee_count is maintained by PostgreSQL trigger (trg_mentee_count), not computed at query time. Match scoring is 60% keyword overlap + 40% pgvector cosine similarity.

## V2 Feature Areas (Implement Only After Corresponding Backend Phase Is Complete)

| Feature | Backend phase | Key sections | Gates |
|---|---|---|---|
| JapaBot (RAG-grounded) | Phase 41 | §69 | `/ai/chat` amended |
| AI Content Studio (admin) | Phase 42 | §75 | `studio.*` RBAC |
| Participation queue (admin) | Phase 42 | §76 | `participation.review` RBAC |
| Visa Checklist | Phase 43 | §70 | `checklist.use` RBAC |
| Readiness Assessment | Phase 43 | §71 | `assessment.take` RBAC |
| Cost of Living Calculator | Phase 43 | §72 | `col_calculator.use` RBAC |
| Scholarship Finder | Phase 43 | §73 | `scholarship.browse` RBAC |
| Remittance Rate Tracker | Phase 44 | §74 | `remittance.view` RBAC |
| Referral system | Phase 45 | §60 | `referral.use` RBAC |
| Self-serve ads | Phase 45 | §61 | `ads.self_serve.create` RBAC |
| Newsletter | Phase 45 | §62 | `newsletter.subscribe` RBAC |
| Jobs board | Phase 45 | §63 | `jobs.browse` RBAC |
| Gamification | Phase 45 | §64 | `gamification.view` RBAC |
| Content import | Phase 46 | §65 | `import.use` RBAC |
| Advanced analytics | Phase 46 | §66 | `analytics.advanced` RBAC |
| Travel search | Phase 46 | §67 | `travel.search` RBAC |

**API-Readiness Gate applies to all v2 features.** Verify against `api-routes-catalog.md` — all v2 routes are marked as "V2 planned" in the catalog. Once the corresponding backend phase lands, the planned routes become available.

**Removed surface:** `apps/tools` was consolidated into `apps/main` (`/tools/{tool}`) — ADR-086 superseded. `tools.japa.to` and per-tool subdomains 301 to `japa.to/tools/{tool}`; the `jc-tools-*` skills were deleted.
