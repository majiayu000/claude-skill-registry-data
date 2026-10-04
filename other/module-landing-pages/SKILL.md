---
name: module-landing-pages
description: "One-route pattern: public marketing landing plus signed-in workspace. Use when creating or fixing a landing page or a feature's front door, guests see an error, 'make /X work signed out', signed-in users land on a pitch, or ModuleLanding / AuthedWorkspaceCTA. NOT for (public) share viewers or free tools."
---

# module-landing-pages — one route, two audiences, zero errors

**The pattern:** a feature's URL serves BOTH the marketing pitch and the workspace. Anonymous visitors always get a rendered marketing page — **never a login wall, never an error**. Signed-in users get a per-page decision: land on the marketing page with a one-tap "Open {Workspace}" pill in the header, or get bounced server-side straight into the workspace. Marketing pages are where the platform's front-door infrastructure gets built — treat them as load-bearing, not brochureware.

## The three invariants

1. **Anonymous never errors.** `utils/supabase/middleware.ts` hard-blocks ONLY `/administration`, `/api/admin`, `/dashboard`, `/scraper`. Everything else renders for guests. **Never add a route to `requiresAuth`** to "protect" a feature — protect at the resource level instead (see Access gating below). The `(core)` layout (`app/(core)/layout.tsx`) builds a guest Redux user for anon instead of redirecting; your page inherits that for free. **Feature has no landing yet?** Server-branch guests to `<ModuleSignInGate title="X" route="/x" />` (`features/auth/components/module-landing/ModuleSignInGate.tsx`) — the sanctioned interim (Arman ruling 2026-07-29, applied fleet-wide that day); replace it with a real `ModuleLanding` when one ships. Never hand-roll a sign-in panel and never let the workspace render for guests and error client-side.
2. **Authed gets a decision, per page.** Pick a posture (table below). The deciding factor: **if the marketing page shows a clear, easy way in at the top (`AuthedWorkspaceCTA`), authed users may land there; if it can't, bounce them in server-side.** Never leave an authed user on a pitch with no route into the app — that is a defect (the Legal pages had it).
3. **Marketing pages live in `(core)`, not `(public)`.** They render inside `AppShell` via `MarketingPageShell` so they're publicly crawlable AND inherit the glass header, sign-up CTA, and authed continuity (`features/education/FEATURE.md` §"Why (core), not (public)"). `(public)` is for share viewers, free tools, and compliance docs — a different, fixed-viewport shell.

## The three postures for a signed-in user

| Posture | When | Mechanism | Exemplar |
|---|---|---|---|
| **Bounce in** | Workspace lives at a sub-route; pitch has no value to members | Server page: `getServerAuth()` → `if (isAuthenticated) redirect("/x/new")` → else `<XLanding />` | `app/(core)/chat/page.tsx` |
| **Branch in layout** | Marketing page and workspace share the SAME URL | Server layout: guest → `<XLanding />`, authed → workspace. Neither tree leaks into the other's bundle | `app/(core)/notes/layout.tsx` (also `sandbox`, `documents`, `data`, `workbooks`) |
| **Land with CTA** | The page is a hub/directory/content surface valuable to both audiences | Everyone gets the marketing page; `AuthedWorkspaceCTA` renders the header pill for authed; optional authed-only island personalizes on top | `/education` hub (`EducationHub.tsx` + `StudyTodayCard`), `/features`, `/education/learn` |

`getServerAuth()` (`utils/supabase/getServerAuth.ts`) is request-scope cached — the layout already called it; your call is free. Always decide **server-side** (no client flash, no bundle leak).

## Build recipe — new feature landing

1. **Landing body = `ModuleLanding`** (`features/auth/components/module-landing/ModuleLanding.tsx`). Prop-driven hero + capabilities + steps + sub-areas + related modules + final CTA. It mounts `AuthedWorkspaceCTA` and `ModuleLandingConversionNudges` for you — authed pill and guest nudges, each silent for the wrong audience. **Never hand-roll a hero clone** (the ~900-line Legal duplicates predate `ModuleLanding` and are the anti-example).
2. **Register it** in `MODULE_LANDING_DIRECTORY` (`features/auth/components/module-landing/landings/directory.ts`) — that's what puts it on `/features` and in other landings' `relatedModules` grids. An unregistered landing is invisible.
3. **Wrap the route** in `MarketingPageShell` (`features/shell/components/MarketingPageShell.tsx`) — `bg-textured`, no top offset, content rides under the glass header. Route file stays a thin composition (see `app/(core)/legal/page.tsx`).
4. **Every CTA has a real `href`.** `primaryCtaHref` for guests (usually `/sign-up` or the tool itself); `workspaceHref`/`workspaceLabel` for the authed pill. A bare `<Button>` with no href/onClick is a dead CTA — defect on sight.
5. **Metadata** via `createRouteMetadata` / `createDynamicRouteMetadata` (`utils/route-metadata.ts`) with a unique favicon `letter` — never hand-roll `<title>`. Add the route to `app/sitemap.xml/route.ts` if it should be indexed. Serving on a satellite origin? Pin `metadataBase` (education pins `EDU_ORIGIN` — `features/education/route-helpers.ts`).
6. **Guest data reads are cookie-free.** Public content a guest page renders uses the anon script client + `unstable_cache`/ISR + a `pub_read` RLS policy (`features/education/publishing/queries.ts` is the reference) — never the cookie-bound server client, or ISR breaks and anon 401s.

## Data-driven marketing at scale (the Education tier)

When a feature needs MANY marketing pages (axes × slugs), don't multiply components — copy education's system: content registries in `features/<x>/data/`, one `SectionRenderer` with typed block kinds (`prose`, `feature-grid`, `steps`, `stat-bar`, `faq`, `cta`, …), thin route files, `generateStaticParams` + ISR, per-slug `opengraph-image.tsx`, JSON-LD. Contract: `app/(core)/education/ROUTING.md`. New block kind = extend the union + one renderer branch — never a bespoke page body.

## Access gating — resource-level, never route-level

- A tool page whose **record** the visitor can't access: `requireAccess(type, id, level, { redirectTo })` (`utils/permissions/requireAccess.ts`) → redirect to the **view** route, never `/login`, never 404. Every education `[id]/edit` page is the pattern.
- The rare genuinely-authed-only page (e.g. `/education/creator`): server `redirect("/login?redirectTo=" + path)` — a redirect, never an error page.
- Unknown slug → `notFound()`, not a redirect.

## Verify before done

- Signed-out browser (incognito): the route renders the marketing page — no login bounce, no error, no blank shell.
- Signed-in: the chosen posture works — either bounced into the workspace, or landed with the "Open {X}" pill visible in the header right slot.
- Click every CTA. All navigate.
- `view-source`: title/description/OG present; JSON-LD if content-tier.

## Known divergences (fix on sight when touching these files)

- Legal landings (`features/legal/**/Legal*Landing.tsx`, `CaWcLanding.tsx`): hand-rolled pre-`ModuleLanding` clones, historically shipped dead CTAs and no `AuthedWorkspaceCTA` — migrate toward `ModuleLanding` when working there.
- Education uses its own `EduHero`/`SectionRenderer` (deliberate — data-driven tier) and does NOT mount guest conversion nudges; that asymmetry is known, not a license to fork a third hero.
