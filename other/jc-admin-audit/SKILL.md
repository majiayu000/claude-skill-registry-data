---
name: jc-admin-audit
description: Use when performing a comprehensive quality audit of the JapaConnect Admin Panel (apps/admin) before merge or release. Verifies RBAC CRUD completeness per entity, full DataTable spec compliance, LayerChart usage, SPA architecture, and security.
---

# JapaConnect Admin Panel — Audit Skill

Work file-by-file. Conventions: `jc-admin-develop`.

## A. RBAC CRUD Completeness Matrix (Run First — Highest Priority)
Build a matrix of EVERY entity managed in the panel × required backend routes:

| Entity | List | Get | Create | Update | Delete | State routes | Frontend exposes all? |
|---|---|---|---|---|---|---|---|

- Verify each route against JEOS `api-routes-catalog.md` or live probe
- **Any entity where super-admin cannot perform full CRUD from the UI is a Critical finding** — whether the gap is a missing backend route (⛔ MISSING RBAC CRUD ENDPOINTS block) or a missing frontend control
- State-capable entities (users, orgs, content, spaces, claims): verify BOTH directions exist and are surfaced (Ban AND Unban, Suspend AND Unsuspend, Approve AND Reject)
- **Japa Academy entities (ADR-063):**
  - `universities` (Section 39 space type): List/Get/Create/Update/Delete + Verify/Unverify + status transitions (publish/draft/archive) + CSV bulk import
  - `academy_instructor_profiles`: List/Get + Approve/Reject + Suspend/Unsuspend + tier/commission update. **Both directions of every state transition required.**
  - `university/tracks` (course approval): List/Get + Approve/Reject (sets `is_published_to_academy`)
  - `university/payouts`: List/Get + Process (trigger payout) + Mark-failed. State: pending→processing→paid/failed
- **Sensitive data check:** `academy_instructor_profiles.payout_method` (jsonb) must be masked in the admin UI — never displayed raw (Critical security finding if exposed)

## B. DataTable Spec Compliance (Per Entity List Page)
- [ ] Sortable (URL-param) · [ ] Searchable (`?q=` debounced) · [ ] Filterable (`?filter=` panel) · [ ] Paginated (page-size selector, API meta)
- [ ] Action column: View (modal) / Edit / Delete on every row
- [ ] Conditional state actions per row state
- [ ] Bulk selection + contextual bulk bar
- [ ] Create button on non-readonly entities
- [ ] Readonly entities have Delete/Remove/Clear in action column
- [ ] Destructive actions behind `<Dialog.Root>` (no `window.confirm`) · [ ] View never navigates
Flag any list page using a custom table instead of the shared `<DataTable>`.

## C. API Consumption Verification
Every `fetch()` route confirmed against the catalog. Uncatalogued routes → Critical (⚠️ block).

## D. LayerChart Compliance
Dashboard + all 5 analytics pages use LayerChart exclusively · no Chart.js/canvas/raw-SVG charts · colors `var(--color-*)` (dark-mode verified) · fixed-height containers · skeletons · data from analytics endpoints with `?from=&to=` support.

## E. SPA Architecture
`ssr=false`/`prerender=false` · zero `+page.server.ts` · auth guard on every protected route · `goto()` navigation · token refresh present.

## F. Security
Permission-node gating on every destructive/privileged action (UI-side, not just backend) · CSRF on all mutations · `{@html}` audit · no PII/secrets in console.log · session validated per mount.

## G. Data Fetching Quality
try/catch + error state + retry · loading skeletons per table/chart · pagination state in URL (survives back/forward).

## H. Bits UI, Svelte 5, Accessibility, i18n
Apply `jc-main-audit` sections D, B(runes), H, I. Admin-specific a11y: `aria-sort`, disabled-not-hidden bulk buttons, focus return on dialog close, `aria-live` on tables.

## I. V2 (JEOS v1.23.1) Compliance Checklist
Additional audit items for §§79–102 admin surfaces (Phases 24–27). Run these alongside sections A–H for any v2 admin page.

- [ ] **ADR-088 AI generation columns present** on all §§79–101 admin content tables: `ai_generated` (bool), `ai_model` (text), `hitl_reviewed_by` (text/uuid), `ai_generated_at` (timestamptz). Missing any column on a content table → Critical finding.
- [ ] **HITL review gate enforced before publish** on all AI-generated content — no admin action can set content to published/active state without `hitl_reviewed_by` being populated. Bypass possible → Critical finding.
- [ ] **Geo-aware tool pattern compliance** — all §§90–97, §§99–101 tool admin list endpoints accept `?dest=` filter; no hardcoded nationality in queries or UI defaults. Hardcoded nationality → High finding.
- [ ] **Feature-flag middleware returns 404 (not 403) when disabled** (ADR-042) — probe a disabled feature endpoint and verify the response code is 404, not 403. Returning 403 → Medium finding.
- [ ] **Admin list endpoints have filter + sort + paginate** — no infinite scroll on any v2 admin list. Verify `?page=&limit=&sort=&filter=` params are accepted and API returns `meta` with pagination data. Infinite scroll → High finding.
- [ ] **Mentorship trigger exists** — `trg_mentee_count` PostgreSQL trigger is present and `active_mentee_count` on mentor profiles is NOT computed at query time (no `COUNT(*)` subquery in the mentor list endpoint). Trigger missing or count computed at query time → High finding.
- [ ] **Route catalog completeness** — ~819 routes total (~475 v1 + ~344 v2), 297 RBAC nodes, 18 Golden Rules. Verify all v2 admin routes for §§79–102 are catalogued in `api-routes-catalog.md`.

## Report Format
```
## Audit Report — Admin Panel (apps/admin)
**Files Audited:** [n] · **Status:** PASS / NEEDS FIXES
### Critical / High / Medium / Low
[lists — RBAC CRUD gaps always Critical]
### RBAC CRUD Matrix
[the full entity × routes table]
### Compliance Summary
| RBAC CRUD completeness | ✅/❌ |
| DataTable spec | ✅/❌ |
| API routes verified | ✅/❌ |
| LayerChart | ✅/❌ |
| SPA architecture | ✅/❌ |
| Security | ✅/❌ |
| Bits UI · Svelte 5 · A11y · i18n | ✅/❌ |
| V2 ADR-088 AI columns + HITL gate | ✅/❌ |
| V2 geo-aware tool pattern | ✅/❌ |
| V2 feature-flag 404 (not 403) | ✅/❌ |
| V2 admin list filter+sort+paginate | ✅/❌ |
| V2 mentorship trigger (trg_mentee_count) | ✅/❌ |
```
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
