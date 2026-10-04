---
name: context-assignment
description: "Context and scope-tagging UI. Use when adding a context picker to a surface, tagging an entity to scopes, setting or filtering by the active (working) context, showing per-entity context status, prompting for context on upload, or editing context-assignment/**, active-context/**, or appContextSlice."
---

# Context assignment — picking the right component

## The mental model (read this or you WILL wire it wrong)

1. **Membership, not ownership.** A person belongs to MULTIPLE organizations,
   all equal (no personal or business type — `common-docs/policies/access-ladder.md`).
   Never assume one org per user. Every project and task belongs to exactly one
   organization (`organization_id` NOT NULL, live); a SCOPE assignment on them
   can be empty ("unassigned"), and that is normal, not an error.
2. **The hierarchy:** organization → scope types (the org's custom dimensions,
   e.g. Clients, Matters) → scopes (instances, e.g. "Acme Corp") → context
   items (typed fields per scope). Tasks may live in projects but DON'T have
   to; projects may live in orgs but DON'T have to.
3. **A scope NEVER implies its organization.** Org is an independent context
   dimension — it is part of a selection only when explicitly checked.
   Display follows the same rule (`ContextSummaryChips` enforces it).
4. **Three runtime layers — NEVER conflate them** (full table:
   `../common-docs/systems/account/scopes-context/STATE.md` → "Runtime context — three layers"):
   - **Layer A — Active (working/passive) context** = "what I'm doing right
     now"; ephemeral; lives in `appContextSlice`; feeds every agent run
     automatically (execute-instance stamps it). MULTI-scope (keyed by scope id
     since 2026-06-12), single org/project/task, plus independent active scope
     **types** (`active_scope_type_ids`, 2026-06-30 — "whole dimension in play,
     no instance chosen"). **Writers MUST be Surface A** (ESLint-gated; the
     write actions include `setActiveScopeTypes`).
   - **Layer B — Reference tree** = what *exists* (org→type→scope→item). Cache
     only; fetched once at boot. **Being consolidated onto the hierarchy owner**
     — read scope data via hierarchy selectors, do NOT reach for the fragmented
     `scopeTypes`/`scopes`/… fan-out slices in new code.
   - **Layer C — Durable object assignment** = "this entity belongs to these";
     persisted in canonical `platform.associations` via the `setEntityScopes`
     chokepoint, **from the user's explicit UI selection**. (The legacy
     `ctx_scope_assignments` table is RETIRED — FE cut over 2026-06, zero DB
     functions reference it; never write to or read from it.)
   - A user ACTION (Layer C) must read the explicit selection, **never** Layer A
     just because it's loaded. A successful write that sourced Layer A is *worse*
     than a failure — it silently mis-binds. Never auto-convert active → durable
     (suggest only). The condemned `agent_surface` binding service
     (`features/surfaces`) is the cautionary example of doing this wrong.

## Component selection table

| You need… | Use | Mode/notes |
|---|---|---|
| Tag an entity (file/note/agent/…) inline on a page | `ContextAssignmentField` | `mode="assignment"`, pass `subject`; use `dimensions={["scopes"]}` when the surface is scope-only (no project/task FK intent) |
| Same, without blocking the page | `ContextAssignmentPopover` | trigger = your button |
| Same, as an explicit modal step | `ContextAssignmentDialog` | controlled `open` |
| Same, floating/draggable | `ContextAssignmentWindow` | inline-controlled |
| Set the WORKING context from a header/toolbar | `ActiveContextButton` | live-apply popover; sizes `xs`/`sm`, `iconOnly` for rails |
| Same field inside a tab panel / drawer (no trigger) | `ActiveContextPanel` | composes `ContextAssignmentField mode="active"`; default `checkboxVariant="standard"`; used by `RunControlsMenu` Context tab |
| Clear working context (rose Eraser + "Context", app-wide) | `ClearContextButton` | dispatches `clearContext`; wired into every Surface A control |
| Show context status per entity (amber/green nudge) | `ContextStatusButton` | pass `knownScopeCount` on list rows (bulk!), omit on single-entity surfaces |
| Display a selection readably | `ContextSummaryChips` | compact chips for headers; org only if explicit |
| Labeled active/filter breakdown in the field footer | `ContextSelectionSummary` | Org · Scope Types (group) · per-type scopes · Projects · Tasks |
| Prompt for context during an upload | `UploadContextPrompt` | Save awaits `awaitFileIds()` — handles both races |
| Filter a list by context (no saving!) | `ContextAssignmentField mode="filter"` | emits via `onSelectionChange`; zero save-side effects |

