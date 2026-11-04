---
name: jc-main-debug
description: Use when reviewing or debugging code in the JapaConnect Main App (apps/main, SSR). Diagnoses SSR/hydration mismatches, Svelte 5 Runes violations, Bits UI lifecycle errors, app-shell/layout drift (ADR-058), profile learning hub and cross-app link defects (ADR-060), LayerChart rendering issues, and Rule 16 violations.
---

# JapaConnect Main App — Review & Debugging Skill

Apply the stack conventions from `jc-main-develop`. Run every check in order.

## 0. API-Readiness Check First
If the bug involves data not loading: verify the endpoint actually exists (`curl` the route) **before** debugging frontend code. If the route is missing, output the ⚠️ MISSING BACKEND API ROUTES alert (format in `jc-main-develop`) and pause.

## 1. SSR / Hydration
- `window`/`document`/`navigator` access without `if (browser)` guard from `$app/environment`
- Bits UI primitives instantiated server-side without guard
- `load()` data diverging between server and client render → hydration mismatch
- `jc_theme` cookie read in root layout **before first paint** (else theme flash)
- Auth from `$page.data.session` — never localStorage

## 2. Svelte 5 Runes Violations
| Forbidden | Correct |
|---|---|
| `export let foo` | `let { foo } = $props()` |
| `$: d = x * 2` | `let d = $derived(x * 2)` |
| `$: { sideEffect() }` | `$effect(() => { ... })` |
| `on:click` | `onclick` |
| `createEventDispatcher()` | callback props |

## 3. Bits UI Errors
- v1 single-component API (`<Select>`) instead of dot-notation (`<Select.Root>`)
- `e.stopPropagation()` on `<DropdownMenu.Trigger>` — breaks dismiss logic
- `<Dialog.Content>` outside `<Dialog.Portal>` — breaks stacking/focus trap
- Manual `role`/`aria-*` on primitives — remove, Bits UI manages ARIA
- `bind:value` on Trigger instead of Root · plain `<Select>` where searchable `<Combobox.Root>` is needed

