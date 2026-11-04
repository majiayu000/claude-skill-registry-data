---
name: jc-main-audit
description: Use when performing a comprehensive quality audit of the JapaConnect Main App (apps/main) before merge or release. Covers Rule 16, Svelte 5, Bits UI, app-shell/layout compliance (ADR-058), profile learning hub and cross-app compliance (ADR-060), LayerChart 2.0.1, SSR/SEO, security, accessibility, and i18n.
---

# JapaConnect Main App — Audit Skill

Work file-by-file. Produce the structured report at the end. Conventions reference: `jc-main-develop`.

## A. API Consumption Verification (Run First)
For every `fetch()` and `load()` call found:
1. Extract the route · 2. Confirm it exists in JEOS `api-routes-catalog.md` or via live probe · 3. Any route the frontend calls that the backend doesn't serve → **Critical** finding with the ⚠️ MISSING BACKEND API ROUTES block listing them all.

## B. Architectural Compliance (per route file)
`load()` fetches from `/api/v1/*` (no static data) · no `any` types · `$props()`/`$derived()`/`$effect()` only · `onclick` not `on:click` · auth from `$page.data.session` · dark mode via `[data-theme]` · all strings `$t()`

## C. Rule 16
Flag every hardcoded array rendered to UI (nav, countries, tags, groups, post types, **chart datasets**) with file · line · violation · fix.

## D. Bits UI Compliance
All dropdowns/modals/selects/tooltips/accordions/tabs are Bits UI primitives · no manual `role`/`aria-*` on primitives · `<Dialog.Content>` inside `<Dialog.Portal>`.

## E. LayerChart Compliance
- Every chart on analytics/dashboard pages uses LayerChart, pinned `layerchart@2.0.1` — flag any Chart.js, raw D3 DOM, canvas, hand-rolled SVG, or unpinned/`@next` version
- Chart colors exclusively `var(--chart-*)`/`var(--color-*)` (verify dark-mode rendering)
- Fixed-height container wraps every chart; per-chart skeleton present; data from API with dates converted to `Date`

## E2. App Shell & Layout Compliance (ADR-058)
- Every surface renders inside `AppShell` (three-column shell) — flag any top-nav-bar or bespoke layout that isn't one of the three exceptions (blog/CPT single, `/create`, guest homepage)
- `FeedCard` is one variant-driven component (type pill + props) — flag per-content-type card forks
- Nav-collapse persisted via `ui.nav_collapsed` (not localStorage); account dropdown on the right-sidebar avatar; Space switcher in the left nav
- Blog/CPT single: transparent `ReactionRail` + `CreatorCard` (not the search/avatar bar). `/create`: tabbed `[ Guide | Settings/SEO ]` with dynamic Guide. Guest `/`: Page Builder landing; authenticated `/`: Primary timeline
- Discover uses existing `/suggestions/*` (no invented backend route)

## E3. Profile Learning Hub & Cross-App (ADR-060)
- Dashboard hub tabs present and API-sourced: `/dashboard/learning` (`me/enrollments`), `/dashboard/certificates` (`me/certificates`), `/dashboard/knowledge-base` (docs + bookmarks) — flag any hardcoded lists
- No Learn/Docs surface re-implemented in this app (lesson player, curriculum rail, docs nav tree belong to `jc-learn-*` / `jc-docs-*`)
- Cross-app links use absolute subdomain URLs (`academy.japa.to`, `docs.japa.to`)
- Certificate cards link to the public shareable page `/certificates/:id`; earned certificates badge the public profile
- Dashboard is private: no ad slots, not indexed

## E4. Geo-Aware Personalization (ADR-064)
- Feed header shows inline "Showing: [Country] · Change" control — NOT buried in settings; wired to `PATCH /api/v1/me/profile` (`content_country_preference`) with feed invalidation
- Guest homepage geo content is SSR (no client flicker); degrades gracefully when `GeoContext` absent
- `?geo=` is a re-weight/boost, never a hard filter — non-local content must still appear (flag any hard exclusion)
- University discovery (`/universities`) defaults country filter from `ContentCountry`; explicit filter always wins
- No hardcoded country/region lists driving geo behavior — all from `GET /api/v1/geo/me` or API params

