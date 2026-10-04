---
name: drag-and-drop
description: "Implement drag-and-drop in LWC using HTML5 Drag and Drop API, keyboard alternatives, accessible announcements, and file drop zones. NOT for handling a file the user dropped onto the component - use lwc/file-upload-patterns."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - User Experience
  - Reliability
triggers:
  - "lwc drag drop"
  - "reorder list lwc"
  - "drag file into lwc"
  - "kanban drag and drop lwc"
  - "drag drop isn't working"
  - "we're having issues with drag drop"
tags:
  - lwc
  - drag-drop
  - a11y
inputs:
  - "items to reorder or move"
  - "accessibility requirements"
outputs:
  - "component with dragstart/dragover/drop handlers + keyboard fallback"
dependencies: []
version: 1.0.1
author: Pranav Nagrecha
updated: 2026-08-14
---

# LWC Drag and Drop

Native HTML5 Drag and Drop works in LWC — no library needed. Three things make
it harder than it looks, and all three fail **silently**: `dragover` must call
`preventDefault()` or the drop is rejected; `dataTransfer` is only valid during
the event; and LWC has **no event modifiers**, so the `ondragover.prevent`
syntax people bring from Vue is ignored without a warning.

## Build Order: Keyboard First, Drag Last

Drag is a pointer gesture with no fallback. HTML5 drag events do not fire on
touch and are unreachable by keyboard, so a drag-only component is unusable by
keyboard users, screen-reader users, and every mobile user at once.

1. **Explicit controls** — Alt+Up / Alt+Down on a focusable row (plus Home/End
   and Escape). Works everywhere.
2. **Announcements** — an `aria-live` region carrying pick-up, each move with
   position *and* total, and cancellation. `aria-grabbed` and `aria-dropeffect`
   are deprecated in ARIA 1.1; do not use them.
3. **Drag** — layered on a component that already works.

Built in that order the component is correct on every device from the first
commit. Built drag-first, the keyboard path is retrofitted onto a state machine
designed around pointer events, and it shows.

## Adoption Signals

Any reordering UI (priority list, board columns, file drop zones). Not for
complex trees or cross-window drag — wrap a specialised library in one component
for those, and verify it under Lightning Web Security in a real org.

## Recommended Workflow

1. Template: `draggable="true"` plus `ondragstart`, `ondragover`, `ondragenter`,
   `ondragleave`, `ondragend`, `ondrop`, and `onkeydown`. Use `lwc:ref` /
   `this.refs` for DOM access rather than `this.template.querySelector()`.
2. `event.preventDefault()` inside the `dragover` handler — there is no `.prevent`
   modifier in LWC, and without the call `drop` never fires.
3. `dataTransfer.setData` synchronously in `dragstart`, `getData` synchronously
   in `drop`. Outside those windows reads return an empty string.
4. Reorder by **id array**, copying before mutating and reassigning the property.
   `splice` on a reactive array in place does not re-render.
5. Cleanup in `dragend`, not `drop` — `dragend` fires whether or not a drop
   occurred, so abandoned drags do not leave stuck state. Guard `dragleave`
   against descendant elements with an enter/leave counter.
6. Jest: assert `preventDefault` was called on `dragover`, cover both interaction
   paths, and assert the announcement contains the position and the total. jsdom
   has drag events but no `DataTransfer` — stub it.

## Key Considerations

- Touch devices do not fire drag events at all. The keyboard/explicit-control
  path is what serves them; a pointer polyfill is not the answer.
- Inside `role="listbox"`, bare arrows belong to navigation. Reorder takes a
  modifier or the accessibility work makes the component less accessible.
- An `aria-live` region only announces on text *change* — blank it and reset on
  the next microtask, or two identical moves announce once.
- Keep the `dragover` handler trivial. It fires at pointer frequency; put
  highlighting in `dragenter`/`dragleave`, which fire once per boundary.
- Third-party drag libraries fight shadow DOM (global queries cannot reach the
  shadow tree) and run under Lightning Web Security distortions — and most ship
  no keyboard path, so the hard part remains yours.

## Worked Examples (see `references/examples.md`)

- *Priority list reorder* — the wrong version and the right one side by side,
  with the keyboard path and live-region announcements.
- *Announcement model* — the three moments a screen-reader user needs, and the
  reset-then-set trick that makes them fire.
- *File drop zone* — layered over a real `<input type="file">`, with enter/leave
  counting and the folder-drop case.
- *Jest tests* — both paths, plus the `DataTransfer` stub jsdom lacks.

## Common Gotchas (see `references/gotchas.md`)

- **`ondragover.prevent` is Vue syntax** — LWC ignores it silently and `drop`
  never fires.
- **`dataTransfer` outside the event returns an empty string** — read and write
  synchronously.
- **`dragleave` fires when entering a child** — count enters and leaves.
- **Cleanup in `drop` only** — abandoned drags leave the dragging class stuck.

## Top LLM Anti-Patterns (full list in `references/llm-anti-patterns.md`)

- Framework event modifiers LWC does not have.
- No keyboard path — which also means no touch support.
- `aria-grabbed` / `aria-dropeffect`, both deprecated in ARIA 1.1.
- Reaching for a drag library, which fights shadow DOM and LWS and still leaves
  you to build the keyboard path.

## Official Sources Used

- Lightning Web Components Developer Guide — https://developer.salesforce.com/docs/platform/lwc/guide/
- Access Elements the Component Owns (`lwc:ref`) — https://developer.salesforce.com/docs/platform/lwc/guide/create-components-dom-work.html
- Shadow DOM — https://developer.salesforce.com/docs/platform/lwc/guide/create-dom.html
- How LWS Works — https://developer.salesforce.com/docs/platform/lwc/guide/security-lwsec-architecture.html
- LWS Distortion Viewer — https://developer.salesforce.com/tools/lws-distortion-viewer
- LWC Recipes — https://github.com/trailheadapps/lwc-recipes
