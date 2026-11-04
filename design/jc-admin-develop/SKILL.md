---
name: jc-admin-develop
description: Use when building new pages or components for the JapaConnect Admin Panel (apps/admin, port 3001, SPA). Covers the mandatory DataTable spec (sort/search/filter/paginate/actions/bulk/create), the RBAC CRUD Gate, LayerChart dashboards, and SPA auth patterns.
---

# JapaConnect Admin Panel — Development Skill

Internal SPA (adapter-static) for moderation, user management, analytics, configuration. Design: dev.to admin — dense, action-first.

## ⛔ GATE 1 — API-READINESS (Run Before Any Implementation)
List every endpoint the feature consumes → verify each exists (JEOS `api-routes-catalog.md` or live probe) → if ANY missing: STOP, output:
```
⚠️ MISSING BACKEND API ROUTES — implementation paused
Feature: [name]
Missing routes: [list]
Action needed: implement these routes in the Go backend before frontend work continues.
```
Never mock, never hardcode around a gap.

## ⛔ GATE 2 — RBAC CRUD (Non-Negotiable, Run Per Entity)
**Super-admin must be able to perform full CRUD on every entity managed in this panel.** Before implementing ANY entity management page, verify the backend exposes ALL of:
- `GET /api/v1/admin/[entity]` (list, with `?page=&limit=&sort=&q=&filter=`)
- `GET /api/v1/admin/[entity]/:id` (detail)
- `POST /api/v1/admin/[entity]` (create)
- `PATCH /api/v1/admin/[entity]/:id` (update)
- `DELETE /api/v1/admin/[entity]/:id` (delete)
- State-transition routes where the entity has states: `POST .../suspend`, `POST .../unsuspend`, `POST .../ban`, `POST .../unban`, `POST .../approve`, `POST .../reject`, etc.
- All of the above RBAC-gated by permission nodes

If ANY CRUD or state route is missing: STOP, output:
```
⛔ MISSING RBAC CRUD ENDPOINTS — implementation paused
Entity: [entity]
Missing: [e.g. PATCH /api/v1/admin/tags/:id, POST /api/v1/admin/users/:id/unban]
Super-admin CRUD is non-negotiable. Backend must expose these before this page is built.
```

## 📋 DATATABLE SPEC — MANDATORY FOR EVERY ENTITY LIST PAGE
Every entity list uses the shared `<DataTable>` with ALL of the following. No exceptions, no "simple list" shortcuts:

1. **Sortable** — every sortable column header toggles asc/desc; state in URL params
2. **Searchable** — search input wired to `?q=` (debounced 300ms)
3. **Filterable** — collapsible filter panel (`<Accordion.Root>`) with entity-specific filters wired to `?filter=`
4. **Paginated** — page size selector (25/50/100) + navigation; from API `meta`
5. **Action column** — EVERY row, via `<DropdownMenu.Root>` (⋮):
   - **View** (opens `<Dialog.Root>` preview modal — never navigates away)
   - **Edit** (opens modal/dialog form)
   - **Delete** (opens `<Dialog.Root>` confirmation)
   - **State actions** where the entity supports them: Suspend/Unsuspend, Ban/Unban, Approve/Reject, Activate/Deactivate, Verify/Unverify — shown conditionally on current state (e.g. suspended row shows Unsuspend)
6. **Bulk actions** — per-row checkboxes (`Set<string>`), select-all, bulk bar visible when `selectedIds.size > 0` with contextual actions (Delete, Suspend, Approve, Export)
7. **Create button** — top-right of the table, for ALL non-readonly entities; opens the create form in `<Dialog.Root>`
8. **Readonly entities** (audit logs, impersonation logs, webhook deliveries, sessions): no Create/Edit, but the action column MUST still include **Delete/Remove/Clear** (single-row delete + a "Clear all" or "Clear older than…" bulk option), plus View