## E5. University Discovery (Section 39)
- `/universities` and `/universities/[slug]` render inside `AppShell` (NOT exceptions, NOT standalone layouts)
- All university data from `GET /api/v1/universities` / `GET /api/v1/universities/:slug` — no hardcoded university data (Rule 16)
- Single university page tabs: Overview/Posts/Forums/Courses/Members/Reviews/Compare — all API-sourced
- JSON-LD: `ItemList` of `EducationalOrganization` on list, `EducationalOrganization` + `AggregateRating` on single
- University logo served as profile image via Section 34 media + imgproxy (not a hardcoded URL)

## F. SSR & SEO
Indexable routes render content in server HTML · `<svelte:head>` with title/description on every indexable route · JSON-LD: Article (blog), QAPage (solved threads), Person/Organization (profiles) · images lazy · `data-sveltekit-preload-data="hover"` on body.

## G. Security
CSRF token on all mutations · `{@html}` only for TipTap-rendered backend content — flag all other instances as XSS risk · auth-required routes guarded server AND client side · no secrets in client code or `PUBLIC_JC_*`.

## H. Accessibility (WCAG 2.1 AA)
Meaningful `alt` · labeled buttons/links · logical focus order, no `tabindex>0` · visible focus rings · 4.5:1 contrast · no interactive `<div>` without role+keyboard handler.

## I. i18n
List hardcoded strings not in `$t()` · flag keys in `en.json` missing from `fr.json`.

## Report Format
```
## Audit Report — Main App (apps/main)
**Files Audited:** [n] · **Status:** PASS / NEEDS FIXES
### Critical (block merge) / High (this sprint) / Medium (before v1.0) / Low
[lists]
### Compliance Summary
| Category | Status |
| API routes verified | ✅/❌ |
| Rule 16 | ✅/❌ |
| Svelte 5 Runes | ✅/❌ |
| Bits UI | ✅/❌ |
| App Shell / Layout (ADR-058) | ✅/❌ |
| Profile hub / Cross-app (ADR-060) | ✅/❌ |
| Geo-aware personalization (ADR-064) | ✅/❌ |
| University discovery (§39) | ✅/❌ |
| LayerChart | ✅/❌ |
| SSR/SEO | ✅/❌ |
| Security | ✅/❌ |
| Accessibility | ✅/❌ |
| i18n | ✅/❌ |
```
**V2 main app phases (33–38):** Identity Tools UI (Phase 33) → Jobs/Gamification/Referral (Phase 34) → Newsletter/Import/Travel (Phase 35) → QA (Phase 36) → Community Features UI (Phase 37) → Mentorship Matching UI (Phase 38). See `ROADMAP-MAIN.md` for task breakdown.

**V2 community features UI (Phase 37, §§79–89, §98):** Community Story Wall (§79 — filterable testimonials by origin/destination/visa/profession), Destination Wiki (§80 — collaborative versioned KB pages with reputation-gated editing), Scam Alert Board (§81 — moderated scam reporting with subscriptions), Japa Planning Groups (§82 — private peer groups with milestones and check-ins), Visa Timeline Tracker (§83 — personal milestone logging with anonymous sharing), Community Digest Widget (§84 — auto-generated digest), Mutual Aid Board (§85 — Needs/Offers/Skill Swaps), Community Calendar (§86 — institutional dates calendar), Japa Stage Profiles (§87 — seven-stage relocation journey on profiles), Ask-an-Expat AMA (§88 — specialized forum AMA threads), Achievement Feed (§89 — opt-in milestone feed), Service Directory (§98 — geo-indexed business directory). All community feature pages must follow the geo-aware tool pattern: destination country selector is the first input, no hardcoded nationality, ?dest= filter on list endpoints.

**V2 mentorship UI (Phase 38, §102, ADR-110):** Mentor browsing/search, mentor profile pages, mentorship request flow, incoming/outgoing requests management, connection active/complete/cancel flows. Match scoring display (60% keyword overlap + 40% pgvector cosine similarity). DM auto-open on connection accept (§48).