## 4. LayerChart Issues
- Chart rendered without fixed-height container → collapses to 0px
- Hardcoded hex colors in chart classes → breaks dark mode; must use `var(--chart-*)`/`var(--color-*)`
- Chart data hardcoded → Rule 16 violation
- Wrong version: must be pinned `layerchart@2.0.1` (Svelte 5). Low-level `<Chart>` needs scales from `d3-scale`; high-level `AreaChart`/`LineChart`/`BarChart` do not (d3-scale is bundled)
- Date strings from API not converted to `Date` objects before passing to a time axis
- Missing skeleton state while chart data loads
- `<Tooltip.Root>` (LayerChart's) confused with Bits UI `<Tooltip.Root>` — check import source

## 4b. App Shell & Layout Drift (ADR-058)
- A surface built as a standalone layout or with a top-nav bar instead of rendering inside `AppShell` (three-column shell) — flag unless it is one of the three exceptions (blog/CPT single, `/create`, guest homepage)
- `FeedCard` forked per content type (separate components / large `{#if content_type}` layout branches) instead of one variant-driven component with a type pill
- Left-nav collapse state read/written to `localStorage` instead of `ui.nav_collapsed` via `PATCH /api/v1/me/account`
- Account dropdown placed in the left nav (should anchor to the right-sidebar avatar); Space switcher moved out of the left nav
- Blog/CPT single: `ReactionRail` boxed/bordered so it looks like a second nav (must be transparent, part of the article); search/avatar bar shown instead of `CreatorCard`
- `/create`: right panel is a plain settings drawer instead of the tabbed `[ Guide | Settings/SEO ]`; missing dynamic field-focus Guide
- Guest `/` rendering the app shell instead of the Page Builder landing (or authenticated `/` not showing the Primary timeline)

## 5. Rule 16 Violations
- Hardcoded arrays for nav, tags, spaces, countries, post types, chart data
- `load()` returning static data · mutations updating only local `$state`
- Optimistic updates without rollback on API failure

## 6. Tailwind v4
- `@apply` in `<style>` → inline utilities · `theme()` → `var(--color-*)` · `dark:` variant → `[data-theme="dark"]`

## 7. SEO & A11y
- Indexable routes need `<svelte:head>` title/description/OG + JSON-LD (Article/QAPage/Person/Organization)
- Images: `loading="lazy" decoding="async"` · icon buttons: `aria-label` · `<div onclick>` → `<button>` · focus rings visible

## 7b. Profile Learning Hub & Cross-App (ADR-060)
- Certificates, enrollments, or knowledge-base lists hardcoded instead of fetched from `GET /api/v1/me/certificates` / `GET /api/v1/me/enrollments` (Rule 16 violation)
- Learn or Docs surfaces **re-implemented inside the main app** (a lesson player, curriculum rail, or docs nav tree built here) — those belong to the `jc-learn-*` / `jc-docs-*` apps; the main app links out by absolute subdomain URL
- Cross-app links hardcoded to a wrong/relative path instead of `academy.japa.to` / `docs.japa.to` (breaks the shared-session deep link)
- Certificate cards not linking to the public shareable page `/certificates/:id`; earned certificates missing as badges on the public profile
- Dashboard treated as a public surface — it is private: no ad slots, and it must not be indexed

## 7c. Geo-Aware Personalization (ADR-064)
- **Guest homepage geo flicker:** geo-weighted content must be in the SSR HTML, not loaded client-side — if the page flashes global content then swaps to geo, the SSR path is broken
- **Feed override control missing:** the feed header must show "Showing: [Country] · Change" inline — if it's buried in settings or absent, that's a defect
- **Hard geo filtering:** content hidden by geo (non-local posts not appearing at all) instead of re-weighted — ADR-064 says re-weight, never hide. Check the `?geo=` param isn't being used as a hard filter
- **Override not respected:** user changes `content_country_preference` but feed doesn't update — check that the feed invalidation fires after `PATCH /api/v1/me/profile`
- **University discovery hardcoded:** `/universities` list or `/universities/[slug]` data hardcoded instead of from `GET /api/v1/universities` — Rule 16 violation
- **University page outside the shell:** `/universities` or `/universities/[slug]` built as a standalone layout — they render INSIDE `AppShell`, they are NOT exceptions

## Output Protocol
1. **Root cause** — one sentence · 2. **Broken code** · 3. **Fixed code** (surgical, minimal) · 4. **Secondary findings**
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

## 7d. V2 Community Features — Debug Patterns (Phase 37, §§79–89, §98)

### Geo-Aware Filter Missing on Community Feature Pages
- **Symptom:** community feature list page (Story Wall, Scam Alert Board, Mutual Aid, Service Directory, etc.) shows all results regardless of destination, or the `?dest=` param is not sent to the API.
- **Check:** the `load()` function in `+page.server.ts` — does it read `$page.url.searchParams.get('dest')` and pass it as `?dest=` to the API list endpoint? If the param is read but not forwarded, the API returns unfiltered results.
- **Check:** the destination selector component — does it update the URL with `?dest=[value]` on change (via `goto` or `invalidateAll`)? If the selector updates local `$state` but doesn't update the URL, the `load()` won't re-run with the new filter.
- **Fix:** ensure the selector writes `?dest=` to the URL and `load()` forwards it to the API call.

### Hardcoded Nationality in Tool UI
- **Symptom:** a community feature page filters or labels content by a hardcoded nationality (e.g. `"Nigerian"` or a hardcoded country code array) instead of using the destination country selector.
- **Check:** grep for country name strings, ISO codes, or nationality constants in component files under `/community/*` routes. Any inline array like `const countries = ['NG', 'GB', 'US']` is a violation.
- **Fix:** replace with `GET /api/v1/geo/countries` fetch in `load()`; pass the list as props to the selector component.

### Destination Selector Not First Input
- **Symptom:** the destination country selector appears after other filters (e.g. profession, visa type, sort) in the DOM order, or is buried in a "Filters" dropdown instead of being the primary top-level input.
- **Check:** inspect the filter bar component — the destination `<Select.Root>` or `<Combobox.Root>` must be the first element. If it's inside a collapsible "Advanced Filters" panel, that's a violation.
- **Fix:** move the destination selector to the first position in the filter bar, outside any collapsible panel.

### Missing DM Auto-Open on Mentorship Accept
- **Symptom:** user accepts a mentorship request (or their request is accepted), but the DM thread is not opened — the user stays on the requests page and must manually navigate to Messages.
- **Check:** the accept handler in the requests management component — after the `PATCH /api/v1/mentorship/requests/:id` (status: accepted) succeeds, does the code navigate to `/messages?thread=[connection_id]` or open the DM modal? If the handler only updates local `$state` without triggering DM navigation, the auto-open is missing.
- **Fix:** in the accept handler's success path, add `goto('/messages?thread=' + connectionId)` or open the DM modal with the connection thread ID. The connection ID / thread ID should come from the PATCH response.

### Svelte 5 Runes Violations in New Community Feature Components
- **Symptom:** community feature components (Story Wall cards, Wiki editor, Scam Alert form, Planning Group milestone tracker, etc.) use Svelte 4 patterns — `export let`, `$:` reactive statements, `on:click`, `createEventDispatcher`, or writable stores for local UI state.
- **Check:** run the Svelte 5 Runes violation table (Section 2 above) against all files under `$lib/components/community/` and `/community/*` routes.
- **Common violations in new components:**
  - `export let story` in a StoryCard → should be `let { story } = $props()`
  - `$: filtered = stories.filter(...)` → should be `let filtered = $derived(stories.filter(...))`
  - `on:click={() => subscribe()}` → should be `onclick={() => subscribe()}`
  - `createEventDispatcher()` for request actions → should be callback props (`onaccept`, `ondecline`)
  - `writable(false)` for modal open state → should be `let open = $state(false)`
- **Fix:** apply the migration table from Section 1 of this skill.