```svelte
<script lang="ts">
  let { columns, rows, totalRows, entity,
    page = $bindable(1), pageSize = $bindable(25),
    q = $bindable(''), filters = $bindable({}),
    sort = $bindable({ key: 'created_at', dir: 'desc' }),
    selectedIds = $bindable(new Set<string>()),
    readonly = false, stateActions = [],
    onCreate, onView, onEdit, onDelete, onStateAction, onBulkAction,
  }: DataTableProps = $props();
</script>
```

## LayerChart — Dashboard & Analytics (Mandatory)
Admin Dashboard and every Analytics page (Traffic, Content, Search, Community, Revenue) use **LayerChart** exclusively:
- Line/Area (`<Spline>`, `<Area>`): signups over time, DAU/MAU, content volume, revenue
- Bars (`<Bars>`): top spaces by activity, content by type, reports by category
- Arc/Pie (`<Arc>`): geo distribution, user group split
- Stat cards: value + delta + sparkline (`<Chart>` + `<Spline>`, no axes)
- Colors ONLY `var(--color-*)` · fixed-height containers · data from `/api/v1/admin/analytics/*` · skeleton per chart · date-range picker (`<Popover.Root>` + range) driving `?from=&to=` on the analytics endpoints

## SPA Architecture
`ssr = false`, `prerender = false` root layout · no `+page.server.ts` anywhere · auth guard on mount (`$effect` → `goto('/login')`) · session from `$page.data.session` · silent token refresh · `goto()` for navigation · fetch pattern: `$effect` with loading/error/`finally`, reactive to page/sort/filter params.

## RBAC-Gated UI
`let canX = $derived(session?.permissions.includes('entity.action') ?? false)` — hide/disable unauthorized controls proactively; never rely only on backend 403.

## University Management (Section 39 + ADR-063)
Three admin entity surfaces, all with full DataTable spec + Gate 2 RBAC CRUD:

### Universities (Section 39 — space type `university`)
- **List:** `GET /api/v1/admin/universities` — filterable by country, ranking, tuition range; sortable; paginated. DataTable with all spec features.
- **Create/Edit:** `POST/PATCH /api/v1/admin/universities` — all standard Space fields + `university_fields` custom fields (incl. logo + feature_image upload via Section 34 media). The logo doubles as the university page's profile image.
- **Delete:** `DELETE /api/v1/admin/universities/:id` (soft delete).
- **Verify:** `POST /api/v1/admin/universities/:id/verify` — mark as officially verified (state action, conditional on row state).
- **Bulk import:** CSV upload with field mapping for large-scale population. Maps to a bulk endpoint.
- **Status:** published / draft / archived (state actions for each transition).

### Instructor Profiles (ADR-063 — creator economy)
- **List:** `GET /api/v1/admin/instructors` — filterable by `status` (pending/approved/rejected/suspended), `tier` (standard/verified/partner); sortable; paginated.
- **Review applications:** pending instructors have a review action → opens `<Dialog.Root>` with identity, content samples, approve/reject buttons.
- **State transitions (BOTH directions):** `POST /:id/approve` AND `/:id/reject`, `/:id/suspend` AND `/:id/unsuspend` — all conditional on current state.
- **Tier management:** `PATCH /:id` to set `tier` and optional `commission_pct_override`.
- **KYC review:** `kyc_status` visible in detail view; sensitive `payout_method` (jsonb) masked in UI, never shown raw.

### University Course Approval (ADR-063)
- **List:** `GET /api/v1/admin/academy/tracks` — filterable by `is_published_to_academy` status, instructor, category; sortable; paginated.
- **Approve/Reject:** `POST /:id/approve` AND `/:id/reject` — approve sets `is_published_to_academy = true` and enqueues `academy:notify_course_approved`. Both directions required.
- **Payout management:** `GET /api/v1/admin/academy/payouts` — list `academy_instructor_payouts` by period/status; `POST /:id/process` to trigger `academy:send_instructor_payout`; `POST /:id/mark-failed` for failed transfers. State: pending → processing → paid / failed.