**V2 tool pages on main app (`/tools/*`):** Visa Checklist, Readiness Assessment, Cost of Living, Scholarship Finder, Remittance Rate Tracker, JapaBot (full-page). Each tool is also available at its own domain/subdomain via `apps/tools` (§78) — the main app renders these within the community layout; `apps/tools` renders them tool-first without community nav.

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

## E6. V2 Community Features & Mentorship (Phases 37–38, §§79–102, ADRs 087–110)

### Geo-Aware Tool Pattern Compliance (all §§79–101 pages)
- **Destination selector first:** every community feature page (Story Wall, Destination Wiki, Scam Alert Board, Planning Groups, Visa Timeline, Digest Widget, Mutual Aid, Community Calendar, Japa Stage, AMA, Achievement Feed, Service Directory) must have the destination country selector as the **first input** — before any other filter or content. Flag if a secondary filter appears before the destination selector.
- **`?dest=` filter on list endpoints:** all community feature list pages must pass `?dest=` to their API list endpoints as the primary filter axis. Flag any list endpoint call missing `?dest=` or using a different param name.
- **No hardcoded nationality:** flag any hardcoded nationality string, array, or constant in community feature pages. The destination country is the primary axis — origin nationality is a secondary filter only where applicable (e.g. Story Wall §79). Nationality lists must come from `GET /api/v1/geo/countries`, never inline.
- **Destination selector populated from API:** the destination selector options must come from `GET /api/v1/geo/countries` (or equivalent API), not a hardcoded array — Rule 16 violation if hardcoded.

### ADR-088 HITL Review Gate on AI-Generated Community Content
- Any AI-generated content on community feature pages (wiki summaries, digest text, scam alert summaries, etc.) must pass through a Human-In-The-Loop review before publish. Flag any AI-generated content that is published directly without a review state.
- The UI must show a "Pending Review" state for AI-generated content and provide a review/approve/reject flow for moderators. Flag if the review flow is missing or bypassable.
- Flag any code path that sets AI-generated content to "published" status without going through the HITL gate.

### Rule 16 Compliance on Community Feature Pages
- Flag every hardcoded array rendered to UI on community feature pages (destination lists, story categories, scam types, milestone templates, calendar event types, service categories, AMA topics) with file · line · violation · fix.
- All community feature data must come from `/api/v1/community/*` endpoints — no static data in `load()` or component-level constants.

### Svelte 5 Runes Compliance on New Pages
- All new community feature and mentorship components must use Svelte 5 strict Runes: `$state`, `$derived`, `$props`, `$effect` only. Flag `export let`, `$:`, `on:click`, `createEventDispatcher`, or any Svelte 4 pattern.
- Flag writable stores used for local UI state in new components — should be `$state()`.

### ADR-058 Shell Compliance on New Pages
- All community feature pages and mentorship pages must render inside `AppShell` (three-column shell). They are NOT exceptions. Flag any standalone layout or top-nav-bar pattern.
- `FeedCard` must be the one variant-driven component for story cards, achievement cards, mutual aid listings — flag per-type card forks.
- Nav-collapse persisted via `ui.nav_collapsed` (not localStorage) on all new pages.

### Mentorship-Specific (Phase 38, §102, ADR-110)
- Mentor browsing/search page has destination country as first filter; `?dest=` passed to mentor list endpoint.
- Match score display present where applicable (60% keyword overlap + 40% pgvector cosine similarity) — flag if score is hardcoded or not from API.
- Mentorship request flow uses Bits UI `<Dialog.Root>`; CSRF token on the `POST` mutation.
- Requests management page has Incoming/Outgoing tabs (Bits UI `<Tabs.Root>`); Accept/Decline/Cancel/Complete actions are `PATCH` calls.
- **DM auto-open on accept (§48):** when a mentorship request is accepted, the UI must automatically open the DM thread. Flag if the accept handler does not trigger DM navigation/modal open.

### Compliance Summary Additions
Add these rows to the report's compliance summary table:
```
|| V2 community features (§§79–101) | ✅/❌ |
|| V2 mentorship (§102, ADR-110) | ✅/❌ |
|| Geo-aware tool pattern | ✅/❌ |
|| ADR-088 HITL review gate | ✅/❌ |
```
