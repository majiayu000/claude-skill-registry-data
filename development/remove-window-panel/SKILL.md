---
name: remove-window-panel
description: "No-trace removal recipe for a window panel or overlay. Use when deleting, killing, or retiring a window/overlay, or consolidating X into Y and deleting X ('kill this panel', 'remove the X window'). NOT for adding or opening an overlay (use overlay-system)."
---

# Remove a Window Panel (kill it completely)

Deleting a window panel/overlay means removing it from **every** place the registration system spreads it across — then proving zero residue. A panel that "looks deleted" but leaves a stale `OverlayId`, a dangling opener, or a tile is a half-kill. **No shims. No back-compat aliases. No fallback opener that forwards to the replacement. No commented-out block or `// removed X` tombstone. No dead panel name left in a comment.**

Read the [`overlay-system`](../overlay-system/SKILL.md) skill first if you don't know how the overlay layer is wired. This skill is the reverse operation. Editing the WindowPanel component primitive itself (drag, resize, tray) → the [`window-panels`](../window-panels/SKILL.md) skill, not this one.

## The keystone strategy — pull the union member, let TypeScript hunt

`OverlayId` is `keyof typeof OVERLAY_CATALOGUE` — the keys of [`features/overlays/catalogue.ts`](../../../features/overlays/catalogue.ts) — and the OverlayController's selectors are typed against it. So:

1. **Delete the catalogue entry first** — that removes the union member.
2. **Run `pnpm type-check`.** Every *hard* reference now fails to compile — the controller's `isOpenById` / `dataById` selectors, the opener's `OVERLAY_ID as const`, and any typed dispatch site. The compiler hands you the list.
3. **Grep finds the *soft* references** the compiler can't see — the tile, registry metadata, url-sync, comments, docs. Do both; neither alone is complete.

## The removal checklist — every place a panel hides

Parameterize on `<overlayId>` (camelCase, e.g. `agentContentSidebarWindow`), `<slug>` (kebab, e.g. `agent-content-sidebar-window`), `<Component>` (e.g. `AgentContentSidebarWindow`), and the tile id / label / urlSync key.

| # | Location | What to remove |
|---|---|---|
| 1 | `features/overlays/catalogue.ts` | The `<overlayId>: { … }` entry — its key IS the `OverlayId` union member. **Do this first.** |
| 2 | `features/window-panels/windows/**/<Component>.tsx` | The component file — `git rm`. |
| 3 | `features/overlays/openers/<overlayId>.tsx` | The opener file — `git rm`. No forwarding shim. |
| 4 | `features/window-panels/registry/windowRegistryMetadata.ts` | The whole entry (slug + overlayId + label + defaultData + any `deprecated:` block). |
| 5 | `features/window-panels/tools-grid/toolsGridTiles.ts` | The `{ id: "tile.<…>", overlayId: "<overlayId>" }` tile. |
| 6 | `features/overlays/OverlayController.tsx` | **Four sub-sites:** the `const <Component> = lazyOverlay(() => import(...))`, the `isOpenById` selector entry, the `dataById` selector entry, and the gated JSX render block. |
| 7 | `features/window-panels/url-sync/initUrlHydration.ts` | Any `registerPanelHydrator("<urlSyncKey>", …)` for this panel. |
| 8 | `features/window-panels/windows/<feature>/callbacks.ts` | Only if it was a **callback-aware** opener — delete its callback contract. |
| 9 | `features/admin/**` (FeatureAdminMap), `FEATURE.md`, README/docs | Any map row, table row, or prose naming the panel. |

Not every panel touches all nine — a panel with no `urlSync` skips 7, a non-callback panel skips 8. Steps 1–6 are universal.

## The rewire step — repoint every opener before you delete it

A panel is *used* by whatever opens it. Find and repoint each to the replacement **before** removing the dead one:

```bash
# Every way to open it:
grep -rn "useOpen<Component>\|<Component>Controller" --include="*.ts*" .   # opener hook + declarative wrapper
grep -rn 'openOverlay({ overlayId: "<overlayId>"' --include="*.ts*" .       # raw dispatch sites
grep -rn "panels=<urlSyncKey>" --include="*.ts*" .                          # ?panels= deep links in code/docs
```

The Tools-grid tile is itself a usage — decide per task: **remove it** (capability gone) or **repoint** its `overlayId` to the replacement (capability moved). Confirm the replacement actually covers the dead panel's capability — parity is the user's call, never a silent capability drop.

## Do NOT delete shared infrastructure the panel happened to touch

The single biggest over-kill mistake. Before removing anything the dead component imported, owned, or was marked with, prove it's unused elsewhere (`grep` / `Explore` subagent):

- **The `deprecated:` metadata mechanism** (red ring + banner) is shared by many windows. Remove the panel's *entry*, never the field type in `windowRegistryTypes.ts` or the rendering in `WindowPanel.tsx`.
- **Shared icons** in `toolsGridTiles.ts` — the import stays if another tile uses it.
- **Shared exports the component re-exported.** A window may `export const ALL_TABS` / `TabContent` that siblings import. If you delete the *owner* of a shared export, you orphan its consumers — relocate the shared piece first. (Check `export` lines in the component before `git rm`.)
- **A `import type` in OverlayController** that the deleted block used may still serve a sibling block — leave it if `grep` shows another user.

## Clean comments, don't just delete

Other files may *name* the dead panel in a comment ("the same composition the legacy X used"). **Reword to keep the useful doc and drop the dead name** — don't delete the whole comment, don't leave the dead name. The user's bar: not even a comment mentions it.

## Verify — the kill isn't done until this passes

1. **Re-grep every token**, case-insensitive, across the repo (exclude `node_modules`, `.next*`, `.claude/worktrees`). Must be empty:
   ```bash
   grep -rni "<overlayId>\|<Component>\|<slug>\|<label>\|tile.<tile-id>\|<urlSyncKey>" \
     --include="*.ts" --include="*.tsx" --include="*.md" . | grep -v node_modules
   ```
2. **Deleted files gone**; no import of the deleted opener/component paths survives.
3. **`pnpm type-check`** clean for every touched file (every controller selector, opener, and dispatch site is typed against `keyof typeof OVERLAY_CATALOGUE`, so a missed reference *cannot* compile — that is the safety net).
4. **`pnpm check:doctrine`** passes.
5. **Spawn an independent `Explore` subagent** to re-verify from scratch — hand it the checklist above and the token list. The user expects this as the standard final gate, not optional.
6. **Inspect `git status`** — commit **only** the panel's files. If unrelated files are dirty (concurrent work), stage your paths explicitly; never fold them in.

## Worked example

The kill of **Agent Editor (Sidebar)** (`agentContentSidebarWindow` → replaced by `agentAdvancedEditorWindow`) touched exactly steps 1–6 + the comment cleanup, had zero external opener callsites (only the tile opened it), and kept the `deprecated:` mechanism + `FileStack` icon (both used elsewhere). That's the canonical shape: small, total, no residue.
