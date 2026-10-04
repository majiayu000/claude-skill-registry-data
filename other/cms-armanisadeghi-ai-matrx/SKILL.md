---
name: cms-surfaces
description: Use when adding/changing a CMS surface manifest, the site_structure/html_pages_structure framing XML, a CMS context menu/extraSections wiring, or the cms-authoring platform skill. Also use when a new CMS route/tab needs an agent entry point.
---

# CMS Surfaces — Skill

This skill is the builder checklist for the CMS's Surface Values layer (manifests + framing XML +
menus). Read [FEATURE.md](FEATURE.md) first for the data model / API surface; this file is only
about how CMS surfaces expose themselves to agents. Full plan and rationale:
`.cursor/plans/cms_surfaces_rollout_74296af4.plan.md` (do not edit — historical record).

---

## The five surfaces (registry: `features/surfaces/manifests/registry.ts`)

| Surface | Manifest | Route |
|---|---|---|
| `matrx-user/cms` | `cms.manifest.ts` | `/cms` (hub) |
| `matrx-user/cms-site` | `cms-site.manifest.ts` | `/cms/[siteId]` |
| `matrx-user/cms-page` | `cms-page.manifest.ts` | `/cms/[siteId]/pages/[pageId]` |
| `matrx-user/cms-component` | `cms-component.manifest.ts` | `/cms/[siteId]/components` |
| `matrx-user/html-page` | `html-page.manifest.ts` | `/cms/html-pages/[pageId]` |

Each exports a `createXxxScope(values)` helper — always build scope through it, never hand-roll a
`SurfaceScopePayload` object at a call site.

## The framing idea — read this before adding a value

Every website surface (all four except the hub) emits the **same** `site_structure` XML —
`features/cms/utils/buildSiteStructureXml.ts`. It's the "big picture": site id/slug/policy/URLs,
every page's routing+status flags, every shared component. The node the user is on gets
`current="true"`. Standalone pages emit the smaller sibling `html_pages_structure`
(`features/html-pages/utils/buildHtmlPagesStructureXml.ts`) instead — never the site tree.

**Consequence:** local surface values should stay narrow (identity + active content), not
re-describe the whole site. If you're tempted to add "sibling pages list" or "site name" as a new
per-surface value, check whether `site_structure` already carries it first.

Both builders are pure, size-capped (`MAX_XML_CHARS`), and degrade by dropping `title` from
non-current pages before ever truncating — never emit an unbounded string.

## Where the cache comes from

`app/(core)/cms/[siteId]/SiteLayoutClient.tsx`'s `SiteContext` owns `pages`/`components` for the
whole site subtree (fetched once on site enter) plus `buildStructureXml(current)`. Every route
under `/cms/[siteId]/**` reads pages/components from `useSiteContext()` — never re-fetch the full
list locally. **After any create/update/delete/publish/discard/rollback, call
`refreshPages()`/`refreshComponents()`** so the next `site_structure` build reflects it; skipping
this means agents see stale flags (e.g. `has_draft="false"` right after a draft save).

---

## Adding a new surface value

1. Add the `SurfaceValue` to the manifest's `surfaceSpecific` array (`features/surfaces/manifests/*.ts`). Pick a `sortOrder` band consistent with neighbors (see the block comments in `cms-page.manifest.ts` — 200s framing, 250s identity, 400s editor, 450s SEO).
2. Add the field to `createXxxScope`'s `values` parameter type (required if `alwaysAvailable: true`, optional otherwise).
3. Run `npx tsx scripts/emit-surface-sync-sql.ts` and copy the regenerated rows for your surface into a new migration (pattern: `migrations/cms_surfaces_seed.sql`) — apply via Supabase MCP `apply_migration`, then verify live with `execute_sql`, then record the ledger row (`public._schema_migrations`, `source='matrx-frontend'`).
4. Run `pnpm check:surface-drift` — must be clean before moving on.

## Wiring a new mount point (menu + Pro inputs)

Follow `surface-authoring` (existing-surface runtime rollout) + `context-menu-v3` for the mechanics. CMS-specific notes:

- Use **v3** (`EditableContextMenu`/`NonEditableContextMenu` from `features/context-menu-v3/`) — the only context menu (v2 was deleted 2026-07-19).
- `getApplicationScope` is a plain function (no `useCallback`) that calls `buildApplicationScopeFromMenuContext` with a live `createXxxScope(...)` built from current component state + `useSiteContext()`.
- `extraSections` handlers must be the route's **real** save/publish/discard/preview/rollback callbacks — never toast stubs.
- Monaco-based editors (`HtmlPageEditor`'s HTML tab) have no `HTMLTextAreaElement` ref — pass `contextData.htmlContent` and skip `getTextarea`; Copy/AI actions still work through the content-based fallback.
- `ProTextarea`/`ProInput` replace plain `Textarea`/`Input` wherever the field is bindable content (HTML/CSS/JS bodies, SEO fields) — pass `surfaceName` + `getApplicationScope`.

## Verifying end to end

1. `pnpm check:surface-drift` — manifests vs. DB rows.
2. Type-check touched files (`npx tsc --noEmit`).
3. Manual: right-click a wired region → confirm the v3 menu opens, the surface footer/inspector shows populated values (especially `site_structure`/`html_pages_structure` — should be compact XML, not empty), and any `extraSections` action (Save Draft, Publish, etc.) actually performs the mutation.

---

## The `cms-authoring` platform skill (agent-facing, not this file)

Separate artifact — a row in `skill.definition` (`skill_id: cms-authoring`), applied via
`migrations/cms_surfaces_seed.sql`. Teaches agents the two-content-system model, draft/publish
twins, URL rules, the `agent_write_policy` gate, and the aidream CMS tool map
(`cms_page`/`cms_site`/`cms_component`/`cms_find_page`/`cms_inspect`/`html_page`/`cms_verify`). It
is **opt-in** via `skill_config.included` on CMS system agents — never auto-attach it to every
agent. Update its `body` in a new migration (same NOT-EXISTS-guard pattern) if the model changes;
do not hand-edit the DB row directly.

---

## Forbidden

- New Surface Values manifest outside `features/surfaces/manifests/` or a `createXxxScope` bypass (hand-built scope object).
- Re-fetching the full page/component list inside a child route instead of reading `useSiteContext()`.
- Any bespoke or non-v3 context menu on a CMS surface.
- Stuffing "big picture" data (site name, sibling pages, policy) into a new narrow value when `site_structure`/`html_pages_structure` already carries it.
- Skipping `refreshPages()`/`refreshComponents()` after a mutation — causes stale `site_structure`.
- Auto-attaching `cms-authoring` to agents outside CMS system agents.

---

## Change-log expectations

After any non-trivial change to a CMS surface: update [FEATURE.md](FEATURE.md)'s entry points /
invariants + change log, and re-run `pnpm check:surface-drift` before considering the change done.
