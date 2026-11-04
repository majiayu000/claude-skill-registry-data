---
name: jc-main-refactor
description: Use when updating, modernizing, or refactoring existing JapaConnect Main App code (apps/main). Migrates Svelte 4 to Svelte 5 Runes, adopts Bits UI primitives, migrates legacy layouts to the unified app shell (ADR-058), consolidates the profile learning hub and cross-app links (ADR-060), converts charts to LayerChart 2.0.1, removes hardcoded data per Rule 16.
---

# JapaConnect Main App — Updating & Refactoring Skill

Apply conventions from `jc-main-develop`. Do not change behavior — modernize implementation only. One-line comment per change.

## 0. API-Readiness Gate
If a refactor requires an endpoint that doesn't exist (e.g. replacing hardcoded data with an API call), verify the route first. Missing → output the ⚠️ alert and pause.

## 1. Svelte 4 → 5 Migration
`export let` → `$props()` · `$:` → `$derived()` · reactive side-effect blocks → `$effect()` · `createEventDispatcher` → callback props · writable stores for local UI state → `$state()` · `on:event` → `onevent`

## 2. Bits UI Adoption
| Manual pattern | Replace with |
|---|---|
| Custom dropdown `<ul>` toggle | `<DropdownMenu.Root>` |
| Custom modal + focus trap | `<Dialog.Root>` |
| Raw `<select>` | `<Select.Root>` / searchable `<Combobox.Root>` |
| CSS hover tooltip | `<Tooltip.Root>` |
| Manual accordion / tabs / popover | `<Accordion.Root>` / `<Tabs.Root>` / `<Popover.Root>` |

## 3. Chart Migration → LayerChart 2.0.1
Any chart built with Chart.js, D3 direct DOM, canvas, inline SVG math, or any other library **must** be rewritten in LayerChart (pinned `layerchart@2.0.1`, prefer high-level compound charts):

```svelte
<!-- BEFORE: Chart.js canvas, manual lifecycle, breaks SSR -->
<canvas bind:this={el}></canvas>

<!-- AFTER: LayerChart v2 compound chart, declarative, SSR-safe -->
<div class="h-64 w-full">
  <AreaChart {data} x="date" y="count"
    props={{ area: { class: 'fill-[var(--chart-1)]/20 stroke-[var(--chart-1)]' } }} tooltip />
</div>
```
Use `AreaChart`/`LineChart`/`BarChart` for the mapped dashboard widgets (ADR-059); drop to the low-level `<Chart><Svg>…</Svg></Chart>` only when a compound chart can't express it. Convert API date strings to `Date` objects · colors via `var(--chart-*)`/`var(--color-*)` only · add skeleton state · pin `layerchart@2.0.1` and remove the old chart library from package.json if unused.

## 3b. Legacy Layout → Unified App Shell (ADR-058)
Migrate pre-shell layouts to the single three-column shell:
- Replace any top-nav-bar layout / bespoke per-page layout with `AppShell` (`LeftNav` + center + `RightSidebar`) — except the three exceptions (blog/CPT single, `/create`, guest homepage).
- Collapse a per-content-type `FeedCard` (separate components or big `{#if content_type}` layout branches) into one variant-driven `FeedCard` with a content-type pill + additive props.
- Move nav-collapse state from `localStorage` to `ui.nav_collapsed` (`PATCH /api/v1/me/account`); move the account dropdown to the right-sidebar avatar; keep the Space switcher in the left nav.
- Blog/CPT single: make the reaction rail borderless/transparent (`ReactionRail`); replace the search/avatar bar with `CreatorCard`.
- `/create`: convert the settings drawer into the tabbed `[ Guide | Settings/SEO ]` panel with the dynamic field-focus Guide.
- Guest `/`: render the Page Builder landing (fallback `/explore`); keep authenticated `/` on the Primary timeline.

## 4. Rule 16 — Hardcoded Data Removal
Replace static arrays (nav, countries, tags, groups, post types, chart datasets) with API fetches. Verify the endpoint exists first (Gate 0).

## 5b. Profile Learning Hub & Cross-App (ADR-060)
- Replace hardcoded certificate/enrollment/knowledge-base lists with `GET /api/v1/me/certificates`, `GET /api/v1/me/enrollments`, and the bookmark routes (no new backend needed).
- Extract any Learn/Docs surface re-implemented in this app (lesson player, curriculum rail, docs nav tree) — replace with an absolute deep link to `academy.japa.to` / `docs.japa.to`; those apps own those surfaces.
- Consolidate scattered learning links into the dashboard hub tabs: `/dashboard/learning`, `/dashboard/certificates`, `/dashboard/knowledge-base`.
- Point certificate cards at the public shareable page `/certificates/:id`; add earned-certificate badges to the public profile.

