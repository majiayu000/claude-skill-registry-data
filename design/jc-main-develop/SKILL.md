---
name: jc-main-develop
description: Use when building new pages or components for the JapaConnect Main App (apps/main, port 3000, SSR). Covers SvelteKit 2 + Svelte 5 Runes + Bits UI + Tailwind v4 + LayerChart 2.0.1, the unified X.com-style app shell (ADR-058) and its three exceptions, the profile learning hub and cross-app links into Learn and Docs (ADR-060), the full visual design language, the API-Readiness Gate, and Rule 16.
---

# JapaConnect Main App — Development Skill

You are building JapaConnect's public-facing community platform. SSR via adapter-node + Bun, port 3000. **The single most important rule for layout: everything renders inside the unified app shell (below). This is the structural ground truth — do not build any surface as a standalone layout except the three documented exceptions.**

## ⛔ API-READINESS GATE — RUN BEFORE ANY IMPLEMENTATION
Before writing a single line for any page or component:
1. **List every API endpoint** the feature will consume (reads + mutations).
2. **Verify each exists** — check the JEOS `api-routes-catalog.md`, or probe the running backend (`curl -s http://localhost:8080/api/v1/...`).
3. **If ANY endpoint is missing or returns 404:** STOP. Do not implement. Do not mock. Do not hardcode placeholder data. Output the alert and wait:

```
⚠️ MISSING BACKEND API ROUTES — implementation paused
Feature: [feature name]
Missing routes:
  - GET  /api/v1/...
Action needed: implement these routes in the Go backend before frontend work continues.
```

Never work around a missing endpoint. Rule 16 (no hardcoded data) makes mocking a violation, not a shortcut.

## Non-Negotiable Stack
- SvelteKit 2.x, adapter-node, Bun runtime · Svelte 5 **strict Runes** (`$state`, `$derived`, `$props`, `$effect`)
- Bits UI (latest stable), dot-notation (`<Dialog.Root>`, `<Select.Trigger>`) for ALL interactive primitives
- Tailwind CSS v4 — utilities via `class`; theme via CSS custom properties; dark mode = `[data-theme="dark"]` from `jc_theme` cookie (never Tailwind `dark:`)
- **LayerChart `2.0.1`** (pinned; `bun add layerchart@2.0.1`) for ALL data visualization · Lucide Svelte icons · TypeScript, zero `any`
- Forbidden: `export let`, `$:`, `on:click`, `createEventDispatcher`, localStorage (auth or UI state), AI attribution in comments/commits

---

# THE APP SHELL — Structural Ground Truth (ADR-058)

The main app is **one shell** with a short, closed list of exceptions. Build every surface inside it. Never revert to a top-nav bar or a per-page bespoke layout.

## Desktop: three columns
```
┌──────────────┬────────────────────────────┬──────────────────────────┐
│  LEFT NAV    │       CENTER COLUMN        │   RIGHT SIDEBAR          │
│  collapsible │  tab bar → sort bar →      │  sticky search + avatar  │
│  260 / 72px  │  scrolling content ~600px  │  then contextual widgets │
│  (fixed)     │                            │  ~350px                  │
└──────────────┴────────────────────────────┴──────────────────────────┘
```
Grid: `grid-template-columns: 260px 1fr 350px` (nav expanded) / `72px 1fr 350px` (collapsed). Below `1280px` hide the right sidebar; below `768px` collapse to a single column + bottom tab bar. Per-route change happens **inside** the center column (tabs) and **inside** the right sidebar (widgets) — never by discarding the shell.

Components: `AppShell.svelte` (grid) wraps `LeftNav.svelte` + center `<slot>` + `RightSidebar.svelte`.

## Left nav — collapsible (Hashnode-style)
- Expanded (~260px): icon + label; Spaces sub-nav visible; full Compose button.
- Collapsed (~72px): icons only; Spaces → icon + hover-flyout; Compose → circular FAB.
- Chevron toggle by the logo. Persist state server-side via `PATCH /api/v1/me/account` under `ui.nav_collapsed` — **never localStorage**. Default expanded desktop / collapsed tablet.
- Items from `GET /api/v1/menus/primary_nav` (RBAC + `visibility`-gated; supports `is_ad_slot` items). Seed order: **Explore · Home · Discover · Notifications · Messages · Profile** — divider — **Spaces (sub-nav) · Forum · Blog · Universities · Compare · [More]** — divider — **Compose** — **avatar + Space switcher** (bottom; Space switcher stays here, not in the account menu).

