---
name: jc-academy-develop
description: Use when building new pages or components for the JapaConnect Academy app (apps/academy, port 3003, SSR, academy.japa.to). Covers the unified app shell adapted for Academy (ADR-060), the lesson-player reading exception, the SSR/CSR progress boundary, TrackCard, LayerChart 2.0.1 progress analytics, and the API-Readiness Gate.
---

# JapaConnect Academy — Development Skill

Course/track platform at `academy.japa.to`. SSR (adapter-node + Bun). API base `/api/v1/academy/*`. **Layout is the unified app shell (ADR-058) adapted for Academy (ADR-060) — build inside it; the lesson player is the one exception.**

## ⛔ API-READINESS GATE
Same as `jc-main-develop`: list endpoints → verify (catalog or probe) → any missing: STOP + ⚠️ MISSING BACKEND API ROUTES alert. Never mock. Known routes: `GET /academy/catalog` (marketplace catalog, filters on `is_published_to_academy`), `GET /academy/catalog/options`, `GET /academy/tracks`, `GET /academy/tracks/:slug`, `POST /academy/tracks/:id/enroll`, `GET /me/enrollments`, `GET /academy/lessons/:id`, `POST /academy/lessons/:id/progress`, `POST /academy/lessons/:id/complete`, `GET /academy/quizzes/:id` + `POST /academy/quizzes/:id/submit`, `GET /me/certificates` — verify each before use. **Japa Academy (ADR-063) routes**: `POST /academy/instructor/apply` (creator application), `GET /academy/instructor/me` (own instructor status), `GET /academy/my/tracks` (instructor course list), `POST /academy/my/tracks/:id/submit` (submit course to marketplace), `GET /academy/my/payouts` (instructor payout history), `GET /academy/my/earnings` (earnings + revenue series) — verify each before use.

## Japa Academy Marketplace (ADR-063 — unified shell)

Japa Academy is the Academy platform presented as a worldwide creator marketplace under its own brand. Since the ADR-063 consolidation there is a **single Academy shell** — the former Learn/University dual-shell is gone. The canonical host is `academy.japa.to` (or a custom domain from the `academy.subdomain` / `academy.custom_domain` system_settings, routed by the edge proxy). Not open sourced (ADR-063 §1).
- **Marketplace catalog:** `GET /academy/tracks` returns only `is_published_to_academy = true` courses. `TrackCard` adds a price badge (`price_kobo` → formatted) and instructor name. Free and Pro-included courses show "Free" / "Pro".
- **Creator flow:** `POST /academy/instructor/apply` → `academy_instructor_profiles.status = 'pending'`. Admin approves → `academy:notify_instructor_approved`. Approved instructor creates a track → `POST /academy/my/tracks/:id/submit` → admin approves course → `academy:notify_course_approved` → `is_published_to_academy = true`.
- **Instructor dashboard:** `/dashboard/instructor` — course list with enrollment counts (`total_enrolled`), revenue overview from `GET /academy/my/payouts` + `GET /academy/my/earnings`, pending/approved course status. LayerChart for revenue over time.
- **Pro dual-access:** Pro subscribers enroll in any academy course for free. The UI shows "Included with Pro" instead of a price for Pro users. Creators are still compensated (Pro stream rate, ADR-063 §7) — this is backend, not visible in the UI.
- **Course reviews:** reuse the polymorphic `reviews` table (`entity_type = 'academy_track'`). Star ratings and counts from `review_aggregates`. No course-specific review UI — use the same review component as Section 29.
- **SSR/CSR boundary unchanged:** marketplace catalog is public (SSR); instructor dashboard and payout data are CSR (session-guarded).

