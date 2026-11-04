---
name: jc-admin-debug
description: Use when reviewing or debugging JapaConnect Admin Panel code (apps/admin, SPA). Diagnoses DataTable spec violations, RBAC gaps, SPA auth issues, LayerChart problems, and Svelte 5/Bits UI errors.
---

# JapaConnect Admin Panel — Review & Debugging Skill

Conventions and gates: `jc-admin-develop`. Run checks in order.

## 0. Gates First
- Data not loading? Verify the route exists before debugging frontend. Missing → ⚠️ MISSING BACKEND API ROUTES alert, pause.
- Entity page missing an action (edit, delete, unban)? Check if the backend route exists. Missing → ⛔ MISSING RBAC CRUD ENDPOINTS alert, pause. A frontend "fix" that hides the action is NOT acceptable — super-admin CRUD is non-negotiable.

## 1. DataTable Spec Violations
Check the page against the mandatory spec — flag every miss:
- [ ] Sortable columns (URL-param driven, survives navigation)
- [ ] Search input wired to `?q=`, debounced
- [ ] Filter panel wired to `?filter=`
- [ ] Pagination with page-size selector from API `meta`
- [ ] Action column with View + Edit + Delete on every row
- [ ] State actions (Suspend/Unsuspend, Ban/Unban, Approve/Reject) present AND conditional on current state — a banned user's row must show Unban, not Ban
- [ ] Bulk checkboxes + select-all + contextual bulk bar
- [ ] Create button (top) on non-readonly entities
- [ ] Readonly entities still have Delete/Remove/Clear in the action column
- Bulk selection reset on page change · destructive actions behind `<Dialog.Root>` confirmation (never `window.confirm`) · View opens a modal, never navigates

## 2. SPA Auth
Root layout `ssr=false`/`prerender=false` · auth guard `$effect` + `goto('/login')` on every protected route · no `+page.server.ts` files · `goto()` not `window.location.href` · 403 → permission error UI, not blank screen.

## 3. Data Fetching
`$effect` (not `onMount`) so param changes re-fetch · reactive params inside effect scope · try/catch + error state + `finally { loading = false }` · `$derived` for computed counts.

## 4. LayerChart
Fixed-height container present · colors `var(--color-*)` only (test dark mode) · API date strings → `Date` objects · data from `/api/v1/admin/analytics/*` not hardcoded · skeleton per chart · LayerChart `Tooltip` vs Bits UI `Tooltip` import collision — alias one (`import { Tooltip as ChartTooltip } from 'layerchart'`).

## 5. RBAC UI
Permission-node checks (`session.permissions.includes(...)`) not role-string checks · destructive controls hidden/disabled without permission · state-action buttons permission-gated individually (ban ≠ suspend permission). **Japa Academy**: `academy.instructor.approve` ≠ `university.instructor.suspend` ≠ `academy.course.approve` ≠ `academy.payout.process` — each is a separate node, gate each action individually.

## 6. Bits UI / Svelte 5
Apply the full violation tables from `jc-main-debug` sections 2–3.

## 6b. Japa Academy Admin (ADR-063 + Section 39)
- **Instructor approval missing both directions:** approve without reject (or vice versa) — Gate 2 requires BOTH directions of every state transition. A pending instructor must have Approve AND Reject; an approved instructor must have Suspend AND Unsuspend.
- **Payout method exposed:** `academy_instructor_profiles.payout_method` (jsonb) shown raw in the admin UI — Critical security finding. Must be masked.
- **University course approval one-directional:** only Approve without Reject — both required. Approve sets `is_published_to_academy = true`; Reject keeps it false.
- **Payout state machine broken:** `academy_instructor_payouts` status must go pending→processing→paid or →failed. A jump from pending to paid (skipping processing) or from paid back to pending is a defect.
- **University logo not uploading:** logo upload must go through Section 34 media (SeaweedFS + imgproxy) — if it's stored as a raw URL string, that's a defect.

## 7. Accessibility
`<th scope="col">` + `aria-sort` on sortable headers · bulk buttons `disabled` (not hidden) when nothing selected · focus returns to trigger on dialog close · `aria-live="polite"` on table container during load.

## 8. V2 (JEOS v1.23.1) Debug Patterns
Debug patterns for §§79–102 admin surfaces (Phases 24–27). ~819 routes total (~475 v1 + ~344 v2), 297 RBAC nodes, 18 Golden Rules.

- **Missing ADR-088 columns on admin content tables:** An admin content table for §§79–101 (stories, wiki revisions, scam alerts, digests, AMAs, services, arrival checklists, housing guides, attestations, tax guides) is missing one or more of `ai_generated`, `ai_model`, `hitl_reviewed_by`, `ai_generated_at`. Symptom: admin form has no HITL review step, or AI-generated content can be published without review. Fix: add the missing columns via migration, update the admin form to require `hitl_reviewed_by` before publish.
- **HITL review gate bypassed:** Content with `ai_generated = true` is in published/active state but `hitl_reviewed_by` is NULL. Symptom: AI-generated story/wiki revision/digest visible to users without human review. Root cause: the publish/approve endpoint doesn't check `hitl_reviewed_by` when `ai_generated = true`. Fix: enforce server-side check — reject publish if `ai_generated = true AND hitl_reviewed_by IS NULL`.
- **Geo-aware filter missing (?dest= not implemented):** A §§90–97 or §§99–101 tool admin list endpoint doesn't accept `?dest=` parameter, or the DataTable filter panel lacks a destination country dropdown. Symptom: admin can't filter tool content by destination country, or nationality is hardcoded in the query. Fix: add `?dest=` filter param to the endpoint, add destination dropdown to the filter panel, remove any hardcoded nationality from queries.
- **Feature-flag returning 403 instead of 404:** A disabled v2 feature endpoint returns HTTP 403 (Forbidden) instead of HTTP 404 (Not Found) per ADR-042. Symptom: admin UI shows a permission error instead of "feature disabled" for a v2 feature that hasn't been enabled yet. Fix: update the feature-flag middleware to return 404 when a feature is disabled (not 403). The admin frontend should handle 404 as "feature not available" rather than "permission denied."
- **Admin list using infinite scroll instead of pagination:** A v2 admin list page uses infinite scroll or "load more" instead of the standard DataTable pagination with page-size selector. Symptom: no page-size selector (25/50/100), no pagination navigation, URL params don't include `?page=&limit=`. Fix: replace infinite scroll with standard DataTable pagination, ensure the API endpoint returns `meta` with total count + page info.
- **Mentorship active_mentee_count computed at query time (trigger missing):** The mentor list endpoint computes `active_mentee_count` via a `COUNT(*)` subquery or join instead of reading the maintained column. Symptom: mentor list is slow, or `active_mentee_count` is inconsistent with actual mentee connections. Root cause: `trg_mentee_count` PostgreSQL trigger is missing or disabled. Fix: create/enable the trigger that maintains `active_mentee_count` on INSERT/UPDATE/DELETE of mentee connections, remove the query-time computation from the endpoint.

## Output Protocol
1. Root cause (one sentence) · 2. Broken code · 3. Fixed code · 4. Secondary findings
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