## Center column
Tab bar at top swaps content per route (Home: Following/For You · Space: Feed/Forum/Members/About · Profile: Posts/Replies/Media/Likes/Spaces · Forum: All/Q&A/Discussions/Solved · Blog: Latest/Featured/Series · Discover: Spaces/People/Organizations/Tags/Universities). Sort bar (Relevant/Latest/Popular/Rising) sits below the tab bar on feed surfaces, `position: sticky; top: var(--nav-height)`.

**`FeedCard` is ONE variant-driven component** — never a different card per content type. Identical base for every type: avatar, name, Space badge, timestamp, **content-type pill**, preview (title+excerpt or text), engagement bar. Type extras are additive props (`showVoteRail`, `showFeatureImage`), not layout forks. Native ad slots (`feed_native_*`) and inline form embeds render as cards inside the stream.

## Right sidebar
Sticky top bar: global search input + **user avatar at far right** (→ account dropdown). Below: route-aware widgets — global defaults (trending tags, suggested spaces, `sidebar_top` ad, optional form embed) + per-route overlays via a `sidebar` slot.

## Mobile (≤768px)
Single column. Left nav → hamburger (top-left). Right sidebar hidden (widgets via "More info" affordance). Bottom tab bar: **Home · Spaces · Compose · Notifications · Profile**. Compose opens the modal composer.

## Compose flow
Compose button/tab → `ComposeModal.svelte` with a content-type selector. Discussion-type posts compose inline in the modal; blog/CPT route to `/create`. `/forum/[category]/new` remains for full-page new threads.

---

# THE THREE EXCEPTIONS (only these break the shell)

### 1. Blog single (`/blog/[slug]`) & CPT singles — dev.to reading layout
- Left nav auto-collapses to 72px.
- `ReactionRail.svelte`: a **borderless, transparent** vertical strip in the article's LEFT margin (react + count, bookmark, comment count, share). It belongs to the article — must read as distinct from the bordered 72px nav, separated by a clear gap. Do NOT box it or make it look like a second nav.
- Center: article (cover image, title, author line, `.prose` TipTap HTML with `.prose-table-wrapper` tables, inline ad slots `content_top`/`content_inline_*`).
- Right: `CreatorCard.svelte` REPLACES the search/avatar bar — avatar, name, `@handle`, bio, Primary Space badge, follower count, `<FollowButton>`, then "More from author".
- Below article: Reddit-style nested comments (unified comment engine, Section 49).

### 2. Create page (`/create`) — dev.to `/new` layout
- Left nav collapsed. **Form is the main LEFT working area** (cover → title → tags · required Space selector → TipTap body → sticky Save draft / Publish bar).
- Right panel is a **tabbed switcher: `[ Guide | Settings/SEO ]`**.
  - `CreateGuidePanel` (default): dynamic help that reacts to focused field — Space→primary-space rule, Tags→discovery tip, Series→grouping, body→`/ @ # [[` reference. Not a static tips list.
  - `CreateRightPanel` (Settings/SEO): feature image, tags, space assignment, schedule, canonical, visibility, custom fields (Section 06), SEO (meta title/description/OG/index).
- Space selector must require ≥1 primary space before Publish enables.

### 3. Guest homepage (`/` unauthenticated) — Hashnode-style landing
- NOT the shell. Rendered by the Page Builder from the `homepage` route-assignment (falls back to `/explore` when none assigned).
- Slim marketing header → hero/slider → "Explore by destination" grid → trending discussions → featured universities → latest blog → newsletter form embed → CTA banner → footer. Ad slots: `hero_below`, `landing_inline_1`, `landing_footer`.
- **Geo-aware (ADR-064):** the "Explore by destination" grid and trending discussions are geo-weighted server-side via `VisitorContext.ContentCountry` — a guest from Nigeria sees "planning to relocate" content; a guest from the UK sees "settling in / community" content; a global traveler is routed toward Japa Academy. This is SSR (no client flicker) and degrades gracefully when `GeoContext` is absent (falls back to global). The `?geo=` param always wins over the resolved `ContentCountry`.
- Authenticated `/` is the Primary timeline in the shell (ADR-032, unchanged).

---

# UNIVERSITY DISCOVERY (Section 39 — inside the shell)

Universities are a first-class space type (`space_type = 'university'`) with a dedicated discovery page and single-page profile. Both render inside `AppShell` — they are NOT exceptions.