## ⚠️ SSR/CSR BOUNDARY — Academy's Critical Rule
**User-specific data is NEVER server-rendered.** Progress, enrollment status, completed lessons, quiz scores → CSR only, guarded by session:
```svelte
// +page.server.ts — public content ONLY (track, curriculum, lesson HTML)
// +page.svelte — user data:
$effect(async () => {
  if (!data.session) return;
  const r = await fetch(`/api/v1/me/enrollments`);
  if (r.ok) enrollments = (await r.json()).data;
});
```
A `+page.server.ts` touching `/me/enrollments` or `/academy/lessons/:id/progress` is a critical defect (leaks one user's progress into cached SSR responses).

## The Shell (ADR-058 primitives, ADR-060 drift)
Adopt `AppShell` (collapsible `LeftNav` + center + `RightSidebar`), `ui.nav_collapsed` server-persistence (never localStorage), sticky right-sidebar search+avatar, dark-mode tokens, mobile single-column + bottom bar. Nav items from `GET /api/v1/menus/academy_nav` (ADR-054).
- **Left nav (learning-oriented):** Explore (catalog) · My Learning · Paths · Certificates · Bookmarks.
- **Center:** catalog grid / track detail / lesson player.
- **Right sidebar:** continue-learning card, streak + progress ring, up-next lesson.
- **`TrackCard`** is ONE variant-driven card (Ghost-style: thumbnail, title, `LevelBadge`, duration, instructor, rating, enrolled count, enroll/continue/locked). Never fork per level/type.

## Lesson Player — Academy's Reading Exception (ADR-060, dev.to-single analog)
Route `(app)/tracks/[slug]/[module]/[lesson]` (or `/academy/lessons/:id`). Left nav auto-collapses to 72px. Three zones:
- `CurriculumRail` — module→lesson tree in the content's LEFT margin: current (▶), completed (✓), locked (🔒), not-started (○). Sticky/scrollable. Belongs to the content — visually distinct from the collapsed nav, NOT a second nav.
- Center — lesson by `lesson_type`: `article` (SSR TipTap `.prose` + `.prose-table-wrapper`), `video` (browser-guarded init, `progress_secs` tracking), `quiz` (quiz engine), `checklist` (TaskList). Mark complete → `POST /academy/lessons/:id/complete` (optimistic `Set`, `marking` guard, rollback, auto-next).
- Right — lesson meta: track progress ring, Next lesson →, notes.
- No ads. Access verified server-side (403 if not enrolled and not `is_preview` → redirect to enroll).

## Track Detail (widened overview)
`/academy/tracks/[slug]`: SSR hero + stats · `<Tabs.Root>` Overview | Curriculum | Reviews · `<Accordion.Root type="multiple">` curriculum · instructor card · enroll CTA · `Course` JSON-LD.

## LayerChart — Learner Analytics (ADR-059)
Pinned `layerchart@2.0.1`. "My Learning" dashboard: progress over time (`LineChart`), weekly activity (`BarChart`), completion/time-spent, streak sparklines. High-level compound charts preferred:
```svelte
<script lang="ts">import { LineChart } from 'layerchart'; let { data } = $props();</script>
<div class="h-64 w-full"><LineChart {data} x="date" y="pct"
  props={{ spline: { class: 'stroke-[var(--chart-1)]' } }} tooltip /></div>
```
Rules: colors via `var(--chart-*)`/`var(--color-*)` only (dark-mode safe) · fixed-height containers · data from `/api/v1/me/*` + `/academy/*` (verify via Gate!) · per-chart skeleton · dates → `Date`.

## Difficulty & Progress Tokens (CSS custom properties, dark-mode safe — never hardcode hex)
`--level-beginner` (green) · `--level-intermediate` (amber) · `--level-advanced` (red) · `--color-progress` · `--color-locked`. Define once in the theme; reference as variables.

## Stack
Identical base to `jc-main-develop`: Svelte 5 Runes, Bits UI dot-notation, Tailwind v4, LayerChart 2.0.1, Lucide, TypeScript, `$t()` i18n (en+fr), Rule 16, no AI attribution. Canonical URLs on `academy.japa.to`.

## Deliverables Per Task
1. Gate output · 2. surface built INSIDE `AppShell` (or the lesson-player exception, explicitly) · 3. `+page.server.ts` (public content only — no user progress) · 4. `+page.svelte` (SSR content + CSR progress, skeletons) · 5. components · 6. JSON-LD · 7. types
**V2 academy app:** No new pages in v2. Japa Academy (ADR-063) is already implemented. The academy app may receive minor amendments if Japa Academy course visibility is affected by v2 persona authorship or the AI Content Studio publishing courses. **Per ADR-060, v2 community features (§§79–89), functional tools (§§90–101), and mentorship (§102) are not part of the academy platform** — they live in the Main app (community) and Tools app (functional tools). However, academy content may be cross-referenced from these features (e.g. a functional tool may link to a relevant academy track). Total platform route count is now ~819 (~475 v1 + ~344 v2); 18 Golden Rules (R18: always use bun).

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
