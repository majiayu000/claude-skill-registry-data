---
name: context-menu-v3
description: "The universal v3 right-click menu (EditableContextMenu / NonEditableContextMenu). Use when adding a right-click menu to a surface, fixing a fake menu with no Copy or Export, a missing Download as Markdown, or a bespoke per-surface menu. NOT for an assigned rollout shard (use context-menu-rollout)."
---

# context-menu-v3 — wire the universal menu onto a surface

The deep contract is **[`features/context-menu-v3/FEATURE.md`](../../../features/context-menu-v3/FEATURE.md)** — read it once. This skill is the rollout recipe; editing the v3 internals is that FEATURE.md's job, and a worker assigned a shard from `pnpm check:context-menu` follows the `context-menu-rollout` skill on top of this one. The proven reference is **`/demos/context-menu/canonical`** (every panel is a real v3 wiring; copy the one that matches your surface). The v2 menu (`UnifiedAgentContextMenu`) was deleted 2026-07-19 — every surface renders v3.

## Pick the wrapper

- **`EditableContextMenu`** — a textarea / editor. Gives Cut / Paste / Insert / Save / Delete on top of everything else — and auto-registers a WidgetHandle from the same callbacks, so agents launched from the menu can stream `widget_text_*` edits into the surface in place (nothing extra to wire; proof at `/demos/context-menu/inline-edit`).
- **`NonEditableContextMenu`** — a viewer / rendered display / read-only text. No text mutation; **Copy / AI / Export / Download / Convert still work** because the menu self-resolves content from the DOM.

A surface with both modes (editor + preview) uses **both** — one per mode.

## 🚨 THE DENSITY LAW — labels only, macOS-terse (Arman, 2026-08-25)

A menu item is a **short verb phrase**: `Edit rule…`, `See its keywords`, `Revert to pack…`. **No `description` / subtext, ever**, with ONE exception: a `disabled` item carries a `description` naming why it's off and where it works ("Unchanged from the pack", "Works on the Keyword Workbench"). Rule of thumb: if macOS wouldn't put it in a menu, neither do we. Any other description requires Arman's explicit approval, requested AFTER the menu ships bare — and ~95% will be refused. An agent that ships prose under menu rows has failed the task.

## 🚨 CANONICAL SECTIONS — check the registry BEFORE writing any `extraSections`

**[`features/context-menu-v3/SECTIONS.md`](../../../features/context-menu-v3/SECTIONS.md)** is the registry of shared per-identity section builders (keyword, class, level, page, CRM row, …) and THE ADOPTION PROTOCOL. The short form: if the right-clicked thing already has a registered builder, USE it — and grow it with the actions this surface makes obvious (every consumer gains them). If the thing appears on 2+ surfaces and has no builder, extract + register one. Only a truly page-local identity gets inline `extraSections`. Actions impossible on this surface stay visible-but-`disabled` with the reason as the tooltip — the menu is identical everywhere; only availability changes.

## Wire a surface — the mechanical steps

1. **Import the wrapper statically** — it's the light shell; children render synchronously, and only `MenuContent` lazy-loads on first open. Never wrap it in a per-consumer `next/dynamic` (that re-adds a loading fallback and a layout-collapse null state for zero benefit).
   ```tsx
   import { EditableContextMenu } from "@/features/context-menu-v3/EditableContextMenu";
   ```
2. **Wrap the region** in `<EditableContextMenu …>` (or `NonEditableContextMenu`).
3. **Pass the identity + value props:** `sourceFeature` (required), `surfaceName` (registry surface → AI actions + bound agents + value mappings), `getApplicationScope` (live, preferred) / `contextData` (static), `extraSections`, and for editables `getTextarea` + `onTextReplace` / `onTextInsertBefore|After`; history props and `scope` / `scopeId` as the surface needs. Use `placementMode` for per-placement visibility. Types: `@/features/context-menu-v3/types` (`EditableContextMenuProps` / `NonEditableContextMenuProps`).
   `sourceFeature` names the actual product, not the nearest allowed label. If it is missing, register the product in `aidream/aidream/services/conversation_context/source_attribution.py`, regenerate the contract with its generator, and deploy the registry before the caller. Never cast or misattribute the caller to satisfy the allow-list.
