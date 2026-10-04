---
name: lwc-drag-and-drop
description: "HTML5 drag-and-drop API in LWC — draggable=\"true\", dataTransfer.setData / getData, ondragover preventDefault, drop zones, visual hover state, accessibility (keyboard alternatives, aria-grabbed deprecation), and shadow DOM event leakage. NOT for uploading a file the user dropped on the component — use lwc/file-upload-patterns."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
triggers:
  - "lwc html5 drag and drop dataTransfer"
  - "lwc draggable kanban swimlane"
  - "lwc drop zone preventDefault dragover"
  - "lwc reorder list with drag drop"
  - "drag drop accessibility keyboard alternative lwc"
  - "ondragstart ondrop lwc shadow dom event"
  - "lwc dragenter dragleave hover state"
tags:
  - drag-and-drop
  - dataTransfer
  - accessibility
  - kanban
  - dom-events
inputs:
  - "Source: list of draggable items, each with a stable id"
  - "Target: drop zones and the action that fires on drop"
  - "Whether keyboard users need an alternative (almost always: yes)"
outputs:
  - "Component template with draggable items + drop zones"
  - "Drag-state machine (idle / dragging / over-target) with visual feedback"
  - "Keyboard-accessible alternative path (move up/down buttons, kbd shortcuts)"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-05-05
---

# LWC Drag and Drop

The HTML5 drag-and-drop API is the only built-in drag mechanism
that works in LWC without a third-party library. The shape is
fixed: source elements get `draggable="true"`, the source fires
`dragstart` (where the developer stashes data on
`event.dataTransfer`), the target fires `dragover` (which must
call `event.preventDefault()` to be a valid drop target) and
`drop` (where the developer reads the data and acts).

The mistakes are repeatable. The `ondragover` handler forgets
`event.preventDefault()` and the drop never fires. Or
`dataTransfer.setData('text', id)` works in Chrome and not Firefox
because Firefox requires a non-empty data type. Or the developer
tries to read `dataTransfer.getData` in `dragenter` (it returns
empty in `dragenter` and `dragover` for security reasons, only
populated in `drop`). And the accessibility story is grim: HTML5
drag-and-drop has no native keyboard equivalent, so a
keyboard-only user cannot use a drag-only UI at all.

In Salesforce, the Lightning Locker / Lightning Web Security
sandboxing imposes one additional constraint: the
`dataTransfer.types` and `dataTransfer.items` lookup may be
filtered. Use `setData(type, value)` + `getData(type)` for the
type names you control; expect them to round-trip exactly.

## Recommended Workflow

1. **Decide whether HTML5 drag-and-drop is the right primitive.**
   For sortable lists with handles, a third-party library
   (Sortable.js wrapped in an LWC) is more accessible and more
   ergonomic. For drag-between-columns kanban, HTML5 native is
   reasonable. For file uploads, use a file-input or the
   `lightning-file-upload` component.
2. **Stash a stable identifier in `dataTransfer`.** Set the data
   in `dragstart` with a custom MIME-style type
   (`application/x-acme-card`) and a JSON-encoded payload. Read it
   in `drop`.
3. **Always `preventDefault` on `dragover`.** This is what makes
   the element a valid drop target. Forgotten 90% of the time on
   first drafts.
4. **Track the drag state in JS, not via dataTransfer.** Maintain
   a `@track draggedId` field. `dataTransfer.getData` returns
   empty during `dragover` for security; you cannot read your own
   data mid-drag.
5. **Provide a keyboard alternative.** Up/down arrow keys when
   the item is focused, plus a "Move to..." button that opens a
   menu of valid destinations. Without this, the component fails
   WCAG and is unusable for keyboard-only users.
6. **Use `dragenter`/`dragleave` to drive the visual hover state.**
   `dragover` fires every ~50ms during the drag and is too noisy
   for class toggling. Track an `over-target` boolean from the
   enter/leave pair.
7. **Clean up state on `dragend` regardless of drop success.** The
   user can drop outside any target or hit Escape; `dragend`
   fires in either case. Reset the visual state and clear
   `draggedId`.

## What This Skill Does Not Cover

- **File-drop upload** — see `lwc/lwc-file-upload-drop` and
  `lightning-file-upload`.
- **Sortable lists with a third-party library** — see
  `lwc/lwc-sortablejs-wrapper`.
- **Aura drag-and-drop** — Aura is deprecated for new development.
- **Touch drag (mobile)** — HTML5 drag-and-drop has limited touch
  support; use a touch-aware library.