## Stack & Design
Same base stack as all JC apps (Svelte 5 Runes, Bits UI dot-notation, Tailwind v4, TypeScript, Lucide, `$t()` i18n, no AI attribution). Sidebar `#1C1B22`, content `#F7F7F7`/dark, accent `#3B49DF`, success/danger/warning tokens, 14px compact density, `[data-theme="dark"]`.

## Deliverables Per Task
1. Gate 1 + Gate 2 output (routes verified) · 2. `+page.svelte` with full-spec DataTable or LayerChart dashboard · 3. CRUD form dialogs · 4. types · 5. confirmation of every `/api/v1/admin/*` route used
**V2 admin phases (20–27):** Persona Management + Content Studio (Phase 20) → Newsletter + Jobs (Phase 21) → Gamification/Analytics/Commerce (Phase 22) → QA (Phase 23) → Community Features Admin (Phase 24) → Tools Admin + HITL Queues (Phase 25) → QA Update (Phase 26) → Mentorship Admin (Phase 27). See `ROADMAP-ADMIN.md` for task breakdown.

**New admin surfaces in v2:** AI Persona management (`/admin/personas`), Content Studio (`/admin/studio`), Participation queue (tab in moderation queue), RAG index status widget, Remittance provider management, Newsletter composer, Gamification badge/challenge CRUD, Advanced analytics dashboard.

**V2 community features admin (Phase 24, §§79–89, §98):** Story verification (§79), wiki revision approval (§80), scam alert moderation (§81), planning group management (§82), visa timeline admin (§83), digest generation/publish (§84), mutual aid moderation (§85), calendar review (§86), japa stage profiles (§87), AMA moderation (§88), achievement management (§89), service directory verification/claim review (§98). All admin-managed content tables must carry ADR-088 AI generation columns (ai_generated, ai_model, hitl_reviewed_by, ai_generated_at) with mandatory HITL review before publish. Admin list endpoints must filter + sort + paginate (no infinite scroll).

**V2 functional tools admin (Phase 25, §§90–97, §§99–101):** Visa route management (§90), embassy polling configuration (§91), arrival checklist approval (§92), processing time tracker (§93), credential checker management (§94), CV formatter standards (§95), housing guide management (§96), attestation approval (§97), language test requirements (§99), tax guide/treaty management (§100), community locator review (§101). All tools follow the geo-aware tool pattern — destination country is the primary data axis, no hardcoded nationality, ?dest= filter on list endpoints.

**V2 mentorship admin (Phase 27, §102, ADR-110):** Mentorship connection management, mentor profile review. Verify active_mentee_count is maintained by PostgreSQL trigger (trg_mentee_count), not computed at query time. Match scoring is 60% keyword overlap + 40% pgvector cosine similarity.

## V2 (JEOS v1.23.1) Development Notes — New Admin DataTable Pages
New admin DataTable pages required for §§79–102 (Phases 24–27). Each page follows the mandatory DataTable spec + Gate 1 + Gate 2. ~819 routes total (~475 v1 + ~344 v2), 297 RBAC nodes, 18 Golden Rules — verify all v2 admin routes against `api-routes-catalog.md` before implementation.