## 5c. Geo-Aware Personalization (ADR-064) & University Discovery (Section 39)
- **Hardcoded geo → VisitorContext:** any hardcoded country/region list or `?geo=` default → consume `GET /api/v1/geo/me` for `ContentCountry`. The feed header gets an inline "Showing: [Country] · Change" control wired to `PATCH /api/v1/me/profile` (`content_country_preference`).
- **Client-side geo flicker → SSR:** if the guest homepage loads global content then swaps to geo client-side, move the geo-weighted fetch into `+page.server.ts` so it's in the initial HTML.
- **Hard geo filter → re-weight:** if `?geo=` is used to exclude non-local content, change to a boost/optional-filter (ADR-064: re-weight, never hide).
- **University pages → shell + API:** any standalone-layout university page → migrate into `AppShell`; any hardcoded university data → `GET /api/v1/universities` / `GET /api/v1/universities/:slug`. Add JSON-LD `EducationalOrganization` + `AggregateRating`.
- **University discovery:** add `/universities` (grid, filters from API, geo-aware default country) and `/universities/[slug]` (tabs: Overview/Posts/Forums/Courses/Members/Reviews/Compare) if not present.

## 6. Standard Patterns
- Skeletons: `{#if loading}<Skeleton/>{:else if error}<ErrorState/>{:else if empty}<EmptyState/>{:else}...{/if}` — skeleton shape matches real content
- Optimistic UI with rollback for reactions/bookmarks/follows
- Tailwind v4: remove `@apply`, `theme()`, `dark:` variant
- i18n sweep: hardcoded strings → `$t()`, keys in `en.json` + `fr.json`
- A11y: `<div onclick>` → `<button>`, `aria-label` on icon buttons, `alt` on images, visible focus rings
- Types: eliminate `any`, derive from API response types
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

## 5d. V2 Community Features & Mentorship — Refactoring Notes (Phases 37–38, §§79–102)

### Apply Geo-Aware Tool Pattern to Existing Pages That Hardcode Nationalities
- **Identify:** grep for hardcoded nationality strings, country code arrays, or `?nationality=` params in existing pages (especially pre-v2 community surfaces, forum filters, profile filters, or any page that filters by origin country). Any inline `const countries = [...]` or hardcoded `"Nigerian"` / `"Ghanaian"` labels are candidates.
- **Refactor:** replace hardcoded nationality arrays with `GET /api/v1/geo/countries` fetched in `load()`. Replace `?nationality=` params with `?dest=` as the primary filter axis. Add a destination country selector as the first input on the page (Bits UI `<Select.Root>` or `<Combobox.Root>`).
- **Origin as secondary:** where origin filtering is still needed (e.g. Story Wall §79), keep it as a secondary filter — but destination country is always first and primary.
- **Pre-select from preference:** if the user has `content_country_preference` (ADR-064), pre-select the destination selector to that value; explicit selection always wins.

### Ensure New Community Feature Pages Use Svelte 5 Runes (Not Svelte 4 Patterns)
- **Identify:** audit all files under `$lib/components/community/` and `/community/*` routes for Svelte 4 patterns: `export let`, `$:` reactive statements, `on:click`, `createEventDispatcher`, writable stores for local UI state.
- **Refactor:** apply the Svelte 4 → 5 migration table (Section 1):
  - `export let story` → `let { story } = $props()`
  - `$: filtered = items.filter(...)` → `let filtered = $derived(items.filter(...))`
  - `$: { sideEffect() }` → `$effect(() => { ... })`
  - `on:click={...}` → `onclick={...}`
  - `createEventDispatcher()` → callback props (`onaccept`, `ondecline`, `oncomplete`)
  - `writable(false)` for modal/panel open state → `let open = $state(false)`
- **Verify:** no writable stores for local UI state in new community components — use `$state()`. Shared cross-component state that genuinely needs a store is fine, but local UI state (modal open, selected tab, filter values) should be `$state`.

### Migrate Community Feature Charts to LayerChart 2.0.1
- **Identify:** any chart in community feature pages (Visa Timeline Tracker §83 milestone progress, Planning Groups §82 milestone charts, Achievement Feed §89 stats, Service Directory §98 analytics) built with Chart.js, raw D3, canvas, inline SVG, or any non-LayerChart library.
- **Refactor:** rewrite in LayerChart (pinned `layerchart@2.0.1`, prefer high-level compound charts):
  - Milestone progress over time → `LineChart` or `AreaChart`
  - Achievement stats breakdown → horizontal `BarChart`
  - Service Directory category distribution → horizontal `BarChart`
  - Planning Group participation trends → `AreaChart`
- **Rules:** colors via `var(--chart-*)`/`var(--color-*)` only (dark-mode safe) · data from API (Rule 16) · fixed-height container · per-chart skeleton · convert API date strings to `Date` objects · remove old chart library from `package.json` if unused after migration.
- **Do not confuse** LayerChart's `<Tooltip.Root>` with Bits UI's `<Tooltip.Root>` — check the import source.
