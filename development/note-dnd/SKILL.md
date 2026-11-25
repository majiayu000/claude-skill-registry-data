---
name: note-dnd
description: Map of the drag & drop of EasyTask notes (tasks, sections, groups, open tabs, sidebar tree) - pointer controller, hit test, owners of the split view, live drag shifts, Ctrl cross-note drag and Alt copy, autoscroll and scroll lock, DB queries, tests and e2e. Use before changing or debugging anything that is dragged, a drop zone, the live drag, or the drag between the two notes of the split view.
---

# Note drag & drop (EasyTask)

The drag of tasks, sections and groups is the app's own code, not dnd-kit's sensors and droppables: dnd-kit re-rendered the whole note on every `over` change. Everything is in `src/pages/workspacePage/components/` unless said otherwise. Read the header comment of each file before editing it: each one explains why it is built that way.

## The pieces

| File | Role |
| --- | --- |
| `note-dnd.ts` | Pure logic on the `NoteDataTree` (no DOM, no DB): `NoteDragKind` / `NoteOverKind` (`new-group` included), `ACCEPTS`, `computeDropZone`, `computeSectionTarget` / `computeTaskTarget` / `computeGroupTarget`. |
| `note-dnd-pointer.ts` | Pointer controller (`createPointerDrag`): primary button, 5px threshold (`DRAG_DISTANCE`), swallows the click after a drop, cancels on Esc, resize, blur and `pointercancel`. It follows **Ctrl** (crossing allowed) and **Alt** (copy at the release): a change of either calls `move` again. |
| `note-dnd-hit.ts` | Hit test: zones are nodes in a module-level Map (`registerZone`), measured once at the start (`measureZones`) plus the scroll of their ancestors, and tested on every move (`hitTest(pointer, { owner, cross })`). |
| `note-dnd-owner.ts` | Every open note (each pane of the split view) has its own provider with an `owner` id. Registry keys are `<owner>~task-5` (`ownerKey` / `stripOwner` / `ownerOfKey`). `registerNoteOwner(owner, noteId, store)`, `otherOwners`, `hasOtherNote`. |
| `note-dnd-state.ts` | Store of the hover state (`createNoteDndStore`, `useNoteDndSelector`); `useNoteDrop` / `useNoteDrag` for the rows; `useNoteMoves` / `useGroupMoves` do the drops inside one note. |
| `note-dnd-cross.ts` | `useCrossNoteMoves`: drop in the other note, a move or (Alt) a copy. Optimistic update of **both** notes, rollback if the write fails, **one** undo step. |
| `note-dnd-live.ts` | Pure maths of the live drag: snapshot of the sizes (`buildLiveSnapshot`), `computeLiveShifts`, `computeLiveSlot`, zone hysteresis. Lists: `s-<sectionId>`, `t-<taskId>`, `g-<groupId>`, `groups`, `b-<pane>` (tabs). |
| `note-dnd-shift.ts` | Visual side of the live drag: registry of the wrappers (`registerShiftNode`, `SHIFT_ATTR` `data-*` attributes) moved with `style.transform` in `requestAnimationFrame`, never through React state. `SHIFT_DURATION` follows the animation speed. |
| `note-dnd-overlay.ts` | The preview: a `position: fixed` box moved by transform once per frame. |
| `note-dnd-autoscroll.ts` | Edge autoscroll (row of groups sideways, list of a group vertically). With **Ctrl** the source note is locked (`startScrollLock`: wheel and autoscroll) and only the other note scrolls (`otherScrollers`). |
| `NoteDndProvider.tsx` | Wires everything for one pane: start, move (own zone or, crossing, the zone of the other note and its tree), the target announced to the other note (`incoming`), the drop, the timeout of the optimistic update. |
| `NoteDragOverlay.tsx` | Renders the preview. |
| `groups/NewGroupSlot.tsx` | Thin `new-group` slot on the edge of a group: a section dropped there becomes a new group. Invisible and without pointer events unless a section is dragged. |

Sidebar tree (notes and folders), separate code in `sidebar/`: `use-tree-dnd.ts`, `tree-dnd.ts`, `flat-tree.ts`, live drag in `tree-dnd-live.ts`, `tree-live-shift.ts`, `use-tree-live.ts`. Under 200 rows the tree is not virtualized (`FileTreeParts.tsx`) and the rows must register just the same (bug of card 187).

DB (`src/db/queries/`): `move.ts` (moves inside a note, `assertSameWorkspace`, `AcrossNotes`) and `cross-note.ts` (`moveDBTaskToNote`, `moveDBSectionToNote`, `moveDBSectionToNewGroupOfNote`, `moveDBGroupToNote`, `copyDB*ToNote`). Moves stay inside one workspace.

## Rules that broke things before

- **Keys carry the owner.** A new zone or wrapper must be registered with the owner of its provider (`useNoteDndOwner()`), or the two panes (or the same note open twice) overwrite each other's `new-group-<index>` and rows.
- **No React state per pointer move.** Hover goes to the store with selectors; shifts are transforms. A `setState` in `move` re-renders the whole note (see the drag-perf memory and the benchmark in the e2e-spec skill).
- **A zone must exist to be hit.** An empty container (a note without groups, a group without sections) needs its own zone, otherwise the drop does nothing (card 200).
- **Without Ctrl, zones of another owner are ignored.** Releasing Ctrl during the drag makes them invalid again; `move` runs again on every Ctrl/Alt change.
- **"Shifted" only if something moved.** Report a live shift only when at least one node is registered and displaced, otherwise the drop line disappears with nothing in its place (card 187).
- **Ctrl+click is the multi-selection.** Below `DRAG_DISTANCE` it is a click, never a drag.
- The order in the DOM can differ from the data (hide completed, completed last): the live drag uses the DOM order.

## Tests

- Unit (vitest + jsdom), next to the files: `note-dnd*.test.ts(x)`, `NoteDndProvider*.test.tsx` (`.cross`, `.live`), `sidebar/*live*.test.ts(x)`. jsdom has no layout: tests stub `getBoundingClientRect`, follow the existing ones.
- e2e (skill e2e-spec): `cross-note-drag.e2e.ts` (split view, Ctrl, Alt), `live-drag.e2e.ts`, `live-drag-scroll.e2e.ts`, `live-drag-sidebar.e2e.ts`, `live-drag-tabs.e2e.ts`, `split-workspace.e2e.ts`. Helpers: `pane(index)`, `paneTab(index, name)`, `setLiveDrag(on)` in `e2e/helpers.ts`. Drag with `browser.action("pointer")` in steps; hold Ctrl/Alt with `browser.action("key")` around the pointer actions.
- For a bug: first a failing test that reproduces it, then the fix.
- Hand checks the e2e cannot do: smoothness (no jumps or flashes at the landing), and the drag between notes on WebKitGTK if available.