All in `features/scopes/components/context-assignment/` except
`ActiveContextButton` + `ActiveContextPanel` (`features/scopes/components/active-context/` —
Surface A writers MUST live there; ESLint + FEATURE.md enforce it).

## Hard rules

- **Fetch discipline.** The org/type/scope tree is fetched ONCE at boot into
  Redux (`ensureScopeTree` → `state.scopesTree`) and refreshed only by
  `scopeTreeInvalidationMiddleware` on structural mutations. Components NEVER
  refetch it. It is **durably warm-cached across hard reload** by the sync
  engine (`scopesTreePolicy` in `features/scopes/redux/scopesSlice.ts`): a warm
  boot rehydrates the tree before paint and `ensureScopeTree()` skips the
  network entirely (no `staleAfter`/`remote.fetch` — the tree changes rarely). Projects/tasks/items go through
  `context-assignment/data.ts` (60s TTL + in-flight dedup). List surfaces use
  `getEntityScopesBulk`/`primeEntityScopes` — N rows must never mean N
  requests. Add new reads to `data.ts`, never to a component.
- **Write paths.** Scopes → `useEntityScopes().setScopes` /
  `setEntityScopes` thunk only. Active context → dispatch from
  `active-context/` components only. Entity FKs (e.g. a note's project_id)
  → that feature's save pipeline, applied from `onSaved`'s selection (see
  `features/notes/components/NoteContextSection.tsx` as the template).
- **Dimension gating.** Pass `dimensions={["scopes"]}` (or any subset of
  `"scopes" | "projects" | "tasks"`) to hide sections that do not apply —
  e.g. project settings (scope tagging only) vs notes (scopes + project/task
  FK intent). Default is all three. Org dropdown (assignment) and org rows
  (active/filter) are independent of `dimensions`.
- **Org default-but-changeable.** Assignment mode defaults to **"All
  organizations"** (`ALL_ORGS` sentinel — nothing filtered, scope sections
  grouped per org, `selection.organizationId = null`). Surfaces that "enforce"
  an org pass `defaultOrganizationId` to override that default; the user can
  always switch (including back to All).
- **No layout shift.** Fixed section heights; fixed-size check targets;
  status icons swap glyphs, never dimensions.
- **Mobile = one bottom sheet.** Every wrapper (`ContextAssignmentPopover`,
  `ContextAssignmentDialog`, `ContextAssignmentWindow`, `UploadContextPrompt`,
  `ActiveContextButton`) switches to `ContextSheet` on `useIsMobile()` — never a
  desktop popover/dialog/window on a phone. `ContextSheet` (built on the
  `BottomSheet` primitive) hosts the body with **`fill`**, which makes the
  field's own section list the single scroll area and pins the footer. Never set
  a fixed `sectionHeight` inside a sheet (that re-introduces nested scrolling) —
  pass `fill` instead. The field's org-of-record row stacks (`flex-col
  sm:flex-row`) so it never overflows a narrow screen.
- **Project/task durable links are LIVE** via `associationsService.setTargets`
  (`platform.associations`, replace-semantics) — the field's live save path and
  `UploadContextPrompt` both write them. Never reintroduce a log-and-toast stub.
- **Active context is MULTI-SCOPE — never radio.** Any number of scopes per
  scope type (Arman, 2026-07-07). Toggle with `addActiveScope` /
  `removeActiveScope` (additive/surgical); never evict same-type siblings, and
  never read a `scope_selections` KEY as a scope_type_id — use
  `selectActiveScopeIdsByType`.

## Live references

- Design surface / every variant demoed: `/demos/scopes/context-lab`
  (`app/(dev)/demos/scopes/context-lab/page.dev.tsx`).
- Real integrations to copy from: files table cell
  (`features/files/components/surfaces/desktop/FileContextCell.tsx`), upload
  prompt host (`features/files/components/surfaces/PageShell.tsx`), note
  adapter (`NoteContextSection.tsx`), header button (`ChatRunHeader.tsx`),
  run-controls tab (`RunControlsMenu.tsx` Context tab → `ActiveContextPanel`).
- Current state: `features/scopes/FEATURE.md` (the live SOR for scope/context on the FE).