## `/universities` — discovery list (center column)
- Filters: country (Geo Space selector), ranking tier, tuition range, programs, scholarship — all from `GET /api/v1/universities?country=&q=&page=`
- Sort: world ranking | country ranking | name | member count | follower count
- Layout: grid of university cards (logo, name, country, ranking, top programs) or list toggle
- Each card: `<FollowButton>`, View button → `/universities/[slug]`
- SEO: JSON-LD `ItemList` of `EducationalOrganization`
- **Geo-aware:** default country filter pre-populated from `VisitorContext.ContentCountry` (a UK visitor sees UK universities first). Explicit filter always wins.

## `/universities/[slug]` — single university page (center column + right sidebar)
- Header: logo (profile image), name, country flag, rankings, quick stats bar
- Center tabs: Overview (rich wiki TipTap) · Posts (content in this Space) · Forums (threads) · Courses (linked `academy_tracks` from Section 36) · Members · Reviews (Section 29 ratings) · Compare (link to Section 30 comparison)
- Right sidebar: key custom field values (ranking, tuition, programs, etc.)
- "Compare" button → opens Section 30 comparison with this university pre-selected as Item 1
- SEO: JSON-LD `EducationalOrganization` + `AggregateRating` from Section 29
- All data from `/api/v1/universities/:slug` — no hardcoded university data (Rule 16)

---

# GEO-AWARE PERSONALIZATION (ADR-064 — consumed in the frontend)

The backend resolves `VisitorContext` (ADR-064) and exposes `ContentCountry` via `GET /api/v1/geo/me`. The frontend consumes it as a **default**, never a hard filter:

- **Feed header override control:** an inline control in the feed header ("Showing: Nigeria · Change") — NOT buried in settings. Surfaced from `VisitorContext.ContentCountry`; changing it calls `PATCH /api/v1/me/profile` (`content_country_preference`) and invalidates the feed. Important for a diaspora audience that straddles two countries.
- **Feed sort:** the `?geo=` param on feed/trending/discovery routes defaults to `ContentCountry` when absent. Explicit `?geo=all` for global. Never hide non-local content — re-weight only.
- **Guest homepage:** geo-weighted SSR (above). No client flicker — the geo-resolved content is in the initial HTML.
- **Killswitch:** if `geo_personalization.enabled = false`, all surfaces show global content. The frontend does not need to check this — the backend returns global results when the killswitch is off.

---

# Full Visual Design Language

**Design references per surface** (applied WITHIN the shell): Ghost.org for the blog **list** (magazine cards, large feature image, serif-ish title, reading time); Reddit for **forum threads** (vote rail, nested threaded replies, Best/Top/New tabs); dev.to for **reading & profiles/dashboards** (the blog single, `/create`, profile analytics). These are visual cues layered onto the one shell — not separate layouts.

