---
name: core-route-headers
description: "(core) route header and body-height conformance via PageHeader. Use when fixing a (core) page's header, title bar, breadcrumbs, sub-route nav, body height (h-page, calc(100dvh…)), mobile header, or buttons hidden behind the avatar, or on a header-conformance assignment. NOT for /administration/* routes."
---

# core-route-headers — (core) shell header + page conformance

**Read `features/shell/components/header/variants/USAGE.md` first** — it is the canonical spec for the injection zone, variants, and body-height table. This skill is the *fix workflow*: how to classify a broken route, which exemplar to copy, and how to verify in the browser on desktop AND mobile.

For the cross-page composition rules that accompany this header contract (one
coherent control, icon/title rows, intentional spacing, tap targets, and no
competing route menus), also read the shared policy at
`/policies/no-dead-ends.md`.

## The mental model (one paragraph)

The shell header is a **solid band** (the page's own background colour) over the page, with transparent controls and one 8px fade below it that the shell alone draws. The shell owns the far edges (hamburger left, org/canvas/avatar right); the route owns ONLY the center zone via `<PageHeader>` (`features/shell/components/header/PageHeader.tsx` — Server Component, portals into `#shell-header-center`; `desktop=` / `mobile=` props for per-breakpoint content). `.shell-main` is pulled up under the header with a negative margin, so the page body **already fills the viewport** and content scrolls *behind* the band. Everything broken in this repo is one of two sins: rendering header chrome **in the body**, or **subtracting the header height** from the body.

## Gold standards — copy these, don't invent

| Route | What it proves | Key files |
|---|---|---|
| `/agents/all` | List page: `PageHeader` + injected list header, body scrolls behind glass | `app/(core)/agents/all/page.tsx`, `packages/chat/src/agents/components/shell/AgentsListHeader.tsx` |
| `/agents/[id]/build` | The masterpiece: back tap-target + `[id]` dropdown selector + measurement-collapsing mode nav + save/options — **no title/description block** | `packages/chat/src/agents/components/shared/AgentHeader.tsx`, `AgentModeController.tsx` |
| `/chat/[conversationId]` | Scroll-behind-glass body + left/right icons + **route-injected sidebar menu** (no double menu) | `app/(core)/chat/[conversationId]/page.tsx`, `features/shell/constants/route-menu-registry.ts` |
| `/organizations/[orgId]/scopes/**` | Best breadcrumb nav: full-path breadcrumb, per-level sibling dropdowns, mobile drawer — mounted ONCE at the layout | `features/scope-system/components/ScopesRouteHeader.tsx`, mounted in `app/(core)/organizations/[orgId]/layout.tsx` |
| `/tasks` | Resizable panels: per-panel `pt-[var(--shell-header-h)]` only where static top UI must clear the glass | `app/(core)/tasks/` |

**Anti-examples** — the two CMS pages formerly listed here (`app/(core)/cms/page.tsx`,
`app/(core)/cms/html-pages/page.tsx`) have both been **fixed** (verified 2026-07-28) and are
now a *positive* example instead: they share ONE `CmsHubHeader`
(`features/cms/components/CmsHubHeader.tsx`) wrapping `RouteHeader` + `RouteModeNav`, with
no title text — the section nav IS the identity, and each page passes only its contextual
tap-buttons via `right`. Copy that shape for any two-or-more-page hub.

To find live offenders, don't trust a list in this file — run `pnpm check:page-headers` and
grep the route for the failure classes below. A hardcoded anti-example list rots the moment
someone fixes it.

## Failure classes — classify before you touch anything

1. **Faux in-body header** — a body-rendered bar with title + actions (`border-b` + `bg-card`/`bg-background/*`). Move controls into `<PageHeader>`; delete the bar.
2. **Banned height math** — `h-[calc(100dvh-…)]`, `h-page`, `h-screen`, `min-h-screen` on a (core) body. Replace with `h-full overflow-hidden` (see USAGE.md body-type table).
   A **route layout boundary** is different: it must never put `{children}`
   behind unconditional vertical clipping. Use `overflow-y-auto
   overflow-x-hidden` as the fallback there; full-height leaf editors and
   tables retain their own inner scroll, while natural-height leaves cannot be
   amputated by one missed class.
3. **Title/description block in a dashboard page** — marketing copy inside app chrome. **Delete it**; the header center carries a `text-sm` title at most.
4. **Missing top clearance for floating/static content** — content that must NOT slide behind the glass (grid of cards with action buttons, sticky toolbars) needs `pt-[var(--shell-header-h)]` (never a hardcoded `pt-12`); freely-scrolling content gets **no** top padding so it floats behind the glass. This is the `/agents/all` mobile bug: card buttons float up into the header.
5. **Desktop actions vanish on mobile** — `hidden lg:flex` with no mobile counterpart. The rule: desktop actions collapse into one or two **bottom sheets** on mobile (`HeaderActions` in `features/shell/components/header/variants/shared/` renders `BottomSheet` below `lg`; or `BottomSheet` from `@ai-matrx/design-system` directly). `packages/chat/src/agents/components/shared/AgentHeaderMobile.tsx` exists but is commented out in `AgentHeader.tsx` — that class of gap.
6. **Double menus** — a page-level nav next to the sidebar. Large routes register ONE menu in `features/shell/constants/route-menu-registry.ts` (desktop `RouteMenuSlot` + `MobileRouteMenuSlot` come free).
7. **Avatar collision** — `ml-auto` / `justify-between` actions in the body drifting behind the fixed avatar (the old `pr-14` hack). Fixed automatically by moving actions into the bounded center zone.

## Templates — reach for these FIRST

Two drop-in templates in `features/shell/components/header/templates/` cover almost every route; consuming one is the default, hand-rolling is the exception:

- **`EntityModeHeader`** — the agents pattern for any `[id]` route: back chevron + entity-name **sibling dropdown** + center `RouteModeNav` + **declarative `actions`** (`{label, icon, onPress|href, primary?, destructive?}`). Desktop renders them as tap targets; **mobile renders back + name + ONE `…` that opens a bottom drawer** containing modes AND actions. Reference consumer: `/schedules/[id]` (`features/scheduling/components/detail/ScheduleDetail.tsx`).
- **`CrumbTrailHeader`** — the org/scopes pattern for drill-down hierarchies: clickable trail, per-level sibling dropdowns, mobile collapses to the last crumb.
- **`MobilePanelShell`** — any multi-pane route (sidebar+detail, IDE, inspector rails): pass the existing desktop layout **verbatim** as `desktop`, plus `main` + `panels`; below `md` each side panel becomes a bottom drawer behind ONE `…` tap target. A genuinely dense workspace may set `collapseBelow="lg" | "xl" | "2xl"` so panels collapse before they crush the primary work; the default stays `md`. It auto-dismisses on **route change only** — an in-panel action that is not navigation (picking a session, flipping a `?search_param`, firing a run) must close the drawer itself by calling **`useMobilePanelClose()`** at the action site. That hook is a no-op outside a drawer, so the same component is safe in the desktop pane. Consumers: `/rag/data-stores` (store rows), transcripts studio (`StudioSidebar` pick/create), transcripts cleanup (`CleanupPad` Clean Up), agent Hindsight (`collapseBelow="2xl"`).

**Button rules** (live catalogue: `/demos/button-demo`):
- Header tap buttons are `variant="transparent"` (owner, 2026-10-03): the shell paints the header band solid, so nothing moves behind it and "glass only floats" rules glass out. Icons must match the shell's own buttons. Never add a border, shadow, fade or solid strip under the header — the shell owns that boundary once (`.shell-header-fade`; guard `features/shell/__tests__/header-top-boundary.test.ts`).
- The page's ONE primary action → `variant="solid"` (primary). Delete/remove → solid `bgColor="bg-destructive" hoverBgColor="hover:bg-destructive/90"`.
- **Standalone tap buttons self-space (44px)** — never wrap `TapTargetButton` controls in `gap-*`/`p-*`.
- **Route navigation stays compact at every width.** `RouteModeNav` items match the Agents header; never add `min-h-11`, `min-w-11`, responsive padding, or a 44px minimum to its visible pill. Mobile reachability comes from its 52px bottom-sheet rows, not a taller shell header.
- Related actions can share a `TapTargetButtonGroup` (`TapTargetButtonForGroup` children). Search surfaces: see the SearchToolbar / SearchGroup patterns in the demo.

**Mobile doctrine:** don't cram. As few header items as possible — back + identity + one `…` → bottom drawer. A truncated 8-letter dropdown is worse than a drawer. Only keep richer mobile headers where a route has a genuinely great concept (chat).

## Compose with RouteHeader — the default

`RouteHeader` (`features/shell/components/header/RouteHeader.tsx`) is the canonical three-part injection: `left` (back tap-target + identity), `center` (the ONE nav/selection control — usually `RouteModeNav`), `right` (tap-target actions). Prefer it over hand-rolled `<PageHeader>` rows and over `HeaderStructured` whenever the route has sub-views. **No title text in the center when a nav can live there** — "Content Manager"-style labels are filler; the nav IS the identity. A lone `text-sm font-medium` title on the left is fine for single-view routes.

Sibling routes sharing one header (e.g. `/cms` + `/cms/html-pages`) get ONE shared header component in the feature (`features/cms/components/CmsHubHeader.tsx` is the reference) — never two diverging copies.

## Fix recipe by route archetype

- **List/gallery page** → copy `/agents/all`: `PageHeader` with a small injected header (search / filters / New), body `h-full overflow-hidden`, scroll container inside, floating grid content gets `pt-[var(--shell-header-h)]` if it has interactive elements at the top.
- **Detail/editor `[id]` page** → copy `/agents/[id]/build`: `ChevronLeftTapButton` back (from `@ai-matrx/tap-target/buttons`), entity **dropdown** (not a static title) for `[id]` routes, actions right. No title/description prose.
- **Sub-mode family** (build/run/templates…) → `RouteModeNav` (`features/shell/components/header/RouteModeNav.tsx`) — measurement-driven full → icons → menu collapse. It is the ONE control for mode switching; never pair it with a second selector. **Give every item an `icon`** — the icon-only stage is skipped entirely when even one lacks it, so the nav jumps straight from full text to a dropdown.
- **Drill-down hierarchy** (org → type → item…) → `ScopesRouteHeader` pattern: one layout-level breadcrumb header, pathname-gated, per-level sibling dropdowns, mobile drawer.
- **Actions overflow** → `HeaderStructured` / `HeaderActions` (see USAGE.md variants) — inline on `lg+`, glass dropdown for overflow, `BottomSheet` on mobile.
- **Right slot** (save status, page-scoped icons) → `PageHeaderRightPortal` (`features/shell/components/header/PageHeaderRightPortal.tsx`).

Per-breakpoint content: `<PageHeader desktop={…} mobile={…} />`. Mobile never gets *nothing* — at minimum back + title + one sheet trigger holding the desktop actions.

## Detection — finding offenders

```bash
pnpm check:page-headers            # faux-header markers (KNOWN NARROW — misses bg-background/* bars)
pnpm check:scroll-chain:strict     # all route pages/layouts + cross-component bounded-height chains
grep -rln "calc(100dvh\|calc(100vh\|h-screen\|h-page" app/\(core\) --include="*.tsx"
grep -rLn "PageHeader" <route dir>  # route family never injecting the header
grep -rn "pt-12\|pt-10\|pt-8" <route dir>  # hardcoded header offsets → var(--shell-header-h)
```
Find a new faux-header class combo? **Add it to `FAUX_HEADER_MARKERS` in `scripts/check-page-headers.ts`** in the same change — the guard must learn what you learned.

## RouteModeNav — the three-stage contract

The center nav MUST degrade **icon + text → icon only → `…` menu**, driven by measured space, never by breakpoints. All three stages are load-bearing; a nav that skips one is a defect. Two invariants keep it honest (both were live bugs on `/marketing`, fixed 2026-07-20):

- **Each hidden measurer carries `w-max`.** They are block-level siblings in one shrink-to-fit absolute box, so without it every measurer stretches to the widest one and the icons measurer reports the FULL width — making `iconsW <= avail` unreachable and turning the icon-only stage into dead code.
- **The fit test reserves `FLANK_GUTTER` (32px).** `centerSlotWidth` returns the theoretical maximum, so an exact-fit test picks `full` when the pill is 1px from the shell's own icons. Collapse *before* the flanks are touched, not when they collide.

**Selection must be obvious in BOTH themes.** Never style the selected item with `--matrx-glass-bg-active` directly — that low-alpha tint reads in dark and vanishes against light-mode glass, which is exactly how the selected route became invisible in light. Use the `--shell-nav-selected-bg` / `-text` / `-shadow` + `--shell-nav-unselected-text` tokens (`styles/shell.css`): light resolves to a solid raised pill with a real text-colour delta, dark keeps the glass tint. Selection also needs a genuine *unselected* baseline — `--shell-nav-text` (0.82 black) sits too close to its own hover value to signal state.

## Gotchas proven in the field

- **Radix `asChild` wrappers take ONE child.** Injecting `<PageHeader>` as a sibling inside `NonEditableContextMenu`/any trigger wrapper crashes with "Primitive.span failed to slot". Put the header OUTSIDE the wrapper.
- **Turbopack HMR corruption can 404 sub-routes** (route matches on baseline, 404s after rapid edits, root still 200). Recompile/restart the dev server before diagnosing your diff.
- **`RouteModeNav` root must be `w-full`** — it measures its own box; without `w-full` a compact first paint locks it in the "menu" variant forever (fixed 2026-07-13; don't regress it).
- **Mobile header budget:** left identity truncates (`max-w-[100px] sm:max-w-[180px]`), secondary right actions hide below `sm` (`hidden sm:inline-flex`) — one primary action stays.

## Verify in the browser — mandatory, both viewports

1. Reuse a running dev server (`pnpm dev:status`) or `preview_start`; log in via `/login` with `admin@admin.com` / `<see AI_ADMIN_PASSWORD in .env>`.
2. Navigate to the route. **Desktop (1280×800):** no in-body title bar; actions in the header center; nothing behind the avatar; no dead strip at the bottom; content scrolls behind the glass.
3. **Intermediate (~700–900px):** the center nav must have already stepped down a stage rather than sitting flush against the shell icons. Skipping this width is how a nav that only ever does full → menu passes review.
4. **Mobile (375×812 via `resize_window`):** every desktop action reachable (bottom sheet, not vanished); no interactive element floating into the glass header; single scroll area.
5. **Both themes.** The app's theme is a `.dark` class, NOT `prefers-color-scheme` — `resize_window`'s `colorScheme` does nothing. Toggle with `document.documentElement.classList.toggle('dark')`. Light mode is where selected-state contrast dies; check it explicitly.
6. Screenshot each. A visible flaw in your own screenshot is a failure — fix it, don't present it.

## Do not break

- `/administration/*` and `(transitional)`/`(legacy)` sit **below** the header — `h-page`/header-calc is *correct* there. Never "fix" them with this recipe.
- The rules in `app/(core)/_read_first_route_rules/` and the scaffold in `.claude/skills/new-route-scaffold/SKILL.md` (SSR, hydrators, skeleton `loading.tsx` — no spinners).
- Mobile rules in `.claude/skills/ios-mobile-first/SKILL.md` (`h-dvh` not `h-screen` for non-shell pages, `pb-safe`, drawer-not-dialog).
- Lucide only, no emojis, semantic color classes, component-library loading states.