### Community Features Admin Pages (Phase 24, §§79–89, §98)
Each page is a full-spec DataTable with CRUD + state actions per Gate 2:
- **Story Wall verification** (`/admin/stories`): list pending stories, verify/reject, filter by `ai_generated` flag. ADR-088 columns required on stories table.
- **Destination Wiki revision approval** (`/admin/wiki/revisions`): list pending revisions, approve/reject with diff view. ADR-088 columns required.
- **Scam Alert Board moderation** (`/admin/scam-alerts`): list reported scams, verify/remove, filter by severity + destination. ADR-088 columns required.
- **Planning Group management** (`/admin/planning-groups`): CRUD + member management, filter by destination country.
- **Visa Timeline admin** (`/admin/visa-timelines`): CRUD + timeline entry moderation, filter by destination.
- **Digest generation/publish** (`/admin/digests`): list generated digests, HITL review before publish, filter by status. ADR-088 columns required.
- **Mutual Aid moderation** (`/admin/mutual-aid`): list aid requests/offers, approve/remove, filter by destination + status.
- **Community Calendar review** (`/admin/calendar`): list events, approve/reject, filter by destination + date range.
- **Japa Stage profiles** (`/admin/japa-stage`): CRUD + profile moderation, filter by stage + destination.
- **AMA moderation** (`/admin/amas`): list AMAs, approve/reject, manage questions. ADR-088 columns required.
- **Achievement management** (`/admin/achievements`): CRUD badges/achievements, filter by type.
- **Service Directory verification/claim review** (`/admin/services`): list services, verify/unverify, review ownership claims, filter by destination + status. ADR-088 columns required.

### Functional Tools Admin Pages (Phase 25, §§90–97, §§99–101)
Each page follows the geo-aware tool pattern — `?dest=` filter on list endpoints, destination country as primary data axis:
- **Visa Route management** (`/admin/visa-routes`): CRUD + comparison config, `?dest=` filter.
- **Embassy polling configuration** (`/admin/embassy-alerts`): CRUD polling targets, filter by destination.
- **Arrival Checklist approval** (`/admin/arrival-checklists`): list + approve/reject checklists, `?dest=` filter. ADR-088 columns required.
- **Processing Time Tracker** (`/admin/processing-times`): CRUD processing time data, `?dest=` filter.
- **Credential Checker management** (`/admin/credential-checker`): CRUD credential requirements, `?dest=` filter.
- **CV Formatter standards** (`/admin/cv-formatter`): CRUD template standards, filter by destination.
- **Housing Guide management** (`/admin/housing-guides`): CRUD guides, `?dest=` filter. ADR-088 columns required.
- **Attestation approval** (`/admin/attestations`): list + approve/reject attestation guides, `?dest=` filter. ADR-088 columns required.
- **Language Test requirements** (`/admin/language-tests`): CRUD test requirements, `?dest=` filter.
- **Tax Guide/treaty management** (`/admin/tax-guides`): CRUD tax guides + treaty data, `?dest=` filter. ADR-088 columns required.
- **Community Locator review** (`/admin/community-locator`): list + review/verify entries, `?dest=` filter.

### Mentorship Admin Page (Phase 27, §102, ADR-110)
- **Mentorship connection management** (`/admin/mentorship`): list connections, manage mentor profiles, filter by status + destination. Verify `active_mentee_count` is trigger-maintained (trg_mentee_count) — do NOT compute at query time in the admin list endpoint.

### Cross-Cutting Development Notes
- **ADR-088 AI generation columns:** Every admin content table for §§79–101 that can contain AI-generated content must have `ai_generated` (bool), `ai_model` (text), `hitl_reviewed_by` (text/uuid), `ai_generated_at` (timestamptz). The admin create/edit form must surface a HITL review step before publish — the publish/approve action must populate `hitl_reviewed_by` with the admin user's ID.
- **Geo-aware tool pattern:** All §§90–97, §§99–101 admin list endpoints must accept `?dest=` as a filter param. No hardcoded nationality anywhere — the destination country is the primary data axis. The DataTable filter panel must include a destination country dropdown.
- **Feature-flag middleware (ADR-042):** Disabled features return 404, not 403. Admin pages should handle 404 gracefully (feature disabled message, not a permission error).
- **Admin list pagination:** All v2 admin list endpoints must support `?page=&limit=&sort=&filter=` and return `meta` with pagination data. No infinite scroll — use the standard DataTable pagination with page-size selector (25/50/100).

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