**Tokens (CSS custom properties, dark-mode-safe — never hardcode hex):**
- `--color-bg` (#FAFAFA / #0A0A0A), `--color-surface`, `--color-surface-subtle`, `--color-border`, `--color-muted`, `--color-primary` (#3B49DF), `--color-text`, `--chart-1..5`
- Radius: `--radius` (8px controls, 12px cards). Nav height: `--nav-height`.

**Typography:** sentence case everywhere; two weights (400/500) in chrome; blog/article body may use a reading serif. Body 16px / line-height 1.7. No ALL CAPS.

**Spacing:** generous whitespace; hairline `1px solid var(--color-border)`; cards = surface bg + border + 12px radius + ~1rem 1.25rem padding.

**Profiles (`/u/[username]`, `/org/[slug]`):** cover + avatar header, name/bio/Primary Space badge/join date/follow counts, then center tabs (Posts/Replies/Media/Likes/Spaces; org adds About/Members). Right sidebar: follow button, mutual spaces, org affiliations. **Earned certificates render as badges here** (social proof), linking to public cert pages.

**Profile learning hub — cross-app entry point (ADR-060).** The dashboard (`/dashboard`) is the single entry into the Learn and Docs apps; all tabs consume existing routes (no new backend), and cross-app links work off the shared session cookie + the ADR-054 cross-app menu system:
- **Learning tab (`/dashboard/learning`):** continue-learning cards from `GET /api/v1/me/enrollments`, resume links deep-linking into `academy.japa.to`; progress via LayerChart `LineChart`.
- **Certificates tab (`/dashboard/certificates`):** grid from `GET /api/v1/me/certificates`; each links to its public, shareable cert page `/certificates/:id` (same certs badge the public profile).
- **Knowledge Base tab (`/dashboard/knowledge-base`):** deep-links into Docs (users audience, `docs.japa.to/docs/users`) + the user's bookmarked doc pages.

Learn and Docs are separate SvelteKit apps (owned by the `jc-learn-*` / `jc-docs-*` skills) that share this app's session and theme — link to them by absolute subdomain URL; don't re-implement their surfaces here.

**Empty/loading:** shared `EmptyState` (404/403/500/empty-list; icon + message + primary action) — visually DISTINCT from `LoadingSkeleton` (still-loading ≠ nothing-here). Every async section gets a skeleton.

---

# LayerChart — Data Visualization (ADR-059)

Pinned `layerchart@2.0.1` (Svelte 5; d3-scale bundled). Used on user/org dashboards and profile analytics tabs. Prefer high-level compound charts; component-to-widget map:

| Widget | Component | Source |
|---|---|---|
| Impressions over time | `AreaChart` (bisect-x tooltip) | `me/analytics` |
| Follower/member growth | `LineChart` | `me/analytics/followers` |
| Top posts / spaces | horizontal `BarChart` | `me/analytics/content` |
| Reactions breakdown | stacked `BarChart` / radial arc | `me/analytics` |
| Readers by country | horizontal `BarChart` | Umami (Section 40) |

```svelte
<script lang="ts">
  import { AreaChart } from 'layerchart';
  let { data }: { data: { date: Date; views: number }[] } = $props();
</script>
<div class="h-64 w-full">
  <AreaChart {data} x="date" y="views"
    props={{ area: { class: 'fill-[var(--chart-1)]/20 stroke-[var(--chart-1)]' } }}
    tooltip />
</div>
```

Rules: chart colors ONLY via CSS custom properties (dark-mode safe) · data ONLY from API (Rule 16) · every chart in a fixed-height container · per-chart skeleton at final dimensions · dashboard shell + metric cards SSR, charts hydrate client-side · round every displayed number · dashboards are private (no ad slots). Do not confuse LayerChart's `<Tooltip.Root>` with Bits UI's — check the import source.

# API Contract (Rule 16)
All data from `/api/v1` — `+page.server.ts` `load()` fetches from API, never returns static data. Mutations: `fetch` + CSRF token from `$page.data.csrfToken`; auth from `$page.data.session`. Lists: `{ data: T[], meta: { total, page, limit, next_cursor? } }`. Errors: `throw error(status, message)`.

# Rendering Strategy & Routing (ADR-032/058)
- Root `/`: **authenticated** → Primary timeline (shell); **guest** → Page Builder homepage, fallback `/explore`. Resolve in root `+layout.server.ts` — no client redirect flash.
- SSR for indexable routes (`/explore`, `/forum/*`, `/blog/*`, `/spaces/*`, `/u/*`, `/org/*`, CPT singles); auth feed and `/discover`/`/notifications`/`/messages` are auth-gated. Blog/CPT single and `/create` render their exception layouts (nav auto-collapsed).
- `/discover` consumes existing `/api/v1/suggestions/*` — no new backend route.
- Optimistic UI + rollback for reactions/bookmarks/follows. `data-sveltekit-preload-data="hover"` on `<body>`.

# TipTap Triggers (Locked)
`/` slash commands · `@` mentions · `#` tags · `[[` interlinking.

# i18n
Every user-facing string: `$t('key')`; add keys to `en.json` AND `fr.json`.

# Deliverables Per Task
1. API-Readiness Gate output · 2. surface built INSIDE `AppShell` (or one of the three exceptions, explicitly) · 3. typed `+page.server.ts` `load()` · 4. `+page.svelte` (Runes, Bits UI, skeletons, dark mode) · 5. sub-components in `$lib/components/` · 6. types in `$lib/types/index.ts`.
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

## V2 Community Feature Pages — Development Notes (Phase 37, §§79–89, §98)

All 11 community feature pages render inside `AppShell` (center column + right sidebar widgets). They are NOT exceptions to the shell — they follow the same `+page.server.ts` `load()` → API → `+page.svelte` (Runes, Bits UI, skeletons) pattern as every other surface.

**Geo-aware tool pattern (mandatory on all §§79–101 pages):**
- The destination country selector is the **first input** on every community feature page — before any other filter or content. Use a Bits UI `<Select.Root>` or `<Combobox.Root>` populated from `GET /api/v1/geo/countries` (never hardcoded).
- All list endpoints consume `?dest=` as the primary filter axis. The `?dest=` value drives the API query (e.g. `GET /api/v1/community/stories?dest=GB`).
- **No hardcoded nationality** anywhere in the UI — the destination country is the axis, not the user's origin nationality. Origin is a secondary filter where applicable (e.g. Story Wall §79 supports origin filtering, but destination is primary).
- When the user has a `content_country_preference` (ADR-064), pre-select the destination selector to that value; explicit selection always wins.

**Per-feature development notes:**
- **Story Wall (§79):** filterable testimonial cards (origin/destination/visa/profession filters). Use `FeedCard` variant for each story. `?dest=` is the primary filter; origin/visa/profession are secondary.
- **Destination Wiki (§80):** collaborative versioned KB pages. Reputation-gated editing — check `can_edit` from the API response before showing the edit affordance. Render wiki content via TipTap HTML (`.prose`). Version history in a right-sidebar widget or tab.
- **Scam Alert Board (§81):** moderated scam reports with subscription. Subscription toggle via `PATCH` on the report or board. Moderation status badge from API.
- **Japa Planning Groups (§82):** private peer groups with milestones and check-ins. Group detail page inside the shell; milestone progress via LayerChart if charts are needed.
- **Visa Timeline Tracker (§83):** personal milestone logging with optional anonymous sharing. Timeline visualization (LayerChart `LineChart` or custom). Anonymous-share toggle must be explicit and opt-in.
- **Community Digest Widget (§84):** auto-generated digest — render as a right-sidebar widget or a dedicated `/community/digest` page. Content from API; no client-side aggregation.
- **Mutual Aid Board (§85):** Needs/Offers/Skill Swaps — tabbed board (Bits UI `<Tabs.Root>`) with three tabs. Each listing is a `FeedCard` variant.
- **Community Calendar (§86):** institutional dates calendar. Use a calendar component (not a chart); events from `GET /api/v1/community/calendar?dest=`.
- **Japa Stage Profiles (§87):** seven-stage relocation journey rendered on user profiles (`/u/[username]`). Adds a "Japa Stage" tab or section to the existing profile page. Stage data from API.
- **Ask-an-Expat AMA (§88):** specialized forum AMA threads. Extends the existing forum engine (Section 49) with AMA-specific UI (question voting, answered status, host highlight).
- **Achievement Feed (§89):** opt-in milestone feed. `FeedCard` variants for achievement events. Opt-in toggle via `PATCH /api/v1/me/profile`.
- **Service Directory (§98):** geo-indexed business directory. List view with `?dest=` primary filter; detail pages for each listing. JSON-LD `LocalBusiness` on detail pages.

**ADR-088 HITL review gate:** Any AI-generated content on community feature pages (e.g. wiki summaries, digest text, scam alert summaries) must pass through a Human-In-The-Loop review before publish. The UI must show a "Pending Review" state for AI-generated content and a review/approve/reject flow for moderators. Never publish AI-generated content directly — the HITL gate is mandatory.

## V2 Mentorship Pages — Development Notes (Phase 38, §102, ADR-110)

Mentorship pages render inside `AppShell`. All data from `/api/v1/mentorship/*` endpoints.

- **Mentor browsing/search (`/mentorship`):** list of mentors with filters (destination country first, then profession, visa type, availability). `?dest=` primary filter. Search via Meilisearch-backed endpoint. Match score display where applicable (60% keyword overlap + 40% pgvector cosine similarity) — render the score as a percentage badge on each mentor card.
- **Mentor profile page (`/mentorship/[id]`):** mentor bio, expertise areas, destination country, availability, past connections count. "Request Mentorship" button (Bits UI `<Dialog.Root>` for the request flow).
- **Mentorship request flow:** modal with message field, goals field, preferred schedule. Submits to `POST /api/v1/mentorship/requests`. CSRF token required.
- **Requests management (`/mentorship/requests`):** two tabs (Incoming / Outgoing) via Bits UI `<Tabs.Root>`. Actions: Accept / Decline / Cancel / Complete — each a `PATCH` on the request resource.
- **Connection active/complete/cancel flows:** once accepted, a connection is active. The UI must show connection status badges (Pending → Active → Completed / Cancelled). "Complete" and "Cancel" actions require confirmation (Bits UI `<Dialog.Root>`).
- **DM auto-open on accept (§48):** when a mentorship request is accepted (either party), the UI must automatically open the DM thread between the two parties. This is wired via the existing DM system (§48) — on accept response, navigate to `/messages?thread=[connection_id]` or open the DM modal. Do not require the user to manually start a conversation.