4. Build scope through **`buildApplicationScopeFromMenuContext`** (`@/features/context-menu-v3/utils/build-application-scope`) — it guarantees the 5 baselines from the live DOM.

## ONE MENU PER PANE — delegate per row, never nest

A list, table, or grid gets **one** wrapper around the whole pane, not one per row. Nesting Radix triggers opens two menus and appears nowhere in this repo. Per-row context comes from **`resolveContextOnOpen(target)`**: the shell calls it with the right-clicked element before opening, and the returned object is merged over `contextData`, so the same single menu can say `Edit "China"` on a row and show list-level rows on empty space. Worked reference: `features/user-lists/components/ListDetailClient.tsx` + its `dom-anchors.ts` (read the clicked row/group off `data-*` attributes).

⚠️ **`className` on the wrapper styles the menu POPUP, not the trigger.** Layout classes there silently break the popup instead of the pane — style the child element you wrap.

⚠️ **An overlay/window surface must mount its own menu.** Without one, a right-click inside the window is answered by the page underneath, handing the user THAT page's surface, values and agents — silently wrong, and it looks like it works.

## Unlock the new capabilities (do this, don't skip it)

- **`contentSource?: ContentSource`** (rich-document source: `{type:"note",noteId}`, `{type:"chat-message",…}`, `{type:"raw"}` default) → lights up **Copy-as variants, Export, Download as Markdown, Convert** and links Convert→Task to the right parent. A surface with a real entity should pass its source, not raw.
- **`entity?: {type,id,title,resourceType?,isOwner?}`** → lights up **Attach To** (scope tagging) and **Share**. Omit on raw fragments.

## Verify — non-negotiable

- `pnpm type-check` clean.
- **Open the menu on the surface and watch the console.** v3 SCREAMS in dev if the menu opens inert ("INERT MENU on …") or a surface dropped a declared value ("VALUE MAPPING GAP on …"). A clean open = the values are wired. A scream = fix the wiring (provide `getApplicationScope`/`contextData.content`, or make the wrapped content selectable for the DOM fallback).
- For controlled editable fields, use the menu to replace text and confirm the owning state and derived output change together. A menu that changes only the DOM is not wired. Each field needs the callbacks for its own state.
- The acceptance test for any content surface: right-click **without selecting** → **Export → Download as Markdown** saves the whole content as `.md`; highlight first → saves the selection.

## Layout & density knobs (2026-08-22)

The desktop menu is model-driven: `model/menu-model.ts` (what exists) → `model/layouts.ts` (`classic` | `tiered` | `command`) → `MenuContent.tsx` (density `comfortable` | `compact`). Pass `menuLayout` / `menuDensity` on the wrapper only when a surface must deviate; the platform defaults are the CAPS constants in `types.ts`. A surface's `extraSections` need NO layout awareness — a long section folds into one submenu named by its `label` (+ optional `icon`) in tiered/command. Never add a layout by writing JSX in the renderer — add an arrangement in `layouts.ts`. 🚨 THE LOSSLESS LAW: a layout may never hide, rename, or drop a row Classic shows; grouping needs Arman's explicit approval (History is the only one today). Compare all four on `/demos/context-menu/layouts`.

## Doctrine

- **Reuse, never fork.** Every action (copy/export/convert/print/attach/share/AI) delegates to an existing system. A surface contributes its own items via **`extraSections`** (declarative anchors), never a bespoke menu.
- **One menu.** No per-surface context-menu component. If a surface still has one, collapse it into a direct `Editable/NonEditableContextMenu` usage.
