---
name: board-items
description: "Putting a platform feature on the Board (/board) as an Add-menu item with its real component and full agent surface. Use when adding a feature, record type or 'X on the board', or editing features/spatial/items/** or a tile body."
---

# board-items — a feature on the Board, for real

The Board (`/board`, `features/spatial/`) is the person's own canvas and is meant to become the ONE
UI: they drop in anything the platform supports and do their actual work there. Two laws decide
whether an item is done:

1. **The tile IS the feature.** Its body is the feature's canonical component — the same core the
   feature's own page renders, with every option, button and mode. A look-alike ("a simple note
   box", "just the preview") is a defect, however clean it looks. Arman: *"if they can't do their
   actual work, the entire thing breaks."*
2. **An agent can do in the tile everything a PERSON can do on the feature's page.** The item declares
   the feature's own surface (values, write targets, client tools) and mounts it for the tile's record.
   A record item without its full surface is a defect, and so is a gap the page's surface already had
   (e.g. an agent can't read or edit a document's body): closing it is part of this task.

Mechanics live in `features/spatial/FEATURE.md` (The Board section). Read it once.

## The contract — `features/spatial/items/types.ts`

A `BoardItemType` registered in `features/spatial/items/catalog.ts` (through `work-items.tsx`,
`feature-items.tsx`, `content-items.tsx`, `data-items.tsx`, or a new `<area>-items.tsx` you add to the
catalog) appears in every board's Add menu, Start panel and agent tools with no other change.

| Field | What it must be |
|---|---|
| `key`, `label`, `icon`, `group`, `defaultSize` | Registry key (= `source.entity` for records); singular noun; Lucide icon (domain icons from `components/icons/domain-icons.ts`); size that fits the real component |
| `matches(source)` | `source.kind === "entity" && source.entity === key` for records |
| `Body` | The feature's canonical component for ONE record — never a new renderer |
| `surface` | `{ name, Host? }` for every record item; `{ none: reason }` ONLY for board-only content (label, web page) |
| `startNew` | One entry or a list (`startNewEntries()` reads both). Each is `create` — synchronous, returns the item to place NOW; the body creates the record through the feature's canonical create path (with the organization gate) on the person's FIRST ACTION (a Create click, or the first words typed), never in a mount effect (a remount or a removed tile would leave stray records; `NoteItemBody` only starts a client-side draft on mount) — or a `Picker` (e.g. chat's "Chat with an agent" uses the one agent picker) |
| `bringIn` | A picker built from the feature's canonical picker; most already exist in `features/resource-manager/resource-picker/` (Documents, Notes, Tables, Tasks, Files…) |
| `href` | The record's page — no dead ends |

The saved form is a REFERENCE (`{ kind: "entity", entity, id, meta? }`, `board/document.ts`), never a
copy of the record. `id` is null until the record exists; `meta.seed` carries pasted text for a record
not created yet. A body changes what the tile refers to only through `onSource`.

## Recipe — adding a feature

1. **Find the canonical component.** Walk the feature's route down to the component that renders one
   record with all its controls (for notes: `NoteContentEditor` + `NoteMetadataBar`, not the inner
   `NoteEditorCore`). Leave out only the app's own navigation (sidebars, tabs of OTHER records, back
   buttons). Done when every control on the feature's page for that record exists in the tile.
2. **Find the feature's surface.** `features/surfaces/manifests/*.manifest.ts`: its `surfaceName`,
   values, `writeTargets`, `clientTools`, and WHERE the feature's page mounts `SurfaceRuntimeProvider`.
   - Mounted inside the canonical component → `surface: { name }`, no `Host`.
   - Mounted at page level → extract a record-scoped host component, use it on the page AND as the
     item's `Host` (one component, two consumers — never a board-only copy).
   - No surface, or one with no write targets / tools for what the page can do → author or extend it
     with the `surface-authoring` skill (a new surface is registered server-side in `ui.ui_surface`,
     or every send beside it fails 422). Done when the manifest covers every read and every action
     the page offers.
   - Declare `briefValues` (1-5 values that say WHICH record this is and its state at a glance: a
     note's title + first line, a table's name + row count, a task's status + due date). They are the
     `basics` agents see for every item that is not live. Without them the first declared values are
     used — often ids, which tell an agent nothing. `surface-declare.ts` checks the names.
3. **Write the item** in the matching `*-items.tsx`, with `startNew` / `bringIn` / `href`.
4. **Fit the plane.** Tiles sit in a zoomed, transformed world: `position: fixed` and components that
   assume the viewport (`WindowPanel`) break there; portals and popovers must still open usably.
   Test at the item's `defaultSize` and zoomed out. Fix by the component's own props or a portal
   container — never by forking its UI. A fix that belongs in an `@ai-matrx/*` package is made in the
   package (THE SAME-SESSION LAW).
5. **Prove it in the browser with real data** (docs/official/browser-testing.md): add one of each
   (new and brought in), do one real task in the tile, see the change on the feature's own page.
   Select the tile and confirm exactly ONE registration of its surface, scoped to that record. Then,
   with a DIFFERENT tile live, ask the board agent to change your item: it must find it in
   `board_items` (with its basics), read it with `board_open_item`, and change it with
   `board_item_act` (through the approval card where the target asks first) — in one turn.
6. **Record it:** `features/spatial/FEATURE.md` change log; the feature's FEATURE.md notes its board
   item and shared host.

## How the board keeps surfaces honest

- `packages/chat/src/surfaces/runtime/SurfaceRuntimeContext.tsx` `SurfaceActivity`: everything under
  `active={false}` registers nothing. The board wraps every tile; only the LIVE tile (selected, being
  worked in, or focused) registers its surface globally. So your component may register its surface
  unconditionally — never add your own "am I on a board?" switch.
- Every tile ALSO registers into its own capture (`SurfaceActivity capture`), live or not. That is
  how an agent reaches any item in the same turn, in two requests:
  1. The board's `board_items` value (always in context) lists every item: id, title, kind, surface,
     and a dormant item's `basics` (its `briefValues`). The LIVE tile's full surface is already in
     context through the surface chain.
  2. `board_open_item(id)` returns that item's values, write targets and client tools, and selects
     it; `board_item_act(id, target+value | tool+input)` applies one through the ONE writeback /
     client-tool runtime, approval card included.
  So an item whose surface is registered by its Body or `Host` is fully reachable with no board
  code. Never write per-item agent tools on the board. `features/spatial/tools/item-surfaces.ts`.
- `board_read` gives positions, excerpts, each tile's `surface` and `live_tile_id`; `board_focus`
  makes a tile live (shows it to the person).
- A component that registers a side door outside the surface runtime (like custom fields'
  `registerCustomFieldsDoor`) must check `useSurfaceDormant()` so dormant copies are not offered.

## Red flags — stop

- "The full component is too big for a tile — I'll render a lighter version." → Render the canonical
  component; fix what breaks in the plane.
- "The page's surface is page-level, so the tile gets none for now." → Extract the record-scoped host;
  that IS the task.
- "I'll set `surface: { none }` until the surface exists." → `none` is for board-only content only.
- "Agents can't do that on the page either, so it's a separate follow-up." → The page's gap is this
  gap. Extend the feature's surface (`surface-authoring`) as part of the item.
- "I'll create the record when the tile mounts, guarded against double-mount." → Create on the
  person's first action; mounting is not intent.
- "Agents can already move and arrange the tile, that's enough." → Arranging is the board's job; the
  item's job is the feature's own reads and writes.
- "I'll add a board tool so agents can edit my item." → Declare it on the feature's surface; the
  bridge reaches it. A board-specific tool is a second path that drifts.
